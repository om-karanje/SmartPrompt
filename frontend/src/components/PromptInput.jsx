export default function PromptInput({ value, onChange, onAnalyze, onUseSample, sampleOptions, selectedSample, setSelectedSample }) {
  return (
    <section className="panel">
      <label className="label">Enter your workplace prompt</label>
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Enter your workplace prompt..."
        rows={8}
      />

      <div className="toolbar">
        <select value={selectedSample} onChange={(event) => setSelectedSample(event.target.value)}>
          <option value="">Choose sample prompt</option>
          {sampleOptions.map((sample) => (
            <option key={sample.id} value={sample.prompt}>{sample.label}</option>
          ))}
        </select>
        <button onClick={onUseSample}>Use Sample Prompt</button>
        <button className="primary" onClick={onAnalyze}>Analyze Prompt</button>
      </div>
    </section>
  );
}
