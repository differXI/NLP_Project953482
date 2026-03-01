import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function Insights({ data }) {
  if (!data) return null;

  const sent = Object.entries(data.sentiment_counts).map(([k,v])=>({name:k,value:v}));
  const cat = Object.entries(data.category_counts).map(([k,v])=>({name:k,value:v}));

  return (
    <div>
      <h2>{data.professor}</h2>
      <p>Avg Rating: {data.avg_rating}</p>
      <p>Avg Difficulty: {data.avg_difficulty}</p>

      <h3>Sentiment</h3>
      <BarChart width={400} height={200} data={sent}>
        <XAxis dataKey="name"/>
        <YAxis/>
        <Tooltip/>
        <Bar dataKey="value"/>
      </BarChart>

      <h3>Categories</h3>
      <BarChart width={400} height={200} data={cat}>
        <XAxis dataKey="name"/>
        <YAxis/>
        <Tooltip/>
        <Bar dataKey="value"/>
      </BarChart>
    </div>
  );
}
