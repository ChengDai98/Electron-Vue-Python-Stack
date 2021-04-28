<template>
    <div>
        <div id="myChart">

        </div>

            <List header="Header" footer="Footer" border size="small">
                <ListItem>
                    Averaging
                    <InputNumber :min="0" v-model="value1" size="small"> 
                    </InputNumber>
                </ListItem>
                <ListItem>
                    Frequency
                    <InputNumber :min="0" v-model="value2" size="small"> 
                    </InputNumber>
                </ListItem>
                <ListItem>
                    Amplitude
                    <InputNumber :min="0" :step="0.02" v-model="value3" size="small"> 
                    </InputNumber>
                </ListItem>
            </List>

        <div>
            <i-switch v-model="switch1" @on-change="change" />
        </div>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from '../axios';
export default {
    name: 'DynamicLineChart',
    data () {
        return {
        	// 实时数据数组
            switch1 : false,
            value1 : 7,
            value2 : 20,
            value3 : 0.02,
            date: [],
            yieldRate: [],
            //yieldIndex: [],
            // 折线图echarts初始化选项
            echartsOption: {
                legend: {
                    data: ['电阻'],
                },
                xAxis: {
                    name: '时间',
                    nameTextStyle: {
                        fontWeight: 600,
                        fontSize: 18
                    },
                    type: 'category',
                    boundaryGap: false,
                    data: this.date,	// 绑定实时数据数组
                },
                yAxis: {
                    name: '电阻',
                    nameTextStyle: {
                        fontWeight: 600,
                        fontSize: 18
                    },
                    type: 'value',
                    scale: true,
                    axisLabel: {
                        interval: 'auto',
                        formatter: '{value}'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                },
                series: [
                    {
                        name:'电阻',
                        type:'line',
                        smooth: false,
                        data: this.yieldRate,	// 绑定实时数据数组
                    }
                ]
            }
        }
    },
    mounted () {
        this.myChart = echarts.init(document.getElementById('myChart'), 'light');	// 初始化echarts, theme为light
        this.myChart.setOption(this.echartsOption);	// echarts设置初始化选项
        setInterval(this.addData, 1000);	// 每三秒更新实时数据到折线图
    },
    methods: {
    	// 获取当前时间
        getTime : function() {	
            var ts = arguments[0] || 0;
            var t, h, i, s;
            t = ts ? new Date(ts * 1000) : new Date();
            h = t.getHours();
            i = t.getMinutes();
            s = t.getSeconds();
            // 定义时间格式
            return (h < 10 ? '0' + h : h) + ':' + (i < 10 ? '0' + i : i) + ':' + (s < 10 ? '0' + s : s);
        },
        // 添加实时数据
        addData : function() {
        	// 从接口获取数据并添加到数组
            if (this.switch1 == false) return
            axios.get('/resistence').then((res) => {
                this.yieldRate.push(res.data.val1);
                this.date.push(this.getTime(Math.round(new Date().getTime() / 1000)));
                // 重新将数组赋值给echarts选项
                this.echartsOption.xAxis.data = this.date;
                this.echartsOption.series[0].data = this.yieldRate;
                this.myChart.setOption(this.echartsOption);
            });
        },
        change : function(status) {
            console.log(status)
            this.$Message.info('switch status：' + status);
            axios.post('/resistence', {}).then()
        },
    }
}
</script>

<style>
#myChart{
  width: 100%;
  height: 500px;
  margin: 0 auto;
}
</style>