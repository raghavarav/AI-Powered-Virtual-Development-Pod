function runAgents() {
    const fileInput = document.getElementById("fileInput");
    const loader = document.getElementById("loader");
    const results = document.getElementById("results");
  
    if (!fileInput.files[0]) {
      alert("Please upload a requirements file.");
      return;
    }
  
    loader.textContent = "Processing...";
  
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
  
    fetch("http://127.0.0.1:8000/run_agents/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        loader.textContent = "";
        results.classList.remove("hidden");
  
        // Display results
        document.getElementById("user_story").innerText = data.user_story || "No data available";
        document.getElementById("design").innerText = data.design || "No data available";
        document.getElementById("code").innerText = data.code || "No data available";
        document.getElementById("test_case").innerText = data.test_case || "No data available";
      })
      .catch((error) => {
        loader.textContent = "Error processing the file.";
        console.error("Error:", error);
      });
  }
  
  function askManager() {
    const managerQuery = document.getElementById("managerQuery").value;
    const managerChatOutput = document.getElementById("managerChatOutput");
  
    if (!managerQuery.trim()) {
      alert("Please enter a query.");
      return;
    }
  
    const formData = new FormData();
    formData.append("query", managerQuery);
  
    fetch("http://127.0.0.1:8000/manager_chat/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        const newMessage = document.createElement("div");
        newMessage.className = "mt-2 text-sm text-gray-300";
        newMessage.textContent = `You: ${managerQuery}\nManager: ${data}`;
        managerChatOutput.appendChild(newMessage);
        document.getElementById("managerQuery").value = "";
        managerChatOutput.scrollTop = managerChatOutput.scrollHeight;
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error sending query.");
      });
  }
  