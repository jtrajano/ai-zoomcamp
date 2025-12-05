export interface ExecutionResult {
    logs: string[];
    error?: string;
}

export class ExecutionService {
    private pyodideWorker: Worker | null = null;

    constructor() {
        // Initialize workers if needed
    }

    async runJavaScript(code: string): Promise<ExecutionResult> {
        return new Promise((resolve) => {
            const logs: string[] = [];
            const workerCode = `
        const logs = [];
        const originalConsoleLog = console.log;
        console.log = (...args) => {
            logs.push(args.map(a => String(a)).join(' '));
            // originalConsoleLog(...args); // Optional: if we want to see it in browser devtools
        };
        
        try {
            // Basic safety wrapping
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

            // Timeout execution after 5 seconds
            setTimeout(() => {
                worker.terminate();
                resolve({ logs, error: 'Execution timed out.' });
            }, 5000);
        });
    }

    async runPython(code: string): Promise<ExecutionResult> {
        // For a real implementation, we would load Pyodide here.
        // Since Pyodide is heavy, we'll mock it for the MVP or use a CDN loader if requested.
        // Given the constraints and "safe execution", a real isolated environment is best.

        // Placeholder implementation for Python:
        return {
            logs: [],
            error: "Python execution requires loading Pyodide (heavy). Implemented as placeholder."
        };
    }
}

export const executionService = new ExecutionService();
