window.addEventListener("DOMContentLoaded", () => {
  const messages = document.getElementById("mensajes");    
  const websocket = new WebSocket("wss://5678-misw4406-tutorial5cqrse-0pton2wd2wp.ws-eu83.gitpod.io/");
  
  websocket.onmessage = ({ data }) => {
    const message = document.createElement("li");
    const content = document.createTextNode(data);
    message.appendChild(content);
    messages.appendChild(message);
  };
});