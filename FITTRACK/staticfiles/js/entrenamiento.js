document.addEventListener('DOMContentLoaded', function () {
  const formulario = document.getElementById('formulario-entreno');
  const daysContainer = document.getElementById('daysContainer');
  const monthYearLabel = document.getElementById('monthYear');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');

  if (!formulario || !daysContainer || !monthYearLabel || !prevBtn || !nextBtn) return;

  let currentDate = new Date();
  let currentYear = currentDate.getFullYear();
  let currentMonth = currentDate.getMonth();

  function renderCalendar(year, month) {
    currentYear = year;
    currentMonth = month;
    daysContainer.innerHTML = '';

    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);
    const daysInMonth = lastDayOfMonth.getDate();

    let startDay = firstDayOfMonth.getDay();
    startDay = (startDay === 0) ? 7 : startDay;

    monthYearLabel.textContent = firstDayOfMonth.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

    for (let i = 1; i < startDay; i++) {
      const emptyDiv = document.createElement('div');
      emptyDiv.classList.add('day', 'empty');
      daysContainer.appendChild(emptyDiv);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const dayDiv = document.createElement('div');
      dayDiv.classList.add('day');
      dayDiv.dataset.day = day;
      dayDiv.textContent = day;

      daysContainer.appendChild(dayDiv);
    }

    const entrenamientos = obtenerEntrenamientos();
    marcarEntrenosEnCalendario(entrenamientos);
  }

  function marcarEntrenosEnCalendario(entrenamientos) {
    const days = document.querySelectorAll('#daysContainer .day');
    days.forEach(day => {
      const tag = day.querySelector('.entreno-tag');
      if (tag) tag.remove();
    });

    entrenamientos.forEach(ent => {
      const fechaEnt = new Date(ent.fecha);
      const dayNum = fechaEnt.getDate();

      if (fechaEnt.getFullYear() === currentYear && fechaEnt.getMonth() === currentMonth) {
        const dayDiv = document.querySelector(`#daysContainer .day[data-day='${dayNum}']`);
        if (dayDiv) {
          const tag = document.createElement('div');
          tag.classList.add('entreno-tag');
          tag.textContent = ent.tipo;
          tag.style.cursor = 'pointer';
          tag.style.backgroundColor = '#a9bbd8';
          tag.style.borderRadius = '4px';
          tag.style.padding = '2px 5px';
          tag.style.marginTop = '2px';
          tag.style.fontSize = '0.75rem';
          tag.title = 'Ver detalles';

          tag.addEventListener('click', () => {
            window.location.href = `/templates/detalle.html?id=${ent.id}`;
          });

          dayDiv.appendChild(tag);
        }
      }
    });
  }

  function obtenerEntrenamientos() {
    return JSON.parse(localStorage.getItem('entrenamientos')) || [];
  }

  function guardarEntrenamientos(entrenamientos) {
    localStorage.setItem('entrenamientos', JSON.stringify(entrenamientos));
  }

  formulario.addEventListener('submit', function (e) {
    e.preventDefault();

    const tipo = formulario.tipo.value;
    const fecha = formulario.fecha.value;
    const descripcion = formulario.descripcion.value;
    const id = formulario.dataset.editando || Date.now().toString();

    const nuevoEntreno = { id, tipo, fecha, descripcion };

    let entrenamientos = obtenerEntrenamientos();

    if (formulario.dataset.editando) {
      entrenamientos = entrenamientos.map(ent =>
        ent.id === id ? nuevoEntreno : ent
      );
      delete formulario.dataset.editando;
    } else {
      entrenamientos.push(nuevoEntreno);
    }

    guardarEntrenamientos(entrenamientos);
    formulario.reset();
    renderCalendar(currentYear, currentMonth);
  });

  prevBtn.addEventListener('click', () => {
    if (currentMonth === 0) {
      currentMonth = 11;
      currentYear--;
    } else {
      currentMonth--;
    }
    renderCalendar(currentYear, currentMonth);
  });

  nextBtn.addEventListener('click', () => {
    if (currentMonth === 11) {
      currentMonth = 0;
      currentYear++;
    } else {
      currentMonth++;
    }
    renderCalendar(currentYear, currentMonth);
  });

  renderCalendar(currentYear, currentMonth);
});
