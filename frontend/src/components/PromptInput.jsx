export default function PromptInput({
  value,
  onChange,
  onAnalyze,
  onUseSample,
  sampleOptions,
  selectedSample,
  setSelectedSample,
}) {
  const samples = sampleOptions?.length ? sampleOptions : [];

  return (
    <section className="panel prompt-panel">
      <div className="panel-header">
        <div>
          <p className="section-label">Prompt intake</p>
          <h2>Analyze, understand, and optimize your workplace prompts.</h2>
        </div>
        <div className="char-pill">{value.length} chars</div>
      </div>

      <label className="field-label">Enter Your Prompt</label>
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Example: Write an email to my manager about the project progress and next steps for the week."
        rows={8}
      />

      <div className="helper-row">
        <span>SmartPrompt analyzes your prompt's clarity, structure, constraints, and workplace relevance.</span>
        <span>{value.trim() ? 'Ready to analyze' : 'Awaiting prompt'}</span>
      </div>

      <div className="sample-toolbar">
        <select
          value={selectedSample}
          onChange={(event) => setSelectedSample(event.target.value)}
          aria-label="Choose a sample prompt"
        >
          <option value="">Choose a sample prompt</option>
          {samples.map((sample) => (
            <option key={sample.id || sample.prompt} value={sample.prompt}>
              {sample.label}
            </option>
          ))}
        </select>
        <button type="button" className="secondary" onClick={onUseSample}>Use Sample</button>
        <button
          type="button"
          className="secondary"
          onClick={() => {
            onChange('');
            setSelectedSample('');
          }}
        >
          Clear
        </button>
        <button type="button" className="primary primary-cta" onClick={onAnalyze}>Analyze Prompt</button>
      </div>
    </section>
  );
}
