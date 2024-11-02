const API_URL = "http://127.0.0.1:5000/";

//ENDPOINT PARA OBTENER LA JUGADA DE LA COMPUTADORA
export async function pcMove() {
  const response = await fetch(`${API_URL}computer-move`);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const data = await response.json();
  return data.move;
}

//ENDPOINT PARA OBTENER LA MATRIZ DE DISCOS
export async function getDiscs(matrix) {
  const response = await fetch(`${API_URL}discs`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ matrix }),
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const data = await response.json();
  return data.matrix;
}

//ENDPOINT PARA VER QUIEN EMPIEZA
export async function whoStarts() {
  const response = await fetch(`${API_URL}starter`);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const data = await response.json();
  return data.starter;
}

//FUNCION PARA INICIALIZAR LOS ENDPOINTS
export async function initialize() {
  try {
    await pcMove();
    await getDiscs();
    await whoStarts();
  } catch (error) {
    console.error("Error initializing:", error);
  }
}

window.initialize = initialize;
