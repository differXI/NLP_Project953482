import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [q, setQ] = useState("");

  const handleChange = (e) => {
    const newValue = e.target.value;
    setQ(newValue);

    if (newValue.length >= 3 || newValue.length === 0) {
      onSearch(newValue);
    }
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        placeholder="Search professor..."
        value={q}
        onChange={handleChange}
        style={{ padding: '8px', marginRight: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
      />
      <button 
        onClick={() => onSearch(q)}
        style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', background: '#3b82f6', color: 'white', cursor: 'pointer' }}
      >
        Search
      </button>
    </div>
  );
}
