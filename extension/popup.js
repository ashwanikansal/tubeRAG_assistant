let messagesDiv = document.getElementById("chatWindow")
let input = document.getElementById("userInput")
let sendBtn = document.getElementById("sendBtn")
let loaderInterval = null

async function getCurrentVideoId() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0].url;
      if (!url) return resolve(null);

      const patterns = [
        /[?&]v=([A-Za-z0-9_-]{11})/,       // typical ?v=ID
        /youtu\.be\/([A-Za-z0-9_-]{11})/,  // youtu.be/ID
        /shorts\/([A-Za-z0-9_-]{11})/,     // shorts/ID
        /embed\/([A-Za-z0-9_-]{11})/       // embed/ID
      ];

      let videoId = null;
      for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) {
          videoId = match[1];
          break;
        }
      }

      console.log("Extracted videoId:", videoId);
      resolve(videoId);
    });
  });
}


// --------- Chat helpers ---------
function addMessage(text, role) {
  const div = document.createElement("div")
  div.className = "message " + role
  div.textContent = text
  messagesDiv.appendChild(div)
  messagesDiv.scrollTop = messagesDiv.scrollHeight
}

function startLoader() {
  stopLoader()
  const loader = document.createElement("div")
  loader.id = "loader"
  loader.className = "message assistant loader"
  loader.textContent = "Thinking"
  messagesDiv.appendChild(loader)

  let dots = 0
  loaderInterval = setInterval(() => {
    dots = (dots + 1) % 4
    loader.textContent = "Thinking" + ".".repeat(dots)
    messagesDiv.scrollTop = messagesDiv.scrollHeight
  }, 500)
}

function stopLoader() {
  const loader = document.getElementById("loader")
  if (loader) loader.remove()
  if (loaderInterval) clearInterval(loaderInterval)
  loaderInterval = null
}

// --------- Storage helpers ---------
async function loadHistory(videoId) {
  if (!videoId) return

  // Make sure messagesDiv exists
  if (!messagesDiv) messagesDiv = document.getElementById("chatWindow")
  if (!messagesDiv) return

  // Clear previous messages
  messagesDiv.innerHTML = ""

  chrome.storage.local.get([videoId], (result) => {
    const history = result[videoId] || []
    console.log("history adding...")
    history.forEach((msg) => addMessage(msg.text, msg.role))
  })
}

function saveMessage(videoId, text, role) {
  chrome.storage.local.get([videoId], (result) => {
    const history = result[videoId] || []
    console.log(result)
    history.push({ text, role, ts: Date.now() })
    chrome.storage.local.set({ [videoId]: history })
  })
}

// --------- Send message to backend ---------
async function sendMessage() {
  const question = input.value.trim()
  if (!question) return

  const videoId = await getCurrentVideoId()
  if (!videoId) return

  addMessage(question, "user")
  saveMessage(videoId, question, "user")
  input.value = ""

  startLoader()

  chrome.runtime.sendMessage(
    { type: "ASK_BACKEND", payload: { videoId, question } },
    (response) => {
      stopLoader()

      if (!response || response.error) {
        const err = "Error: " + (response?.error || "Unknown error")
        addMessage(err, "assistant")
        saveMessage(videoId, err, "assistant")
        return
      }

      addMessage(response.answer, "assistant")
      saveMessage(videoId, response.answer, "assistant")
    }
  )
}

// --------- Event listeners ---------
sendBtn.addEventListener("click", sendMessage)
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage()
})

document.getElementById("closePopup").onclick = () => window.close()
document.getElementById("clearHistoryBtn").onclick = () => {
  chrome.storage.local.clear(() => {
    messagesDiv.innerHTML = ""
    alert("All chat history cleared!")
  })
}

// // Load auto-open settings
// chrome.storage.local.get(["autoOpenChat"], (result) => {
//   document.getElementById("autoOpenCheckbox").checked =
//     result.autoOpenChat || false
// })

// document.getElementById("autoOpenCheckbox").addEventListener("change", (e) => {
//   chrome.storage.local.set({ autoOpenChat: e.target.checked })
// })

// Load chat history on popup open
(async () => {
  const videoId = await getCurrentVideoId()

  if (videoId) {
    console.log("Loading History...")
    await loadHistory(videoId)
  }
})()
