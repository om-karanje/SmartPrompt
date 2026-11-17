export default function PromptScore({ title, score, breakdown, weights }) {
  const total = score ?? 0;

  return (
    <section className="panel score-panel">
      <p className="section-label">Scoring</p>
      <h3>{title}</h3>
      <div className="score-ring">
        <span>{total}</span>
      </div>
      <div className="score-grid">
        {Object.entries(breakdown || {}).map(([label, value]) => (
          <div key={label} className="score-row">
            <span>{label}</span>
            <strong>{value} / {weights?.[label] ?? value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
