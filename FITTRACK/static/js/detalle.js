function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

function mostrarDetalle(entreno) {
  const contenedor = document.getElementById('detalle-entreno');
  const btnGroup = document.getElementById('btnGroup');

  if (!entreno) {
    contenedor.innerHTML = '<p>Entrenamiento no encontrado.</p>';
    btnGroup.style.display = 'none';
    return;
  }

  contenedor.innerHTML = `
    <p><strong>Tipo:</strong> ${entreno.tipo}</p>
    <p><strong>Fecha:</strong> ${entreno.fecha}</p>
    <p><strong>Descripción:</strong> ${entreno.descripcion}</p>
  `;

  btnGroup.style.display = 'flex';

  // Botón editar
  document.getElementById('editarBtn').onclick = () => {
    // Redirige correctamente a la URL definida por Django
    window.location.href = `/registro_del_entrenamiento/?id=${entreno.id}`;
  };

  // Botón eliminar
  document.getElementById('eliminarBtn').onclick = () => {
    if (confirm('¿Estás seguro de que deseas eliminar este entrenamiento?')) {
      eliminarEntrenamiento(entreno.id);
    }
  };
}

function eliminarEntrenamiento(id) {
  let entrenamientos = JSON.parse(localStorage.getItem('entrenamientos')) || [];
  entrenamientos = entrenamientos.filter(ent => ent.id !== id);
  localStorage.setItem('entrenamientos', JSON.stringify(entrenamientos));
  alert('Entrenamiento eliminado.');
  // Redirige correctamente
  window.location.href = '/registro_del_entrenamiento/';
}

document.addEventListener('DOMContentLoaded', () => {
  const id = getQueryParam('id');
  if (!id) {
    mostrarDetalle(null);
    return;
  }
  const entrenamientos = JSON.parse(localStorage.getItem('entrenamientos')) || [];
  const entreno = entrenamientos.find(e => e.id === id);
  mostrarDetalle(entreno);
});
