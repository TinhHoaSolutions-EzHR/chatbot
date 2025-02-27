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

const decodeChunk = (event: string, chunk: string): ChatStreamChunk => {
  switch (event) {
    case ChatMessageStreamEvent.METADATA:
      return {
        event: ChatMessageStreamEvent.METADATA,
        data: parseJSONDataChunk<IChatMessageResponse>(chunk),
      };
    case ChatMessageStreamEvent.DELTA:
    case ChatMessageStreamEvent.TITLE_GENERATION:
      return {
        event,
        data: parseJSONDataChunk<string>(chunk),
      };
    case ChatMessageStreamEvent.STREAM_COMPLETE:
      return {
        event: ChatMessageStreamEvent.STREAM_COMPLETE,
        data: parseJSONDataChunk<Omit<IChatMessageResponse, 'message'>>(chunk),
      };
    default:
      return {
        event: ChatMessageStreamEvent.ERROR,
        data: parseJSONDataChunk<string>(chunk),
      };
  }
};

export const decodeChatStreamChunks = (chunk: string): ChatStreamChunk[] => {
  const lines = chunk.trim().split('\n');

  try {
    const events: string[] = [];
    const receivedChunks: string[] = [];

    for (const line of lines) {
      if (line.startsWith(CHAT_STREAM_EVENT_KEY)) {
        events.push(line.slice(CHAT_STREAM_EVENT_KEY_LENGTH).trim());
      } else if (line.startsWith(CHAT_STREAM_DATA_KEY)) {
        receivedChunks.push(line.slice(CHAT_STREAM_DATA_KEY_LENGTH).trim());
      }
    }

    return events.map((ev, idx) => decodeChunk(ev, receivedChunks[idx]));
  } catch (error) {
    console.error('[DecodeChatStreamChunk]: ', error);
    throw error;
  }
};
