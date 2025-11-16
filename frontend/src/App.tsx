import { useState } from 'react';
import UploadConversation from './components/UploadConversation';
import AnalyseConversation from './components/AnalyseConversation';
import Reports from './components/Reports';

type Screen = 'upload' | 'analyse' | 'reports';

function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('upload');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <nav className="flex gap-4">
            <button
              className={`px-4 py-2 rounded ${
                currentScreen === 'upload'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              onClick={() => setCurrentScreen('upload')}
            >
              Upload Conversation
            </button>
            <button
              className={`px-4 py-2 rounded ${
                currentScreen === 'analyse'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              onClick={() => setCurrentScreen('analyse')}
            >
              Analyse Conversation
            </button>
            <button
              className={`px-4 py-2 rounded ${
                currentScreen === 'reports'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              onClick={() => setCurrentScreen('reports')}
            >
              Reports
            </button>
          </nav>
        </div>
      </div>
      <div className="max-w-7xl mx-auto">
        {currentScreen === 'upload' && <UploadConversation />}
        {currentScreen === 'analyse' && <AnalyseConversation />}
        {currentScreen === 'reports' && <Reports />}
      </div>
    </div>
  );
}

export default App;
