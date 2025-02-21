<!-- Create Shelf Page -->
<template>
    <el-container>
        <!-- Header Section -->
        <el-header>
            <Breadcrumb></Breadcrumb>
        </el-header>
        <el-divider />

        <!-- Main Section -->
        <el-main>

            <!-- Form to Create Shelf -->
            <el-form :model="form" label-width="120px" style="max-width: 650px">
                <el-form-item label="Shlef Name">
                    <el-input id="input_name" v-model="form.name" placeholder="Limit to 50 characters (Supports Chinese characters, English letters (both uppercase and lowercase), numbers, and underscores; underscore cannot be the first character)"/>
                </el-form-item>
                <el-form-item label="Data Type">
                    <el-radio-group id="data_type" v-model="radio" color="blue">
                        <el-radio-button name="data_type" value="pic" label="pic" @click="set_qx_value(1)">Image</el-radio-button>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="Shelf Version">
                    V1
                </el-form-item>
            </el-form>
            <el-form id="test" v-if="qx.quanxian===1" :model="form" label-width="120px" style="max-width: 1550px" :key="1">
                <el-form-item label="Annotation Type">
                    <el-radio-group v-model="form.type">
                    <el-radio name="marking_type_pic" id="pic_assortment" label="pic_cla" border @click="set_pic_value(1)">Image</el-radio>
                    <el-radio name="marking_type_pic" id="object" label="pic_det" border @click="set_pic_value(2)">Object</el-radio>
                </el-radio-group>
                </el-form-item>
            </el-form>
            <el-form id="test" v-if="pic.quanxian===1 && qx.quanxian===1" :model="form" label-width="120px" style="max-width: 650px" :key="1">
                <el-form-item label="Annotation Template">
                    <el-radio-group v-model="form.model">
                    <el-radio name="module" label="ss">tmp1</el-radio>
                    <el-radio name="module" label="sm">tmp2</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>

            <el-form id="test" v-if="pic.quanxian===2 && qx.quanxian===1" :model="form" label-width="120px" style="max-width: 650px" :key="1">
                <el-form-item label="Annotation Template">
                    <el-radio-group v-model="form.model">
                    <el-radio name="module" label="rec">tmp3</el-radio>
                </el-radio-group>
            </el-form-item>
            </el-form>

            <el-row class="mb-4">
                <el-button type="primary" @click="createdata">Create & Import</el-button>
                <el-button type="success">Create</el-button>
                <el-button type="warning" @click="cancel">Cancel</el-button>
            </el-row>
        </el-main>
    </el-container>
</template>

<script>
import Breadcrumb from "../BreadCrumb.vue"
import { reactive } from 'vue'
import { ref } from 'vue'

export default{
    components: {
        Breadcrumb,
    },
    setup(){
        let form = reactive({
            name: '',
            type: '',
            model: '',
            direction: '',
            single: '',
        });
        let qx = reactive({
            quanxian : 0,
        });
        let txt = reactive({
            quanxian : 0,
        });
        let pic = reactive({
            quanxian: 0,
        })
        let bqw = 1;
        let radio = ref('');
        return{
            form,
            bqw,
            radio,
            qx,
            txt,
            pic,
        }
    },
    methods: {
        // Form Validation
        isfull(){
            let inputName=document.getElementById("input_name");
            let dataType=document.getElementsByName("data_type");
            let markingTypePic=document.getElementsByName("marking_type_pic");
            let markingTypeText=document.getElementsByName("marking_type_text");
            let markingTypeTable=document.getElementsByName("marking_type_table");
            let markingTypeVideo=document.getElementsByName("marking_type_video");
            let markingTypeAudio=document.getElementsByName("marking_type_audio");
            let module=document.getElementsByName("module");
            let dataPara=document.getElementsByName("dataPara");
            return (
                (dataType[0].checked) && ((inputName.value!=""&&markingTypePic[0]&&(module[0].checked||module[1].checked)) ||
                (inputName.value!=""&&markingTypePic[1].checked&&(module[0].checked)) || (inputName.value!=""&&markingTypePic[2]&&(module[0].checked||module[1].checked))||
                (inputName.value!=""&&markingTypePic[3]&&(module[0].checked)))
                ||
                ((dataType[1].checked&&(dataPara[0].checked||dataPara[1].checked)) && ((inputName.value!=""&&markingTypeText[0].checked&&(module[0].checked||module[1].checked))||
                (inputName.value!=""&&markingTypeText[1].checked&&(module[0].checked))||(inputName.value!=""&&markingTypeText[2].checked&&(module[0].checked||module[1].checked||module[2].checked||module[3].checked))||
                (inputName.value!=""&&markingTypeText[3].checked&&(module[0].checked))))
                || 
                (dataType[2].checked && inputName.value!=""&&(markingTypeTable[0].checked))
                || 
                (dataType[3].checked && inputName.value!=""&&(markingTypeVideo[0].checked||markingTypeVideo[1].checked))
                || 
                (dataType[4].checked && inputName.value!=""&&(markingTypeAudio[0].checked||markingTypeAudio[1].checked))
                )
        },

        // Create Dataset
        createdata() {
            let inputName=document.getElementById("input_name");
            if (this.isfull()){
                let name = this.form["name"];
                    let specy = this.radio;
                    let label_type = this.form["type"];
                    let label_model = this.form["model"];
                    let is_single = this.form["single"];// Data deduplication setting
                    let direction = this.form["direction"];
                    const data = {
                        "data_id": name,
                        "group_id": name,
                        "name": name,
                        "version": "V1",
                        "num": 0,
                        "in_state": "finished",
                        "specy": specy,// Data type from "Data Type" selection saved in this.radio
                        "mark_state": 0,
                        "clear_state": "-",
                        "label_type": label_type,
                        "label_model": label_model,
                        "data_single": is_single,
                        "direction": direction,
                    };
                    console.log(data);
                    return fetch("/api/adddata",{
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(data)
                    })
                    .then(res => res.json())
                    .then((j)=>{
                        if(j.isok === "repeat"){
                            alert("Dataset name already exists!");
                        }
                        else{
                            this.$router.push("/index/manage/dataset/insert");
                        }
                        
                    })
            }
            else if(inputName.value==""){
                inputName.setAttribute("placeholder", "Please enter dataset name!");
            }
        },
        cancel(){
            this.$router.push("/index/manage/dataset")
        },
        set_qx_value(num){
            this.qx.quanxian = num;
        },
        set_pic_value(num){
            this.pic.quanxian = num;
        },

        set_txt_value(num){
            this.txt.quanxian = num;
        },
    }
}
</script>



<style scoped>
    .el-header  {
        height: 56px;
    }
    .el-divider{
        margin: 0;
    }
    .mb-4{
        margin-left: 120px;
    }
    .mb-4 .el-button{
        width: 110px;
    }
    #placeholderChange::-webkit-input-placeholder
    {
        color: red;
    }
    #placeholderChange::-moz-placeholder
    {
        color: red;
    }
    #placeholderChange::-ms-input-placeholder
    {
        color: red;
    }
    #placeholderChange::-ms-input-placeholder
    {
        color: red;
    }
    #pic_assortment
    {
        background: url("../../assets/book.jpeg") no-repeat;
        width:312px;
        height:160px;
        background-position-x:100px;
    }
    #object
    {
        background: url("../../assets/book.jpeg") no-repeat;
        width:312px;
        height:160px;
        background-position-x:100px;
    }
    
</style>