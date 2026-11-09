/* Funciones de gráficas con Chart.js (Integrantes 4 y 5).
   Los datos llegan desde Django con el filtro json_script. */

const HP_COLORES = ["#4338ca", "#0d8f82", "#b9770e", "#c2414b", "#7c74e8", "#5fb8ad"];
const HP_MONEDA = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN", maximumFractionDigits: 0 });

Chart.defaults.font.family = "Figtree, system-ui, sans-serif";
Chart.defaults.color = "#646a82";

function sinDatos(canvas) {
  const ctx = canvas.getContext("2d");
  ctx.font = "14px Figtree, sans-serif";
  ctx.fillStyle = "#646a82";
  ctx.textAlign = "center";
  ctx.fillText("Sin datos en este periodo", canvas.width / 2, 60);
}

function graficaBarras(id, datos, etiqueta, horizontal = false) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  if (!datos.valores.length) return sinDatos(canvas);
  new Chart(canvas, {
    type: "bar",
    data: {
      labels: datos.etiquetas,
      datasets: [{ label: etiqueta, data: datos.valores, backgroundColor: "#4338ca", borderRadius: 4, maxBarThickness: 46 }],
    },
    options: {
      indexAxis: horizontal ? "y" : "x",
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: (c) => HP_MONEDA.format(c.raw) } } },
      scales: {
        [horizontal ? "x" : "y"]: { beginAtZero: true, ticks: { callback: (v) => HP_MONEDA.format(v) }, grid: { color: "#eceef4" } },
        [horizontal ? "y" : "x"]: { grid: { display: false } },
      },
    },
  });
}

function graficaDona(id, datos) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  if (!datos.valores.some((v) => v > 0)) return sinDatos(canvas);
  new Chart(canvas, {
    type: "doughnut",
    data: { labels: datos.etiquetas, datasets: [{ data: datos.valores, backgroundColor: ["#b9770e", "#0d8f82", "#4338ca", "#c2414b"], borderWidth: 2 }] },
    options: { cutout: "62%", plugins: { legend: { position: "bottom" } } },
  });
}
