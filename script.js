function sendMessage() {
    const chatBox = document.getElementById("chatBox");
    const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value.trim();
  
    if (messageText) {
      // Create a new message bubble
      const newMessage = document.createElement("div");
      newMessage.classList.add("message", "sent");
      newMessage.textContent = messageText;
  
      // Add the message to the chat box and clear the input field
      chatBox.appendChild(newMessage);
      messageInput.value = "";
      chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest message
    }
  }
  