export default function OutputComparison({ originalOutput, optimizedOutput, evaluation }) {
  const scores = evaluation?.scores || {};
  return (
    <section className="panel">
      <h3>Original vs Optimized Output</h3>
      <div className="comparison-grid">
        <div>
          <h4>Original Prompt Output</h4>
          <pre>{originalOutput || 'No output generated yet.'}</pre>
        </div>
        <div>
          <h4>Optimized Prompt Output</h4>
          <pre>{optimizedOutput || 'No output generated yet.'}</pre>
        </div>
      </div>

      <h4>Output Evaluation</h4>
      <table>
        <thead>
          <tr>
            <th>Dimension</th>
            <th>Original</th>
            <th>Optimized</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(scores).map(([dimension, values]) => (
            <tr key={dimension}>
              <td>{dimension}</td>
              <td>{values.Original}</td>
              <td>{values.Optimized}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="analysis-note">{evaluation?.summary || 'Automated LLM-based evaluation'}</p>
    </section>
  );
}
