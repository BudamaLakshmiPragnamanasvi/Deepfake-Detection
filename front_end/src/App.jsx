import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState("Loading...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/data")
      .then(res => res.json())
      .then(res => setData(res.data))
      .catch(() => setData("Error connecting ❌"));
  }, []);

  return (
    <div>
      <h1>Deepfake Detection</h1>
      <p>{data}</p>
    </div>
  );
}

export default App;