// src/components/RankingDashboard.jsx
import React, { useState, useEffect } from 'react';
import { getTopProfessors } from '../api';

const RankingDashboard = () => {
  const [rankings, setRankings] = useState([]);
  const [sortBy, setSortBy] = useState('rating');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getTopProfessors(sortBy, 15) // ดึง 15 อันดับ
      .then(res => {
        setRankings(res.data);
      })
      .catch(err => console.error("Error fetching rankings:", err))
      .finally(() => setLoading(false));
  }, [sortBy]);

  return (
    <div style={{ background: 'white', padding: 24, borderRadius: 12, boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
      <h2 style={{ marginTop: 0, color: '#1f2937' }}>🏆 Top Professors Ranking</h2>
      
      <div style={{ marginBottom: 20 }}>
        <label style={{ marginRight: 10, fontWeight: 'bold' }}>Sort by: </label>
        <select 
          value={sortBy} 
          onChange={(e) => setSortBy(e.target.value)}
          style={{ padding: '8px 12px', borderRadius: 6, border: '1px solid #d1d5db' }}
        >
          <option value="rating">Top Rated</option>
          <option value="easiest">Easiest</option>
          <option value="hardest">Hardest</option>
          <option value="most_reviews">Most Reviewed</option>
        </select>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: 40, color: '#6b7280' }}>Loading rankings...</div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ padding: 12 }}>Rank</th>
              <th style={{ padding: 12 }}>Name</th>
              <th style={{ padding: 12 }}>Rating</th>
              <th style={{ padding: 12 }}>Difficulty</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((prof, index) => (
              <tr key={prof.name} style={{ borderBottom: '1px solid #e5e7eb' }}>
                <td style={{ padding: 12, fontWeight: 'bold', color: index < 3 ? '#f59e0b' : '#374151' }}>
                  #{index + 1}
                </td>
                <td style={{ padding: 12 }}>{prof.name}</td>
                <td style={{ padding: 12 }}>⭐ {prof.avg_rating}</td>
                <td style={{ padding: 12 }}>🔥 {prof.avg_difficulty}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default RankingDashboard;