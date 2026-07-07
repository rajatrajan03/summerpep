# LeetCode AI Assistant

LeetCode AI Assistant is a Chrome Extension Manifest V3 project that helps with LeetCode problem analysis. The current codebase focuses on the extension shell, popup UI, background service worker, and a readiness-aware content-script pipeline for reading LeetCode problem pages.

## Current State

Implemented so far:

- MV3 extension manifest and service worker
- Popup UI with actions for reading the current problem, requesting an AI solution, and inserting code into the editor
- Background message routing between popup and content scripts
- Content-script modules for parsing, extraction, editor insertion, and messaging
- Readiness-aware LeetCode extraction with section parsing and best-effort fallbacks
- Shared utility modules for constants, helpers, defaults, and storage
- **AI request and response-validation fully operational**
- **Keyboard-driven productivity workflow:** Alt+Shift+A to generate solutions, Alt+Shift+V to insert cached code instantly
- **Solution caching:** Generated solutions persist in session storage for multiple insertions
- **Extension badge:** Shows generation progress ("⏳") and completion status ("✓")
- **Notifications:** Real-time feedback for generation, completion, and errors

Planned next:

- Improve message-passing contracts and shared protocol definitions
- Add theme support for dark mode
- Continue tuning extraction edge cases from real LeetCode layouts
- Prepare Chrome Web Store submission assets

## Repository Structure

```text
LeetCode-AI-Assistant/
├── manifest.json
├── popup.html
├── popup.css
├── popup.js
├── background.js
├── content/
│   ├── extractor.js
│   ├── editor.js
│   ├── parser.js
│   └── messaging.js
├── api/
│   └── ai.js
├── utils/
│   ├── storage.js
│   ├── constants.js
│   ├── defaults.js
│   └── helpers.js
├── assets/
├── icons/
└── docs and root files
```

## Architecture Overview

The extension currently follows this flow:

1. The user opens the popup from the Chrome toolbar.
2. The popup requests the active LeetCode page snapshot from the background service worker.
3. The background worker checks the active tab and forwards the request to the content script.
4. The content script waits for the LeetCode page to settle, then reads the DOM and returns structured problem data with field-level status and fallback warnings.
5. The popup displays the extracted data.
6. The popup can also request a generated AI solution through the background worker.

The AI path is present in code, but the project priority remains on extraction hardening and documentation before further feature work.

## Coding Standards

This project follows these working rules:

- Use modern JavaScript and ES modules.
- Keep files small and focused.
- Prefer async/await for asynchronous code.
- Avoid jQuery and deprecated Chrome APIs.
- Keep message passing explicit and easy to trace.
- Use defensive null checks around DOM access.
- Prefer reusable helpers over duplicated logic.
- Avoid unnecessary dependencies during early development.
- Prefer readiness-aware extraction and fallback data instead of failing on the first missing node.

## Testing the Current Build

At this stage, the project is best validated manually in Chrome:

1. Load the unpacked extension from the workspace root.
2. Open a LeetCode problem page.
3. **Quick-start workflows:**
   - Press `Alt+Shift+L` to open the popup.
   - Press `Alt+Shift+R` to open the popup and auto-read the current problem.
   - Press `Alt+Shift+A` to extract the problem and generate an AI solution (shows notification when ready).
   - Press `Alt+Shift+V` to instantly insert the cached solution code into the editor.
4. **Manual actions via popup:**
   - Open the popup and click "Read Current Problem" to see the problem details.
   - Once a problem is read, click "Generate AI Solution" to get AI-generated approach, explanation, complexity analysis, and code.
   - Click "Insert Code into Editor" to send the code to the Monaco editor.
5. Confirm the field-status line reports which fields were found and whether the page was still settling.
6. Confirm notifications appear when solutions are generated or when actions complete.
7. Check the badge on the extension icon (shows "⏳" while generating, "✓" when ready).

AI requests are now operational with the new Alt+Shift+A workflow, but can be triggered manually via the popup "Generate AI Solution" button as well.

## Roadmap

1. [x] Keyboard-driven productivity workflow (Alt+Shift+A, Alt+Shift+V)
2. [x] AI solution generation and caching
3. [ ] Improve message-passing protocol and error contracts
4. [ ] Add theme and dark mode support
5. [ ] Continue tuning extraction edge cases from real LeetCode layouts
6. [ ] Prepare packaging and store submission assets
