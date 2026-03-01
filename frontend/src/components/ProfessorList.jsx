import ProfessorCard from "./ProfessorCard";

export default function ProfessorList({ profs, onSelect }) {
  return (
    <div>
      {profs.map(p=>(
        <ProfessorCard key={p} prof={p} onSelect={onSelect}/>
      ))}
    </div>
  );
}
