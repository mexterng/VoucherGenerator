// Overlay
const qrCodeDisplay = document.getElementById('qrCodeDisplay');
const overlay = document.getElementById('overlay');
const overlayImage = document.getElementById('overlayImage');

qrCodeDisplay.addEventListener('click', () => {
    overlay.style.display = 'flex'; // Overlay anzeigen
    overlayImage.src = qrCodeDisplay.src; // Das vergrößerte Bild setzen
});

overlay.addEventListener('click', () => {
    overlay.style.display = 'none'; // Overlay verbergen
});



// Select all buttons with class "generateButton"
const buttons = document.getElementsByClassName("generateButton");
            
// Add event listener to each button to trigger code generation
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function() {
        generateCode(this.getAttribute("duration"));
    });
}
// Function to generate the code based on duration and handle the response
function generateCode(duration) {
fetch("/generate_code", { 
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ duration: duration })
})
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            document.getElementById("help").innerText = "Weitere Informationen für die Nutzung."
            document.getElementById("keyDisplay").innerText = "Code für " + duration + ": " + data.key;
            const qrCodeDisplay = document.getElementById("qrCodeDisplay");
            qrCodeDisplay.src = "data:image/png;base64," + data.qr_code;
            document.getElementById("logo").style.display = "none";
            qrCodeDisplay.style.display = "block";
        } else {
            document.getElementById("keyDisplay").innerText = data.message ? data.message : data.error;
            document.getElementById("qrCodeDisplay").style.display = "none";
        }
    })
    .catch(error => {
        console.error("Fehler:", error.message);
        document.getElementById("keyDisplay").innerText = error.message;
        document.getElementById("qrCodeDisplay").style.display = "none";
    });
}

