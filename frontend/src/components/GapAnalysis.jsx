const statusIcon = {
  present: '✓',
  partial: '⚠',
  missing: '✗',
};

export default function GapAnalysis({ gapAnalysis = [], contributions = {}, weights = {} }) {
  return (
    <section className="panel">
      <h3>11-Component Prompt Analysis</h3>
      <div className="gap-grid">
        {gapAnalysis.map((item) => (
          <div key={item.component} className="gap-item">
            <span className={`status ${item.status}`}>{statusIcon[item.status] || '•'}</span>
            <div>
              <strong>{item.component}</strong>
              <p>{item.explanation}</p>
              <span className="component-contribution">
                Score contribution: {contributions[item.component] ?? 0} / {weights[item.component] ?? 0}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
