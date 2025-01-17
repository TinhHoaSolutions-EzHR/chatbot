import { ChatMessageStreamEvent, ChatStreamChunk, IChatMessageResponse } from '@/types/chat';

// The `c` stands for "content", the `data` of the streaming response is in the format of
// {"c": A JSON OBJECT}
const CHAT_STREAM_DATA_CONTENT = 'c';

const CHAT_STREAM_EVENT_KEY = 'event:';
const CHAT_STREAM_DATA_KEY = 'data:';

const CHAT_STREAM_EVENT_KEY_LENGTH = CHAT_STREAM_EVENT_KEY.length;
const CHAT_STREAM_DATA_KEY_LENGTH = CHAT_STREAM_DATA_KEY.length;

function fixPythonLiterals(data: string): string {
  return data
    .replace(/\bTrue\b/g, 'true') // Replace True with true
    .replace(/\bFalse\b/g, 'false') // Replace False with false
    .replace(/\bNone\b/g, 'null') // Replace None with null
    .replace(/"/g, '\\"') // Handle improperly escaped quotes
    .replace(/'/g, '"'); // Replace single quote with double quotes
}

function parseJSON<T>(data: string) {
  const parsedValue: { [CHAT_STREAM_DATA_CONTENT]: T } = JSON.parse(fixPythonLiterals(data));
  return parsedValue;
}

export const decodeChatStreamChunk = (chunk: string): ChatStreamChunk => {
  const lines = chunk.trim().split('\n');

  try {
    let currentEvent = '';
    // This is a temporary solution for the error of getting multiple `event` and `data` in a single chunk, for example
    // ```
    // event: delta
    // data: {'c': '.'}
    //
    // event: delta
    // data: {'c': '.'}
    //
    // ```
    // Have to deal with this manually before backend team find a solution. However, this behavior only appears for the event
    // `delta`, which is the response from the openai model.
    // TODO: Modify this logic
    const receivedChunks: string[] = [];

    for (const line of lines) {
      if (line.startsWith(CHAT_STREAM_EVENT_KEY)) {
        currentEvent = line.slice(CHAT_STREAM_EVENT_KEY_LENGTH).trim();
      } else if (line.startsWith(CHAT_STREAM_DATA_KEY)) {
        receivedChunks.push(line.slice(CHAT_STREAM_DATA_KEY_LENGTH).trim());
      }
    }

    switch (currentEvent) {
      case ChatMessageStreamEvent.METADATA:
        return {
          event: ChatMessageStreamEvent.METADATA,
          data: parseJSON<IChatMessageResponse>(receivedChunks[0])[CHAT_STREAM_DATA_CONTENT],
        };
      case ChatMessageStreamEvent.DELTA:
        return {
          event: ChatMessageStreamEvent.DELTA,
          data: receivedChunks.reduce<string>((acc, cur) => acc + parseJSON<string>(cur)[CHAT_STREAM_DATA_CONTENT], ''),
        };
      case ChatMessageStreamEvent.STREAM_COMPLETE:
        return {
          event: ChatMessageStreamEvent.STREAM_COMPLETE,
          data: parseJSON<Omit<IChatMessageResponse, 'message'>>(receivedChunks[0])[CHAT_STREAM_DATA_CONTENT],
        };
      default:
        return {
          event: ChatMessageStreamEvent.ERROR,
          data: parseJSON<string>(receivedChunks[0])[CHAT_STREAM_DATA_CONTENT],
        };
    }
  } catch (error) {
    console.error(['Error decoding chat stream: ', error]);
    throw error;
  }
};
