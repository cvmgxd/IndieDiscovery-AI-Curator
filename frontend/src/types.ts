export interface MetricBreakdown {
    obscurity: number;
    polish: number;
    sentiment: number;
}

export interface GameEntry {
    id: string;
    title: string;
    url: string;
    vibe: string;
    smart_score: number;
    sentiment: string;
    description: string;
    image_url?: string;
    reasoning: string;
    metrics: MetricBreakdown;
}
