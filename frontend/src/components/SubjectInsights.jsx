import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

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

function round(value, decimals) {
  return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

export default function SubjectInsights({ data, onBack }) {
  if (!data) return null;

  // Prepare sentiment data
  const sentData = Object.entries(data.sentiment_distribution || {}).map(([k, v]) => ({
    name: k,
    value: v
  }));

  // Prepare category data
  const catData = Object.entries(data.category_counts || {}).map(([k, v]) => ({
    name: k.replace('_', ' '),
    value: v,
    originalKey: k
  }));

  // Prepare top professors data
  const profData = Object.entries(data.top_professors || {}).map(([name, rating]) => ({
    name: name.split(' ').slice(0, 2).join(' '), // First 2 words
    rating: round(rating, 2),
    fullName: name
  }));

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h2 style={{ margin: 0 }}>{data.name}</h2>
          <span style={{
            padding: '4px 12px',
            borderRadius: 12,
            fontSize: 12,
            fontWeight: 500,
            background: data.type === 'online' ? '#ecfdf5' : '#fffbeb',
            color: data.type === 'online' ? '#059669' : '#d97706'
          }}>
            {data.type === 'online' ? '🌐 Online' : '🏛️ Onsite'}
          </span>
        </div>
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

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: 'white', border: '1px solid #e5e7eb', borderRadius: 8, textAlign: 'center' }}>
          <div style={{ fontSize: 12, color: '#6b7280', marginBottom: 4 }}>Avg Quality</div>
          <div style={{ fontSize: 24, fontWeight: 600, color: '#3b82f6' }}>{data.avg_quality}</div>
        </div>
        <div style={{ padding: 16, background: 'white', border: '1px solid #e5e7eb', borderRadius: 8, textAlign: 'center' }}>
          <div style={{ fontSize: 12, color: '#6b7280', marginBottom: 4 }}>Avg Difficulty</div>
          <div style={{ fontSize: 24, fontWeight: 600, color: '#f59e0b' }}>{data.avg_difficulty}</div>
        </div>
        <div style={{ padding: 16, background: 'white', border: '1px solid #e5e7eb', borderRadius: 8, textAlign: 'center' }}>
          <div style={{ fontSize: 12, color: '#6b7280', marginBottom: 4 }}>Total Reviews</div>
          <div style={{ fontSize: 24, fontWeight: 600, color: '#8b5cf6' }}>{data.total_reviews}</div>
        </div>
      </div>

      {/* Course Codes */}
      {data.course_codes && data.course_codes.length > 0 && data.course_codes[0] !== 'N/A' && (
        <div style={{ marginBottom: 24 }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: 14 }}>Course Codes</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {data.course_codes.slice(0, 15).map((code, idx) => (
              code !== 'N/A' && (
                <span
                  key={idx}
                  style={{
                    padding: '4px 10px',
                    background: '#f3f4f6',
                    borderRadius: 12,
                    fontSize: 12,
                    color: '#374151'
                  }}
                >
                  {code}
                </span>
              )
            ))}
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
        {/* Sentiment Distribution */}
        <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: '#f9fafb' }}>
          <h3 style={{ marginTop: 0 }}>Sentiment Distribution</h3>
          <ResponsiveContainer width={400} height={250}>
            <BarChart data={sentData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis dataKey="name" tick={{ fill: '#6b7280' }} tickLine={false} />
              <YAxis tick={{ fill: '#6b7280' }} tickLine={false} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 4, padding: 8 }}>
                        <div style={{ fontWeight: 600 }}>{payload[0].payload.name.charAt(0).toUpperCase() + payload[0].payload.name.slice(1)}</div>
                        <div>Count: {payload[0].payload.value}</div>
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
                {item.name}: {item.value}
              </span>
            ))}
          </div>
        </div>

        {/* Top Professors */}
        <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: '#f9fafb' }}>
          <h3 style={{ marginTop: 0 }}>Top Professors</h3>
          <ResponsiveContainer width={400} height={250}>
            <BarChart data={profData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis
                dataKey="name"
                tick={{ fill: '#6b7280', fontSize: 11 }}
                tickLine={false}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#6b7280' }} tickLine={false} domain={[0, 5]} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 4, padding: 8 }}>
                        <div style={{ fontWeight: 600 }}>{payload[0].payload.fullName}</div>
                        <div>Rating: {payload[0].payload.rating}</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="rating" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Category Breakdown */}
        {catData.length > 0 && (
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
                      return (
                        <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 4, padding: 8 }}>
                          <div style={{ fontWeight: 600 }}>{payload[0].payload.name}</div>
                          <div>Mentions: {payload[0].payload.value}</div>
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
          </div>
        )}
      </div>
    </div>
  );
}
