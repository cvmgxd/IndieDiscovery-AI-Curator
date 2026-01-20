'use client';

import React, { useEffect, useState } from 'react';
import GameCard from '../components/game_card';
import { GameEntry } from '../types';

export default function DiscoveryDashboard() {
  const [games, setGames] = useState<GameEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
        const response = await fetch(`${apiUrl}/api/discover`, { cache: 'no-store' });
        if (!response.ok) throw new Error('Failed to fetch from backend');
        const data: GameEntry[] = await response.json();
        setGames(data);
      } catch (error) {
        console.error("Failed to fetch games:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  return (
    <main style={{ minHeight: '100vh', padding: '20px 20px 50px 20px', position: 'relative' }} className="pixel-grid">
      {/* Desktop Branded Window */}
      <div className="window" style={{ maxWidth: '800px', margin: '0 auto 40px auto' }}>
        <div className="window-header">
          <div className="window-title">C:\INDIE_DISCOVERY\WELCOME.EXE</div>
          <div className="window-controls">
            <div className="window-button">_</div>
            <div className="window-button">□</div>
            <div className="window-button">×</div>
          </div>
        </div>
        <div style={{ padding: '20px', textAlign: 'center', background: '#fff' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '8px', color: '#000' }}>
            Indie Discovery
          </h1>
          <p style={{ fontSize: '1rem', color: '#666' }}>
            AI-POWERED EXPERIMENTAL GAME CURATOR v1.0
          </p>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', marginTop: '100px' }}>
          <div style={{
            display: 'inline-block',
            padding: '20px',
            background: '#fff',
            border: '2px solid #000'
          }}>
            <div style={{ marginBottom: '10px' }}>SCANNING SECTORS...</div>
            <div style={{ width: '200px', height: '20px', background: '#eee', border: '1px solid #888' }}>
              <div style={{ width: '60%', height: '100%', background: 'var(--win-title-blue)' }}></div>
            </div>
          </div>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '30px'
        }}>
          {games.map(game => (
            <GameCard key={game.id} game={game} />
          ))}
        </div>
      )}

      {/* Retro Taskbar */}
      <div className="taskbar">
        <button className="start-button">
          <span style={{ fontSize: '1.2rem' }}>🪟</span> Start
        </button>
        <div style={{
          marginLeft: '4px',
          padding: '0 8px',
          height: '22px',
          display: 'flex',
          alignItems: 'center',
          background: '#eee',
          border: '1px solid #888',
          boxShadow: 'inset 1px 1px 0 #fff',
          fontSize: '0.7rem'
        }}>
          Search: FEATURED_GEMS.DB
        </div>
        <div className="tray">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </main>
  );
}
