import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from "recharts";
import "./TrendChart.css";

export default function TrendChart({ data }) {
  if (!data || data.error) {
    return (
      <div className="trend-chart-container">
        <div className="error-message">
          {data?.error || "No trend data available"}
        </div>
      </div>
    );
  }

  // Check if we have prediction data or just trend data
  const hasPrediction = data.future && data.future.predicted_ratings;

  // Prepare chart data for trend view
  let chartData = [];

  if (hasPrediction) {
    // Prediction view: combine historical + future
    const historicalData = data.historical.dates.map((date, i) => ({
      date: date.substring(5), // Show MM-DD only
      fullDate: date,
      actualRating: data.historical.ratings[i],
      trendLine: data.historical.trend_line[i],
      isFuture: false
    }));

    const futureData = data.future.dates.map((date, i) => ({
      date: date.substring(5),
      fullDate: date,
      predictedRating: data.future.predicted_ratings[i],
      lowerBound: data.future.lower_bound[i],
      upperBound: data.future.upper_bound[i],
      isFuture: true
    }));

    chartData = [...historicalData, ...futureData];
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

  const getTrendIcon = () => {
    if (trendDirection === "increasing") return "📈";
    if (trendDirection === "decreasing") return "📉";
    return "➡️";
  };

  const getTrendClass = () => {
    if (trendDirection === "increasing") return "trend-up";
    if (trendDirection === "decreasing") return "trend-down";
    return "trend-stable";
  };

  return (
    <div className="trend-chart-container">
      <div className="trend-header">
        <h3>Rating Trend Analysis</h3>
        {trendDirection && (
          <div className={`trend-badge ${getTrendClass()}`}>
            <span className="trend-icon">{getTrendIcon()}</span>
            <span className="trend-text">{trendDirection}</span>
            {trendPercentage && <span className="trend-percent">{trendPercentage}</span>}
          </div>
        )}
      </div>

      {hasPrediction && (
        <div className="prediction-info">
          <div className="prediction-card">
            <div className="prediction-label">Next Semester Prediction</div>
            <div className="prediction-value">{data.next_semester_prediction}</div>
            <div className="prediction-confidence">
              Confidence: {data.confidence}% | R²: {data.model_quality.r_squared}
            </div>
          </div>
        </div>
      )}

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <YAxis
            domain={[1, 5]}
            tick={{ fontSize: 12 }}
            stroke="#666"
            label={{ value: 'Rating', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="custom-tooltip">
                    <div className="tooltip-date">{data.fullDate}</div>
                    {data.actualRating !== undefined && (
                      <div className="tooltip-item">
                        <span className="tooltip-label">Actual:</span>
                        <span className="tooltip-value">{data.actualRating.toFixed(2)}</span>
                      </div>
                    )}
                    {data.trendLine !== undefined && (
                      <div className="tooltip-item">
                        <span className="tooltip-label">Trend:</span>
                        <span className="tooltip-value">{data.trendLine.toFixed(2)}</span>
                      </div>
                    )}
                    {data.predictedRating !== undefined && (
                      <div className="tooltip-item predicted">
                        <span className="tooltip-label">Predicted:</span>
                        <span className="tooltip-value">{data.predictedRating.toFixed(2)}</span>
                      </div>
                    )}
                    {data.lowerBound !== undefined && (
                      <div className="tooltip-item">
                        <span className="tooltip-label">Range:</span>
                        <span className="tooltip-value">
                          {data.lowerBound.toFixed(2)} - {data.upperBound.toFixed(2)}
                        </span>
                      </div>
                    )}
                  </div>
                );
              }
              return null;
            }}
          />
          <Legend />

          {/* Actual ratings (historical only) */}
          <Line
            type="monotone"
            dataKey="actualRating"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 4 }}
            name="Actual Rating"
            connectNulls={false}
          />

          {/* Trend line */}
          <Line
            type="monotone"
            dataKey="trendLine"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
            name="Trend Line"
          />

          {/* Predicted ratings (future only) */}
          {hasPrediction && (
            <Line
              type="monotone"
              dataKey="predictedRating"
              stroke="#f59e0b"
              strokeWidth={2}
              strokeDasharray="8 4"
              dot={{ r: 4, fill: "#f59e0b" }}
              name="Predicted Rating"
              connectNulls={false}
            />
          )}

          {/* Confidence interval bounds (future only) */}
          {hasPrediction && (
            <>
              <Line
                type="monotone"
                dataKey="upperBound"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="2 2"
                dot={false}
                name="Upper Bound (95%)"
                hide={true} // Hide from legend
              />
              <Line
                type="monotone"
                dataKey="lowerBound"
                stroke="#f59e0b"
                strokeWidth={1}
                strokeDasharray="2 2"
                dot={false}
                name="Lower Bound (95%)"
                hide={true} // Hide from legend
              />
            </>
          )}
        </LineChart>
      </ResponsiveContainer>

      <div className="chart-legend">
        <div className="legend-item">
          <span className="legend-dot" style={{ background: "#2563eb" }}></span>
          <span>Actual Rating</span>
        </div>
        <div className="legend-item">
          <span className="legend-line" style={{ background: "#10b981", borderStyle: "dashed" }}></span>
          <span>Trend Line</span>
        </div>
        {hasPrediction && (
          <div className="legend-item">
            <span className="legend-dot" style={{ background: "#f59e0b" }}></span>
            <span>Predicted Rating</span>
          </div>
        )}
      </div>

      {data.data_points && (
        <div className="chart-footer">
          Data points: {data.data_points}
        </div>
      )}
    </div>
  );
}
