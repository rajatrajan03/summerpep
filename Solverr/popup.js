import { MESSAGE_TYPES } from './utils/constants.js';
import { truncateText } from './utils/helpers.js';

let currentSolutionCode = '';

function setTextContent(elementId, value) {
  const element = document.getElementById(elementId);

  if (element) {
    element.textContent = value;
  }
}

function setButtonState(buttonId, isLoading, loadingLabel, defaultLabel) {
  const button = document.getElementById(buttonId);

  if (button) {
    button.disabled = isLoading;
    button.textContent = isLoading ? loadingLabel : defaultLabel;
  }
}

function setSnapshotLoadingState(isLoading) {
  setButtonState('refreshButton', isLoading, 'Reading...', 'Read Current Problem');
}

function setAiLoadingState(isLoading) {
  setButtonState('generateButton', isLoading, 'Working...', 'Generate AI Solution');
}

function setInsertCodeButtonState(isEnabled) {
  const button = document.getElementById('insertCodeButton');

  if (button) {
    button.disabled = !isEnabled;
  }
}

function resetProblemFields() {
  setTextContent('problemTitle', 'Not loaded yet');
  setTextContent('problemDescription', 'Not loaded yet');
  setTextContent('problemConstraints', 'Not loaded yet');
  setTextContent('problemLanguage', 'Not loaded yet');
  setTextContent('problemExamples', 'Not loaded yet');
  setTextContent('problemStarterCode', 'Not loaded yet');
}

function renderEmptyState(snapshot) {
  if (!snapshot) {
    setTextContent('emptyState', 'Open a LeetCode problem page, then click Read Current Problem.');
    return;
  }

  if (!snapshot.isLeetCodeProblemPage) {
    setTextContent('emptyState', 'This page is not a LeetCode problem page. Open a problem and try again.');
    return;
  }

  if (snapshot.ready) {
    setTextContent('emptyState', 'Snapshot loaded successfully.');
    return;
  }

  const warnings = Array.isArray(snapshot.warnings) && snapshot.warnings.length > 0 ? ` ${snapshot.warnings.join(' ')}` : '';
  setTextContent('emptyState', `LeetCode content is still settling, so some fields may be missing.${warnings}`);
}

function renderSnapshot(snapshot) {
  const isLeetCodeProblemPage = Boolean(snapshot?.isLeetCodeProblemPage);
  const isReady = Boolean(snapshot?.ready);

  setTextContent(
    'status',
    !snapshot
      ? 'No snapshot available.'
      : !isLeetCodeProblemPage
        ? 'This page is not a LeetCode problem page.'
        : isReady
          ? 'LeetCode problem detected.'
          : 'LeetCode problem detected, but content is still settling.'
  );

  setTextContent('problemTitle', snapshot?.title || 'Not found');
  setTextContent('problemDescription', snapshot?.description ? truncateText(snapshot.description, 220) : 'Not found');
  setTextContent('problemConstraints', Array.isArray(snapshot?.constraints) && snapshot.constraints.length > 0 ? truncateText(snapshot.constraints.join(' | '), 220) : 'Not found');
  setTextContent('problemLanguage', snapshot?.language || 'Not found');
  setTextContent('problemExamples', Array.isArray(snapshot?.examples) && snapshot.examples.length > 0 ? truncateText(snapshot.examples.join(' | '), 220) : 'Not found');
  setTextContent('problemStarterCode', snapshot?.starterCode ? truncateText(snapshot.starterCode, 300) : 'Not loaded yet');

  const fieldStatus = snapshot?.fieldStatus
    ? Object.entries(snapshot.fieldStatus)
      .map(([field, isPresent]) => `${field}: ${isPresent ? 'ok' : 'missing'}`)
      .join(' • ')
    : 'Field status unavailable.';

  const warnings = Array.isArray(snapshot?.warnings) && snapshot.warnings.length > 0 ? ` ${snapshot.warnings.join(' ')}` : '';

  setTextContent('fieldStatus', `${fieldStatus}.${warnings}`);
  renderEmptyState(snapshot);
}

