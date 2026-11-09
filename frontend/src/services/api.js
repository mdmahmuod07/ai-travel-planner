const API_BASE = '/api/v1';

export async function fetchPresets() {
  try {
    const res = await fetch(`${API_BASE}/presets`);
    if (!res.ok) throw new Error('Failed to fetch presets');
    return await res.json();
  } catch (err) {
    console.error('Error fetching presets:', err);
    return [];
  }
}

export async function generatePlanStream(requestData, onLog, onResult, onError) {
  try {
    const response = await fetch(`${API_BASE}/plan/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const jsonStr = line.replace('data: ', '').trim();
          if (!jsonStr) continue;

          try {
            const event = JSON.parse(jsonStr);
            if (event.type === 'log') {
              onLog(event.data);
            } else if (event.type === 'result') {
              onResult(event.data);
            } else if (event.type === 'error') {
              onError(event.data.message || 'Error occurred');
            }
          } catch (e) {
            console.error('Parse error on SSE data:', e, jsonStr);
          }
        }
      }
    }
  } catch (err) {
    onError(err.message || 'Network connection failed');
  }
}

export async function refinePlan(currentPlan, userInstruction) {
  try {
    const res = await fetch(`${API_BASE}/plan/refine`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        current_plan: currentPlan,
        user_instruction: userInstruction
      }),
    });
    if (!res.ok) throw new Error('Refinement failed');
    return await res.json();
  } catch (err) {
    console.error('Refinement error:', err);
    throw err;
  }
}

export async function downloadMarkdown(planData) {
  try {
    const res = await fetch(`${API_BASE}/export/markdown`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(planData),
    });
    if (!res.ok) throw new Error('Export failed');
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${planData.destination.toLowerCase().replace(/\s+/g, '_')}_itinerary.md`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (err) {
    console.error('Markdown export error:', err);
    alert('Failed to download markdown file.');
  }
}
