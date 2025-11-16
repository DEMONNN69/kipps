const API_BASE_URL = 'http://localhost:8000';

export const uploadConversation = async (messages: Array<{ sender: string; message: string }>) => {
  const response = await fetch(`${API_BASE_URL}/api/conversations/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  });
  return response.json();
};

export const analyseConversation = async (conversationId: number) => {
  const response = await fetch(`${API_BASE_URL}/api/analyse/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ conversation_id: conversationId }),
  });
  return response.json();
};

export const getReports = async () => {
  const response = await fetch(`${API_BASE_URL}/api/reports/`);
  return response.json();
};

