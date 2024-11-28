// Modell-Download-Formular
document.getElementById("model-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const modelName = document.querySelector("input[name='model_name']").value;

    fetch("/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ model_name: modelName })
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert(`Model ${data.model} downloaded successfully!`);
                location.reload(); // Seite neu laden, um Dropdown zu aktualisieren
            } else {
                alert(`Error downloading model: ${data.error}`);
            }
        })
        .catch((error) => console.error("Error:", error));
});

// Nachricht senden
document.getElementById("send-btn").addEventListener("click", function () {
    const input = document.getElementById("chat-input").value;
    const dropdown = document.getElementById("model-dropdown").value;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_input: input,
            model_name: dropdown,
            max_length: 100, // Optional: Kann dynamisch gesetzt werden
            temperature: 0.7 // Optional: Kann dynamisch gesetzt werden
        })
    })
    .then(response => response.json())
    .then(data => {
        const outputDiv = document.getElementById("chat-output");
        if (data.success) {
            const userMessage = `<div class="user-message"><b>User:</b> ${data.response.user_message}</div>`;
            const modelResponse = `<div class="model-response"><b>Model:</b> ${data.response.model_response}</div>`;
            outputDiv.innerHTML += userMessage + modelResponse;
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => console.error("Error:", error));
});

