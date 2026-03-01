import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [q, setQ] = useState("");

  return (
    <div style={{marginBottom:20}}>
      <input
        placeholder="Search professor..."
        value={q}
        onChange={(e)=>setQ(e.target.value)}
      />
      <button onClick={()=>onSearch(q)}>Search</button>
    </div>
  );
}
