const chartDom = document.getElementById('main');
const myChart = echarts.init(chartDom);

document.getElementById('calcForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const data = Array.from(formData.values()).map(v => Number(v));
  
  const option = {
    backgroundColor: 'transparent',
    title: {
      text: 'Gráfico',
      left: 'center',
      textStyle: {
        color: '#415a77',
        fontWeight: 'normal',
        fontFamily: "'Roboto', sans-serif"
      }
    },
    radar: {
      indicator: [
        { name: 'Altura (cm)', max: 250 },
        { name: 'Peso (kg)', max: 200 },
        { name: 'Grasa (%)', max: 100 },
        { name: 'Músculo (%)', max: 100 },
        { name: 'Líquidos (%)', max: 100 }
      ],
      shape: 'circle',
      splitNumber: 5,
      axisName: { color: '#4a422a' },
      splitLine: {
        lineStyle: {
          color: [
            'rgba(238, 197, 102, 0.1)',
            'rgba(238, 197, 102, 0.2)',
            'rgba(238, 197, 102, 0.4)',
            'rgba(238, 197, 102, 0.6)',
            'rgba(238, 197, 102, 0.8)',
            'rgba(238, 197, 102, 1)'
          ].reverse()
        }
      },
      axisLine: { lineStyle: { color: 'rgba(220, 207, 136, 1)' } }
    },
    series: [{
      name: 'Rendimiento',
      type: 'radar',
      data: [{ value: data }],
      areaStyle: { opacity: 0.3 },
      lineStyle: { width: 2, color: 'rgba(220, 207, 136, 1)' },
      itemStyle: { color: 'rgba(220, 207, 136, 1)' }
    }]
  };

  myChart.setOption(option);

  // Enviar datos a Django para guardar en BD
  fetch('/guardar_medidas/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      altura: Number(formData.get('Altura')),
      peso: Number(formData.get('Peso')),
      grasa: Number(formData.get('Grasa')),
      musculo: Number(formData.get('Musculo')),
      liquidos: Number(formData.get('Liquidos'))
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('Datos guardados correctamente');
    } else {
      alert('Error al guardar: ' + (data.error || 'Desconocido'));
    }
  })
  .catch(err => alert('Error de red o servidor: ' + err));
});

// Función para obtener el CSRF token (requerido para POST en Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
