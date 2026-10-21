const form = document.querySelector("#check-form");
const messageInput = document.querySelector("#message");
const count = document.querySelector("#char-count");
const button = document.querySelector("#check-button");
const result = document.querySelector("#result");
const error = document.querySelector("#error");

messageInput.addEventListener("input", () => {
  count.textContent = `${messageInput.value.length.toLocaleString()} / 10,000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.hidden = true;
  error.hidden = true;
  button.disabled = true;
  button.textContent = "Checking…";

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: messageInput.value }),
    });
    const data = await response.json();
    if (!response.ok) {
      const detail = typeof data.detail === "string" ? data.detail : "Please enter a valid message.";
      throw new Error(detail);
    }

    const titles = {
      high: "Several strong warning signs",
      suspicious: "Some warning signs found",
      low: "Few warning signs found",
    };
    result.dataset.risk = data.risk;
    document.querySelector("#risk-title").textContent = titles[data.risk] ?? "Check complete";
    document.querySelector("#score").textContent = `Risk score: ${data.score}/100`;
    document.querySelector("#disclaimer").textContent = data.disclaimer;
    const signalList = document.querySelector("#signals");
    signalList.replaceChildren();
    if (data.signals.length === 0) {
      const item = document.createElement("li");
      item.textContent = "No common warning signs were detected. This does not prove the message is safe.";
      signalList.append(item);
    } else {
      for (const signal of data.signals) {
        const item = document.createElement("li");
        item.textContent = signal;
        signalList.append(item);
      }
    }
    result.hidden = false;
  } catch (requestError) {
    error.textContent = requestError instanceof Error
      ? requestError.message
      : "Unable to check the message. Please try again.";
    error.hidden = false;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Check message <span aria-hidden="true">→</span>';
  }
});
