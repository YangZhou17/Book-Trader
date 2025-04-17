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

            <!-- Page title --> 
            <el-row>
                <h1>{{this.pageTitle}}</h1>
            </el-row><br>

            <el-row>
                <!-- Upload book button --> 
                <el-col :span="2">
                    <el-button type="primary" @click="toUpload">Upload Book</el-button>
                </el-col>


                <!-- <el-col :span="4">
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
                </el-col> -->
            </el-row><br>

            <!-- displaying books --> 
            <el-empty v-if="fetchedBooks.length === 0" description="No books available" />
            <el-table v-if="fetchedBooks.length != 0" :data="fetchedBooks" height="400" style="width: 100%" border>
                <el-table-column prop="name" label="Name"/>
                <el-table-column prop="transaction_type" label="Transaction Type" width="100" align="center"/>
                <el-table-column prop="price" label="Price" width="180" align="center"/>
                <el-table-column prop="owner" label="Owner" width="180" align="center">
                    <template v-slot="scope">
                        <el-link :underline="false" @click="goToUploaderProfile(scope.row.owner)">{{ scope.row.owner }}</el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="uploaded_at" label="Uploaded At" width="180" align="center">
                    <template v-slot="scope">
                        {{ formatDate(scope.row.uploaded_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="Rent Duration (days)" width="180" align="center">
                    <template v-slot="scope">
                        {{ scope.row.rent_duration ? scope.row.rent_duration : '(do not apply)' }}
                    </template>
                </el-table-column>
                <el-table-column label="Action" width="150" align="center">
                    <template v-slot="scope">
                        <div v-if="scope.row.owner !== currentUser">
                            <el-button v-if="scope.row.transaction_type === 'sell'" type="success" @click="buyBook(scope.row)">Buy</el-button>
                            <el-button v-if="scope.row.transaction_type === 'rent'" type="success" @click="rentBook(scope.row)">Rent</el-button>
                        </div>
                    </template>
                </el-table-column>
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
        name: "MainPage",
        components:{
            Breadcrumb,
        },
        data(){
            return{
                currentUser: localStorage.getItem("username") || "",
                pageType: "",
                pageTitle: "",
                fetchedBooks: [], 
            }
        },

        methods:{
            fetchBooks(){
                console.log("Fetching data for page:", this.pageType);
                let url = "http://localhost:5001/api/books/" + this.pageType + "/" + this.currentUser; 
               
                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if (data.success) {
                        console.log("Successfully fetched books");
                        this.fetchedBooks = data.books;
                    } else {
                        console.log(data.message);
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

            renderPageTitle(){
                if(this.pageType === 'nearby'){
                    this.pageTitle = "Books From Your School"; 
                }
                else if(this.pageType === 'following'){
                    this.pageTitle = "Books From People You Are Following"; 
                }
                else{
                    this.pageTitle = "Books Recommended For You"; 
                }
            },

            toUpload(){
                this.$router.push("/upload")
            },
            
            goToUploaderProfile(username) {
                this.$router.push(`/profile/${username}`);
            },

            // go to transaction confirmation page
            buyBook(book) {
                console.log("Buying book:", book);
                this.$router.push({ 
                    path: '/transactionConfirm', 
                    query: { 
                        book_id: book.id,
                        book_name: book.name, 
                        book_price: book.price,
                        book_owner: book.owner,
                        book_uploaded: book.uploaded_at, 
                        transaction_type: 'buy'
                    }
                });
            },

            rentBook(book) {
                console.log("Renting book:", book);
                this.$router.push({ 
                    path: '/transactionConfirm', 
                    query: { 
                        book_id: book.id,
                        book_name: book.name, 
                        book_price: book.price,
                        book_owner: book.owner,
                        book_uploaded: book.uploaded_at, 
                        book_rent_duration: book.rent_duration,
                        transaction_type: 'rent'
                    }
                });
            },
        },
            
        mounted() {
            this.pageType = this.$route.query.pageType;
            this.renderPageTitle();
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
</style>
