import asyncio

from server.ai_analyzer import AIAnalyzer
from server.models import GameEntry
from server.scraper_engine import ScraperEngine

scraper = ScraperEngine()
analyzer = AIAnalyzer()


async def discover_game_entries():
    heuristic_results = await scraper.discover()
    candidates = heuristic_results[:12]

    async def analyze_and_map(candidate):
        analysis = await analyzer.analyze_game(
            candidate.title, candidate.description, candidate.rating_count
        )
        return GameEntry(
            id=candidate.id,
            title=candidate.title,
            url=candidate.url,
            image_url=candidate.image_url,
            smart_score=analysis.smart_score,
            vibe=analysis.vibe,
            sentiment=analysis.sentiment_label,
            description=candidate.description,
            reasoning=analysis.reasoning,
            metrics=analysis.metrics,
        )

    tasks = [analyze_and_map(candidate) for candidate in candidates]
    results = await asyncio.gather(*tasks)
    return [entry.model_dump() for entry in results]
