(() => {
  const shared = (globalThis.LeetCodeAIAssistant = globalThis.LeetCodeAIAssistant || {});

  function normalizeLineBreaks(text) {
    return String(text ?? '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  }

  function normalizeText(text) {
    return String(text ?? '').replace(/\s+/g, ' ').trim();
  }

  function normalizeBlockText(text) {
    return normalizeLineBreaks(text)
      .split('\n')
      .map((line) => normalizeText(line))
      .join('\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  function getElementText(element) {
    return normalizeText(element?.innerText ?? element?.textContent ?? '');
  }

  function getElementBlockText(element) {
    return normalizeBlockText(element?.innerText ?? element?.textContent ?? '');
  }

  function getTextFromSelectors(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);

      if (element) {
        const text = getElementText(element);

        if (text) {
          return text;
        }
      }
    }

    return '';
  }

  function getBlockTextFromSelectors(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);

      if (element) {
        const text = getElementBlockText(element);

        if (text) {
          return text;
        }
      }
    }

    return '';
  }

  function getAllTextFromSelectors(selectors) {
    const collectedText = [];

    for (const selector of selectors) {
      document.querySelectorAll(selector).forEach((element) => {
        const text = getElementText(element);

        if (text) {
          collectedText.push(text);
        }
      });
    }

    return collectedText;
  }

  function splitIntoExamples(text) {
    const lines = normalizeBlockText(text).split('\n');
    const examples = [];
    let currentExampleLines = [];
    let collecting = false;

    for (const line of lines) {
      if (/^Example\s*\d*\s*:?/i.test(line)) {
        if (currentExampleLines.length > 0) {
          examples.push(currentExampleLines.join('\n').trim());
        }

        currentExampleLines = [line.trim()];
        collecting = true;
        continue;
      }

      if (!collecting) {
        continue;
      }

      if (/^(Constraints?|Follow\s*-?\s*up|Hints?|Note|Notes?)\s*:?/i.test(line)) {
        break;
      }

      if (line.trim() === '' && currentExampleLines.length === 0) {
        continue;
      }

      currentExampleLines.push(line);
    }

    if (currentExampleLines.length > 0) {
      examples.push(currentExampleLines.join('\n').trim());
    }

    return examples.filter(Boolean);
  }

  shared.parser = {
    normalizeLineBreaks,
    normalizeText,
    normalizeBlockText,
    getElementText,
    getElementBlockText,
    getTextFromSelectors,
    getBlockTextFromSelectors,
    getAllTextFromSelectors,
    splitIntoExamples
  };
})();
