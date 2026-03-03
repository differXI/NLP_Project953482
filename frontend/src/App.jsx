import { useEffect, useState } from "react";
import { getProfessors, getProfessor, searchProf, getProfessorTrend, predictProfessorRating } from "./api";
import SearchBar from "./components/SearchBar";
import ProfessorList from "./components/ProfessorList";
import Insights from "./components/Insights";
import ComparisonDashboard from "./components/ComparisonDashboard";
import "./App.css";

function App() {
  const [profs, setProfs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [data, setData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("individual"); // "individual" or "comparison"

  useEffect(()=>{
    getProfessors().then(r=>setProfs(r.data));
  },[]);

  const selectProf = async (name)=>{
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

  const search = (q)=>{
    searchProf(q).then(r=>setProfs(r.data));
  };

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <h1 className="app-title">
            📊 Course & Instructor Evaluation Analytics
          </h1>
          <p className="app-subtitle">
            NLP-powered sentiment analysis, trend prediction, and multi-label categorization
          </p>
        </header>

        <div className="search-section">
          <SearchBar onSearch={search}/>
        </div>

        <div className="main-content">
          <aside className="sidebar">
            <ProfessorList profs={profs} onSelect={selectProf} selected={selected}/>
          </aside>

          <main className="content-area">
            {/* View Toggle */}
            <div className="view-toggle">
              <button
                className={`view-tab ${view === "individual" ? "active" : ""}`}
                onClick={() => setView("individual")}
              >
                👤 Individual Professor
              </button>
              <button
                className={`view-tab ${view === "comparison" ? "active" : ""}`}
                onClick={() => setView("comparison")}
              >
                📊 Compare Professors
              </button>
            </div>

            {/* Individual View */}
            {view === "individual" && (
              <>
                {loading && (
                  <div className="loading-state">
                    Loading professor data...
                  </div>
                )}

                {!loading && !data && (
                  <div className="empty-state">
                    <div className="empty-icon">👈</div>
                    <div className="empty-text">Select a professor to view analytics</div>
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
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
