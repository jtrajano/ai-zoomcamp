import React, { useEffect, useRef, useState } from 'react';
import Editor, { type OnMount } from '@monaco-editor/react';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { MonacoBinding } from 'y-monaco';

interface CodeEditorProps {
    roomId: string;
    language: string;
    onCodeChange?: (code: string) => void;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ roomId, language, onCodeChange }) => {
    const [editorRef, setEditorRef] = useState<any>(null);
    const providerRef = useRef<WebsocketProvider | null>(null);
    const docRef = useRef<Y.Doc>(new Y.Doc());
    const bindingRef = useRef<MonacoBinding | null>(null);

    useEffect(() => {
        // Connect to WebSocket
        // Note: Use 'ws://localhost:8000/ws' for local backend
        providerRef.current = new WebsocketProvider(
            'ws://localhost:8000/ws',
            roomId,
            docRef.current
        );

        return () => {
            providerRef.current?.destroy();
            docRef.current.destroy();
        };
    }, [roomId]);

    const handleEditorDidMount: OnMount = (editor, monaco) => {
        setEditorRef(editor);
        const type = docRef.current.getText('monaco');

        if (providerRef.current) {
            try {
                bindingRef.current = new MonacoBinding(
                    type,
                    editor.getModel()!,
                    new Set([editor]),
                    providerRef.current.awareness
                );
            } catch (e) {
                console.error("Failed to bind Monaco:", e);
            }
        }
    };

    useEffect(() => {
        if (!editorRef) return;

        // Sync initial value (in case Yjs populated it before listener attached)
        onCodeChange?.(editorRef.getValue());

        const disposable = editorRef.onDidChangeModelContent(() => {
            onCodeChange?.(editorRef.getValue());
        });
        return () => disposable.dispose();
    }, [editorRef, onCodeChange]);

    return (
        <div className="editor-container">
            <Editor
                height="100%"
                defaultLanguage="javascript"
                language={language}
                theme="vs-dark"
                onMount={handleEditorDidMount}
                options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    scrollBeyondLastLine: false,
                    padding: { top: 16 }
                }}
            />
        </div>
    );
};
