export default function Dashboard({ statistics }) {
  const dataset = statistics?.dataset || {};
  const total = statistics?.total_prompts_analyzed || 0;
  const totalRecords = Number(dataset.total_records || 0);
  const constraintCategories = Array.isArray(dataset.constraint_categories) ? dataset.constraint_categories.length : 0;

  const cards = [
    {
      title: 'Total Prompts Analyzed',
      value: statistics?.total_prompts_analyzed ?? 0,
      description: 'All completed prompt evaluation sessions.',
    },
    {
      title: 'Average Original Score',
      value: statistics?.average_original_score ?? 0,
      description: 'Baseline quality before optimization.',
    },
    {
      title: 'Average Optimized Score',
      value: statistics?.average_optimized_score ?? 0,
      description: 'Post-optimization prompt quality.',
    },
    {
      title: 'Average Improvement',
      value: statistics?.average_improvement ?? 0,
      description: 'Net gain from workflow refinement.',
    },
  ];

  return (
    <section className="panel dashboard-panel">
      <div className="section-head">
        <div>
          <p className="section-label">Analytics</p>
          <h3>Performance overview</h3>
        </div>
      </div>

      {total === 0 ? (
        <div className="empty-state">
          <p>No analysis data available yet.</p>
          <span>Run your first prompt analysis to populate this dashboard.</span>
        </div>
      ) : (
        <>
          <div className="stats-grid">
            {cards.map((card) => (
              <div key={card.title} className="stat-box">
                <div className="stat-icon">•</div>
                <span>{card.title}</span>
                <strong>{card.value}</strong>
                <small>{card.description}</small>
              </div>
            ))}
          </div>

          <div className="meta-summary">
            <div>
              <span>Most common prompt type</span>
              <strong>{statistics.most_common_prompt_type}</strong>
            </div>
            <div>
              <span>Most common missing component</span>
              <strong>{statistics.most_common_missing_component}</strong>
            </div>
            <div>
              <span>Total detected constraints</span>
              <strong>{statistics.total_detected_constraints}</strong>
            </div>
          </div>
        </>
      )}

      <div className="chart-block">
        <div className="chart-header">
          <h4>Dataset statistics</h4>
        </div>

        <div className="chart-row">
          <span>Total records</span>
          <div className="bar">
            <div style={{ width: `${Math.min(100, totalRecords ? (totalRecords / 100) * 100 : 0)}%` }} />
          </div>
          <strong>{totalRecords}</strong>
        </div>

        <div className="chart-row">
          <span>Constraint categories</span>
          <div className="bar">
            <div style={{ width: `${Math.min(100, constraintCategories ? (constraintCategories / 10) * 100 : 0)}%` }} />
          </div>
          <strong>{constraintCategories}</strong>
        </div>
      </div>
    </section>
  );
}
