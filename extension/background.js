const BACKEND_BASE_URL = "http://localhost:8000";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "ASK_BACKEND") {
    (async () => {
      try {
        const { videoId, question } = msg.payload;

        const res = await fetch(`${BACKEND_BASE_URL}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ video_id_or_url: videoId, question })
        });

        const data = await res.json();

        if (data.detail) {
          sendResponse({ error: data.detail });
        } else {
          sendResponse({ answer: data.answer, video_id: data.video_id });
        }
      } catch (err) {
        console.error(err);
        sendResponse({ error: err.message || "Request failed" });
      }
    })();

    return true; // keep channel alive
  }
});
