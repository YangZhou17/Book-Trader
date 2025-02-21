<!-- Bookshelf Display Page -->
<template>
    <el-container>
        <!-- Header Element -->
        <el-header >
            <Breadcrumb></Breadcrumb>
        </el-header>
        <el-divider />

        <!-- Main Section -->
        <el-main>
            <el-row>
                <el-col :span="2">
                    <el-button type="primary" @click="tocreate">Create Bookshelf</el-button>
                </el-col>
                <el-col :span="2" :offset="12">
                    <el-select v-model="value" class="m-2" placeholder="Shelf">
                        <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
                <el-col :span="4">
                    <el-cascader v-model="Tvalue" :options="Toptions"  placeholder="All" @change="handleChosenChange"/>
                </el-col>
                <el-col :span="4">
                    <el-input
                        v-model="input"
                        class="w-50 m-2"
                        placeholder="Enter Bookshelf Name"
                        prefix-icon="Search"
                        @change="Searchbyname"
                    >
                    </el-input>
                </el-col>
            </el-row>
            <el-empty :image-size="250" description="Empty" v-if="value=='open' || data_num==0">
            </el-empty>
            <div v-if="value!='open'">
            <div v-for = "(item,index) in MessageShow" :key="item.name">
            <el-divider class="between" border-style="none"></el-divider>
                <div class="table-header">
                    <div class="title">
                        <el-button class="inline-editor" link @click="show_nametxt(index)" id="edit_name">
                            <span title="name" class="inline-editor-txt">{{item["name"]}}</span>
                            <el-icon><Edit /></el-icon>
                        </el-button>
                        <el-input class="inline-editor" placeholder="Please enter a new name" :id="generate_id(index)" type="text" style="width:140px;visibility: hidden" v-model="new_name" visible="false" @change="change_name(item.name)"/>
                        <span>Shelf ID:{{item["group_id"]}}</span>
                    </div>
                    <div class="op">
                        <span class="op-item">
                            <el-icon><DocumentAdd /></el-icon>
                            <span>Add New Version</span>
                        </span>
                        <span class="op-item">
                            <el-icon><Menu /></el-icon>
                            <span>All Versions</span>
                        </span>
                        <el-button class="op-item" link @click="deletedata(item.name)">
                            <el-icon><Delete /></el-icon>
                            <span>Delete</span>
                        </el-button>
                    </div>
                </div>

                <!-- Shelf Display Section -->
                <el-descriptions
                    direction="vertical"
                    :column="8"
                    size="large"
                    border
                >
                    <el-descriptions-item label="Version">{{item["version"]}}</el-descriptions-item>
                    <el-descriptions-item label="Shelf ID">{{item["data_id"]}}</el-descriptions-item>
                    <el-descriptions-item label="Data Count">{{item["num"]}}</el-descriptions-item>
                    <el-descriptions-item label="Latest Import Status">
                        <span>{{item["in_state"]}}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="Type">{{item["specy"]}}</el-descriptions-item>
                    <el-descriptions-item label="Status 1">{{item["mark_state"]}}</el-descriptions-item>
                    <el-descriptions-item label="Status 2">{{item["clear_state"]}}</el-descriptions-item>
                    <el-descriptions-item label="Operations">
                        <el-button type="primary" link key="label" @click="multilabel(item.name,item.specy)">View and Annotate</el-button>
                        <el-button type="primary" link key="label" @click="insert(item.name)">Import</el-button>
                        <el-button type="primary" link key="delete" @click="deletedata(item.name)">Delete</el-button>
                        <el-button type="primary" link key="export" @click="exportdata(item.name)">Export</el-button>
                    </el-descriptions-item>
                </el-descriptions>
            <el-divider class="between" border-style="none"></el-divider>
            </div>
            </div>
            <el-divider class="lower" border-style="none"></el-divider>

            <!-- Pagination Section -->
            <el-pagination
                v-model:currentPage="queryInfo.pagenum"
                v-model:page-size="queryInfo.pagesize"
                :page-sizes="[1, 2, 3,4, 5]"
                :background="background"
                layout="total, sizes, prev, pager, next, jumper"
                :total="data_num"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                v-if="value!='open' && data_num!=0"
                id="pagination"
            />
        </el-main>
    </el-container>
</template>

