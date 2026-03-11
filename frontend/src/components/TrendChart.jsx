import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from "recharts";
import "./TrendChart.css";

export default function TrendChart({ data }) {
  if (!data || data.error) {
    return (
      <div className="trend-chart-container" style={{ 
        display: 'flex', flexDirection: 'column', alignItems: 'center', 
        justifyContent: 'center', height: '350px', 
        backgroundColor: '#f9fafb', border: '2px dashed #e5e7eb', 
        borderRadius: '12px', padding: '20px', textAlign: 'center'
      }}>
        <div style={{ fontSize: '48px', opacity: '0.5', marginBottom: '16px' }}>📉</div>
        <h3 style={{ color: '#4b5563', margin: '0 0 8px 0' }}>Trend Chart Unavailable</h3>
        <p style={{ color: '#6b7280', fontSize: '14px', margin: 0, maxWidth: '80%' }}>
          {data?.error || "Not enough data points to generate a reliable trend."}
        </p>
      </div>
    );
  }

  // Check if we have prediction data or just trend data
  const hasPrediction = data.future && data.future.predicted_ratings;

  // Prepare chart data for trend view
  let chartData = [];
  let showConfidenceInterval = false;

  if (hasPrediction) {
    // Prediction view: combine historical + future
    const historicalData = data.historical.dates.map((date, i) => ({
      date: date.substring(0,7),
      fullDate: date,
      actualRating: data.historical.ratings[i],
      trendLine: data.historical.trend_line[i],
      isFuture: false
    }));

    const futureData = data.future.dates.map((date, i) => ({
      date: date.substring(0,7),
      fullDate: date,
      predictedRating: data.future.predicted_ratings[i],
      lowerBound: data.future.lower_bound[i],
      upperBound: data.future.upper_bound[i],
      isFuture: true
    }));

    chartData = [...historicalData, ...futureData];
    showConfidenceInterval = true;
  } else {
    // Simple trend view
    chartData = data.dates.map((date, i) => ({
      date: date.substring(5),
      fullDate: date,
      actualRating: data.ratings[i],
      trendLine: data.trend_line[i]
    }));
  }

  const trendDirection = data.trend_direction || data.model_quality?.trend_direction;
  const trendPercentage = data.trend_percentage;
  const rSquared = data.model_quality?.r_squared;

  const getTrendIcon = () => {
    if (trendDirection === "increasing") return "📈";
    if (trendDirection === "decreasing") return "📉";
    return "➡️";
  };

  const getTrendClass = () => {
    if (trendDirection === "increasing") return "trend-increasing";
    if (trendDirection === "decreasing") return "trend-decreasing";
    return "trend-stable";
  };

  return (
    <div className="trend-chart-container">
      <div className="trend-header">
        <h3>Rating Trend & Prediction</h3>

        <div className={`trend-indicator ${getTrendClass()}`}>
          <span className="trend-icon">{getTrendIcon()}</span>
          <span className="trend-text">
            {trendDirection || "Stable"} ({trendPercentage >= 0 ? "+" : ""}{trendPercentage}%)
          </span>
        </div>
      </div>

      {rSquared !== undefined && (
        <div className="model-quality">
          <span className="quality-label">Model Quality:</span>
          <span className="quality-value">R² = {rSquared.toFixed(3)}</span>
        </div>
      )}

      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#666', fontSize: 12 }}
            tickLine={false}
          />
          <YAxis
            domain={[1, 5]}
            tick={{ fill: '#666', fontSize: 12 }}
            tickLine={false}
            label={{ value: 'Rating', position: 'insideLeft', angle: -90, dy: -10, fill: '#666' }}
          />
          <Tooltip
            content={({ active, payload, label }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="custom-tooltip">
                    <div className="tooltip-date">{data.fullDate}</div>
                    {data.actualRating !== undefined && (
                      <div>Actual Rating: <strong>{data.actualRating.toFixed(2)}</strong></div>
                    )}
                    {data.trendLine !== undefined && (
                      <div>Trend Line: <strong>{data.trendLine.toFixed(2)}</strong></div>
                    )}
                    {data.predictedRating !== undefined && (
                      <>
                        <div>Predicted: <strong>{data.predictedRating.toFixed(2)}</strong></div>
                        {showConfidenceInterval && (
                          <div className="confidence-interval">
                            Range: {data.lowerBound.toFixed(2)} - {data.upperBound.toFixed(2)}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                );
              }
              return null;
            }}
          />
          <Legend />

          {/* Actual Ratings */}
          <Line
            type="monotone"
            dataKey="actualRating"
            stroke="#3b82f6"
            strokeWidth={2}
            name="Actual Rating"
            dot={{ r: 3 }}
            connectNulls={false}
          />

          {/* Trend Line */}
          <Line
            type="monotone"
            dataKey="trendLine"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="5 5"
            name="Trend Line"
            dot={false}
          />

          {/* Predicted Values */}
          {hasPrediction && (
            <Line
              type="monotone"
              dataKey="predictedRating"
              stroke="#f59e0b"
              strokeWidth={2}
              strokeDasharray="3 3"
              name="Predicted"
              dot={{ r: 4, fill: "#f59e0b" }}
              connectNulls={false}
            />
          )}

          {/* Confidence Interval Bounds */}
          {hasPrediction && showConfidenceInterval && (
            <>
              <Line
                type="monotone"
                dataKey="upperBound"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="2 2"
                opacity={0.3}
                dot={false}
                hideLegend={true}
              />
              <Line
                type="monotone"
                dataKey="lowerBound"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="2 2"
                opacity={0.3}
                dot={false}
                hideLegend={true}
              />
            </>
          )}
        </LineChart>
      </ResponsiveContainer>

      {hasPrediction && (
        <div className="prediction-legend">
          <div className="legend-item">
            <span className="legend-line actual"></span>
            <span>Actual Rating</span>
          </div>
          <div className="legend-item">
            <span className="legend-line trend"></span>
            <span>Trend Line</span>
          </div>
          <div className="legend-item">
            <span className="legend-line predicted"></span>
            <span>Predicted (95% CI)</span>
          </div>
        </div>
      )}
    </div>
  );
}
