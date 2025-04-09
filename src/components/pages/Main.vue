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
                <!-- Upload book button --> 
                <el-col :span="2">
                    <el-button type="primary" @click="toUpload">Upload Book</el-button>
                </el-col>

                <!-- My bookshelf/ public bookshelf -->
                <!-- <el-col :span="2" :offset="12">
                    <el-select v-model="value" class="m-2" placeholder="Shelf">
                        <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col> -->

                <!-- Show selling/renting -->
                <el-col :span="2" :offset="18">
                    <el-select v-model="transactionType" class="m-2" placeholder="Selling" style="width: 100px" @change="fetchBooks">
                        <el-option
                            v-for="item in transactionTypes"
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

            <!-- displaying books --> 
            <el-empty v-if="fetchedBooks.length === 0" description="No books available" />
            <el-table v-if="fetchedBooks.length != 0" :data="fetchedBooks" height="400" style="width: 100%" border>
                <el-table-column prop="name" label="Name" width="180" />
                <el-table-column prop="price" label="Price" width="180" />
                <el-table-column prop="owner" label="Owner" width="180">
                    <template v-slot="scope">
                        <el-link :underline="false" @click="goToUploaderProfile(scope.row.owner)">{{ scope.row.owner }}</el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="uploaded_at" label="Uploaded At">
                    <template v-slot="scope">
                        {{ formatDate(scope.row.uploaded_at) }}
                    </template>
                </el-table-column>
                <el-table-column v-if="transactionType === 'renting'" prop="rent_duration" label="Duration (days)" width="150" />
            </el-table>

            <!-- <el-empty :image-size="250" description="Empty" v-if="value=='open' || data_num==0">
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
                </div> -->

                <!-- Shelf Display Section -->
                <!-- <el-descriptions
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
            <el-divider class="lower" border-style="none"></el-divider> -->

            <!-- Pagination Section -->
            <!-- <el-pagination
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
            /> -->
        </el-main>
    </el-container>
</template>

<script>
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        name: "ManageDateSet",
        components:{
            Breadcrumb,
        },
        data(){
            return{
                transactionType: 'selling', 
                transactionTypes : [
                    {
                        value: 'selling', 
                        label: "Selling", 
                    }, 
                    {
                        value: 'renting', 
                        label: 'Renting', 
                    },
                ],
                fetchedBooks: [], 
            }
        },

        methods:{
            // Fetch selling/renting books by user selection
            fetchBooks(){
                console.log("Fetching data for:", this.transactionType);
                let url = "http://localhost:5001/api/books/" + this.transactionType; 
               
                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if (data.success) {
                        this.fetchedBooks = data.books;
                    } else {
                        console.error(data.message);
                    }
                })
                .catch(err => console.error(err));
            },

            formatDate(datetime) {
                if (!datetime){
                    return ""; 
                }
                return datetime.split("T")[0];
            },

            toUpload(){
                this.$router.push("/upload")
            },
            
            goToUploaderProfile(username) {
                // Implement navigation to uploader's profile based on username
                this.$router.push(`/profile/${username}`);
            },
        },
            
        mounted() {
            this.fetchBooks();
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
