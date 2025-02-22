import { ChatMessageStreamEvent, ChatStreamChunk, IChatMessageResponse } from '@/types/chat';

// The `c` stands for "content", the `data` of the streaming response is in the format of
// {"c": A JSON OBJECT}
const CHAT_STREAM_DATA_CONTENT = 'c';

const CHAT_STREAM_EVENT_KEY = 'event:';
const CHAT_STREAM_DATA_KEY = 'data:';

const CHAT_STREAM_EVENT_KEY_LENGTH = CHAT_STREAM_EVENT_KEY.length;
const CHAT_STREAM_DATA_KEY_LENGTH = CHAT_STREAM_DATA_KEY.length;

function parseJSONDataChunk<T>(data: string) {
  const parsedValue: { [CHAT_STREAM_DATA_CONTENT]: T } = JSON.parse(data);
  return parsedValue[CHAT_STREAM_DATA_CONTENT];
}

export const decodeChatStreamChunk = (chunk: string): ChatStreamChunk => {
  const lines = chunk.trim().split('\n');

  try {
    let currentEvent = '';
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
          data: parseJSONDataChunk<IChatMessageResponse>(receivedChunks[0]),
        };
      case ChatMessageStreamEvent.DELTA:
        return {
          event: ChatMessageStreamEvent.DELTA,
          data: receivedChunks.reduce<string>((acc, cur) => acc + parseJSONDataChunk<string>(cur), ''),
        };
      case ChatMessageStreamEvent.STREAM_COMPLETE:
        return {
          event: ChatMessageStreamEvent.STREAM_COMPLETE,
          data: parseJSONDataChunk<Omit<IChatMessageResponse, 'message'>>(receivedChunks[0]),
        };
      default:
        return {
          event: ChatMessageStreamEvent.ERROR,
          data: parseJSONDataChunk<string>(receivedChunks[0]),
        };
    }
  } catch (error) {
    console.error('[DecodeChatStreamChunk]: ', error);
    throw error;
  }
};
