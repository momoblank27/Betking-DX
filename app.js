let game = {
  balance: 0,
  energy: 100,
  maxEnergy: 100,
  tap: 1,
  level: 1,
  passive: 0,
  assets: [
    {name: "DX Mining Rig", level: 0, baseIncome: 1},
    {name: "DX Server Farm", level: 0, baseIncome: 5},
    {name: "DX Exchange", level: 0, baseIncome: 20}
  ]
};

function tap() {
  if (game.energy <= 0) return;

  game.balance += game.tap;
  game.energy--;

  update();
}

function upgradeTap() {
  let cost = game.tap * 50;

  if (game.balance >= cost) {
    game.balance -= cost;
    game.tap++;
  }
}

function upgradeEnergy() {
  let cost = game.maxEnergy * 2;

  if (game.balance >= cost) {
    game.balance -= cost;
    game.maxEnergy += 20;
    game.energy = game.maxEnergy;
  }
}

function buyAsset(i) {
  let asset = game.assets[i];
  let cost = (asset.level + 1) * asset.baseIncome * 20;

  if (game.balance >= cost) {
    game.balance -= cost;
    asset.level++;
  }
}

function calcPassive() {
  let total = 0;
  game.assets.forEach(a => {
    total += a.level * a.baseIncome;
  });
  game.passive = total;
}

function passiveIncome() {
  game.balance += game.passive;
  update();
}

function regen() {
  if (game.energy < game.maxEnergy) {
    game.energy++;
  }
}

function renderCards() {
  let container = document.getElementById("cards");
  container.innerHTML = "";

  game.assets.forEach((a, i) => {
    let cost = (a.level + 1) * a.baseIncome * 20;

    container.innerHTML += `
      <div class="card">
        <h4>${a.name}</h4>
        <p>Level: ${a.level}</p>
        <p>Income: ${a.level * a.baseIncome}/sec</p>
        <button onclick="buyAsset(${i})">Buy (${cost} DX)</button>
      </div>
    `;
  });
}

function update() {
  calcPassive();

  document.getElementById("balance").innerText = game.balance + " DX";
  document.getElementById("energy").innerText = game.energy + "/" + game.maxEnergy;
  document.getElementById("level").innerText = "Level: " + game.level;
  document.getElementById("income").innerText = "Income/sec: " + game.passive;
  document.getElementById("tap").innerText = "Tap: " + game.tap;

  renderCards();
  save();
}

function save() {
  localStorage.setItem("dxEmpire", JSON.stringify(game));
}

function load() {
  let save = localStorage.getItem("dxEmpire");
  if (save) game = JSON.parse(save);
}

function openTG() {
  window.open("https://t.me/DollarXtoken");
}

setInterval(passiveIncome, 1000);
setInterval(regen, 1000);

load();
update();
let tg = window.Telegram.WebApp;
tg.expand();

let user = tg.initDataUnsafe?.user;

if (user) {
  console.log("User:", user.username);
}
function save() {
  localStorage.setItem("dxEmpire", JSON.stringify(game));

  if (tg) {
    tg.sendData(JSON.stringify(game));
  }
}
async function saveServer() {
  if (!user) return;

  await fetch("https://твой-сервер/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: user.id,
      data: game
    })
  });
}let ref = new URLSearchParams(window.location.search).get("startapp");

if (ref) {
  console.log("Referral:", ref);
}