import React, { useState, useEffect } from 'react';
import { getPredictedRankings } from '../api';

const PredictionDashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

useEffect(() => {
  setLoading(true);
  getPredictedRankings(15) // เรียกฟังก์ชันใหม่ที่สร้างขึ้น
    .then(res => setData(res.data))
    .catch(err => console.error(err))
    .finally(() => setLoading(false));
}, []);

  return (
    <div style={{ background: 'white', padding: 24, borderRadius: 12, boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h2 style={{ margin: 0, color: '#1f2937' }}>✨ Prediction Analytics</h2>
        <span style={{ 
          fontSize: '12px', 
          color: '#3b82f6', 
          background: '#eff6ff', 
          padding: '6px 12px', 
          borderRadius: '20px', 
          fontWeight: '500' 
        }}>
          Forecasted from Latest Sentiment
        </span>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: 40, color: '#6b7280' }}>Analyzing trends...</div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ padding: 12 }}>Rank</th>
              <th style={{ padding: 12 }}>Name</th>
              <th style={{ padding: 12 }}>Actual Rating</th>
              <th style={{ padding: 12, color: '#2563eb' }}>Predicted Rating</th>
              <th style={{ padding: 12 }}>Trend</th>
            </tr>
          </thead>
          <tbody>
            {data.map((prof, index) => {
              // 1. Precise logic for trend states
              const isRising = prof.predicted_rating > prof.avg_rating;
              const isFalling = prof.predicted_rating < prof.avg_rating;
              const isStable = Math.abs(prof.predicted_rating - prof.avg_rating) < 0.01;

              // 2. Determine background color based on trend
              let bgColor = 'white';
              if (isRising) bgColor = '#f0fdf4'; // Light Green
              else if (isFalling) bgColor = '#fff5f5'; // Light Red (Optional)

              return (
                <tr key={prof.name} style={{ borderBottom: '1px solid #e5e7eb', background: bgColor }}>
                  <td style={{ padding: 12, fontWeight: 'bold' }}>#{index + 1}</td>
                  <td style={{ padding: 12 }}>{prof.name}</td>
                  <td style={{ padding: 12 }}>⭐ {prof.avg_rating.toFixed(2)}</td>
                  <td style={{ padding: 12, fontWeight: 'bold', color: '#2563eb' }}>
                    📊 {prof.predicted_rating.toFixed(2)}
                  </td>
                  <td style={{ padding: 12, fontSize: '18px' }}>
                    {/* 3. Improved Icon Logic */}
                    {isRising ? '🚀' : (isFalling ? '📉' : '➡️')}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
      
      <div style={{ 
        marginTop: 20, 
        padding: '12px', 
        borderRadius: '8px', 
        background: '#fffbeb', 
        border: '1px solid #fef3c7', 
        fontSize: '12px', 
        color: '#92400e' 
      }}>
        <strong>💡 Note:</strong> Green rows indicate instructors with a positive rating trend calculated from student sentiment in the most recent reviews.
      </div>
    </div>
  );
};

export default PredictionDashboard;