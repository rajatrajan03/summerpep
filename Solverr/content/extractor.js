(() => {
  const shared = (globalThis.LeetCodeAIAssistant = globalThis.LeetCodeAIAssistant || {});
  const parser = shared.parser;

  const PAGE_READY_TIMEOUT_MS = 10000;
  const PAGE_READY_POLL_MS = 120;

  const TITLE_SELECTORS = [
    '[data-cy="question-title"]',
    '[data-track-load="question-title"]',
    '[data-testid="question-title"]'
  ];

  const DESCRIPTION_SELECTORS = [
    '[data-track-load="question-content"]',
    '[data-track-load="question-description"]',
    '[data-key="description-content"]',
    '[class*="question-content"]',
    'article',
    'section'
  ];

  const EDITOR_ROOT_SELECTORS = [
    '.monaco-editor',
    '[class*="editor"]',
    'textarea.inputarea'
  ];

  const LANGUAGE_SELECTORS = [
    '[data-cy="lang-select"]',
    '[data-testid="lang-select"]',
    '[aria-label*="language"]',
    '[title*="language"]',
    '[data-cy*="language"]',
    '[data-testid*="language"]',
    '.ant-select-selection-item',
    '.select__single-value',
    '[class*="language"]',
    '[class*="lang"]'
  ];

  const LANGUAGE_KEYWORDS = [
    'javascript',
    'typescript',
    'python',
    'python3',
    'java',
    'c++',
    'c#',
    'go',
    'rust',
    'ruby',
    'kotlin',
    'swift',
    'php',
    'scala',
    'racket',
    'bash',
    'mysql',
    'mssql',
    'postgresql',
    'oracle'
  ];

  function escapeRegExp(value) {
    return String(value ?? '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function isNoiseNode(node) {
    const text = parser.normalizeBlockText(node?.textContent ?? '');
    const className = String(node?.className ?? '').toLowerCase();
    const ariaLabel = String(node?.getAttribute?.('aria-label') ?? '').toLowerCase();

    return /monaco|editor|toolbar|footer|navigation|sidebar|header/.test(className)
      || /monaco|editor|toolbar|navigation/.test(ariaLabel)
      || /^$/.test(text);
  }

  function isLikelyProblemTitle(text) {
    const normalizedText = parser.normalizeText(text);

    return Boolean(normalizedText)
      && normalizedText.length <= 120
      && !/^(video solution|solution|editorial|discussion|submissions?|notes?|follow\s*-?\s*up)$/i.test(normalizedText);
  }

  function isSectionHeadingText(text) {
    return /^(description|examples?|constraints?|notes?|note|follow\s*-?\s*up|hints?)\s*:?/i.test(text);
  }

  function getProblemPageRoot() {
    return document.querySelector('[data-track-load="question-content"]')?.closest('main, section, article, div')
      || document.querySelector('[data-track-load="question-description"]')?.closest('main, section, article, div')
      || document.querySelector('main')
      || document.querySelector('article')
      || document.querySelector('[data-track-load="question-description"]')?.closest('section')
      || document.body;
  }

  function getBestTextCandidate(selectors, fallbackRoot = document.body) {
    const directText = parser.getTextFromSelectors(selectors);

    if (directText) {
      return directText;
    }

    const headings = Array.from((fallbackRoot ?? document.body).querySelectorAll('h1, h2, h3, [role="heading"]'));
    const heading = headings.find((element) => {
      const text = parser.getElementText(element);
      return isLikelyProblemTitle(text) && !isSectionHeadingText(text);
    });

    return parser.getElementText(heading);
  }

  function getTitle() {
    return getBestTextCandidate(TITLE_SELECTORS, getProblemPageRoot());
  }

  function scoreDescriptionCandidate(node) {
    if (!node || isNoiseNode(node)) {
      return -1;
    }

    const text = parser.getElementBlockText(node);

    if (!text) {
      return -1;
    }

    let score = text.length;

    if (/example\s*\d*:/i.test(text)) {
      score += 250;
    }

    if (/^example\s*\d*:/im.test(text) || /\nexample\s*\d*:/im.test(text)) {
      score += 120;
    }

    if (/constraints?:/i.test(text)) {
      score += 250;
    }

    if (/follow\s*-?\s*up/i.test(text)) {
      score += 25;
    }

    if (/^description$/i.test(text.trim())) {
      score -= 100;
    }

    if (text.length < 80) {
      score -= 120;
    }

    if (/video solution|discussion|editorial|similar questions/i.test(text)) {
      score -= 400;
    }

    return score;
  }

  function getDescriptionContainer() {
    for (const selector of DESCRIPTION_SELECTORS) {
      const element = document.querySelector(selector);

      if (element) {
        const text = parser.getElementBlockText(element);

        if (text && (/example\s*\d*:/i.test(text) || /constraints?:/i.test(text) || /input:/i.test(text) || text.length > 100)) {
          return element;
        }
      }
    }

    const root = getProblemPageRoot();
    const candidateNodes = Array.from(root.querySelectorAll('section, article, div, p'))
      .filter((node) => node instanceof HTMLElement);

    let bestCandidate = null;
    let bestScore = -1;

    for (const node of candidateNodes) {
      const score = scoreDescriptionCandidate(node);

      if (score > bestScore) {
        bestCandidate = node;
        bestScore = score;
      }
    }

    return bestCandidate;
  }

  function getDescriptionText() {
    const descriptionContainer = getDescriptionContainer();
    return parser.getElementBlockText(descriptionContainer);
  }

  function extractSectionText(descriptionText, startPattern, stopPatterns) {
    const lines = parser.normalizeBlockText(descriptionText).split('\n');
    const collectedLines = [];
    let collecting = false;

    for (const line of lines) {
      if (!collecting && startPattern.test(line)) {
        collecting = true;
        continue;
      }

      if (!collecting) {
        continue;
      }

      if (stopPatterns.some((pattern) => pattern.test(line))) {
        break;
      }

      if (line.trim() !== '') {
        collectedLines.push(line.replace(/^[-*•]\s*/, '').trim());
      }
    }

    return collectedLines.filter(Boolean);
  }

  function extractConstraints(descriptionText) {
    const lines = extractSectionText(descriptionText, /^Constraints?:?/i, [/^Example\s*\d*:/i, /^Follow\s*-?\s*up/i, /^Note:?/i, /^Hints?:?/i]);

    if (lines.length > 0) {
      return lines;
    }

    return parser.getAllTextFromSelectors(['li'])
      .map((line) => parser.normalizeText(line))
      .filter((line) => /0\s*<=|1\s*<=|10\^|n\s*<=|constraints?/i.test(line));
  }

  function normalizeCodeText(text) {
    return String(text ?? '')
      .replace(/\r\n/g, '\n')
      .replace(/\r/g, '\n')
      .replace(/[\u00a0\t]+$/gm, '')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  function getEditorRoot() {
    for (const selector of EDITOR_ROOT_SELECTORS) {
      const element = document.querySelector(selector);

      if (element) {
        if (element.matches('.monaco-editor')) {
          return element;
        }

        if (element.matches('textarea.inputarea')) {
          return element.closest('.monaco-editor') || element.parentElement || element;
        }

        return element.closest('.monaco-editor') || element.closest('div') || element;
      }
    }

    return null;
  }

  function getStarterCode() {
    const editorRoot = getEditorRoot();

    if (!editorRoot) {
      return '';
    }

    const visibleLines = Array.from(editorRoot.querySelectorAll('.view-lines .view-line'));

    if (visibleLines.length > 0) {
      const renderedCode = normalizeCodeText(visibleLines.map((line) => line.textContent ?? '').join('\n'));

      if (renderedCode) {
        return renderedCode;
      }
    }

    const editorInput = editorRoot.querySelector('textarea.inputarea');

    if (editorInput) {
      const value = normalizeCodeText(editorInput.value ?? editorInput.textContent ?? '');

      if (value) {
        return value;
      }
    }

    const fallbackText = normalizeCodeText(
      editorRoot.querySelector('.view-lines')?.textContent
      || editorRoot.querySelector('pre, code')?.textContent
      || editorRoot.textContent
      || ''
    );

    if (fallbackText) {
      return fallbackText;
    }

    return '';
  }

  function getSelectedLanguage() {
    const selectorCandidates = Array.from(document.querySelectorAll([
      ...LANGUAGE_SELECTORS,
      'button',
      '[role="button"]'
    ].join(', ')));

    for (const element of selectorCandidates) {
      if (!(element instanceof HTMLElement)) {
        continue;
      }

      const combinedText = [
        parser.getElementText(element),
        String(element.getAttribute?.('aria-label') ?? ''),
        String(element.getAttribute?.('title') ?? ''),
        String(element.getAttribute?.('data-cy') ?? '')
      ].join(' ');

      if (LANGUAGE_KEYWORDS.some((keyword) => new RegExp(`\b${escapeRegExp(keyword)}\b`, 'i').test(combinedText))) {
        const text = parser.getElementText(element);
        const match = text.match(/(JavaScript|TypeScript|Python3?|Java|C\+\+|C#|Go|Rust|Ruby|Kotlin|Swift|PHP|Scala|Racket|Bash|MySQL|MSSQL|PostgreSQL|Oracle)/i);

        if (match) {
          return match[0];
        }

        const lowerText = text.toLowerCase();
        const exactKeyword = LANGUAGE_KEYWORDS.find((keyword) => lowerText === keyword || lowerText.startsWith(`${keyword} `) || lowerText.endsWith(` ${keyword}`) || lowerText.includes(` ${keyword} `));

        if (exactKeyword) {
          return exactKeyword === 'python3' ? 'Python3' : exactKeyword.replace(/\b\w/g, (character) => character.toUpperCase());
        }

        return text;
      }
    }

    return '';
  }

  function buildProblemData() {
    const description = getDescriptionText();
    const title = getTitle();
    const examples = parser.splitIntoExamples(description);
    const constraints = extractConstraints(description);
    const starterCode = getStarterCode();
    const language = getSelectedLanguage();

    const fieldStatus = {
      title: Boolean(title),
      description: Boolean(description),
      examples: examples.length > 0,
      constraints: constraints.length > 0,
      starterCode: Boolean(starterCode),
      language: Boolean(language)
    };

    const missingFields = Object.entries(fieldStatus)
      .filter(([, isPresent]) => !isPresent)
      .map(([field]) => field);

    return {
      url: location.href,
      title,
      description,
      examples,
      constraints,
      starterCode,
      language,
      isLeetCodeProblemPage: isLeetCodeProblemPage(),
      ready: fieldStatus.title && fieldStatus.description,
      fieldStatus,
      warnings: missingFields.length > 0 ? [`Missing fields: ${missingFields.join(', ')}`] : []
    };
  }

  function waitForProblemPageReady(timeoutMs = PAGE_READY_TIMEOUT_MS) {
    if (!isLeetCodeProblemPage()) {
      return Promise.resolve(buildProblemData());
    }

    return new Promise((resolve) => {
      const startedAt = Date.now();
      let previousSignature = '';
      let stableMatchCount = 0;
      let settled = false;
      let intervalId = null;
      let observer = null;

      const cleanup = () => {
        settled = true;

        if (intervalId) {
          clearInterval(intervalId);
        }

        if (observer) {
          observer.disconnect();
        }
      };

      const complete = (snapshot) => {
        cleanup();
        resolve(snapshot);
      };

      const checkState = () => {
        if (settled) {
          return;
        }

        const snapshot = buildProblemData();
        const signature = [
          location.href,
          snapshot.title,
          snapshot.description.length,
          snapshot.examples.length,
          snapshot.constraints.length,
          snapshot.starterCode.length,
          snapshot.language
        ].join('|');

        if (signature === previousSignature) {
          stableMatchCount += 1;
        } else {
          stableMatchCount = 0;
        }

        previousSignature = signature;

        if (snapshot.ready && stableMatchCount >= 2) {
          complete({ ...snapshot, ready: true });
          return;
        }

        if (Date.now() - startedAt >= timeoutMs) {
          complete({
            ...snapshot,
            ready: snapshot.ready,
            warnings: [...snapshot.warnings, 'LeetCode page took too long to stabilize; returning best-effort data.']
          });
        }
      };

      intervalId = setInterval(checkState, PAGE_READY_POLL_MS);

      observer = new MutationObserver(() => {
        checkState();
      });

      const observerTarget = document.documentElement || document.body;

      if (observerTarget) {
        observer.observe(observerTarget, {
          subtree: true,
          childList: true,
          characterData: true
        });
      }

      checkState();
    });
  }

  function isLeetCodeProblemPage() {
    return /leetcode\.com\/problems\//i.test(location.href);
  }

  shared.extractor = {
    isLeetCodeProblemPage,
    getTitle,
    getDescriptionContainer,
    getDescriptionText,
    getStarterCode,
    getSelectedLanguage,
    buildProblemData,
    waitForProblemPageReady,
    extractProblemData: waitForProblemPageReady
  };
})();
