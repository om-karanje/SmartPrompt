export default function About() {
  return (
    <div className="page-shell">
      <section className="panel project-panel">
        <p className="section-label">About the project</p>
        <h2>Built for clearer, smarter workplace prompting</h2>
        <p>
          SmartPrompt helps employees identify weak workplace prompts, detect missing context,
          and compare before-and-after outputs using a transparent domain-aware workflow.
        </p>

        <div className="feature-grid">
          <div className="feature-card">
            <h3>Prompt Identification</h3>
            <p>Classifies the request type and workplace domain to make the analysis meaningful.</p>
          </div>
          <div className="feature-card">
            <h3>Gap Analysis</h3>
            <p>Surfaces missing role, task, audience, format, and constraint details before output generation.</p>
          </div>
          <div className="feature-card">
            <h3>Explainable Scoring</h3>
            <p>Scores the prompt on clarity, specificity, context, and structure using a transparent rubric.</p>
          </div>
          <div className="feature-card">
            <h3>Optimization</h3>
            <p>Improves the prompt without inventing personal details or changing the user’s intent.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
