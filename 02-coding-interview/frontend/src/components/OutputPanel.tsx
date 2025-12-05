import React from 'react';

interface OutputPanelProps {
    logs: string[];
    error?: string;
    onClear: () => void;
}

export const OutputPanel: React.FC<OutputPanelProps> = ({ logs, error, onClear }) => {
    return (
        <div className="output-panel">
            <div className="output-header">
                <span style={{ color: '#e4e4e7', fontWeight: 500 }}>Console Output</span>
                <button
                    onClick={onClear}
                    className="btn"
                    style={{ padding: '2px 8px', fontSize: '0.8rem', color: '#a1a1aa' }}
                >
                    Clear
                </button>
            </div>
            <div className="output-content">
                {logs.length === 0 && !error && (
                    <div style={{ color: '#52525b', fontStyle: 'italic' }}>Run code to see output...</div>
                )}
                {logs.map((log, i) => (
                    <div key={i} className="log-entry">
                        {'> '}{log}
                    </div>
                ))}
                {error && (
                    <div className="log-error">
                        <strong>Error:</strong> {error}
                    </div>
                )}
            </div>
        </div>
    );
};
