const statusIcon = {
  present: '✓',
  partial: '⚠',
  missing: '✗',
};

export default function GapAnalysis({ gapAnalysis = [] }) {
  return (
    <section className="panel">
      <h3>Domain-Aware Gap Analysis</h3>
      <div className="gap-grid">
        {gapAnalysis.map((item) => (
          <div key={item.component} className="gap-item">
            <span className={`status ${item.status}`}>{statusIcon[item.status] || '•'}</span>
            <div>
              <strong>{item.component}</strong>
              <p>{item.explanation}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
