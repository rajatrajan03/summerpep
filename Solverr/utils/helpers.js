export function normalizeWhitespace(text) {
  return String(text ?? '').replace(/\s+/g, ' ').trim();
}

export function truncateText(text, maxLength = 200) {
  const normalizedText = normalizeWhitespace(text);

  if (normalizedText.length <= maxLength) {
    return normalizedText;
  }

  return `${normalizedText.slice(0, maxLength - 1)}…`;
}

export function isLeetCodeProblemUrl(url) {
  return /leetcode\.com\/problems\//i.test(String(url ?? ''));
}

export function safeJsonParse(text, fallbackValue = null) {
  try {
    return JSON.parse(text);
  } catch {
    return fallbackValue;
  }
}
