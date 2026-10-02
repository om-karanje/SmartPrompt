const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || payload.error || 'Request failed.');
  }

  return response.json();
}

export function fetchExamples() {
  return request('/examples');
}

export function getStatistics() {
  return request('/statistics');
}

export function analyzePrompt(prompt) {
  return request('/analyze', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  });
}

export function generatePrompt(prompt) {
  return request('/generate', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  });
}

export function comparePrompt(prompt) {
  return request('/compare', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  });
}
