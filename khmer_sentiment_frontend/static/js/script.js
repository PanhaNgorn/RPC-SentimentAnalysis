function getCurrentTime() {
  const now = new Date();
  return now.toTimeString().split(' ')[0];
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chatMessages");
  const terminal = document.getElementById("terminalOutput");

  // Display user message in chat
  const userMsg = document.createElement("div");
  userMsg.className = "message outgoing";
  userMsg.innerHTML = `<div class="message-content">${message}</div>`;
  chatBox.appendChild(userMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Log client-side messages with timestamp
  terminal.textContent += `\nClient:\n`;
  terminal.textContent += `Enter Khmer text to analyze sentiment: ${message}\n`;
  terminal.textContent += `[${getCurrentTime()}] 📩 Sending text for analysis: '${message}'\n`;
  terminal.textContent += `[${getCurrentTime()}] 🔄 Processing sentiment analysis...\n`;

  fetch("/get_sentiment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: message })
  })
  .then(res => res.json())
  .then(data => {
  const botMsg = document.createElement("div");
  botMsg.className = "message incoming";
  botMsg.innerHTML = `<div class="message-content">${data.response}</div>`;
  chatBox.appendChild(botMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Log RPC response
  terminal.textContent += `\n< Response: "${data.response}"`;
  if (data.server_log) {
    terminal.textContent += `\n\nServer:\n${data.server_log}`;
  }
  terminal.scrollTop = terminal.scrollHeight;
  })

  // .catch(err => {
    // terminal.textContent += `\n❌ Error: ${err.message}\n`;
  // });
// 
  input.value = "";
}