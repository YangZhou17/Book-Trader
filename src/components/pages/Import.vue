<!-- Import Page -->
<template>
    <!-- Header Element -->
    <el-header>
        <Breadcrumb></Breadcrumb>
    </el-header>
    <el-divider />

    <!-- Dataset Information -->
    <div class="item_heading" id="new_info">Creation Information</div>
    <p class="text_left1" style="left:240px;top:170px">Shelf ID</p>
    <p class="text_left1" style="left:240px;top:210px">Remarks</p>
    <el-row id="memo_row">
        <p id="memo_info" class="text_left1">{{memo_text}}</p>
        <button id="change_memo" @click="changing_memo"></button>
    </el-row>
    <input id="memo_input" type="text" v-model="memo_text">
    <div id="two_btns">
        <el-button id="memo_acknowlege" @click="acknowleging_memo">Confirm</el-button>
        <el-button id="memo_cancel" @click="canceling_memo">Cancel</el-button>
    </div>
    <p class="text_left1" style="left:240px;top:250px">Historical Data</p>
    <p class="text_left2" style="left:350px;top:171px" id="data_id">123456</p>
    <p class="text_left2" style="left:350px;top:250px">No Import Records</p>
    <p class="text_right2" style="left:600px;top:170px">Version</p>
    <p class="text_right2" style="left:690px;top:171px">V1</p>
    <p class="item_heading" id="mark_info">Information</p>
    <p class="text_left1" style="left:240px;top:340px">Type</p>
    <p class="text_left1" style="left:240px;top:380px">Total Data</p>
    <p class="text_left1" style="left:240px;top:420px"># of Labels</p>
    <p class="text_left1" style="left:240px;top:460px">Size</p>
    <p class="text_left2" style="left:350px;top:340px" id="label_type">tmp</p>
    <p class="text_left2" style="left:350px;top:381px">0</p>
    <p class="text_left2" style="left:350px;top:421px">0</p>
    <p class="text_left2" style="left:350px;top:461px">0M</p>
    <p class="text_right1" style="left:600px;top:343px">Tmp</p>
    <p class="text_right1" style="left:600px;top:383px">Tmp</p>
    <p class="text_right1" style="left:600px;top:423px">Tmp</p>
    <p class="text_right2" style="left:690px;top:344px" id="label_module">tmp</p>
    <p class="text_right2" style="left:690px;top:385px">0</p>
    <p class="text_right2" style="left:690px;top:425px">0</p>
    <p class="item_heading" id="data_cle">PLACEHOLDER</p>
    <p class="text_left1" style="left:240px;top:550px">placeholder</p>
    <p class="item_heading" id="data_enhan">PLACEHOLDER</p>
    <p class="text_left1" style="left:240px;top:640px">placeholder</p>
    <p class="item_heading" id="data_intro">Import Data</p>
    <p class="text_left1" style="left:240px;top:730px">Data Annotation Status</p>
    <form id="markingInfo_radio_group">
        <input type="radio" value="no_marking_info" name="marking_info">No Annotation Information&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input type="radio" value="_marking_info" name="marking_info">Has Annotation Information
    </form>

    <el-button id="submit_button" @click="back_index" type="primary">Confirm and Return</el-button>
</template>

