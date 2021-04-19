document.write("<script language='javascript' src=\"https://cdn.staticfile.org/echarts/4.3.0/echarts.min.js\"></script>")
// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));
// 指定图表的配置项和数据
var option = {
        title:{
            x:"center",
            text:"系统进程唤醒延时记录"
        },
        xAxis: {
            name: '进程',
            type: 'category',
            data: [],
        axisLabel: {
                interval:0,      //坐标轴刻度标签的显示间隔(在类目轴中有效) 0:显示所有  1：隔一个显示一个 :3：隔三个显示一个...
                rotate:-20    //标签倾斜的角度，显示不全时可以通过旋转防止标签重叠（-90到90）
            }
        },
        yAxis: {
            name: '延时:毫秒',
            type: 'value'
        },
        series: [{
            data: [],
            type: 'bar',
            itemStyle: {
            normal: {
               label: {
                   show: true,      //开启显示
                   position: 'top', //在上方显示
                   textStyle: {     //数值样式
                       color: 'black',
                       fontSize: 16
                   }
               }
           }
       }
        }]
    };
// 使用ajax 解析json。
myChart.setOption(option);
function get_data() {
            $.ajax({
                url: "/admin/wakeup_lantency",
                success: function (data) {
                    option.xAxis.data=data.process_name;
                    option.series[0].data=data.lantency;
                    myChart.setOption(option);
                }
            })
        }
setInterval(get_data, 3000)