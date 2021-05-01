<template>
    <div class="demo-split">
        <Split v-model="split3">
            <div slot="left" class="demo-split-pane no-padding">
                <Split v-model="split4" mode="vertical">
                    <div slot="top" class="demo-split-pane">
                        <List border=ture size="small">
                            <ListItem>
                                设定步数<Input-number :max="10" :min="1" v-model="step_num" @on-change="set_step"></Input-number>
                            </ListItem>
                            <ListItem>
                                <Button @click.native="upward">上移</Button>
                            </ListItem>
                            <ListItem>
                                <Button type="primary" shape="circle"  @click.native="stop">停止移动</Button>
                            </ListItem>
                            <ListItem>
                                <Button  @click.native="downward">下移</Button>
                            </ListItem>
                        </List>
                    </div>
                    <div slot="bottom" class="demo-split-pane">
                        <List border=ture size="small">
                            <ListItem>
                                <Button @click.native="continous_upward">持续上移</Button>
                            </ListItem>
                            <ListItem>
                                <Button type="primary" shape="circle" @click.native="stop">停止移动</Button>
                            </ListItem>
                            <ListItem>
                                <Button @click.native="continous_downward">持续下移</Button>
                            </ListItem>
                        </List>
                    </div>
                </Split>
            </div>
            <div slot="right" class="demo-split-pane">
                <List border=ture size="small">
                    <ListItem>
                        设置z加速度：<Input-number :max="100" :min="4" v-model="zacc" @on-change="set_acc_z"></Input-number><br>
                    </ListItem>
                    <ListItem>
                        设置z速度：<Input-number :max="10" :min="1" v-model="zv" @on-change="set_v_z"></Input-number><br>
                    </ListItem>
                    <ListItem>
                        输出Z轴位置：{{z_pos}}<br>
                    </ListItem>
                    <ListItem>
                        设定步长: <Input-number :max="10" :min="1" v-model="step_length" @on-change="set_step_length"></Input-number><br>
                    </ListItem>
                    <ListItem>
                        当前步长：{{step_length}}<br>
                    </ListItem>
                    <ListItem>
                        <Button @click.native="reset_pos">返回零位</Button><br>
                    </ListItem>
                    <ListItem>
                        <Button @click.native="force_stop">强制停止移动</Button>
                    </ListItem>
                </List>
            </div>
        </Split>
    </div>
</template>
<script>
    import axios from '../axios';
    export default {
        data () {
            return {
                step_num : 0,
                zacc:20,
                zv:0,
                step_length:0,
                split3: 0.5,
                split4: 0.5,
            }
        },
        methods: {
            set_step : function(status) {
                this.step_num = status
                console.log(status)
            },
            upward : function(status) {
                console.log("U ", this.step_length)
                axios.post('/microscope', {'command' : String("U " + this.step_length)}).then(() => {
                console.log(status)
            })
            },
            downward : function(status) {
                console.log("D ", this.step_length)
                axios.post('/microscope', {'command' : String("D " + this.step_length)}).then(() => {})
                console.log(status)
            },
            stop : function(status) {
                console.log("I")
                axios.post('/microscope', {'command' : String("I")}).then(() => {})
                console.log(status)
            },
            continous_upward : function(status) {
                console.log("U ", this.step_length)
                axios.post('/microscope', {'command' : String("U " + this.step_length)}).then(() => {})
                console.log(status)
            },
            continous_downward : function(status) {
                console.log("D ", this.step_length)
                axios.post('/microscope', {'command' : String("D " + this.step_length)}).then(() => {})
            },
            set_acc_z : function(status) {
                console.log("SAZ ", status)
                axios.post('/microscope', {'command' : String("SAZ " + status)}).then(() => {})
            },
            set_v_z : function(status) {
                console.log("SMZ ", status)
                axios.post('/microscope', {'command' : String("SMZ " + status)}).then(() => {})
            },
            set_step_length : function(status) {
                console.log("C ", status)
                axios.post('/microscope', {'command' : String("C " + status)}).then(() => {})
            },
            reset_pos : function(status) {
                console.log("M")
                axios.post('/microscope', {'command' : String("M")}).then(() => {})
            },
            force_stop : function(status) {
                console.log("K")
                axios.post('/microscope', {'command' : String("K")}).then(() => {})
            }
        }
    }
</script>
<style>
    .demo-split{
        height: 1000px;
        border: 1px solid #45532b;
    }
    .demo-split-pane{
        padding: 20px;
    }
    .demo-split-pane.no-padding{
        height: 600px;
        padding: 0;
    }
</style>