<script>
import { reactive, ref } from "vue";
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        name: "MainTwo",
        components: {
            Breadcrumb,
        },
        data(){
            return{
                picUpVisible: false,
                picUpZipVisible:false,
                textUpZipVisible:false,
                textUpTxtVisible:false,
                textUpExcelVisible:false,
                videoUpVisible:false,
                videoUpZipVisible:false,
                audioUpVisible:false,
                audioUpZipVisible:false,
                fileList: [],
                file: {},
                MessageInfo: reactive({}),
                memo_text:ref(''),
                pre_memo:ref(''),
                split_word:ref('')
            };
        },
        created(){
            this.get_data();
        },
        methods:{
            // Get Data
            get_data(){
                let that = this;
                return fetch("/api/getone").then((res) => res.json())
                .then((j)=>{
                    console.log(j.data);
                    that.MessageInfo = j.data;
                    let data_id = document.getElementById("data_id");
                    data_id.innerHTML = that.MessageInfo["data_id"];
                    let label_type = document.getElementById("label_type");
                    if(that.MessageInfo["specy"]==="pic"){
                        label_type.innerHTML = "tmp";
                    }
    
                    
                })
            },
            back_index(){
                return fetch("/api/clearsession").then((res) => res.json()).then(()=>{
                    this.$router.push("/index/manage/dataset");
                })
            },
            // Change Remarks
            changing_memo()
            {
                this.pre_memo=this.memo_text;
                var change_memo_text=document.getElementById("memo_info");
                change_memo_text.style.visibility='hidden';
                var change_memo_btn=document.getElementById("change_memo");
                change_memo_btn.style.visibility='hidden';
                var change_memo_input=document.getElementById("memo_input");
                change_memo_input.style.visibility='visible';
                var two_btns=document.getElementById("two_btns");
                two_btns.style.visibility='visible';
            },

            // Confirm Remark Modification
            acknowleging_memo()
            {
                var change_memo_text=document.getElementById("memo_info");
                change_memo_text.style.visibility='visible';
                var change_memo_btn=document.getElementById("change_memo");
                change_memo_btn.style.visibility='visible';
                var change_memo_input=document.getElementById("memo_input");
                change_memo_input.style.visibility='hidden';
                var two_btns=document.getElementById("two_btns");
                two_btns.style.visibility='hidden';
            },

            // Cancel Remark Modification
            canceling_memo()
            {
                this.memo_text=this.pre_memo;
                var change_memo_text=document.getElementById("memo_info");
                change_memo_text.style.visibility='visible';
                var change_memo_btn=document.getElementById("change_memo");
                change_memo_btn.style.visibility='visible';
                var change_memo_input=document.getElementById("memo_input");
                change_memo_input.style.visibility='hidden';
                var two_btns=document.getElementById("two_btns");
                two_btns.style.visibility='hidden';
            },
        }
    }

</script>

<style scoped>
    .el-header  
    {
        height: 56px;
    }
    .item_heading
    {
        position:absolute;
        padding-left: 6px;
        border-left: 4px solid;
        height:22px;
        font-weight:700;
        font-size:15px;
    }
    #new_info
    {
        left:230px;
        top:140px;
    }
    #mark_info
    {
        left:230px;
        top:300px;
    }
    #data_cle
    {
        left:230px;
        top:510px;
    }
    #data_enhan
    {
        left:230px;
        top:600px;
    }
    #data_intro
    {
        left:230px;
        top:690px;
    }
    .text_left1
    {
        position:absolute;
        font-size:15px;
        font-weight:300;
    }
    .text_right1
    {
        position:absolute;
        font-size:15px;
        font-weight:300;
    }
    .text_left2
    {
        position:absolute;
        font-size:15px;
    }
    .text_right2
    {
        position:absolute;
        font-size:15px;
    }
    .el-divider
    {
        position:absolute;
        top:92px;
        left:200px;
    }
    #markingInfo_radio_group
    {
        position:absolute;
        font-size:15px;
        left:420px;
        top:747px
    }
    #fashion_choice
    {
        position:absolute;
        font-size:15px;
        left:420px;
        width:200px;
        top:787px;
    }
    #local_choice
    {
        position:absolute;
        font-size:15px;
        left:620px;
        top:787px;
        visibility: hidden;
    }
    #submit_button
    {
        position:absolute;
        font-size:15px;
        left:420px;
        top:830px;
    }
    #memo_row
    {
        position:absolute;
        left:370px;
        top:213px;
        border-style:none;
    }
    #change_memo
    {
        float: left;
        background:url(../../assets/chage_memo.jpg);
        height:15px;
        width:15px;
        margin-left:-20px;
        margin-top: 16px;
        border-style:none;
    }
    #memo_input
    {
        height:15px;
        width:200px;
        position:absolute;
        top:230px;
        left:350px;
        visibility:hidden;
    }
    #memo_acknowlege
    {
        position:absolute;
        border-style:none;
        height:19px;
        width:50px;
        left:0px;
    }
    #memo_cancel
    {
        position:absolute;
        border-style:none;
        height:19px;
        width:50px;
        right:0px;
    }
    #two_btns
    {
        position:absolute;
        top:230px;
        left:558px;
        font-size:12px;
        height:19px;
        width:100px;
        border-style:solid;
        border-width:1px;
        visibility:hidden;
    }
</style>