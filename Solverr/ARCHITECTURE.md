# Architecture

## Purpose

LeetCode AI Assistant is a Chrome Extension Manifest V3 project designed to help analyze LeetCode problems. The current architecture is intentionally lean and separates page extraction, popup display, background orchestration, and future AI integration.

## Current Modules

### `manifest.json`
Defines the extension entry points, permissions, and content-script registration.

### `popup.html`, `popup.css`, `popup.js`
Provide the extension UI shown from the Chrome toolbar. The popup requests problem data, renders extracted information and AI response placeholders, and exposes the insert-code action for the Monaco editor workflow.

### `background.js`
Acts as the MV3 service worker. It is responsible for routing messages between the popup and the content scripts, coordinating tab checks, and handling keyboard shortcut commands.

### `content/parser.js`
Contains reusable DOM text helpers used by the extraction layer.

### `content/extractor.js`
Extracts problem-related data from the active LeetCode page. It now waits for the page to settle, uses section-aware parsing, and returns best-effort snapshots with field status and warnings.

### `content/editor.js`
Contains Monaco editor insertion logic for later code insertion support.

### `content/messaging.js`
Registers the content-script message handlers.

### `api/ai.js`
Contains prompt construction, response validation, and request logic for AI integration scaffolding.

### `utils/*`
Shared constants, defaults, storage helpers, and text utilities.

## Runtime Flow

1. **Popup-driven workflow:**
   - User opens the popup.
   - Popup asks background worker for the active page snapshot.
   - Background worker verifies the current tab and forwards the request to the content script.
   - Content script waits for LeetCode content to stabilize, then reads the DOM and returns structured problem data.
   - Popup renders that data together with extraction field status.
   - User can click "Generate AI Solution" to request AI output via the background worker's REQUEST_AI_SOLUTION handler.
   - User can click "Insert Code into Editor" to send cached code to the Monaco editor.

2. **Keyboard-driven productivity workflow (new):**
   - User presses `Alt+Shift+A` on a LeetCode problem page.
   - Background worker handles the "extract-and-generate" command:
     - Extracts problem snapshot using GET_PAGE_SNAPSHOT.
     - Requests AI solution via api/ai.js with the extracted data.
     - Caches solution in chrome.storage.session.cachedSolution.
     - Updates extension badge to "⏳" (working) then "✓" (ready).
     - Shows notification when complete.
   - User presses `Alt+Shift+V` to instantly insert the cached code.
   - Background worker handles the "insert-cached-code" command:
     - Retrieves cached solution from session storage.
     - Sends INSERT_CODE message with the code to the content script.
     - Shows notification when insertion completes.
   - If popup is open, it automatically displays any cached solution via loadCachedSolution() in DOMContentLoaded.

3. **Other keyboard shortcuts:**
   - `Alt+Shift+L`: Opens the popup.
   - `Alt+Shift+R`: Opens the popup and auto-reads the current problem.


## Design Principles

- Keep MV3 responsibilities separated (popup, background, content, API).
- Keep DOM parsing isolated from popup UI logic.
- Use background message routing instead of direct popup-to-page coupling.
- Prefer small modules with single responsibilities.
- Use session storage for ephemeral data (cached solutions, auto-read flags).
- Use local storage for persistent user data (API keys).
- Use sync storage for preferences (AI endpoint, model selection).
- Provide real-time feedback via badge and notifications.
- Keep keyboard-driven workflows fast and lightweight.
- Use readiness-aware extraction and fallback data instead of failing on the first missing node.

## Current Architectural Risks

- Real-world LeetCode layouts can still require selector tuning.
- Badge updates are fire-and-forget; consider tracking background task state in session storage for better robustness.
- Notification icons reference a hardcoded path; ensure icon files exist at build time.
- AI API calls are blocking; consider adding timeout handling and request cancellation.
- No persistent history of generated solutions; users must re-generate on browser restart.

## Next Architectural Step

The next task is to improve message-passing protocol by centralizing request/response shape definitions to avoid brittle string literals.
