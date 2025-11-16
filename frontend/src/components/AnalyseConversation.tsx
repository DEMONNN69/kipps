import { useState } from 'react';
import { analyseConversation } from '../api';

export default function AnalyseConversation() {
  const [conversationId, setConversationId] = useState('');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleAnalyse = async () => {
    try {
      const id = parseInt(conversationId);
      const data = await analyseConversation(id);
      setResult(data);
      setError('');
    } catch (err) {
      setError('Analysis failed');
      setResult(null);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Analyse Conversation</h2>
      <div className="mb-4">
        <input
          type="number"
          className="p-2 border border-gray-300 rounded mr-2"
          value={conversationId}
          onChange={(e) => setConversationId(e.target.value)}
          placeholder="Conversation ID"
        />
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={handleAnalyse}
        >
          Analyse
        </button>
      </div>
      {result && (
        <div className="mt-4 p-4 bg-gray-50 rounded border">
          <pre className="text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
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

