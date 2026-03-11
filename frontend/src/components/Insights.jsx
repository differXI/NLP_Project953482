import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import TrendChart from "./TrendChart";

const COLORS = {
  positive: "#10b981",
  negative: "#ef4444",
  neutral: "#6b7280"
};

const CATEGORY_COLORS = {
  teaching_clarity: "#3b82f6",
  speaking_pace: "#8b5cf6",
  course_structure: "#ec4899",
  communication: "#f59e0b",
  professional_behavior: "#10b981"
};

export default function Insights({ data, trendData, predictionData, onBack }) {
  if (!data) return null;

  // Prepare sentiment chart data
  const sentData = Object.entries(data.sentiment_counts || {}).map(([k, v]) => ({
    name: k,
    value: v,
    percentage: data.sentiment_percentages?.[k] || 0
  }));

  // Prepare category chart data
  const catData = Object.entries(data.category_counts || {}).map(([k, v]) => ({
    name: k.replace('_', ' '),
    value: v,
    originalKey: k
  }));

  // Combine trend and prediction data (prefer prediction)
  const combinedTrendData = predictionData || trendData;

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <h2 style={{ margin: 0 }}>{data.professor}</h2>
        {onBack && (
          <button
            onClick={onBack}
            style={{
              padding: '8px 16px',
              background: '#f3f4f6',
              border: '1px solid #d1d5db',
              borderRadius: 6,
              cursor: 'pointer',
              fontSize: 13,
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.background = '#e5e7eb'}
            onMouseLeave={(e) => e.target.style.background = '#f3f4f6'}
          >
            ← Back to List
          </button>
        )}
      </div>

      <p>Avg Rating: <strong>{data.avg_rating}</strong></p>
      <p>Avg Difficulty: <strong>{data.avg_difficulty}</strong></p>

      {/* Courses Taught */}
      {data.courses && data.courses.length > 0 && (
        <div style={{ marginBottom: 20 }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: 14 }}>Courses Taught</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {data.courses.map((course, idx) => (
              <span
                key={idx}
                style={{
                  padding: '4px 10px',
                  background: '#f3f4f6',
                  borderRadius: 12,
                  fontSize: 13,
                  color: '#374151'
                }}
              >
                {course}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Trend Chart */}
      {combinedTrendData && (
        <div style={{ marginBottom: 24 }}>
          <TrendChart data={combinedTrendData} />
        </div>
      )}

      {/* Charts Grid */}
      <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
        {/* Sentiment Chart */}
        <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: '#f9fafb' }}>
          <h3 style={{ marginTop: 0 }}>Sentiment Distribution</h3>
          <ResponsiveContainer width={400} height={250}>
            <BarChart data={sentData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis dataKey="name" tick={{ fill: '#6b7280' }} tickLine={false} />
              <YAxis tick={{ fill: '#6b7280' }} tickLine={false} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const d = payload[0].payload;
                    return (
                      <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 4, padding: 8 }}>
                        <div style={{ fontWeight: 600 }}>{d.name.charAt(0).toUpperCase() + d.name.slice(1)}</div>
                        <div>Count: {d.value}</div>
                        <div>Percentage: {d.percentage}%</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {sentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name] || "#6b7280"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div style={{ marginTop: 12, fontSize: 12, color: '#6b7280' }}>
            {sentData.map(item => (
              <span key={item.name} style={{ marginRight: 16 }}>
                <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: COLORS[item.name], marginRight: 4 }}></span>
                {item.name}: {item.percentage}%
              </span>
            ))}
          </div>
        </div>

        {/* Category Chart */}
        <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: '#f9fafb' }}>
          <h3 style={{ marginTop: 0 }}>Category Breakdown</h3>
          <ResponsiveContainer width={400} height={250}>
            <BarChart data={catData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis
                dataKey="name"
                tick={{ fill: '#6b7280', fontSize: 11 }}
                tickLine={false}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#6b7280' }} tickLine={false} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const d = payload[0].payload;
                    return (
                      <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 4, padding: 8 }}>
                        <div style={{ fontWeight: 600 }}>{d.name}</div>
                        <div>Mentions: {d.value}</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {catData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[entry.originalKey] || "#6b7280"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div style={{ marginTop: 12, fontSize: 12, color: '#6b7280' }}>
            {catData.map(item => (
              <span key={item.name} style={{ marginRight: 16 }}>
                <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: CATEGORY_COLORS[item.originalKey], marginRight: 4 }}></span>
                {item.name}: {item.value}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
