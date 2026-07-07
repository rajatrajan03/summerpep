import { STORAGE_KEYS } from './constants.js';
import { DEFAULT_SETTINGS } from './defaults.js';

export async function getApiKey() {
  const result = await chrome.storage.local.get(STORAGE_KEYS.API_KEY);
  return result[STORAGE_KEYS.API_KEY] ?? '';
}

export async function setApiKey(apiKey) {
  await chrome.storage.local.set({ [STORAGE_KEYS.API_KEY]: apiKey });
}

export async function getSettings() {
  const result = await chrome.storage.sync.get(STORAGE_KEYS.SETTINGS);
  return { ...DEFAULT_SETTINGS, ...(result[STORAGE_KEYS.SETTINGS] ?? {}) };
}

export async function setSettings(settings) {
  await chrome.storage.sync.set({ [STORAGE_KEYS.SETTINGS]: settings });
}
