const ABORT_ERROR_NAME = 'AbortError';

export function checkAbortError(error: unknown): error is DOMException {
  return error instanceof DOMException && error.name === ABORT_ERROR_NAME;
}
