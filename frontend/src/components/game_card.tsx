import React, { useState } from 'react';
import { GameEntry } from '../types';
import RatingInsight from './rating_insight';

interface GameCardProps {
    game: GameEntry;
}

const GameCard: React.FC<GameCardProps> = ({ game }) => {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className="window animate-fade-in" style={{
            display: 'flex',
            flexDirection: 'column',
            color: '#000',
            transition: 'all 0.3s ease',
            height: 'fit-content' // Allow window to grow with content
        }}>
            {/* Title Bar */}
            <div className="window-header">
                <div className="window-title">
                    {game.title}.SCR
                </div>
                <div className="window-controls">
                    <div className="window-button" style={{ cursor: 'pointer' }}>?</div>
                    <div className="window-button" style={{ cursor: 'pointer' }} onClick={() => setExpanded(!expanded)}>{expanded ? '■' : '□'}</div>
                    <div className="window-button" style={{ cursor: 'pointer' }}>×</div>
                </div>
            </div>

            {/* Content Area */}
            <div style={{ padding: '8px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {/* Image Section */}
                <div className="win98-inset" style={{
                    height: '140px',
                    width: '100%',
                    position: 'relative',
                    overflow: 'hidden',
                    background: '#000'
                }}>
                    {game.image_url ? (
                        <img
                            src={game.image_url}
                            alt={game.title}
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        />
                    ) : (
                        <div style={{
                            width: '100%', height: '100%',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            background: '#444'
                        }}>
                            <span style={{ fontSize: '2rem' }}>🎮</span>
                        </div>
                    )}

                    {/* Score Tag */}
                    <div style={{
                        position: 'absolute',
                        top: '4px',
                        right: '4px',
                        background: '#ffff00',
                        color: '#000',
                        padding: '2px 6px',
                        border: '1px solid #000',
                        fontSize: '0.6rem',
                        fontWeight: 'bold',
                        fontFamily: 'Press Start 2P'
                    }}>
                        {game.smart_score.toFixed(1)}
                    </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h3 style={{ fontSize: '0.8rem', color: '#000', margin: 0, maxWidth: '80%' }}>{game.title}</h3>
                    <RatingInsight reasoning={game.reasoning} metrics={game.metrics} />
                </div>

                <div style={{ display: 'flex', gap: '4px' }}>
                    <span style={{ fontSize: '0.6rem', padding: '2px 4px', background: '#e0e0e0', border: '1px solid #888' }}>
                        {game.vibe}
                    </span>
                    <span style={{ fontSize: '0.6rem', padding: '2px 4px', background: '#e0e0e0', border: '1px solid #888' }}>
                        {game.sentiment}
                    </span>
                </div>

                {/* Growable Description Container */}
                <div className="win98-inset" style={{
                    maxHeight: expanded ? '2000px' : '80px', // Large enough to show full desc
                    overflow: expanded ? 'visible' : 'hidden', // Allow expansion to push window down
                    background: '#fff',
                    padding: '8px',
                    fontSize: '0.9rem',
                    lineHeight: '1.2',
                    transition: 'max-height 0.5s ease-in-out',
                    position: 'relative'
                }}>
                    <div
                        dangerouslySetInnerHTML={{ __html: game.description }}
                        style={{
                            fontSize: '0.85rem'
                        }}
                    />
                    {!expanded && (
                        <div style={{
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            right: 0,
                            height: '20px',
                            background: 'linear-gradient(transparent, #fff)'
                        }} />
                    )}
                </div>

                <div style={{ display: 'flex', gap: '4px', marginTop: 'auto' }}>
                    <button
                        style={{ flex: 1, fontSize: '0.6rem', padding: '4px' }}
                        onClick={() => setExpanded(!expanded)}
                    >
                        {expanded ? 'LESS_INFO.SYS' : 'READ_MORE.TXT'}
                    </button>
                    <a
                        href={game.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="win98-button"
                        style={{ flex: 2, textTransform: 'uppercase', fontSize: '0.6rem', padding: '4px' }}
                    >
                        RUN_GAME.BAT
                    </a>
                </div>
            </div>
        </div>
    );
};

export default GameCard;
