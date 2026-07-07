export const APP_NAME = 'LeetCode AI Assistant';
export const LEETCODE_PROBLEM_URL_PATTERN = /https:\/\/leetcode\.com\/problems\//i;

export const MESSAGE_TYPES = Object.freeze({
  GET_PAGE_SNAPSHOT: 'GET_PAGE_SNAPSHOT',
  PAGE_SNAPSHOT: 'PAGE_SNAPSHOT',
  INSERT_CODE: 'INSERT_CODE',
  INSERT_CODE_RESULT: 'INSERT_CODE_RESULT',
  CONTENT_READY: 'CONTENT_READY',
  ERROR: 'ERROR'
});

export const STORAGE_KEYS = Object.freeze({
  API_KEY: 'apiKey',
  SETTINGS: 'settings'
});

export const AI_RESPONSE_FIELDS = Object.freeze([
  'approach',
  'explanation',
  'timeComplexity',
  'spaceComplexity',
  'code',
  'dryRun',
  'edgeCases'
]);
