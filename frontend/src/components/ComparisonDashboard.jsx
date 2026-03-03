import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { compareProfessors } from "../api";
import "./ComparisonDashboard.css";

export default function ComparisonDashboard({ availableProfessors }) {
  const [selectedProfs, setSelectedProfs] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);

  const availableProfsList = availableProfessors || [];

  const toggleProfessor = (profName) => {
    if (selectedProfs.includes(profName)) {
      setSelectedProfs(selectedProfs.filter(p => p !== profName));
    } else if (selectedProfs.length < 5) {
      setSelectedProfs([...selectedProfs, profName]);
    }
  };

  const handleCompare = async () => {
    if (selectedProfs.length < 2) {
      alert("Please select at least 2 professors to compare");
      return;
    }

    setLoading(true);
    try {
      const response = await compareProfessors(selectedProfs);
      setComparisonData(response.data);
    } catch (error) {
      console.error("Error comparing professors:", error);
      alert("Failed to compare professors");
    } finally {
      setLoading(false);
    }
  };

  const clearSelection = () => {
    setSelectedProfs([]);
    setComparisonData(null);
  };

  // Prepare chart data
  const getRatingChartData = () => {
    if (!comparisonData) return [];
    return comparisonData.professors.map(p => ({
      name: p.name.split(' ').pop(), // Last name only
      fullName: p.name,
      rating: p.avg_rating,
      difficulty: p.avg_difficulty
    }));
  };

  const getPercentageChartData = () => {
    if (!comparisonData) return [];
    return comparisonData.professors.map(p => ({
      name: p.name.split(' ').pop(),
      fullName: p.name,
      positive: p.positive_percentage,
      negative: p.negative_percentage
    }));
  };

  const getRadarData = () => {
    if (!comparisonData || !comparisonData.professors) return [];

    // Normalize values for radar chart (0-100 scale)
    const maxRating = 5;
    const maxDiff = 5;

    return comparisonData.professors.map(p => ({
      professor: p.name.split(' ').pop(),
      fullName: p.name,
      Quality: (p.avg_rating / maxRating) * 100,
      Easiness: ((maxDiff - p.avg_difficulty) / maxDiff) * 100,
      Positive: p.positive_percentage,
      Consistency: Math.max(0, 100 - (p.rating_std * 20))
    }));
  };

  return (
    <div className="comparison-dashboard">
      <div className="comparison-header">
        <h2>📊 Professor Comparison</h2>
        <p className="comparison-subtitle">Compare up to 5 professors side by side</p>
      </div>

      {/* Professor Selection */}
      <div className="selection-section">
        <div className="selection-header">
          <h3>Select Professors to Compare</h3>
          <div className="selection-actions">
            <span className="selected-count">{selectedProfs.length}/5 selected</span>
            {selectedProfs.length > 0 && (
              <button className="btn-clear" onClick={clearSelection}>Clear All</button>
            )}
          </div>
        </div>

        <div className="professor-pool">
          {availableProfsList.slice(0, 50).map((prof, i) => (
            <button
              key={i}
              className={`professor-chip ${selectedProfs.includes(prof) ? 'selected' : ''}`}
              onClick={() => toggleProfessor(prof)}
              disabled={!selectedProfs.includes(prof) && selectedProfs.length >= 5}
            >
              {prof}
              {selectedProfs.includes(prof) && <span className="chip-check">✓</span>}
            </button>
          ))}
        </div>

        <button
          className="btn-compare"
          onClick={handleCompare}
          disabled={selectedProfs.length < 2 || loading}
        >
          {loading ? "Comparing..." : "Compare Now"}
        </button>
      </div>

      {/* Comparison Results */}
      {comparisonData && (
        <div className="comparison-results">
          {/* Summary Table */}
          <div className="comparison-table-card">
            <h3>Summary Statistics</h3>
            <div className="comparison-table">
              <div className="table-header">
                <div className="table-cell">Professor</div>
                <div className="table-cell">Rating</div>
                <div className="table-cell">Difficulty</div>
                <div className="table-cell">Reviews</div>
                <div className="table-cell">Positive %</div>
              </div>
              {comparisonData.professors.map((prof, i) => (
                <div key={i} className={`table-row ${i === 0 ? 'top-ranked' : ''}`}>
                  <div className="table-cell">
                    {i === 0 && <span className="rank-badge">🏆</span>}
                    {prof.name}
                  </div>
                  <div className="table-cell">
                    <span className="rating-badge">{prof.avg_rating}</span>
                  </div>
                  <div className="table-cell">{prof.avg_difficulty}</div>
                  <div className="table-cell">{prof.num_ratings}</div>
                  <div className="table-cell">
                    <span className="positive-badge">{prof.positive_percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Charts */}
          <div className="comparison-charts-grid">
            {/* Rating & Difficulty Bar Chart */}
            <div className="chart-card-comparison">
              <h3>Rating vs Difficulty</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={getRatingChartData()} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-45} textAnchor="end" height={60} />
                  <YAxis domain={[0, 5]} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="custom-tooltip">
                            <div style={{ fontWeight: 600, marginBottom: 8 }}>{data.fullName}</div>
                            {payload.map(p => (
                              <div key={p.dataKey} style={{ color: p.color }}>
                                {p.dataKey}: {p.value}
                              </div>
                            ))}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Legend />
                  <Bar dataKey="rating" fill="#3b82f6" name="Average Rating" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="difficulty" fill="#8b5cf6" name="Avg Difficulty" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Sentiment Percentage Chart */}
            <div className="chart-card-comparison">
              <h3>Sentiment Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={getPercentageChartData()} margin={{ top: 20, right: 20, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-45} textAnchor="end" height={60} />
                  <YAxis domain={[0, 100]} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="custom-tooltip">
                            <div style={{ fontWeight: 600, marginBottom: 8 }}>{data.fullName}</div>
                            {payload.map(p => (
                              <div key={p.dataKey} style={{ color: p.color }}>
                                {p.name}: {p.value}%
                              </div>
                            ))}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Legend />
                  <Bar dataKey="positive" fill="#10b981" name="Positive %" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="negative" fill="#ef4444" name="Negative %" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Radar Chart */}
            <div className="chart-card-comparison chart-card-full">
              <h3>Multi-Dimensional Comparison</h3>
              <ResponsiveContainer width="100%" height={350}>
                <RadarChart data={getRadarData()} margin={{ top: 20, right: 80, bottom: 20, left: 80 }}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis dataKey="professor" tick={{ fontSize: 11 }} />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fontSize: 10 }} />
                  <Radar
                    name="Quality"
                    dataKey="Quality"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="Easiness"
                    dataKey="Easiness"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="Positive Feedback"
                    dataKey="Positive"
                    stroke="#f59e0b"
                    fill="#f59e0b"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="Consistency"
                    dataKey="Consistency"
                    stroke="#8b5cf6"
                    fill="#8b5cf6"
                    fillOpacity={0.3}
                  />
                  <Legend />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="custom-tooltip">
                            <div style={{ fontWeight: 600, marginBottom: 8 }}>{data.fullName}</div>
                            {payload.map(p => (
                              <div key={p.dataKey} style={{ color: p.color }}>
                                {p.name}: {p.value.toFixed(1)}
                              </div>
                            ))}
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {selectedProfs.length > 0 && !comparisonData && (
        <div className="compare-prompt">
          <p>Click "Compare Now" to see the comparison results</p>
        </div>
      )}
    </div>
  );
}
