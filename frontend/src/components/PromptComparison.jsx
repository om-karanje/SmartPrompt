export default function PromptComparison({ originalPrompt, optimizedPrompt }) {
  return (
    <section className="panel">
      <h3>Original vs Optimized Prompt</h3>
      <div className="comparison-grid">
        <div>
          <h4>Original Prompt</h4>
          <pre>{originalPrompt}</pre>
        </div>
        <div>
          <h4>Optimized Prompt</h4>
          <pre>{optimizedPrompt}</pre>
        </div>
      </div>
      <button className="copy-btn" onClick={() => navigator.clipboard.writeText(optimizedPrompt)}>
        Copy Optimized Prompt
      </button>
    </section>
  );
}
