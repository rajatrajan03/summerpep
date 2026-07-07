import { safeJsonParse } from '../utils/helpers.js';

export function buildPrompt(problemData) {
  return [
    'You are a LeetCode study assistant.',
    'Return only valid JSON with these keys: approach, explanation, timeComplexity, spaceComplexity, code, dryRun, edgeCases.',
    'The code must be ready to paste into the selected programming language when possible.',
    '',
    'Problem data:',
    JSON.stringify(problemData, null, 2)
  ].join('\n');
}

export function validateAiResponse(rawResponse) {
  const parsedResponse = typeof rawResponse === 'string' ? safeJsonParse(stripMarkdownFences(rawResponse)) : rawResponse;

  if (!parsedResponse || typeof parsedResponse !== 'object') {
    return { ok: false, error: 'AI response is not valid JSON.' };
  }

  const requiredFields = ['approach', 'explanation', 'timeComplexity', 'spaceComplexity', 'code', 'dryRun', 'edgeCases'];
  const missingFields = requiredFields.filter((field) => typeof parsedResponse[field] !== 'string' || parsedResponse[field].trim() === '');

  if (missingFields.length > 0) {
    return { ok: false, error: `AI response is missing fields: ${missingFields.join(', ')}.` };
  }

  return { ok: true, data: parsedResponse };
}

function stripMarkdownFences(text) {
  const normalizedText = String(text ?? '').trim();

  if (!normalizedText.startsWith('```')) {
    return normalizedText;
  }

  return normalizedText
    .replace(/^```json\s*/i, '')
    .replace(/^```\s*/i, '')
    .replace(/```\s*$/i, '')
    .trim();
}

export async function requestAiSolution({ apiKey, endpoint, model, problemData }) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: 'system',
          content: 'You are a concise, accurate LeetCode assistant. Return only JSON.'
        },
        {
          role: 'user',
          content: buildPrompt(problemData)
        }
      ],
      temperature: 0.2
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`AI request failed with status ${response.status}: ${errorText}`);
  }

  const payload = await response.json();
  const content = payload?.choices?.[0]?.message?.content;

  if (typeof content !== 'string' || !content.trim()) {
    throw new Error('AI response did not contain content.');
  }

  const validation = validateAiResponse(content);

  if (!validation.ok) {
    throw new Error(validation.error);
  }

  return validation.data;
}
