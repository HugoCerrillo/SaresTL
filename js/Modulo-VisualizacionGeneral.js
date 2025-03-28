const table = document.getElementById("MiembrosGeneral");
const modal = document.getElementById("modal");
const modalEmergente = document.getElementById("emergenteModal");
const inputs = document.querySelectorAll("input");
const inputsEmergentes = document.getElementById("claveEmergente");
const form = document.querySelector("#respuesta");
const nuevo = document.getElementById("#nuevo");
const guar = document.getElementById("guardar");
const envia = document.getElementById("enviarFormulario");
const elimina = document.getElementById("eliminarButton");

let count = 0;

window.addEventListener("click", (e) => {
  if (e.target.matches("#editarButton")) {
    let data = e.target.parentElement.parentElement.children;
    fillData(data);
    modal.classList.toggle("translate");
    try {
      envia.style.display = "block";
      guar.style.display = "none";
      elimina.style.display = "none";
    } catch (error) {

    }

  }

  if (e.target.matches("#cerrar")) {
    modal.classList.toggle("translate");
    count = 0;
  }

  if (e.target.matches("#nuevo")) {
    modal.classList.toggle("translate");
    try {
      envia.style.display = "none";
      guar.style.display = "block";
    } catch (error) {

    }

  }
  if (e.target.matches("#deleteButton")) {
    let data = e.target.parentElement.parentElement.children;
    fillData(data);
    modal.classList.toggle("translate");
    try {
      envia.style.display = "none";
      guar.style.display = "none";
      elimina.style.display = "block";
    } catch (error) {

    }

  }
});


const fillData = (data) => {
  for (let index of inputs) {
    index.value = data[count].textContent;
    console.log(index);
    count += 1;
  }
};
