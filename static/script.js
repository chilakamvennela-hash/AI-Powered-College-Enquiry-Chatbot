const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");
const suggestionArea = document.getElementById("suggestionArea");

function currentTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, role, time = currentTime()) {
  const article = document.createElement("article");
  article.className = `message ${role === "user" ? "user-message" : "bot-message"}`;
  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "user" ? "🙂" : "🤖";
  const wrap = document.createElement("div");
  wrap.className = "bubble-wrap";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text; // textContent prevents HTML/script injection.
  const stamp = document.createElement("time");
  stamp.textContent = time;
  wrap.append(bubble, stamp);
  article.append(avatar, wrap);
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}

function showTyping() {
  const article = document.createElement("article");
  article.className = "message bot-message";
  article.id = "typingIndicator";
  article.innerHTML = '<div class="message-avatar">🤖</div><div class="bubble-wrap"><div class="bubble typing"><span></span><span></span><span></span></div></div>';
  messages.appendChild(article);
  messages.scrollTop = messages.scrollHeight;
}
function hideTyping() {
  document.getElementById("typingIndicator")?.remove();
}

async function sendMessage(message) {
  const text = message.trim();
  if (!text || sendButton.disabled) return;
  addMessage(text, "user");
  input.value = "";
  sendButton.disabled = true;
  suggestionArea.hidden = true;
  showTyping();
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    await new Promise(resolve => setTimeout(resolve, 700));
    hideTyping();
    if (!response.ok) throw new Error(data.error || "Unable to send your question.");
    addMessage(data.answer, "bot");
  } catch (error) {
    hideTyping();
    addMessage(error.message || "Sorry, something went wrong. Please try again.", "bot");
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll(".suggestion-chip").forEach(button => {
  button.addEventListener("click", () => sendMessage(button.textContent));
});

clearButton.addEventListener("click", async () => {
  try {
    const response = await fetch("/api/clear", { method: "POST" });
    if (!response.ok) throw new Error("Could not clear chat history.");
    messages.replaceChildren();
    addMessage("Your chat has been cleared. 👋 What would you like to know about the college?", "bot", "Now");
    suggestionArea.hidden = false;
  } catch (error) {
    addMessage(error.message, "bot");
  }
});

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const data = await response.json();
    if (!response.ok || !data.messages?.length) return;
    messages.replaceChildren();
    data.messages.forEach(item => {
      const time = new Date(item.created_at.replace(" ", "T") + "Z").toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
      addMessage(item.message, item.role, time);
    });
    suggestionArea.hidden = true;
  } catch (error) {
    console.warn("Chat history could not be loaded.", error);
  }
}
loadHistory();
