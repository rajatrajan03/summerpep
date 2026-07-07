(() => {
  const shared = (globalThis.LeetCodeAIAssistant = globalThis.LeetCodeAIAssistant || {});

  function getMonacoInputElement() {
    return document.querySelector('textarea.inputarea');
  }

  function setNativeValue(element, value) {
    const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value')?.set;
    const prototype = Object.getPrototypeOf(element);
    const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
    const setter = valueSetter || prototypeValueSetter;

    if (setter) {
      setter.call(element, value);
    } else {
      element.value = value;
    }
  }

  function insertCodeIntoEditor(code) {
    const editorInput = getMonacoInputElement();

    if (!editorInput) {
      return { ok: false, error: 'Could not find the Monaco editor input.' };
    }

    editorInput.focus();
    setNativeValue(editorInput, code);
    editorInput.dispatchEvent(new InputEvent('input', {
      bubbles: true,
      composed: true,
      inputType: 'insertText',
      data: code
    }));

    return { ok: true };
  }

  shared.editor = {
    getMonacoInputElement,
    insertCodeIntoEditor
  };
})();
