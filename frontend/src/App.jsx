import { useEffect, useState } from "react";
import { getProfessors, getProfessor, searchProf } from "./api";
import SearchBar from "./components/SearchBar";
import ProfessorList from "./components/ProfessorList";
import Insights from "./components/Insights";

function App() {
  const [profs, setProfs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [data, setData] = useState(null);

  useEffect(()=>{
    getProfessors().then(r=>setProfs(r.data));
  },[]);

  const selectProf = (name)=>{
    setSelected(name);
    getProfessor(name).then(r=>setData(r.data));
  };

  const search = (q)=>{
    searchProf(q).then(r=>setProfs(r.data));
  };

  return (
    <div style={{padding:20}}>
      <h1>Course & Instructor Evaluation Analytics</h1>

      <SearchBar onSearch={search}/>
      <ProfessorList profs={profs} onSelect={selectProf}/>

      <Insights data={data}/>
    </div>
  );
}

export default App;
