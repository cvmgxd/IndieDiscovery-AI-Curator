from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio

from models import GameEntry, MetricBreakdown
from scraper_engine import ScraperEngine
from ai_analyzer import AIAnalyzer

app = FastAPI(title="Indie Discovery API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = ScraperEngine()
analyzer = AIAnalyzer()

@app.get("/")
async def root():
    return {"message": "Welcome to the Indie Discovery API"}

@app.get("/discover", response_model=List[GameEntry])
async def discover_games(response: Response):
    # Disable caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # 1. Scrape Candidates (Parallel Deep Scrapes)
    heuristic_results = await scraper.discover()
    
    # 2. AI Enrichment (Parallel Analysis)
    candidates = heuristic_results[:12]
    
    async def analyze_and_map(h):
        analysis = await analyzer.analyze_game(h.title, h.description, h.rating_count)
        return GameEntry(
            id=h.id,
            title=h.title,
            url=h.url,
            image_url=h.image_url,
            smart_score=analysis.smart_score,
            vibe=analysis.vibe,
            sentiment=analysis.sentiment_label,
            description=h.description,
            reasoning=analysis.reasoning,
            metrics=analysis.metrics
        )

    tasks = [analyze_and_map(h) for h in candidates]
    final_results = await asyncio.gather(*tasks)
    
    return list(final_results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
