import { useEffect, useState } from 'react';
import { analyzePrompt, comparePrompt, fetchExamples } from '../services/api';
import PromptInput from '../components/PromptInput';
import PromptScore from '../components/PromptScore';
import GapAnalysis from '../components/GapAnalysis';
import PromptComparison from '../components/PromptComparison';
import OutputComparison from '../components/OutputComparison';

export default function AnalysisPage({ onAnalysis }) {
  const [prompt, setPrompt] = useState('');
  const [sampleOptions, setSampleOptions] = useState([]);
  const [sampleError, setSampleError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedSample, setSelectedSample] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loadingAction, setLoadingAction] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchExamples().then((items) => {
      if (Array.isArray(items) && items.length) {
        setSampleOptions(items);
        setSampleError('');
      } else {
        setSampleError('The workplace prompt dataset returned no examples.');
      }
    }).catch((err) => {
      setSampleError(err.message || 'Unable to load workplace dataset examples.');
    });
  }, []);

  const sampleCategories = [...new Set(sampleOptions.map((item) => item.category))].sort();
  const visibleSamples = selectedCategory === 'all'
    ? sampleOptions
    : sampleOptions.filter((item) => item.category === selectedCategory);

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
        sampleOptions={visibleSamples}
        sampleCategories={sampleCategories}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        selectedSample={selectedSample}
        setSelectedSample={setSelectedSample}
        sampleError={sampleError}
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
            <PromptScore
              title="Original Prompt Score"
              score={analysis.score}
              breakdown={analysis.score_breakdown}
              weights={analysis.score_weights}
            />
          </section>
          <GapAnalysis
            gapAnalysis={analysis.gap_analysis}
            contributions={analysis.score_breakdown}
            weights={analysis.score_weights}
          />

          <PromptComparison
            originalPrompt={prompt}
            optimizedPrompt={analysis.optimized_prompt}
          />

          <PromptScore
            title="Optimized Prompt Score"
            score={analysis.optimized_score}
            breakdown={analysis.optimized_score_breakdown}
            weights={analysis.optimized_score_weights}
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
                <strong>
                  {analysis.optimized_score - analysis.score > 0 ? '+' : ''}
                  {analysis.optimized_score - analysis.score}
                </strong>
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
