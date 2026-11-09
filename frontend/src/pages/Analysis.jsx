import { useEffect, useState } from 'react';
import { analyzePrompt, comparePrompt, fetchExamples } from '../services/api';
import PromptInput from '../components/PromptInput';
import PromptScore from '../components/PromptScore';
import ConstraintList from '../components/ConstraintList';
import PromptComparison from '../components/PromptComparison';
import OutputComparison from '../components/OutputComparison';

const defaultSampleOptions = [
  { id: 1, label: 'Write an email to my manager.', prompt: 'Write an email to my manager.' },
  { id: 2, label: 'Write a leave request.', prompt: 'Write a leave request.' },
  { id: 3, label: 'Make a report about my project.', prompt: 'Make a report about my project.' },
  { id: 4, label: 'Summarize this meeting.', prompt: 'Summarize this meeting.' },
  { id: 5, label: 'Write a message to HR.', prompt: 'Write a message to HR.' },
  { id: 6, label: 'Write a project update for my manager.', prompt: 'Write a project update for my manager.' },
  { id: 7, label: 'Create a task description for a software developer.', prompt: 'Create a task description for a software developer.' },
  { id: 8, label: 'Write a professional email to a client.', prompt: 'Write a professional email to a client.' },
  { id: 9, label: 'Write a performance review.', prompt: 'Write a performance review.' },
  { id: 10, label: 'Create a presentation outline for my project.', prompt: 'Create a presentation outline for my project.' },
];

export default function AnalysisPage({ onAnalysis }) {
  const [prompt, setPrompt] = useState('');
  const [sampleOptions, setSampleOptions] = useState(defaultSampleOptions);
  const [selectedSample, setSelectedSample] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loadingAction, setLoadingAction] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchExamples().then((items) => {
      if (Array.isArray(items) && items.length) {
        setSampleOptions(items);
      }
    }).catch(() => setSampleOptions(defaultSampleOptions));
  }, []);

  const handleAnalyze = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt before analyzing.');
      return;
    }

    setError('');
    setLoadingAction('analyze');
    try {
      const result = await analyzePrompt(prompt);
      setAnalysis(result);
      setComparison(null);
      onAnalysis(result, prompt);
    } catch (err) {
      setError(err.message || 'Unable to analyze the prompt.');
    } finally {
      setLoadingAction('');
    }
  };

  const handleCompare = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt before generating a comparison.');
      return;
    }

    setError('');
    setLoadingAction('compare');
    try {
      const result = await comparePrompt(prompt);
      setComparison(result);
    } catch (err) {
      setError(err.message || 'Unable to compare outputs.');
    } finally {
      setLoadingAction('');
    }
  };

  const handleUseSample = () => {
    if (!selectedSample) return;
    setPrompt(selectedSample);
  };

  return (
    <div className="page-shell">
      <PromptInput
        value={prompt}
        onChange={setPrompt}
        onAnalyze={handleAnalyze}
        onUseSample={handleUseSample}
        sampleOptions={sampleOptions}
        selectedSample={selectedSample}
        setSelectedSample={setSelectedSample}
      />

      {error && <div className="error-box">{error}</div>}
      {loadingAction && (
        <div className="loading-box" role="status" aria-live="polite">
          <span className="loading-spinner" aria-hidden="true" />
          <div className="loading-copy">
            <strong>
              {loadingAction === 'compare' ? 'Generating output comparison' : 'Analyzing your prompt'}
            </strong>
            <span>
              {loadingAction === 'compare'
                ? 'Creating both responses and evaluating their quality. This may take a moment.'
                : 'Reviewing prompt structure, constraints, and workplace context.'}
            </span>
            <span className="loading-progress" aria-hidden="true"><span /></span>
          </div>
        </div>
      )}

      {analysis && (
        <>
          <section className="summary-grid">
            <div className="panel summary-card">
              <p className="section-label">Prompt identification</p>
              <h3>{analysis.prompt_type}</h3>
              <div className="meta-list">
                <div><span>Domain</span><strong>{analysis.domain}</strong></div>
                <div><span>Intent</span><strong>{analysis.intent}</strong></div>
              </div>
              {analysis.summary && <p className="summary-copy">{analysis.summary}</p>}
            </div>
            <PromptScore title="Original Score" score={analysis.score} breakdown={analysis.score_breakdown} />
          </section>
          <ConstraintList constraints={analysis.detected_constraints} />

          <PromptComparison
            originalPrompt={prompt}
            optimizedPrompt={analysis.optimized_prompt}
          />

          <div className="panel score-improvement">
            <p className="section-label">Score improvement</p>
            <h3>Prompt effectiveness uplift</h3>
            <div className="improvement-row">
              <div>
                <span>Original score</span>
                <strong>{analysis.score}</strong>
              </div>
              <div>
                <span>Optimized score</span>
                <strong>{analysis.optimized_score}</strong>
              </div>
              <div>
                <span>Improvement</span>
                <strong>+{Math.max(0, analysis.optimized_score - analysis.score)}</strong>
              </div>
            </div>
          </div>
        </>
      )}

      {comparison && (
        <OutputComparison
          originalOutput={comparison.original_output}
          optimizedOutput={comparison.optimized_output}
          evaluation={comparison.evaluation}
        />
      )}

      <div className="action-row">
        <button
          type="button"
          className="primary action-button"
          onClick={handleCompare}
          disabled={Boolean(loadingAction)}
        >
          {loadingAction === 'compare' ? 'Generating comparison…' : 'Generate Output Comparison'}
        </button>
      </div>
    </div>
  );
}
