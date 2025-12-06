export interface ExecutionResult {
    logs: string[];
    error?: string;
}

export class ExecutionService {
    private pyodideWorker: Worker | null = null;
    private pyodideLogs: string[] = [];

    constructor() {
        // We instantiate the worker only when needed to save resources,
        // or we could do it on startup. For now, lazy load in runPython.
    }

    async runJavaScript(code: string): Promise<ExecutionResult> {
        return new Promise((resolve) => {
            const logs: string[] = [];
            const workerCode = `
        const logs = [];
        const originalConsoleLog = console.log;
        console.log = (...args) => {
            logs.push(args.map(a => String(a)).join(' '));
        };
        
        try {
            const run = new Function('${code.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}');
            run();
            postMessage({ success: true, logs });
        } catch (e) {
            postMessage({ success: false, error: e.toString(), logs });
        }
      `;

            const blob = new Blob([workerCode], { type: 'application/javascript' });
            const worker = new Worker(URL.createObjectURL(blob));

            worker.onmessage = (e) => {
                resolve({
                    logs: e.data.logs,
                    error: e.data.success ? undefined : e.data.error,
                });
                worker.terminate();
            };

            worker.onerror = (e) => {
                resolve({
                    logs: [],
                    error: 'Worker Error: ' + e.message,
                });
                worker.terminate();
            };

            setTimeout(() => {
                worker.terminate();
                resolve({ logs, error: 'Execution timed out.' });
            }, 5000);
        });
    }

    async runPython(code: string): Promise<ExecutionResult> {
        if (!this.pyodideWorker) {
            this.pyodideWorker = new Worker('/pyodide-worker.js');
        }

        return new Promise((resolve) => {
            const logs: string[] = [];
            this.pyodideLogs = []; // internal reset

            const handleMessage = (e: MessageEvent) => {
                const { type, content } = e.data;
                if (type === 'log') {
                    logs.push(content);
                } else if (type === 'error') {
                    // We treat stderr as part of result but maybe separate field? 
                    // For now, let's append to logs or set error.
                    // Typically stderr is just error output, not necessarily a crash.
                    // But our interface has one 'error' string.
                    // Let's accumulate logs and if 'error' event sends content, we use it.
                    logs.push("Error: " + content);
                } else if (type === 'done') {
                    resolve({ logs });
                }
            };

            // One-time listener for valid request-response cycle? 
            // Since worker is long-lived, we need to manage listeners.
            // For simplicity, we can use 'onmessage' but that overrides previous. 
            // If we allow concurrent runs, we need IDs. Assuming sequential for now.
            this.pyodideWorker!.onmessage = handleMessage;

            this.pyodideWorker!.onerror = (e) => {
                resolve({ logs, error: "Worker Error: " + e.message });
                // Assuming we don't terminate long-lived worker on error unless fatal
            };

            this.pyodideWorker!.postMessage({ code });
        });
    }
}

export const executionService = new ExecutionService();
