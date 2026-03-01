export default function ProfessorCard({ prof, onSelect }) {
  return (
    <div
      style={{
        border:"1px solid #ddd",
        padding:10,
        margin:5,
        cursor:"pointer"
      }}
      onClick={()=>onSelect(prof)}
    >
      {prof}
    </div>
  );
}
