// Language Switch
function setLanguage(lang) {
  alert("Language switched to: " + lang);
}

// Load JSON Data
async function loadData(file, elementId) {
  try {
    const response = await fetch(`data/${file}`);
    const data = await response.json();
    const list = document.getElementById(elementId);
    list.innerHTML = "";
    data.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      list.appendChild(li);
    });
  } catch (error) {
    console.error("Error loading data:", error);
  }
}

// Initialize Dashboard
window.onload = () => {
  loadData("notifications.json", "notif-list");
  loadData("schedule.json", "schedule-list");
  loadData("fees.json", "fees-list");
  loadData("library.json", "library-list");
};
