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

      // Eventos botones
      document.getElementById('editarBtn').onclick = () => {
        // Redirigir a la página de entrenamiento con el id para editar
        window.location.href = `/templates/entrenamiento.html?id=${entreno.id}`;
      };

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
      window.location.href = '/templates/entrenamiento.html';
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