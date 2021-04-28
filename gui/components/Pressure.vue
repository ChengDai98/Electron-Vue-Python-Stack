<template> 
    <div>
        <div id="myChart">        
        
        </div>
        <List border size="small">
            <ListItem>
                初始化<i-switch v-model="switch1" @on-change="change" />
            </ListItem>

            <ListItem>
                <RadioGroup v-model="button7" type="button" button-style="solid" @on-change = "selector">
                    <Radio label="高正">
                    </Radio>
                    <InputNumber :max="15" :min="0" :step="0.5" v-model="inputNumber0" @on-change = 'click0'>
                    </InputNumber>

                    <Radio label="高负">
                    </Radio>
                    <InputNumber :max="0" :min="-5" :step="0.5" v-model="inputNumber1" @on-change = 'click1'>
                    </InputNumber>

                    <Radio label="低正">
                    </Radio>
                    <InputNumber :max="2" :min="0" :step="0.2" v-model="inputNumber2" @on-change = 'click2'>
                    </InputNumber>

                    <Radio label="低负">
                    </Radio>
                    <InputNumber :max="0" :min="-2" :step="0.5" v-model="inputNumber3" @on-change = 'click3'>
                    </InputNumber>

                    <Radio label="大气压">
                    </Radio>
                    <InputNumber v-model="inputNumber4" @on-change = 'click4' readonly>
                    </InputNumber>
                </RadioGroup>
            </ListItem>

            <ListItem><h3> 给定值: {{given}} </h3></ListItem>

            <ListItem><h3> 测量值: {{observed}} </h3></ListItem>
        </List>     
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
            inputNumber0 : 0,
            inputNumber1 : 0,
            inputNumber2 : 0,
            inputNumber3 : 0,
            inputNumber4 : 0,
            button7: '大气压',
            switch1: false,
            value8: 25, 
            date: [],
            yieldRate: [],
            yieldIndex: [],
            given : 0,
            observed : 0,
            // 折线图echarts初始化选项
            echartsOption: {
                legend: {
                    data: ['给定值', '输出值'],
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
                    name: '气压值',
                    nameTextStyle: {
                        fontWeight: 600,
                        fontSize: 18
                    },
                    type: 'value',
                    scale: true,
                    splitLine: {
                      show: false
                    },
                    /* boundaryGap: ['15%', '15%'], */
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
                        name:'给定值',
                        type:'line',
                        smooth: false,
                        data: this.yieldRate,	// 绑定实时数据数组

                        itemStyle:{
                            normal:{
                                color:'#17233d', //折点颜色
                                lineStyle:{
                                    color:'#17233d' //折线颜色
                                }
                            }
                        }
                    },
                    {
                        name:'输出值',
                        type:'line',
                        smooth: false,
                        data: this.yieldIndex,	// 绑定实时数据数组
                        itemStyle:{
                            normal:{
                                color:'#ed4014', //折点颜色
                                lineStyle:{
                                    color:'#ed4014' //折线颜色
                                }
                            }
                        }
                    }
                ],
                backgroundColor: '#dcdee2',
                borderColor:'black',
            }
        }
    },
    mounted () {
        this.myChart = echarts.init(document.getElementById('myChart'), 'light');	// 初始化echarts, theme为light
        this.myChart.setOption(this.echartsOption);	// echarts设置初始化选项
        setInterval(this.addData, 100);
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
            /* if(this.switch1 == false) return */

            if(this.switch1 == true) {
                axios.get('/pressure').then(res => {
                  this.yieldRate.push(this.given =  res.data.given);
                  if(this.yieldRate.length > 100) 
                    this.yieldRate.shift()
                  // console.log(this.yieldRate.length)
      
                  this.yieldIndex.push(this.observed = res.data.observed);
                  if(this.yieldIndex.length > 100) 
                    this.yieldIndex.shift()
                  // console.log(this.yieldIndex.length)
      
                  this.date.push(this.getTime(new Date().getTime() / 1000));
                  if(this.date.length > 100) 
                    this.date.shift()
                  // console.log(this.date.length)
                  // 重新将数组赋值给echarts选项
                  this.echartsOption.xAxis.data = this.date;
                  this.echartsOption.series[0].data = this.yieldRate;
                  this.echartsOption.series[1].data = this.yieldIndex;
                  this.myChart.setOption(this.echartsOption);
                })
            }
        },
        change : function(status) {
            console.log(status)
            this.$Message.info('switch status：' + status);
            axios.post('/pressure', {'typeCode' : 0, 'status' : status}).then(() => {
                console.log("send status")
                // add
            })
        },
        selector : function(status) {
            console.log(status)
            if(this.button7 == '大气压') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 4, 'val' : this.inputNumber4}).then(() => {
                    console.log("send values")
                })
            }
            if(this.button7 == '低负') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 3, 'val' : this.inputNumber3}).then(() => {
                    console.log("send values")
                })
            }
            if(this.button7 == '低正') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 2, 'val' : this.inputNumber2}).then(() => {
                    console.log("send values")
                })
            }
            if(this.button7 == '高负') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 1, 'val' : this.inputNumber1}).then(() => {
                    console.log("send values")
                })
            }
            if(this.button7 == '高正') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 0, 'val' : this.inputNumber0}).then(() => {
                    console.log("send values")
                })
            }
        },
        click0 : function(status) {
            this.inputNumber0 = status;
            console.log(this.inputNumber0, status)
            if(this.button7 == '高正') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 0, 'val' : this.inputNumber0}).then(() => {
                    console.log("send values")
                })
            }
        },
        click1 : function(status) {
            this.inputNumber1 = status;
            console.log(this.inputNumber1, status)
            if(this.button7 == '高负') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 1, 'val' : this.inputNumber1}).then(() => {
                    console.log("send values")
                })
            }
        },
        click2 : function(status) {
            this.inputNumber2 = status;
            console.log(this.inputNumber2, status)
            if(this.button7 == '低正') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 2, 'val' : this.inputNumber2}).then(() => {
                    console.log("send values")
                })
            }
        },
        click3 : function(status) {
            this.inputNumber3 = status;
            console.log(this.inputNumber3, status)
            if(this.button7 == '低负') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 3, 'val' : this.inputNumber3}).then(() => {
                    console.log("send values")
                })
            }
        },
        click4 : function(status) {
            this.inputNumber4 = status;
            console.log(this.inputNumber4, status)
            if(this.button7 == '大气压') {
                axios.post('/pressure', {'typeCode' : 1, 'num' : 3, 'val' : this.inputNumber4}).then(() => {
                    console.log("send values")
                })
            }
        }
    }
}
</script>

<style>
#myChart{
  width: 100%;
  height: 400px;
  margin: 0 auto;
}
</style>