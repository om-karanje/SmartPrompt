export default function PromptScore({ title, score, breakdown }) {
  const total = score || 0;
  return (
    <section className="panel">
      <h3>{title}</h3>
      <div className="score-ring">
        <span>{total}</span>
      </div>
      <div className="score-grid">
        {Object.entries(breakdown || {}).map(([label, value]) => (
          <div key={label} className="score-row">
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
