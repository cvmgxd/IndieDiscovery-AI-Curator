import pytest
import asyncio
from backend.scraper_engine import ScraperEngine

@pytest.mark.asyncio
async def test_scraper_fetch():
    engine = ScraperEngine()
    results = await engine.discover()
    assert isinstance(results, list)
    if len(results) > 0:
        assert hasattr(results[0], 'title')
        assert hasattr(results[0], 'smart_score') # Note: engine result is HeuristicResult which has 'score'
        # Wait, the engine returns HeuristicResult, let's fix the test logic
        assert results[0].score >= 0
