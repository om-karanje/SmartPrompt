import { useEffect, useMemo, useState } from 'react';
import { getStatistics } from '../services/api';
import Dashboard from '../components/Dashboard';

function getMostCommon(values, fallback) {
  const counts = values.reduce((result, value) => {
    if (value) result[value] = (result[value] || 0) + 1;
    return result;
  }, {});
  return Object.entries(counts).sort((left, right) => right[1] - left[1])[0]?.[0] || fallback;
}

export default function Home({ onNavigate, sessionAnalyses }) {
  const [datasetStats, setDatasetStats] = useState(null);

  useEffect(() => {
    getStatistics().then(setDatasetStats).catch(() => setDatasetStats(null));
  }, []);

  const stats = useMemo(() => {
    const analyses = sessionAnalyses || [];
    const count = analyses.length;
    const originalScore = analyses.reduce((sum, item) => sum + (Number(item.score) || 0), 0);
    const optimizedScore = analyses.reduce((sum, item) => sum + (Number(item.optimized_score) || 0), 0);
    const constraints = analyses.reduce(
      (sum, item) => sum + (Array.isArray(item.detected_constraints) ? item.detected_constraints.length : 0),
      0
    );
    const missingComponents = analyses.flatMap((item) =>
      (item.gap_analysis || [])
        .filter((gap) => gap.status === 'missing')
        .map((gap) => gap.component)
    );

    return {
      ...datasetStats,
      total_prompts_analyzed: count,
      average_original_score: count ? Math.round(originalScore / count) : 0,
      average_optimized_score: count ? Math.round(optimizedScore / count) : 0,
      average_improvement: count ? Math.round((optimizedScore - originalScore) / count) : 0,
      most_common_prompt_type: getMostCommon(
        analyses.map((item) => item.prompt_type),
        'No analysis data available yet.'
      ),
      most_common_missing_component: getMostCommon(
        missingComponents,
        'No analysis data available yet.'
      ),
      total_detected_constraints: constraints,
    };
  }, [datasetStats, sessionAnalyses]);

  return (
    <div className="page-shell">
      <section className="hero-panel panel">
        <div>
          <p className="section-label">Workspace overview</p>
          <h2>Welcome to SmartPrompt</h2>
          <p className="hero-copy">
            Make every workplace prompt clearer, smarter, and more effective.
          </p>
        </div>

        <button type="button" className="primary action-button" onClick={() => onNavigate('analyzer')}>
          Analyze a Prompt
        </button>
      </section>

      <Dashboard statistics={stats} />
    </div>
  );
}