function renderSolution(solution) {
  currentSolutionCode = solution?.code || '';

  setTextContent('solutionApproach', solution?.approach || 'Not generated yet');
  setTextContent('solutionExplanation', solution?.explanation || 'Not generated yet');
  setTextContent('solutionTimeComplexity', solution?.timeComplexity || 'Not generated yet');
  setTextContent('solutionSpaceComplexity', solution?.spaceComplexity || 'Not generated yet');
  setTextContent('solutionDryRun', solution?.dryRun || 'Not generated yet');
  setTextContent('solutionEdgeCases', solution?.edgeCases || 'Not generated yet');
  setTextContent('solutionCode', currentSolutionCode || 'Not generated yet');
  setInsertCodeButtonState(Boolean(currentSolutionCode));
}

function requestPageSnapshot() {
  setSnapshotLoadingState(true);

  chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_PAGE_SNAPSHOT }, (response) => {
    setSnapshotLoadingState(false);

    if (chrome.runtime.lastError) {
      setTextContent('status', chrome.runtime.lastError.message);
      renderEmptyState(null);
      return;
    }

    if (!response?.ok) {
      setTextContent('status', response?.error || 'Could not read the current page.');
      setTextContent('fieldStatus', 'Field status unavailable.');
      renderEmptyState(null);
      resetProblemFields();
      return;
    }

    renderSnapshot(response.data);
  });
}

function requestAiSolution() {
  setAiLoadingState(true);
  setTextContent('status', 'Requesting AI solution...');

  chrome.runtime.sendMessage({ type: 'REQUEST_AI_SOLUTION' }, (response) => {
    setAiLoadingState(false);

    if (chrome.runtime.lastError) {
      setTextContent('status', chrome.runtime.lastError.message);
      return;
    }

    if (!response?.ok) {
      setTextContent('status', response?.error || 'Could not generate a solution.');
      return;
    }

    setTextContent('status', 'AI solution generated successfully.');
    renderSolution(response.data);
  });
}

function requestInsertCode() {
  if (!currentSolutionCode) {
    setTextContent('status', 'No code is available to insert yet.');
    return;
  }

  const insertButton = document.getElementById('insertCodeButton');

  if (insertButton) {
    insertButton.disabled = true;
    insertButton.textContent = 'Inserting...';
  }

  chrome.runtime.sendMessage({
    type: MESSAGE_TYPES.INSERT_CODE,
    code: currentSolutionCode
  }, (response) => {
    if (insertButton) {
      insertButton.disabled = false;
      insertButton.textContent = 'Insert Code into Editor';
    }

    if (chrome.runtime.lastError) {
      setTextContent('status', chrome.runtime.lastError.message);
      return;
    }

    if (!response?.ok) {
      setTextContent('status', response?.error || 'Could not insert code into the editor.');
      return;
    }

    setTextContent('status', 'Code inserted into the editor.');
  });
}

function loadCachedSolution() {
  chrome.storage.session.get('cachedSolution', (result) => {
    if (chrome.runtime.lastError) {
      return;
    }

    const cachedSolution = result?.cachedSolution;

    if (cachedSolution) {
      setTextContent('status', 'Cached solution available (from Alt+Shift+A).');
      renderSolution(cachedSolution);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const statusElement = document.getElementById('status');
  const refreshButton = document.getElementById('refreshButton');
  const generateButton = document.getElementById('generateButton');
  const insertCodeButton = document.getElementById('insertCodeButton');

  if (statusElement) {
    statusElement.textContent = 'Ready to read the active LeetCode problem.';
  }

  if (refreshButton) {
    refreshButton.addEventListener('click', requestPageSnapshot);
  }

  if (generateButton) {
    generateButton.addEventListener('click', requestAiSolution);
  }

  if (insertCodeButton) {
    insertCodeButton.addEventListener('click', requestInsertCode);
  }

  loadCachedSolution();

  chrome.storage.session.get('autoReadSnapshot', (result) => {
    if (chrome.runtime.lastError) {
      return;
    }

    if (result?.autoReadSnapshot) {
      chrome.storage.session.remove('autoReadSnapshot', () => {
        requestPageSnapshot();
      });
    }
  });
});
