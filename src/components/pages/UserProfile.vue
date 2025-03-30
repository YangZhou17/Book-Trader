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
            <!-- username and basic stats --> 
            <el-row>
                <el-col :span="10">
                    <h1>Hi! {{username}}</h1>
                </el-col>
                <el-col :span="4">
                    <p @click="showFollowers">{{numFollowers}} followers</p>
                </el-col>
                <el-col :span="4">
                    <p @click="showFollowing">{{numFollowing}} following</p>
                </el-col>
                <el-col :span="4">
                    <p>bought and rent {{numTransactions}} books</p>
                </el-col>
            </el-row>

            <!-- Bookshelf: selling or renting-->
            <el-row>
                <el-col :span="2" :offset="20">
                    <el-select v-model="transactionType" class="m-2" placeholder="Selling" style="width: 100px" @change="fetchBooks">
                        <el-option
                            v-for="item in transactionTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-row>

            <!-- Bookshelf: displaying books --> 
            <el-empty v-if="fetchedBooks.length === 0" description="No book uploaded" />
            <el-table v-if="fetchedBooks.length != 0" :data="fetchedBooks" height="400" style="width: 100%" border>
                <el-table-column prop="name" label="Name" width="180" />
                <el-table-column prop="price" label="Price" width="180" />
                <el-table-column prop="uploaded_at" label="Uploaded At">
                    <template v-slot="scope">
                        {{ formatDate(scope.row.uploaded_at) }}
                    </template>
                </el-table-column>
                <el-table-column v-if="transactionType === 'renting'" prop="rent_duration" label="Duration (days)" width="150" />
            </el-table>
        </el-main>
    </el-container>
</template>

<script>
// import { ref } from "vue"
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        components:{
            Breadcrumb,
        },
        data(){
            return{
                username: localStorage.getItem("username") || "",
                numFollowers: 0, 
                numFollowing: 0, 
                numTransactions: 0, 
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
            // Navigate to followers or following page if clicked 
            showFollowers(){
                console.log("showing followers"); 
                this.$router.push("/followers");
            }, 

            showFollowing(){
                console.log("showing following"); 
                this.$router.push("/following");
            },


            // Fetch number of followers, followings, total transactions
            fetchFollowers(){
                console.log("fetching number of followers"); 
                this.numFollowers = 6; 
                // let url = "http://localhost:5001/api/" + this.username + "/followers" ; 

                // fetch(url, {
                //     method: 'GET',
                //     headers: { 'content-type': 'application/json' }
                // })
                // .then(response => response.json())
                // .then((data) => {
                //     this.numFollowers = data.length;
                // })
                // .catch(err => console.error(err));
            }, 

            fetchFollowing(){
                console.log("fetching number of followings"); 
                this.numFollowing = 3; 
                // let url = "http://localhost:5001/api/" + this.username + "/following" ; 

                // fetch(url, {
                //     method: 'GET',
                //     headers: { 'content-type': 'application/json' }
                // })
                // .then(response => response.json())
                // .then((data) => {
                //     this.numFollowing = data.length;
                // })
                // .catch(err => console.error(err));
            }, 

             fetchTransactions(){
                console.log("fetching number of followings"); 
                this.numTransactions = 19; 
                // let url = "http://localhost:5001/api/transactions/" + this.username; 

                // fetch(url, {
                //     method: 'GET',
                //     headers: { 'content-type': 'application/json' }
                // })
                // .then(response => response.json())
                // .then((data) => {
                //     this.numTransactions = data.length;
                // })
                // .catch(err => console.error(err));
            }, 


            // Fetch selling/renting books by user selection
            fetchBooks(){
                console.log("Fetching data for", this.transactionType, "of user", this.username);
                // let url = "http://localhost:5001/api/books/" + this.username + "/" + this.transactionType; 

                // fetch(url, {
                //     method: 'GET',
                //     headers: { 'content-type': 'application/json' }
                // })
                // .then(response => response.json())
                // .then((data) => {
                //     this.fetchedBooks = data.books;
                // })
                // .catch(err => console.error(err));
            },

            formatDate(datetime) {
                if (!datetime){
                    return ""; 
                }
                return datetime.split("T")[0];
            },
        },
            
        mounted() {
            this.fetchFollowers();
            this.fetchFollowing(); 
            this.fetchTransactions();
            this.fetchBooks();
        }

    }
</script>
