import React, { useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CodeEditor } from '../components/CodeEditor';
import { OutputPanel } from '../components/OutputPanel';
import { executionService } from '../services/ExecutionService';

export const RoomView: React.FC = () => {
    const { roomId } = useParams<{ roomId: string }>();
    const [language, setLanguage] = useState('javascript');
    const [code, setCode] = useState('');
    const [logs, setLogs] = useState<string[]>([]);
    const [error, setError] = useState<string | undefined>();
    const [isRunning, setIsRunning] = useState(false);

    // Default to a random room if none provided
    const activeRoom = roomId || 'default-room';

    const handleRunCode = useCallback(async () => {
        setIsRunning(true);
        setLogs([]);
        setError(undefined);

        try {
            let result;
            if (language === 'javascript') {
                result = await executionService.runJavaScript(code);
            } else {
                result = await executionService.runPython(code);
            }
            setLogs(result.logs);
            setError(result.error);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setIsRunning(false);
        }
    }, [code, language]);

    return (
        <div className="app-container">
            {/* Header */}
            <header className="app-header">
                <div className="room-info">
                    <Link to="/" className="brand">
                        CodeInterview.io
                    </Link>
                    <span style={{ color: '#52525b', margin: '0 8px' }}>/</span>
                    <span style={{ color: '#a1a1aa', fontSize: '0.9rem' }}>Room:</span>
                    <span className="room-badge">{activeRoom}</span>
                </div>

                <div className="controls">
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="select-input"
                    >
                        <option value="javascript">JavaScript</option>
                        <option value="python">Python (Mock)</option>
                    </select>

                    <button
                        onClick={handleRunCode}
                        disabled={isRunning}
                        className="btn btn-success"
                    >
                        {isRunning ? 'Running...' : 'Run Code'}
                    </button>

                    <button
                        onClick={() => {
                            navigator.clipboard.writeText(window.location.href);
                            alert("Room link copied!");
                        }}
                        className="btn btn-primary"
                    >
                        Share
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                {/* Editor Section */}
                <div className="editor-section">
                    <CodeEditor
                        roomId={activeRoom}
                        language={language}
                        onCodeChange={setCode}
                    />
                </div>

                {/* Output Section */}
                <div className="output-section">
                    <OutputPanel
                        logs={logs}
                        error={error}
                        onClear={() => { setLogs([]); setError(undefined); }}
                    />
                </div>
            </main>
        </div>
    );
};
