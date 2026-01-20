import re
import feedparser
import httpx
import asyncio
import random
from typing import List, Dict, Optional, Set
from collections import deque
from models import HeuristicResult

class ScraperEngine:
    def __init__(self):
        self.rss_urls = [
            "https://itch.io/games/featured.xml",
            "https://itch.io/games/new-and-popular.xml",
            "https://itch.io/games/newest.xml",
            "https://itch.io/games/tag-experimental.xml",
            "https://itch.io/games/tag-horror.xml",
            "https://itch.io/games/tag-lo-fi.xml"
        ]
        # Track history to ensure variety. Store last 100 game URLs.
        self.history: Set[str] = set()
        self.history_queue: deque = deque(maxlen=100)

    async def fetch_games_from_url(self, client: httpx.AsyncClient, url: str) -> List[Dict]:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code != 200:
                return []
            feed = feedparser.parse(response.text)
            return feed.entries
        except Exception:
            return []

    async def fetch_all_featured_games(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_games_from_url(client, url) for url in self.rss_urls]
            results = await asyncio.gather(*tasks)
            seen = set()
            all_entries = []
            for batch in results:
                for entry in batch:
                    link = entry.get("link")
                    if link and link not in seen:
                        # Skip items that were served in recent refreshes
                        if link not in self.history:
                            all_entries.append(entry)
                        seen.add(link)
            return all_entries

    async def _deep_scrape_candidate(self, client: httpx.AsyncClient, result: HeuristicResult) -> Optional[HeuristicResult]:
        """Scrape full page for a candidate and verify gem status."""
        try:
            resp = await client.get(result.url, timeout=10.0)
            if resp.status_code != 200:
                return None
            
            text = resp.text
            rating_match = re.search(r'"ratingCount":(\d+)', text)
            result.rating_count = int(rating_match.group(1)) if rating_match else 0
            
            # GEM Filtering: 50 or less ratings
            if result.rating_count > 50:
                return None

            desc_match = re.search(r'<div class="formatted_description [^>]+>(.*?)</div>', text, re.DOTALL)
            if desc_match:
                result.description = desc_match.group(1).strip()
            
            # Calculate Obscurity Score
            obscurity = max(0, (50 - result.rating_count) / 50)
            # Add significant "Spice" (random jitter) to vary the order on each refresh
            result.score = (result.score * 0.2) + (obscurity * 0.5) + random.uniform(0.1, 0.4)
            result.pass_heuristic = True
            
            return result
        except Exception:
            return None

    def apply_heuristics(self, entry: Dict) -> HeuristicResult:
        description = entry.get("summary", "")
        image_url = None
        img_match = re.search(r'<img [^>]*src="([^"]+)"', description)
        if img_match:
            image_url = img_match.group(1)
            description = re.sub(r'<img [^>]*>', '', description)
        
        desc_score = min(len(description) / 200, 1.0)
        img_score = 1.0 if image_url else 0.0
        total_score = (desc_score * 0.4) + (img_score * 0.6)
        
        return HeuristicResult(
            id=entry.get("id", entry.get("link", str(random.random()))),
            title=entry.get("title", "Unknown"),
            url=entry.get("link", ""),
            description=description,
            image_url=image_url,
            pass_heuristic=total_score > 0.05, # Very lenient initial pass for variety
            score=total_score
        )

    async def discover(self) -> List[HeuristicResult]:
        entries = await self.fetch_all_featured_games()
        random.shuffle(entries)
        
        async with httpx.AsyncClient() as client:
            # First pass: Fast heuristics
            initial_candidates = [self.apply_heuristics(e) for e in entries[:80]]
            passed_initial = [c for c in initial_candidates if c.pass_heuristic]
            
            # Second pass: Parallel deep-scrape
            tasks = [self._deep_scrape_candidate(client, c) for c in passed_initial[:25]]
            deep_results = await asyncio.gather(*tasks)
            
            results = [r for r in deep_results if r is not None]
        
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Add winners to history so they are not reused soon
        for r in results[:12]:
            if r.url not in self.history:
                self.history.add(r.url)
                if len(self.history_queue) >= self.history_queue.maxlen:
                    oldest = self.history_queue.popleft()
                    self.history.discard(oldest)
                self.history_queue.append(r.url)
        
        return results
        
        return results
