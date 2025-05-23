const chartDom = document.getElementById('main');
const myChart = echarts.init(chartDom);

document.getElementById('calcForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const data = Array.from(new FormData(this).values()).map(v => Number(v));
  
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
});
