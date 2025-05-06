let missions = [];
function updateMissions() {
  const list = document.getElementById('missions-list');
  list.innerHTML = '';
  missions.forEach(mission => {
    const li = document.createElement('li');
    li.textContent = mission;
    list.appendChild(li);
  });
}
// If AI provides missions
if (response.missions) {
  missions = response.missions;
  updateMissions();
}


function displayStory(story) {
  document.getElementById('story-text').innerHTML = `<p>${story}</p>`;
}

function displayOptions(options) {
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';
  options.forEach(option => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = option;
    btn.onclick = () => sendOption(option);
    optionsDiv.appendChild(btn);
  });
}

function updateStats(stats) {
  document.getElementById('health-value').textContent = stats.health;
  document.getElementById('mana-value').textContent = stats.mana;
}

function updateInventory(inventory, money) {
  document.getElementById('inventory').textContent = 'Inventory: ' + inventory.join(', ');
  document.getElementById('money').textContent = 'Gold: ' + money;

  // Update popup inventory list
  const list = document.getElementById('inventory-list');
  list.innerHTML = '';
  inventory.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    li.className = 'inventory-item';
    list.appendChild(li);
  });

  bindInventoryClicks();
}

function submitCustomAction() {
  const input = document.getElementById('custom-input');
  const action = input.value;
  if (action) {
    sendOption(action);
    input.value = '';
  }
}

// Inventory popup toggle
function toggleInventory() {
  const popup = document.getElementById('inventory-popup');
  popup.style.display = (popup.style.display === 'block') ? 'none' : 'block';
}

// Send action to backend / test simulation
function sendOption(option) {
  fetch("http://your-server-url/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: option })
  })
  .then(res => res.json())
  .then(data => {
    const response = JSON.parse(data.response);  // parse JSON string from AI

    displayStory(response.story_text);
    displayOptions(response.options);
    updateStats(response.player_stats);
    updateInventory(response.inventory, response.money);

    if (response.missions) {
      missions = response.missions;
      updateMissions();
    }
  })
  .catch(err => console.error(err));
}


// Add toolbar item text to input box
function bindToolbarClicks() {
  const toolbarItems = document.querySelectorAll('.toolbar-item');
  toolbarItems.forEach(item => {
    item.addEventListener('click', () => {
      const input = document.getElementById('custom-input');
      input.value += (input.value ? ' ' : '') + item.textContent;
      input.focus();
    });
  });
}

// Add inventory item text to input box
function bindInventoryClicks() {
  const inventoryItems = document.querySelectorAll('.inventory-item');
  inventoryItems.forEach(item => {
    item.addEventListener('click', () => {
      const input = document.getElementById('custom-input');
      input.value += (input.value ? ' ' : '') + item.textContent;
      input.focus();
    });
  });
}

// Bind on page load
window.onload = () => {
  bindToolbarClicks();
  bindInventoryClicks();
  document.getElementById('add-mission-btn').addEventListener('click', () => {
  const mission = prompt("Enter a new mission:");
  if (mission) {
    missions.push(mission);
    updateMissions();
  }
});

}
