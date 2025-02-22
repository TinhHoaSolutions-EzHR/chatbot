import { IChatSession } from '@/types/chat';

const YESTERDAY = 1;
const LAST_WEEK = 7;
const LAST_MONTH = 30;

export const groupChatSessions = (chatSessions: IChatSession[]) => {
  const now = new Date();
  const groupedSessions: { [key: string]: IChatSession[] } = {};

  const isSameDay = (aDate: Date, bDate: Date) => aDate.toDateString() === bDate.toDateString();

  const isWithinDays = (date: Date, days: number) => {
    const pastDate = new Date(now);
    pastDate.setDate(now.getDate() - days);
    return date >= pastDate && date < now;
  };

  chatSessions.forEach(session => {
    const sessionDate = new Date(session.updated_at);

    let key: string;

    switch (true) {
      case isSameDay(sessionDate, now):
        key = 'Today';
        break;
      case isWithinDays(sessionDate, YESTERDAY):
        key = 'Yesterday';
        break;
      case isWithinDays(sessionDate, LAST_WEEK):
        key = 'Previous 7 days';
        break;
      case isWithinDays(sessionDate, LAST_MONTH):
        key = 'Previous 30 days';
        break;
      default:
        key = sessionDate.getFullYear().toString();
        break;
    }

    if (!groupedSessions[key]) {
      groupedSessions[key] = [];
    }

    groupedSessions[key].push(session);
  });

  return Object.entries(groupedSessions).map(([title, chatSessions]) => ({
    title,
    chatSessions,
  }));
};
