export default function Dashboard({ statistics }) {
  const dataset = statistics?.dataset || {};
  const total = statistics?.total_prompts_analyzed || 0;

  return (
    <section className="panel">
      <h3>Dashboard / Statistics</h3>
      {total === 0 ? (
        <p>No analysis data available yet.</p>
      ) : (
        <div className="stats-grid">
          <div className="stat-box"><span>Total prompts analyzed</span><strong>{statistics.total_prompts_analyzed}</strong></div>
          <div className="stat-box"><span>Average original score</span><strong>{statistics.average_original_score}</strong></div>
          <div className="stat-box"><span>Average optimized score</span><strong>{statistics.average_optimized_score}</strong></div>
          <div className="stat-box"><span>Average improvement</span><strong>{statistics.average_improvement}</strong></div>
          <div className="stat-box"><span>Most common prompt type</span><strong>{statistics.most_common_prompt_type}</strong></div>
          <div className="stat-box"><span>Most common missing component</span><strong>{statistics.most_common_missing_component}</strong></div>
          <div className="stat-box"><span>Detected constraints</span><strong>{statistics.total_detected_constraints}</strong></div>
        </div>
      )}

      <div className="chart-block">
        <h4>Dataset statistics</h4>
        <div className="chart-row">
          <span>Total records</span>
          <div className="bar"><div style={{ width: `${Math.min(100, (dataset.total_records || 0) / 10)}%` }} /></div>
          <strong>{dataset.total_records || 0}</strong>
        </div>
        <div className="chart-row">
          <span>Constraint categories</span>
          <div className="bar"><div style={{ width: `${Math.min(100, (dataset.constraint_categories || []).length * 10)}%` }} /></div>
          <strong>{(dataset.constraint_categories || []).length}</strong>
        </div>
      </div>
    </section>
  );
}
