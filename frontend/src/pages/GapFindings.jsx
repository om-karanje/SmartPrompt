export default function GapFindings() {
  const findings = [
    'No systematic prompt identification for workplace communication tasks.',
    'Missing prompt components are not explicitly identified and explained.',
    'Workplace-specific domain awareness is often absent from AI prompts.',
    'Structured prompt refinement is limited without a clear before-and-after model.',
  ];

  return (
    <div className="page-shell">
      <section className="panel project-panel">
        <p className="section-label">Prompt quality review</p>
        <h2>Gap Findings</h2>
        <div className="gap-summary-list">
          {findings.map((item, index) => (
            <div key={item} className="gap-summary-item">
              <span>{index + 1}</span>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
