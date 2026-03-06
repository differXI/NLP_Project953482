import { useEffect, useState } from "react";
import { getProfessors, getProfessor, searchProf, getProfessorTrend, predictProfessorRating } from "./api";
import SearchBar from "./components/SearchBar";
import ProfessorList from "./components/ProfessorList";
import Insights from "./components/Insights";
import ComparisonDashboard from "./components/ComparisonDashboard";
import RankingDashboard from "./components/RankingDashboard";

function App() {
  const [profs, setProfs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [data, setData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("ranking"); // "individual", "comparison", or "ranking"

  useEffect(() => {
    getProfessors().then(r => setProfs(r.data));
  }, []);

  const selectProf = async (name) => {
    setView("individual");
    setSelected(name);
    setLoading(true);
    setData(null);
    setTrendData(null);
    setPredictionData(null);

    try {
      // Fetch all data in parallel
      const [detailRes, trendRes, predictionRes] = await Promise.all([
        getProfessor(name),
        getProfessorTrend(name).catch(() => ({ data: null })),
        predictProfessorRating(name, 5).catch(() => ({ data: null }))
      ]);

      setData(detailRes.data);
      setTrendData(trendRes.data);
      setPredictionData(predictionRes.data);
    } catch (error) {
      console.error("Error fetching professor data:", error);
    } finally {
      setLoading(false);
    }
  };

  const search = (q) => {
    searchProf(q).then(r => setProfs(r.data));
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif', background: '#f9fafb', minHeight: '100vh' }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <header style={{ marginBottom: 30, textAlign: 'center' }}>
          <h1 style={{ color: '#1f2937', marginBottom: 8 }}>
            📊 Course & Instructor Evaluation Analytics
          </h1>
          <p style={{ color: '#6b7280', fontSize: 14 }}>
            NLP-powered sentiment analysis, trend prediction, and multi-label categorization
          </p>
        </header>

        <div style={{ marginBottom: 20 }}>
          <SearchBar onSearch={search} />
        </div>

        <div style={{ display: 'flex', gap: 20 }}>
          <div style={{ flex: '0 0 300px' }}>
            <ProfessorList profs={profs} onSelect={selectProf} selected={selected} />
          </div>

          <div style={{ flex: 1 }}>
            {/* View Toggle */}
            <div style={{
              display: 'flex',
              gap: 12,
              marginBottom: 20,
              background: '#f3f4f6',
              padding: '6px',
              borderRadius: '12px',
              width: 'fit-content'
            }}>
              <button
                style={{
                  padding: '10px 20px',
                  border: 'none',
                  borderRadius: '8px',
                  background: view === 'ranking' ? 'white' : 'transparent',
                  color: view === 'ranking' ? '#3b82f6' : '#6b7280',
                  cursor: 'pointer',
                  fontWeight: '500',
                  transition: 'all 0.2s'
                }}
                onClick={() => setView("ranking")}
              >
                🏆 Overall Rankings
              </button>
              <button
                style={{
                  padding: '10px 20px',
                  border: 'none',
                  borderRadius: '8px',
                  background: view === 'individual' ? 'white' : 'transparent',
                  color: view === 'individual' ? '#3b82f6' : '#6b7280',
                  cursor: 'pointer',
                  fontWeight: '500',
                  transition: 'all 0.2s'
                }}
                onClick={() => setView("individual")}
              >
                👤 Individual Professor
              </button>
              <button
                style={{
                  padding: '10px 20px',
                  border: 'none',
                  borderRadius: '8px',
                  background: view === 'comparison' ? 'white' : 'transparent',
                  color: view === 'comparison' ? '#3b82f6' : '#6b7280',
                  cursor: 'pointer',
                  fontWeight: '500',
                  transition: 'all 0.2s'
                }}
                onClick={() => setView("comparison")}
              >
                📊 Compare Professors
              </button>
            </div>

            {/* Individual View */}
            {view === "individual" && (
              <>
                {loading && (
                  <div style={{ textAlign: 'center', padding: 40, color: '#6b7280' }}>
                    Loading professor data...
                  </div>
                )}

                {!loading && !data && (
                  <div style={{ textAlign: 'center', padding: 60, color: '#9ca3af' }}>
                    <div style={{ fontSize: 48, marginBottom: 16 }}>👈</div>
                    <div>Select a professor to view analytics</div>
                  </div>
                )}

                {!loading && data && (
                  <Insights
                    data={data}
                    trendData={trendData}
                    predictionData={predictionData}
                  />
                )}
              </>
            )}

            {/* Comparison View */}
            {view === "comparison" && (
              <ComparisonDashboard availableProfessors={profs} />
            )}
            {/*Ranking View*/}
            {view === "ranking" && (
              <RankingDashboard />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
