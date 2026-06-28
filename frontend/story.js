const { useState } = React

function Story() {
  const [input, setInput] = useState("")
  const [response, setResponse] = useState("")

  async function handleSubmit() {
    if (!input.trim()) return
    try {
      const res = await fetch("http://localhost:8080/v1/content/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer my-api-key"
        },
        body: JSON.stringify({ content: input })
      })
      const data = await res.json()
      setResponse(JSON.stringify(data, null, 2))
    } catch (err) {
      setResponse("Error: " + err.message)
    }
  }

  return (
    <div>
      <label>Enter your prompt for the Bedrock agent:</label>
      <br />
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "400px" }}
      />
      <button onClick={handleSubmit}>Submit</button>
      <pre>{response}</pre>
    </div>
  )
}
