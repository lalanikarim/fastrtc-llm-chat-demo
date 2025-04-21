document.addEventListener("DOMContentLoaded", function () {
  let dataArray_output;
  let animationId_input, animationId_output;
  let chatHistory = [];

  const startButton = document.getElementById("start-button");
  const chatMessages = document.getElementById("chat-messages");
  const typingIndicator = document.getElementById("typing-indicator");

  let client = FastRTCClient({
    additional_inputs_url: "/input_hook",
    additional_outputs_url: "/outputs",
  });
  client.onConnecting(function () {
    startButton.innerHTML = `
                <div class="icon-with-spinner">
                    <div class="spinner"></div>
                    <span>Connecting...</span>
                </div>
            `;
  });
  client.onConnected(function () {
    startButton.innerHTML = `
                <div class="pulse-container">
                    <div class="pulse-circle"></div>
                    <span>Stop</span>
                </div>
            `;
  });
  client.onReadyToConnect(function () {
    startButton.innerHTML = "Start";
  });

  client.setShowErrorCallback(function (message) {
    const toast = document.getElementById("error-toast");
    toast.textContent = message;
    toast.className = "toast error";
    toast.style.display = "block";
  });
  client.onErrorReceived(function (error) {
    showError(error);
  });
  client.setClearErrorCallback(function () {
    // Hide toast after 5 seconds
    setTimeout(() => {
      toast.style.display = "none";
    }, 5000);
  });
  client.onPauseDetectedReceived(function () {
    typingIndicator.style.display = "block";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  });
  client.onResponseStarting(function () {
    typingIndicator.style.display = "none";
  });
  client.onAdditionalOutputs(function (event) {
    const eventJson = JSON.parse(event.data);
    addMessage(eventJson.role, eventJson.content);
  });
  client.getAdditionalInputs(function () {
    return {
      chatbot: chatHistory,
    };
  });

  function updateAudioLevel() {
    const audioLevel = client.getInputAudioLevel();

    const pulseCircle = document.querySelector(".pulse-circle");
    if (pulseCircle) {
      pulseCircle.style.setProperty("--audio-level", 1 + audioLevel);
    }

    animationId_input = requestAnimationFrame(updateAudioLevel);
  }

  client.setUpdateAudioLevelCallback(updateAudioLevel);

  function addMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", role);
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    window.scrollTo(0, document.body.scrollHeight);
    chatHistory.push({ role, content });
  }

  // Add this after other const declarations
  const boxContainer = document.querySelector(".box-container");
  const numBars = 32;
  for (let i = 0; i < numBars; i++) {
    const box = document.createElement("div");
    box.className = "box";
    boxContainer.appendChild(box);
  }

  // Replace the draw function with updateVisualization
  function updateVisualization() {
    animationId_output = requestAnimationFrame(updateVisualization);

    dataArray_output = client.getDataArrayOutput();
    // analyser_output.getByteFrequencyData(dataArray_output);
    const bars = document.querySelectorAll(".box");

    for (let i = 0; i < bars.length; i++) {
      const barHeight = (dataArray_output[i] / 255) * 2;
      bars[i].style.transform = `scaleY(${Math.max(0.1, barHeight)})`;
    }
  }

  client.setUpdateVisualizationCallback(updateVisualization);

  startButton.addEventListener("click", () => {
    if (startButton.textContent === "Start") {
      client.start();
    } else {
      client.stop();
    }
  });
});
