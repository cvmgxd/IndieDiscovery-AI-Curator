import React, { useState } from 'react';
import { MetricBreakdown } from '../types';

interface RatingInsightProps {
    reasoning: string;
    metrics: MetricBreakdown;
}

const RatingInsight: React.FC<RatingInsightProps> = ({ reasoning, metrics }) => {
    const [show, setShow] = useState(false);

    const renderBar = (label: string, value: number) => (
        <div style={{ marginBottom: '4px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.65rem', marginBottom: '1px' }}>
                <span>{label}</span>
                <span>{value}/10</span>
            </div>
            <div style={{ width: '100%', height: '6px', background: '#ccc', border: '1px solid #888', boxShadow: 'inset 1px 1px 0 #fff' }}>
                <div style={{
                    width: `${value * 10}%`,
                    height: '100%',
                    background: label === 'OBSCURITY' ? '#ff00ff' : label === 'POLISH' ? '#0000ff' : '#00ff00'
                }} />
            </div>
        </div>
    );

    return (
        <div style={{ position: 'relative', display: 'inline-block' }}>
            <div
                onMouseEnter={() => setShow(true)}
                onMouseLeave={() => setShow(false)}
                style={{
                    cursor: 'pointer',
                    width: '18px',
                    height: '18px',
                    background: 'var(--win-bg)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '10px',
                    border: '1px solid #000',
                    boxShadow: 'inset 1px 1px 0 #fff, 1px 1px 0 #808080',
                    color: '#000',
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold'
                }}
            >
                ?
            </div>

            {show && (
                <div style={{
                    position: 'absolute',
                    bottom: '100%',
                    right: '0',
                    marginBottom: '4px',
                    padding: '8px',
                    width: '240px',
                    zIndex: 100,
                    fontSize: '0.75rem',
                    lineHeight: '1.2',
                    background: '#ffffe1',
                    color: '#000',
                    border: '1px solid #000',
                    boxShadow: '2px 2px 0 rgba(0,0,0,0.3)',
                    fontFamily: 'VT323, monospace'
                }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '6px', color: '#000080', borderBottom: '1px solid #000', paddingBottom: '2px' }}>
                        GEM_ANALYSIS.HLP - METRIC_BREAKDOWN
                    </div>

                    {renderBar('OBSCURITY', metrics.obscurity)}
                    {renderBar('POLISH', metrics.polish)}
                    {renderBar('SENTIMENT', metrics.sentiment)}

                    <div style={{ marginTop: '8px', borderTop: '1px dotted #888', paddingTop: '4px', fontStyle: 'italic' }}>
                        {reasoning}
                    </div>
                </div>
            )}
        </div>
    );
};

export default RatingInsight;
