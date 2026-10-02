import { useEffect, useState } from 'react';
import { analyzePrompt, comparePrompt, fetchExamples, getStatistics } from '../services/api';
import PromptInput from '../components/PromptInput';
import PromptScore from '../components/PromptScore';
import ConstraintList from '../components/ConstraintList';
import GapAnalysis from '../components/GapAnalysis';
import PromptComparison from '../components/PromptComparison';
import OutputComparison from '../components/OutputComparison';
import Dashboard from '../components/Dashboard';

export default function Home() {
  const [prompt, setPrompt] = useState('Write an email to my manager.');
  const [sampleOptions, setSampleOptions] = useState([]);
  const [selectedSample, setSelectedSample] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchExamples().then(setSampleOptions).catch(() => setSampleOptions([]));
    getStatistics().then(setStats).catch(() => setStats(null));
  }, []);

  const handleAnalyze = async () => {
    setError('');
    setIsLoading(true);
    try {
      const result = await analyzePrompt(prompt);
      setAnalysis(result);
      setComparison(null);
    } catch (err) {
      setError(err.message || 'Unable to analyze the prompt.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompare = async () => {
    setError('');
    setIsLoading(true);
    try {
      const result = await comparePrompt(prompt);
      setComparison(result);
    } catch (err) {
      setError(err.message || 'Unable to compare outputs.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseSample = () => {
    if (!selectedSample) return;
    setPrompt(selectedSample);
  };

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Prompt Identification & Optimization for Workplace Applications</p>
          <h1>SmartPrompt</h1>
        </div>
      </header>

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
      {isLoading && <div className="loading-box">Analyzing prompt...</div>}

      {analysis && (
        <>
          <section className="summary-grid">
            <div className="panel summary-card">
              <h3>Prompt Identification</h3>
              <p><strong>Prompt Type:</strong> {analysis.prompt_type}</p>
              <p><strong>Domain:</strong> {analysis.domain}</p>
              <p><strong>Intent:</strong> {analysis.intent}</p>
            </div>
            <PromptScore title="Original Score" score={analysis.score} breakdown={analysis.score_breakdown} />
          </section>

          <ConstraintList constraints={analysis.detected_constraints} />
          <GapAnalysis gapAnalysis={analysis.gap_analysis} />

          <PromptComparison
            originalPrompt={prompt}
            optimizedPrompt={analysis.optimized_prompt}
          />

          <div className="panel score-improvement">
            <h3>Score Improvement</h3>
            <p>Original Score: {analysis.score}</p>
            <p>Optimized Score: {analysis.optimized_score}</p>
            <p>Improvement: +{Math.max(0, analysis.optimized_score - analysis.score)}</p>
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
        <button className="primary" onClick={handleCompare}>Generate Output Comparison</button>
      </div>

      <Dashboard statistics={stats} />
    </div>
  );
}
