import { useState } from "react";

export default function SubjectList({ subjects, onSelect, selected }) {
  const [filterType, setFilterType] = useState("all"); // all, online, onsite
  const [searchTerm, setSearchTerm] = useState("");

  const filteredSubjects = subjects.filter(s => {
    const matchesType = filterType === "all" || s.type === filterType;
    const matchesSearch = searchTerm === "" ||
      s.name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 16, background: 'white' }}>
      <h3 style={{ marginTop: 0 }}>Subjects/Courses</h3>

      {/* Filter Buttons */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <button
          style={{
            padding: '6px 12px',
            borderRadius: 6,
            border: filterType === 'all' ? '2px solid #3b82f6' : '1px solid #d1d5db',
            background: filterType === 'all' ? '#eff6ff' : 'white',
            cursor: 'pointer',
            fontSize: 13,
            transition: 'all 0.2s'
          }}
          onClick={() => setFilterType("all")}
        >
          All
        </button>
        <button
          style={{
            padding: '6px 12px',
            borderRadius: 6,
            border: filterType === 'online' ? '2px solid #10b981' : '1px solid #d1d5db',
            background: filterType === 'online' ? '#ecfdf5' : 'white',
            cursor: 'pointer',
            fontSize: 13,
            transition: 'all 0.2s'
          }}
          onClick={() => setFilterType("online")}
        >
          🌐 Online
        </button>
        <button
          style={{
            padding: '6px 12px',
            borderRadius: 6,
            border: filterType === 'onsite' ? '2px solid #f59e0b' : '1px solid #d1d5db',
            background: filterType === 'onsite' ? '#fffbeb' : 'white',
            cursor: 'pointer',
            fontSize: 13,
            transition: 'all 0.2s'
          }}
          onClick={() => setFilterType("onsite")}
        >
          🏛️ Onsite
        </button>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Search subjects..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          width: '100%',
          padding: '8px 12px',
          marginBottom: 12,
          border: '1px solid #d1d5db',
          borderRadius: 6,
          boxSizing: 'border-box',
          fontSize: 13
        }}
      />

      {/* Subject List */}
      <div style={{ maxHeight: 400, overflowY: 'auto' }}>
        {filteredSubjects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 20, color: '#9ca3af', fontSize: 13 }}>
            No subjects found
          </div>
        ) : (
          filteredSubjects.map((subject, index) => (
            <div
              key={index}
              onClick={() => onSelect(subject)}
              style={{
                padding: '10px',
                marginBottom: 6,
                border: '1px solid #e5e7eb',
                borderRadius: 6,
                cursor: 'pointer',
                background: selected?.name === subject.name && selected?.type === subject.type
                  ? '#eff6ff'
                  : 'white',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => {
                if (!(selected?.name === subject.name && selected?.type === subject.type)) {
                  e.target.style.background = '#f9fafb';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.background =
                  selected?.name === subject.name && selected?.type === subject.type
                    ? '#eff6ff'
                    : 'white';
              }}
            >
              <div style={{ fontWeight: 500, fontSize: 14, marginBottom: 4 }}>
                {subject.name}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#6b7280' }}>
                <span>
                  {subject.type === 'online' ? '🌐' : '🏛️'} {subject.type}
                </span>
                <span>
                  ⭐ {subject.avg_quality}
                </span>
              </div>
              <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 4 }}>
                {subject.count} reviews • {subject.professor_count} professors
              </div>
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #e5e7eb', fontSize: 12, color: '#6b7280' }}>
        Showing {filteredSubjects.length} of {subjects.length} subjects
      </div>
    </div>
  );
}
