// pyodide-worker.js
importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

async function loadPyodideAndPackages() {
    self.pyodide = await loadPyodide();
    // Load standard packages if needed, e.g. self.pyodide.loadPackage(["numpy"]);
}

let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
    // Make sure to load pyodide first
    await pyodideReadyPromise;

    const { code } = event.data;

    try {
        // Reset output handling for each run
        const logs = [];
        const pushLog = (msg) => {
            logs.push(msg);
            postMessage({ type: 'log', content: msg });
        };

        self.pyodide.setStdout({ batched: pushLog });
        self.pyodide.setStderr({ batched: (msg) => postMessage({ type: 'error', content: msg }) });

        await self.pyodide.runPythonAsync(code);
        postMessage({ type: 'done', logs: logs });

    } catch (error) {
        postMessage({ type: 'error', content: error.message });
        postMessage({ type: 'done' });
    }
};
