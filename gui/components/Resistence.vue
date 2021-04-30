<template>
    <div>
        <div id="myChart">
        </div>
            <div class="demo-split">
            <Split v-model="split1">
                <div slot="left" class="demo-split-pane">
                    <List border=ture size="small">
                    <ListItem>
                        Averaging
                        <InputNumber :min="0" v-model="value1" size="small" @on-change = 'click0'> 
                        </InputNumber>
                    </ListItem>
                    <ListItem>
                        Frequency
                        <InputNumber :min="0" v-model="value2" size="small" @on-change = 'click1'> 
                        </InputNumber>
                    </ListItem>
                    <ListItem>
                        Amplitude
                        <InputNumber :min="0" :step="0.02" v-model="value3" size="small" @on-change = 'click2'> 
                        </InputNumber>
                    </ListItem>
                    <ListItem>
                        Holding Voltage
                        <InputNumber v-model="value4" size="small" @on-change = 'click3'> 
                        </InputNumber>
                    </ListItem>
                    <ListItem>
                         <Select v-model="model1" size="small" style="width:100px">
                            <Option v-for="item in avgList" :value="item.value" :key="item.value" @on-change = 'select0'>{{ item.label }}</Option>
                        </Select>
                    </ListItem>
                </List>
                </div>
                <div slot="right" class="demo-split-pane">
                    <List border=ture size="small">
                        <ListItem>
                            resistence2 : {{resistence2}}
                        </ListItem>

                        <ListItem>
                            averange : {{averange}}    
                        </ListItem>

                        <ListItem>
                            minimum : {{minimum}}    
                        </ListItem>

                        <ListItem>
                            Nagative Peak : {{na_peak}}
                        </ListItem>

                        <ListItem>
                            resistence : {{resistence}}
                        </ListItem>
                    </List>
                </div>
            </Split>
        </div>
            

        <div>
            initialize
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
            avgList: [
                    {
                        value: 'Voltage Clamp',
                        label: 'Voltage Clamp'
                    },
                    {
                        value: 'Current Clamp',
                        label: 'Current Clamp'
                    }
                ],
            model1: '',
            resistence : 0,
            na_peak : 0,
            minimum : 0, 
            averange : 0,
            resistence2 : 0,
            split1: 0.5,
            switch1 : false,
            value1 : 7,
            value2 : 20,
            value3 : 0.02,
            value4 : 0,
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
        setInterval(this.addData, 500);	// 每三秒更新实时数据到折线图
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
                this.yieldRate.push(res.data.resistence2);
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
            axios.post('/resistence', {'code' : 'ch0', val : status}).then(() => {
                console.log(status)
            })
        },
        click0 : function(status) {
            axios.post('/resistence', {'code' : 'c0', val : status}).then(() => {
                console.log(status)
            })
        },
        click1 : function(status) {
            axios.post('/resistence', {'code' : 'c1', val : status}).then(() => {
                console.log(status)
            })
        },
        click2 : function(status) {
            axios.post('/resistence', {'code' : 'c2', val : status}).then(() => {
                console.log(status)
            })
        },
        click3 : function(status) {
            axios.post('/resistence', {'code' : 'c3', val : status}).then(() => {
                console.log(status)
            })
        },
        select0 : function(status) {
            axios.post('/resistence', {'code' : 's0', val : status}).then(() => {
                console.log(status)
            })
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
.demo-split{
        height: 250px;
        border: 1px solid #dcdee2;
    }
.demo-split-pane{
    padding: 10px;
}
</style>