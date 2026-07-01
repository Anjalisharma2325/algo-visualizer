import { useState } from "react";

// Set this to your deployed backend URL once you deploy (e.g. Render/Railway).
// For local dev, the FastAPI default is http://127.0.0.1:8000
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const SORT_ALGORITHMS = [
  { value: "bubble", label: "Bubble Sort" },
  { value: "merge", label: "Merge Sort" },
  { value: "quick", label: "Quick Sort" },
];

const SEARCH_ALGORITHMS = [
  { value: "linear", label: "Linear Search" },
  { value: "binary", label: "Binary Search" },
];

function randomArray(size = 20, max = 100) {
  return Array.from({ length: size }, () => Math.floor(Math.random() * max) + 1);
}

export default function App() {
  const [mode, setMode] = useState("sort"); // "sort" | "search"
  const [array, setArray] = useState(randomArray());
  const [algorithm, setAlgorithm] = useState("bubble");
  const [target, setTarget] = useState(50);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateArray = () => {
    setArray(randomArray());
    setResult(null);
  };

  const handleArrayInput = (e) => {
    const parsed = e.target.value
      .split(",")
      .map((s) => s.trim())
      .filter((s) => s.length > 0)
      .map(Number);
    if (parsed.every((n) => !Number.isNaN(n))) {
      setArray(parsed);
    }
  };

  const runAlgorithm = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const endpoint = mode === "sort" ? "/sort" : "/search";
      const body =
        mode === "sort"
          ? { array, algorithm }
          : { array, algorithm, target: Number(target) };

      const res = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const errBody = await res.json();
        throw new Error(errBody.detail || "Request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const displayArray = result && mode === "sort" ? result.result : array;
  const maxVal = Math.max(...displayArray, 1);

  return (
    <div className="app">
      <header>
        <h1>Algo Visualizer</h1>
        <p className="subtitle">
          Run classic sorting &amp; searching algorithms and see how they perform.
        </p>
      </header>

      <div className="mode-toggle">
        <button
          className={mode === "sort" ? "active" : ""}
          onClick={() => {
            setMode("sort");
            setResult(null);
          }}
        >
          Sort
        </button>
        <button
          className={mode === "search" ? "active" : ""}
          onClick={() => {
            setMode("search");
            setResult(null);
          }}
        >
          Search
        </button>
      </div>

      <div className="controls">
        <div className="control-group">
          <label>Array (comma-separated)</label>
          <input
            type="text"
            value={array.join(", ")}
            onChange={handleArrayInput}
          />
          <button className="secondary" onClick={handleGenerateArray}>
            Randomize
          </button>
        </div>

        <div className="control-group">
          <label>Algorithm</label>
          <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
            {(mode === "sort" ? SORT_ALGORITHMS : SEARCH_ALGORITHMS).map((a) => (
              <option key={a.value} value={a.value}>
                {a.label}
              </option>
            ))}
          </select>
        </div>

        {mode === "search" && (
          <div className="control-group">
            <label>Target value</label>
            <input
              type="number"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            />
          </div>
        )}

        <button className="run-button" onClick={runAlgorithm} disabled={loading}>
          {loading ? "Running..." : "Run"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="bars">
        {displayArray.map((val, i) => (
          <div
            key={i}
            className="bar"
            style={{ height: `${(val / maxVal) * 100}%` }}
            title={val}
          />
        ))}
      </div>

      {result && (
        <div className="metrics">
          <h2>Results</h2>
          <ul>
            <li>
              <strong>Algorithm:</strong> {result.algorithm}
            </li>
            <li>
              <strong>Input size:</strong> {result.input_size}
            </li>
            <li>
              <strong>Comparisons:</strong> {result.comparisons}
            </li>
            {result.swaps !== null && result.swaps !== undefined && (
              <li>
                <strong>Swaps:</strong> {result.swaps}
              </li>
            )}
            <li>
              <strong>Time:</strong> {result.time_ms} ms
            </li>
            {mode === "search" && (
              <li>
                <strong>Found at index:</strong>{" "}
                {result.result === -1 ? "Not found" : result.result}
              </li>
            )}
          </ul>
        </div>
      )}

      <footer>
        <p>
          Built with FastAPI + React ·{" "}
          <a href="https://github.com/" target="_blank" rel="noreferrer">
            View source on GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}
