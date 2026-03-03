import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import TrendChart from "./TrendChart";
import "./Insights.css";

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

export default function Insights({ data, trendData, predictionData }) {
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

  // Combine trend and prediction data
  const combinedTrendData = predictionData || trendData;

  return (
    <div className="insights-container">
      {/* Header */}
      <div className="insights-header">
        <h2 className="professor-name">{data.professor}</h2>
        <div className="rating-badges">
          <div className="rating-badge rating-badge-primary">
            <div className="rating-label">Quality</div>
            <div className="rating-value">{data.avg_rating}</div>
          </div>
          <div className="rating-badge rating-badge-secondary">
            <div className="rating-label">Difficulty</div>
            <div className="rating-value">{data.avg_difficulty}</div>
          </div>
          <div className="rating-badge rating-badge-info">
            <div className="rating-label">Ratings</div>
            <div className="rating-value">{data.num_ratings}</div>
          </div>
        </div>
      </div>

      {/* Courses */}
      {data.courses && data.courses.length > 0 && (
        <div className="courses-section">
          <h4>Courses</h4>
          <div className="courses-list">
            {data.courses.map((course, i) => (
              <span key={i} className="course-tag">{course}</span>
            ))}
          </div>
        </div>
      )}

      {/* Trend Chart */}
      {combinedTrendData && (
        <TrendChart data={combinedTrendData} />
      )}

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Sentiment Chart */}
        <div className="chart-card">
          <h3>Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={sentData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis
                dataKey="name"
                tick={{ fill: '#6b7280' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#6b7280' }}
                tickLine={false}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="custom-tooltip">
                        <div style={{ fontWeight: 600, marginBottom: 4 }}>
                          {data.name.charAt(0).toUpperCase() + data.name.slice(1)}
                        </div>
                        <div>Count: {data.value}</div>
                        <div>Percentage: {data.percentage}%</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {sentData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[entry.name] || "#6b7280"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="chart-summary">
            {sentData.map(item => (
              <div key={item.name} className="summary-item">
                <span
                  className="summary-dot"
                  style={{ background: COLORS[item.name] }}
                ></span>
                <span className="summary-label">{item.name}</span>
                <span className="summary-value">{item.percentage}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Category Chart */}
        <div className="chart-card">
          <h3>Category Breakdown</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={catData} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
              <XAxis
                dataKey="name"
                tick={{ fill: '#6b7280', fontSize: 11 }}
                tickLine={false}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis
                tick={{ fill: '#6b7280' }}
                tickLine={false}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="custom-tooltip">
                        <div style={{ fontWeight: 600, marginBottom: 4 }}>
                          {data.name}
                        </div>
                        <div>Mentions: {data.value}</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {catData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={CATEGORY_COLORS[entry.originalKey] || "#6b7280"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="chart-summary">
            {catData.map(item => (
              <div key={item.name} className="summary-item">
                <span
                  className="summary-dot"
                  style={{ background: CATEGORY_COLORS[item.originalKey] }}
                ></span>
                <span className="summary-label">{item.name}</span>
                <span className="summary-value">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
