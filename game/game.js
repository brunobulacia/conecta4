//TRAYENDO LOS ENDPOINTS DE LA API
import { initialize, getDiscs, pcMove } from "../routes/api.routes.js";
window.addEventListener("load", initialize);

const config = {
  type: Phaser.AUTO,
  width: 600,
  height: 650,
  parent: "game-container",
  scene: {
    preload: preload,
    create: create,
    update: update,
  },
};

let game = new Phaser.Game(config);
let board;
let currentPlayer = "rojo";
let discs = [];
const rows = 6;
const cols = 7;
let floatingDisc;
let floatingCol = Math.floor(Math.random() * cols);

function preload() {
  //Sirve para cargar imagenes o recursos
}

function create() {
  this.cameras.main.setBackgroundColor(0x20242f);
  createBoard(this);
  createFloatingDisc(this);
  this.input.keyboard.on("keydown-LEFT", moveDiscLeft, this);
  this.input.keyboard.on("keydown-RIGHT", moveDiscRight, this);
  this.input.keyboard.on("keydown-SPACE", dropFloatingDisc, this);
}

function createBoard(scene) {
  board = scene.add.graphics();
  board.fillStyle(0x525d65, 1);

  const offsetX = (scene.sys.canvas.width - cols * 77) / 2;
  const offsetY = (scene.sys.canvas.height - rows * 77) / 2;

  for (let i = 0; i < rows; i++) {
    discs[i] = [];
    for (let j = 0; j < cols; j++) {
      discs[i][j] = null;
      board.fillCircle(j * 77 + 37.5 + offsetX, i * 77 + 37.5 + offsetY, 35);
      board.lineStyle(5, 0x000000, 1);
      board.strokeCircle(j * 77 + 37.5 + offsetX, i * 77 + 37.5 + offsetY, 35);
    }
  }
}

function createFloatingDisc(scene) {
  console.log(floatingCol);
  let color = currentPlayer === "rojo" ? 0xc23616 : 0x1e3799;
  const offsetX = (scene.sys.canvas.width - cols * 77) / 2;
  const offsetY = (scene.sys.canvas.height - rows * 77) / 2;

  floatingDisc = scene.add.circle(
    floatingCol * 77 + 37.5 + offsetX,
    offsetY - 38,
    35,
    color
  );
  floatingDisc.setStrokeStyle(5, 0x000000);
}

function moveDiscLeft() {
  if (floatingCol > 0) {
    floatingCol--;
    const offsetX = (this.sys.canvas.width - cols * 77) / 2;
    floatingDisc.x = floatingCol * 77 + 37.5 + offsetX;
  }
  console.log(floatingCol);
}

function moveDiscRight() {
  if (floatingCol < cols - 1) {
    floatingCol++;
    const offsetX = (this.sys.canvas.width - cols * 77) / 2;
    floatingDisc.x = floatingCol * 77 + 37.5 + offsetX;
  }
  console.log(floatingCol);
}

function dropFloatingDisc() {
  if (discs[0][floatingCol] !== null) {
    this.input.keyboard.enabled = true;
    return;
  }
  this.input.keyboard.enabled = false;
  const offsetX = (this.sys.canvas.width - cols * 77) / 2;
  const offsetY = (this.sys.canvas.height - rows * 77) / 2;
  for (let row = rows - 1; row >= 0; row--) {
    if (discs[row][floatingCol] === null) {
      let endY = row * 77 + 37.5 + offsetY;
      this.tweens.add({
        targets: floatingDisc,
        y: endY,
        duration: 500,
        ease: "Bounce.easeOut",
        onComplete: () => {
          discs[row][floatingCol] = currentPlayer;
          sendDiscs();
          if (checkWin(row, floatingCol)) {
            this.add.text(150, 30, `Jugador ${currentPlayer} gana!`, {
              fontSize: "40px",
              fill: "#fff",
              fontFamily: "Roboto",
            });
          } else {
            currentPlayer = currentPlayer === "rojo" ? "azul" : "rojo";
            createFloatingDisc(this);
            if (currentPlayer === "azul") {
              computerMove(this);
            } else {
              this.input.keyboard.enabled = true;
            }
          }
        },
      });
      break;
    }
  }
}

async function sendDiscs() {
  try {
    let matrix = await getDiscs(discs);
    console.log(matrix);
  } catch (error) {
    console.error("Error in getDiscs:", error);
  }
}

async function computerMove(scene) {
  try {
    let col = await pcMove();
    console.log("Move: " + col);
    while (discs[0][col] !== null) {
      col = await pcMove();
    }
    floatingCol = col;
    const offsetX = (scene.sys.canvas.width - cols * 77) / 2;
    floatingDisc.x = floatingCol * 77 + 37.5 + offsetX;
    dropFloatingDisc.call(scene);
  } catch (error) {
    console.error("Error in computerMove:", error);
  }
}

function update() {
  // Lógica adicional del juego
}

function checkWin(row, col) {
  return (
    checkDirection(row, col, 1, 0) ||
    checkDirection(row, col, 0, 1) ||
    checkDirection(row, col, 1, 1) ||
    checkDirection(row, col, 1, -1)
  );
}

function checkDirection(row, col, rowDir, colDir) {
  let count = 0;
  let player = discs[row][col];

  for (let i = -3; i <= 3; i++) {
    let r = row + i * rowDir;
    let c = col + i * colDir;
    if (r >= 0 && r < rows && c >= 0 && c < cols && discs[r][c] === player) {
      count++;
      if (count === 4) {
        return true;
      }
    } else {
      count = 0;
    }
  }
  return false;
}

function placeDisc(pointer) {}
