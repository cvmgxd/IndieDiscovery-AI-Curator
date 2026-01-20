import random
import re
from typing import Dict, List, Optional
from server.models import AIAnalysisResult, MetricBreakdown

class AIAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.vibes = ["Lo-fi", "Experimental", "Horror", "Cosy", "Cyberpunk", "Surreal"]

    async def analyze_game(self, title: str, description: str, rating_count: int) -> AIAnalysisResult:
        # Obscurity Metric: Based on review count
        obscurity = max(0, (15 - rating_count) / 1.5)
        obscurity = min(10.0, obscurity)
        
        # Polish/Density Metric: Length of description + keywords
        clean_desc = re.sub(r'<[^>]*>', '', description)
        polish = min(len(clean_desc) / 200, 10.0)
        
        sentiment_val = 8.0 
        total_score = (obscurity * 0.4) + (polish * 0.3) + (sentiment_val * 0.3)
        
        return AIAnalysisResult(
            vibe="Experimental Gem" if obscurity > 7 else "Polished Niche",
            smart_score=round(total_score, 1),
            sentiment_label="High Quality",
            niche_tags=["Under-the-radar", "Experimental"],
            metrics=MetricBreakdown(
                obscurity=round(obscurity, 1),
                polish=round(polish, 1),
                sentiment=round(sentiment_val, 1)
            ),
            reasoning=f"With only {rating_count} ratings, this title represents a significant density of experimental mechanics that have yet to be discovered by the mainstream."
        )
