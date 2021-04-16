var myChart = echarts.init(document.getElementById('main'));
$.get(test, function(data){
    myChart.setOption({
        series:[
            {
                name:"数据源",
                type:"pie",
                radius:'55%',
                data:data.data_pie
            }
        ]
    })
}, 'json')