(() => {
  const shared = (globalThis.LeetCodeAIAssistant = globalThis.LeetCodeAIAssistant || {});
  const MESSAGE_TYPES = {
    GET_PAGE_SNAPSHOT: 'GET_PAGE_SNAPSHOT',
    INSERT_CODE: 'INSERT_CODE',
    CONTENT_READY: 'CONTENT_READY'
  };

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message?.type === MESSAGE_TYPES.GET_PAGE_SNAPSHOT) {
      (async () => {
        const snapshot = await shared.extractor.extractProblemData();
        sendResponse({ ok: true, data: snapshot });
      })().catch((error) => {
        sendResponse({ ok: false, error: error?.message ?? 'Failed to extract problem data.' });
      });

      return true;
    }

    if (message?.type === MESSAGE_TYPES.INSERT_CODE) {
      try {
        const result = shared.editor.insertCodeIntoEditor(message.code ?? '');
        sendResponse(result);
      } catch (error) {
        sendResponse({ ok: false, error: error?.message ?? 'Failed to insert code.' });
      }

      return true;
    }

    return false;
  });

  chrome.runtime.sendMessage({
    type: MESSAGE_TYPES.CONTENT_READY,
    isLeetCodeProblemPage: shared.extractor.isLeetCodeProblemPage()
  });
})();
