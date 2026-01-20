from pydantic import BaseModel
from typing import List, Optional

class MetricBreakdown(BaseModel):
    obscurity: float
    polish: float
    sentiment: float

class HeuristicResult(BaseModel):
    id: str
    title: str
    url: str
    description: str
    image_url: Optional[str] = None
    pass_heuristic: bool
    score: float
    rating_count: int = 0
    full_description: Optional[str] = None

class AIAnalysisResult(BaseModel):
    vibe: str
    smart_score: float
    sentiment_label: str
    niche_tags: List[str]
    metrics: MetricBreakdown
    reasoning: str

class GameEntry(BaseModel):
    id: str
    title: str
    url: str
    image_url: Optional[str] = None
    smart_score: float
    vibe: str
    sentiment: str
    description: str
    reasoning: str
    metrics: MetricBreakdown
