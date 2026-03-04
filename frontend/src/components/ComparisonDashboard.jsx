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
      alert("Failed to compare professors. Please try again.");
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
    if (!comparisonData || !comparisonData.professors) return [];

    return comparisonData.professors.map(p => ({
      name: p.name.split(' ').pop(), // Last name only
      fullName: p.name,
      rating: p.avg_rating,
      difficulty: p.avg_difficulty
    }));
  };

  const getPercentageChartData = () => {
    if (!comparisonData || !comparisonData.professors) return [];

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
      {/* Selection Section */}
      <div className="selection-section">
        <div className="selection-header">
          <h3>Select Professors to Compare (max 5)</h3>
          <div className="selection-actions">
            <span className="selected-count">
              {selectedProfs.length} / 5 selected
            </span>
            {selectedProfs.length > 0 && (
              <button className="btn-clear" onClick={clearSelection}>
                Clear
              </button>
            )}
          </div>
        </div>

        <div className="professor-pool">
          {availableProfsList.slice(0, 50).map(prof => (
            <button
              key={prof}
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
          {loading ? "Analyzing..." : "Compare Professors"}
        </button>
      </div>

      {/* Results Section */}
      {comparisonData && comparisonData.professors && (
        <div className="comparison-results">
          {/* Summary Cards */}
          <div className="summary-cards">
            <div className="summary-card">
              <div className="summary-label">Highest Rated</div>
              <div className="summary-value">
                🏆 {comparisonData.comparison.highest_rated}
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Easiest</div>
              <div className="summary-value">
                ⬇️ {comparisonData.comparison.easiest}
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Most Consistent</div>
              <div className="summary-value">
                📊 {comparisonData.comparison.most_consistent}
              </div>
            </div>
          </div>

          {/* Comparison Table */}
          <div className="comparison-table-card">
            <h3>Comparison Table</h3>
            <div className="comparison-table">
              <div className="table-header">
                <div>Professor</div>
                <div>Rating</div>
                <div>Difficulty</div>
                <div>Reviews</div>
                <div>Positive %</div>
              </div>

              {comparisonData.professors.map((prof, index) => (
                <div
                  key={prof.name}
                  className={`table-row ${
                    prof.name === comparisonData.comparison.highest_rated ? 'top-ranked' : ''
                  }`}
                >
                  <div className="table-cell">
                    {prof.name === comparisonData.comparison.highest_rated && "🏆 "}
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
            {/* Rating vs Difficulty Bar Chart */}
            <div className="chart-card-comparison">
              <h3>Rating vs Difficulty</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={getRatingChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fill: '#666', fontSize: 11 }} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="rating" fill="#3b82f6" name="Rating" />
                  <Bar dataKey="difficulty" fill="#8b5cf6" name="Difficulty" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Sentiment Bar Chart */}
            <div className="chart-card-comparison">
              <h3>Sentiment Comparison</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={getPercentageChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fill: '#666', fontSize: 11 }} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="positive" fill="#10b981" name="Positive %" />
                  <Bar dataKey="negative" fill="#ef4444" name="Negative %" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Radar Chart */}
            <div className="chart-card-comparison chart-card-full">
              <h3>Multi-Dimensional Comparison</h3>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={getRadarData()}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="professor" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name={comparisonData.professors[0]?.name}
                    dataKey="Quality"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.6}
                  />
                  <Radar
                    name={comparisonData.professors[0]?.name}
                    dataKey="Easiness"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.6}
                  />
                  <Radar
                    name={comparisonData.professors[0]?.name}
                    dataKey="Positive"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.6}
                  />
                  {comparisonData.professors.slice(1).map((prof, index) => (
                    <g key={prof.name}>
                      <Radar
                        name={prof.name}
                        dataKey="Quality"
                        stroke={COLORS[index % COLORS.length]}
                        fill={COLORS[index % COLORS.length]}
                        fillOpacity={0.3}
                      />
                      <Radar
                        name={prof.name}
                        dataKey="Easiness"
                        stroke={COLORS[index % COLORS.length]}
                        fill={COLORS[index % COLORS.length]}
                        fillOpacity={0.3}
                      />
                      <Radar
                        name={prof.name}
                        dataKey="Positive"
                        stroke={COLORS[index % COLORS.length]}
                        fill={COLORS[index % COLORS.length]}
                        fillOpacity={0.3}
                      />
                    </g>
                  ))}
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {!comparisonData && (
        <div className="compare-prompt">
          <div className="compare-icon">📊</div>
          <div>Select 2 or more professors and click "Compare Professors" to see the analysis</div>
        </div>
      )}
    </div>
  );
}

// Color palette for radar chart
const COLORS = ['#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4'];
