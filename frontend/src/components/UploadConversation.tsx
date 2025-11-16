import { useState } from 'react';
import { uploadConversation } from '../api';

export default function UploadConversation() {
  const [jsonText, setJsonText] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    try {
      const parsed = JSON.parse(jsonText);
      const result = await uploadConversation(parsed.messages);
      setConversationId(result.conversation_id);
      setError('');
    } catch (err) {
      setError('Invalid JSON or request failed');
      setConversationId(null);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Conversation</h2>
      <textarea
        className="w-full p-3 border border-gray-300 rounded mb-4 font-mono text-sm"
        rows={10}
        value={jsonText}
        onChange={(e) => setJsonText(e.target.value)}
        placeholder='{"messages": [{"sender": "user", "message": "..."}, {"sender": "ai", "message": "..."}]}'
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={handleSubmit}
      >
        Upload
      </button>
      {conversationId && (
        <div className="mt-4 p-3 bg-gray-100 rounded">
          Conversation ID: {conversationId}
        </div>
      )}
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
    </div>
  );
}