<script>
import { reactive, ref } from "vue"
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        name: "ManageDateSet",
        components:{
            Breadcrumb,
        },
        data(){
            return{
                background :ref(true),
                queryInfo: {
                    query: '',
                    pagenum: 1,
                    pagesize: 2,
                },
                data_num: -1,
                value: ref(''),
                input: ref(''),
                new_name: ref(''),
                MessageInfo: reactive({}),
                MessageShow: reactive({}),
                MessageArray: reactive([]),
                options : [
                    {
                        value: 'my',
                        label: 'My Bookshelf',
                    },
                    {
                        value: 'open',
                        label: 'Public Bookshelf',
                    },
                ],
                Tvalue: ref([]),
                Toptions : [
                    {
                        value: 'pic',
                        label: 'pic',
                        children: [
                            {
                                value: 'pic_cla',
                                label: 'tmp1',
                            },
                            {
                                value: 'pic_det',
                                label: 'tmp2',
                            },
                        ]
                    },
                ]
            }
        },
        methods:{
            generate_id(index){
                return "name_"+index
            },
            exportdata(name){
                const data = {"name":name}
                return fetch("/api/setsession",{
                    method: 'POST',
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res=>res.json())
                .then(()=>{
                    this.$router.push("/index/manage/dataset/4-2");
                })
            },
            handleChosenChange(){
                let that = this;
                const data = {"specy":this.Tvalue[0],"type":this.Tvalue[1]}
                return fetch("/api/searchdata",{
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then((j)=>{
                    that.MessageInfo = j.MessageShow;
                    that.data_num = j.data_num;
                    that.MessageArray = reactive([]);
                    for (let item in that.MessageInfo){
                        that.MessageArray.push(item);
                        if(that.MessageInfo[item]["in_state"]==="finished"){
                            that.MessageInfo[item]["in_state"] = "Completed";
                        }
                        if(that.MessageInfo[item]["specy"]==="pic"){
                            that.MessageInfo[item]["specy"] = "tmp";
                        }
                    }
                    this.handleCurrentChange(1);
                })
            },
            insert(name){
                const data = {"name": name}
                return fetch("/api/setsession",{
                    method: 'POST',
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then(()=>{
                    this.$router.push("/index/manage/dataset/insert");
                })
                
            },
            tocreate(){
                this.$router.push("/index/manage/dataset/create")
            },
            get_datanum(){
                let that = this;
                fetch("/api/getnum").then((res) => res.json().then((j) => {
                    that.data_num = j.data_num;
                    console.log(that.data_num);
                }))
            },
            multilabel(name,specy){
                const data = {"name": name}
                return fetch("/api/setsession",{
                    method: 'POST',
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then(()=>{
                    console.log(specy);
                    if(specy==="tmp"){
                        const data = {"t_type": "all"};
                        fetch("/api/sessiontype",{
                            method: 'POST',
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify(data)
                        })
                        .then((res)=>res.json())
                        .then(()=>{
                            this.$router.push("/index/menu3");
                        })
                        
                    }
                })
            },

            // Search Dataset
            Searchbyname(){
                const data = {"name":this.input};
                let that = this;
                return fetch("/api/searchname",{
                    method: 'POST',
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then((j)=>{
                    that.MessageInfo = j.MessageShow;
                    that.data_num = j.data_num;
                    that.MessageArray = reactive([]);
                    for (let item in that.MessageInfo){
                        that.MessageArray.push(item);
                        if(that.MessageInfo[item]["in_state"]==="finished"){
                            that.MessageInfo[item]["in_state"] = "Completed";
                        }
                        if(that.MessageInfo[item]["specy"]==="pic"){
                            that.MessageInfo[item]["specy"] = "pic";
                        }
                    }
                    this.handleCurrentChange(1);
                })

            },

            // Change Name
            change_name(name){
                const data = {"new_name":this.new_name,"old_name":name};
                return fetch("/api/changename",{
                    method: 'POST',
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then(()=>{
                    this.$router.push("/index/manage/blank")
                })

            },
            show_nametxt(index){
                console.log(index)
                let txt = document.getElementById("name_"+index);
                if(txt.style.visibility==='visible'){
                    txt.style.visibility='hidden';
                }
                else{
                    txt.style.visibility='visible';
                    txt.style.backgroundColor="white";
                }
            },

            // Get Data
            get_data(){
                this.get_datanum();
                let that = this;
                fetch("/api/getdata").then((res) => res.json().then((j)=>{
                    that.MessageInfo = j.MessageInfo;
                    that.MessageArray = reactive([]);
                    for (let item in that.MessageInfo){
                        that.MessageArray.push(item);
                        if(that.MessageInfo[item]["in_state"]==="finished"){
                            that.MessageInfo[item]["in_state"] = "Completed";
                        }
                        if(that.MessageInfo[item]["specy"]==="pic"){
                            that.MessageInfo[item]["specy"] = "tmp";
                        }
                    }
                    this.handleCurrentChange(1);
                }))
            },
            handleSizeChange(newSize){
                this.queryInfo.pagesize = newSize;
                this.handleCurrentChange(1);
            },
            handleCurrentChange(newPage){
                this.queryInfo.pagenum = newPage;
                let start = (this.queryInfo.pagenum - 1) * this.queryInfo.pagesize;
                let end = start + this.queryInfo.pagesize;
                if (this.MessageArray.length < end){
                    end = this.MessageArray.length;
                }
                this.MessageShow = reactive({});
                for (let i = start; i < end; i++){
                    this.MessageShow[this.MessageArray[i]]=this.MessageInfo[this.MessageArray[i]];
                }
            },

            // Used to set the default option for the page form
            setvalue(){
                this.value = this.options[0].value;
            },

            // Delete Data
            deletedata(name){
                let that = this;
                const d_name = {"name": name,}
                console.log(d_name)
                return fetch("/api/deletedata",{
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(d_name)
                })
                .then(res => res.json())
                .then(() => {
                    if(that.data_num>0){
                        that.data_num = that.data_num - 1;
                    }
                    this.$router.push("/index/manage/blank")
                })
            }
        },
        created() {
            this.setvalue();
            this.get_data();
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
    .between{
        margin: 10px;
    }
    .lower{
        margin: 30px;
    }
    .table-header{
        display: flex;
        padding: 15px;
        border: 1px solid #eee;
        border-bottom: none;
        background-color: #f7f7f7;
        justify-content: space-between;
    }
    .table-header .title .inline-editor .el-icon{
        margin-left:10px;
        padding-bottom: -10px;
    }
    .table-header .title{
        display: flex;
        flex-direction: row;
        align-items: center;
        padding-bottom: -10px;
        font-size: 14px;
    }
    .table-header .title .inline-editor{
        margin-right: 20px;
        cursor: pointer;
        display: inline-block;
        white-space: nowrap;
    }
    .table-header .title .inline-editor-initial-txt{
        max-width: 360px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-header .op{
        display: flex;
        flex-direction: row;
        align-items: flex-end;
    }
    .table-header .op .op-item{
        font-size: 14px;
        cursor: pointer;
        margin-right: 22px;
        color: #000;
        text-decoration: none;
    }
    .table-header .op .op-item span{
        font-size: 12px;
        margin-left: 3px;
    }

</style>