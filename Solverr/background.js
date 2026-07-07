import { APP_NAME, MESSAGE_TYPES } from './utils/constants.js';
import { isLeetCodeProblemUrl } from './utils/helpers.js';
import { getApiKey, getSettings } from './utils/storage.js';
import { requestAiSolution } from './api/ai.js';

const CONTENT_SCRIPT_FILES = [
  'content/parser.js',
  'content/extractor.js',
  'content/editor.js',
  'content/messaging.js'
];

function getActiveTab() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs[0] ?? null);
    });
  });
}

function sendMessageToTab(tabId, message) {
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(tabId, message, (response) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }

      resolve(response);
    });
  });
}

async function ensureContentScriptsInjected(tabId) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      files: CONTENT_SCRIPT_FILES
    });
  } catch (error) {
    if (!String(error?.message ?? '').includes('Cannot access contents of url')) {
      throw error;
    }
  }
}

async function ensureLeetCodeContentScripts(tab) {
  if (!tab?.id || !tab.url || !isLeetCodeProblemUrl(tab.url)) {
    throw new Error('Open a LeetCode problem page first.');
  }

  await ensureContentScriptsInjected(tab.id);
}

function updateBadge(text) {
  chrome.action.setBadgeText({ text });
  chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });
}

function clearBadge() {
  chrome.action.setBadgeText({ text: '' });
}

function showNotification(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: chrome.runtime.getURL('icons/icon-48.png'),
    title,
    message
  });
}

chrome.runtime.onInstalled.addListener(() => {
  console.log(`${APP_NAME} installed.`);
});

chrome.commands.onCommand.addListener(async (command) => {
  try {
    if (command === 'read-current-problem') {
      await chrome.storage.session.set({ autoReadSnapshot: true });
    }

    if (command === 'open-popup' || command === 'read-current-problem') {
      await chrome.action.openPopup();
    }

    if (command === 'extract-and-generate') {
      const activeTab = await getActiveTab();

      await ensureLeetCodeContentScripts(activeTab);

      const snapshotResponse = await sendMessageToTab(activeTab.id, { type: MESSAGE_TYPES.GET_PAGE_SNAPSHOT });

      if (!snapshotResponse?.ok) {
        showNotification('LeetCode AI Assistant', 'Could not read the problem. Try again.');
        return;
      }

      const apiKey = await getApiKey();

      if (!apiKey) {
        showNotification('LeetCode AI Assistant', 'Add your API key in settings first.');
        return;
      }

      updateBadge('⏳');

      try {
        const settings = await getSettings();
        const aiResponse = await requestAiSolution({
          apiKey,
          endpoint: settings.aiEndpoint,
          model: settings.aiModel,
          problemData: snapshotResponse.data
        });

        await chrome.storage.session.set({
          cachedSolution: aiResponse
        });

        updateBadge('✓');
        showNotification('LeetCode AI Assistant', 'Solution ready! Press Alt+Shift+V to insert code.');
      } catch (error) {
        clearBadge();
        showNotification('LeetCode AI Assistant', `Generation failed: ${error.message}`);
      }
    }

    if (command === 'insert-cached-code') {
      const sessionData = await chrome.storage.session.get('cachedSolution');
      const cachedSolution = sessionData?.cachedSolution;

      if (!cachedSolution?.code) {
        showNotification('LeetCode AI Assistant', 'No cached solution. Generate one first with Alt+Shift+A.');
        return;
      }

      const activeTab = await getActiveTab();

      await ensureLeetCodeContentScripts(activeTab);

      try {
        await sendMessageToTab(activeTab.id, {
          type: MESSAGE_TYPES.INSERT_CODE,
          code: cachedSolution.code
        });

        showNotification('LeetCode AI Assistant', 'Code inserted into editor!');
      } catch (error) {
        showNotification('LeetCode AI Assistant', `Insertion failed: ${error.message}`);
      }
    }
  } catch (error) {
    console.warn('Failed to handle keyboard shortcut:', error);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === MESSAGE_TYPES.GET_PAGE_SNAPSHOT) {
    (async () => {
      const activeTab = await getActiveTab();

      await ensureLeetCodeContentScripts(activeTab);

      if (!activeTab?.id || !activeTab.url || !isLeetCodeProblemUrl(activeTab.url)) {
        sendResponse({ ok: false, error: 'Open a LeetCode problem page first.' });
        return;
      }

      const response = await sendMessageToTab(activeTab.id, { type: MESSAGE_TYPES.GET_PAGE_SNAPSHOT });
      sendResponse(response ?? { ok: false, error: 'No response from the content script.' });
    })().catch((error) => {
      sendResponse({ ok: false, error: error.message });
    });

    return true;
  }

  if (message?.type === MESSAGE_TYPES.INSERT_CODE) {
    (async () => {
      const activeTab = await getActiveTab();

      await ensureLeetCodeContentScripts(activeTab);

      if (!activeTab?.id || !activeTab.url || !isLeetCodeProblemUrl(activeTab.url)) {
        sendResponse({ ok: false, error: 'Open a LeetCode problem page first.' });
        return;
      }

      const response = await sendMessageToTab(activeTab.id, {
        type: MESSAGE_TYPES.INSERT_CODE,
        code: message.code ?? ''
      });

      sendResponse(response ?? { ok: false, error: 'No response from the content script.' });
    })().catch((error) => {
      sendResponse({ ok: false, error: error.message });
    });

    return true;
  }

  if (message?.type === 'REQUEST_AI_SOLUTION') {
    (async () => {
      const activeTab = await getActiveTab();

      await ensureLeetCodeContentScripts(activeTab);

      if (!activeTab?.id || !activeTab.url || !isLeetCodeProblemUrl(activeTab.url)) {
        sendResponse({ ok: false, error: 'Open a LeetCode problem page first.' });
        return;
      }

      const snapshotResponse = await sendMessageToTab(activeTab.id, { type: MESSAGE_TYPES.GET_PAGE_SNAPSHOT });

      if (!snapshotResponse?.ok) {
        sendResponse(snapshotResponse ?? { ok: false, error: 'Could not read the current problem.' });
        return;
      }

      const apiKey = await getApiKey();

      if (!apiKey) {
        sendResponse({ ok: false, error: 'Add your API key in settings first.' });
        return;
      }

      const settings = await getSettings();
      const aiResponse = await requestAiSolution({
        apiKey,
        endpoint: settings.aiEndpoint,
        model: settings.aiModel,
        problemData: snapshotResponse.data
      });

      sendResponse({ ok: true, data: aiResponse });
    })().catch((error) => {
      sendResponse({ ok: false, error: error.message });
    });

    return true;
  }

  return false;
});
