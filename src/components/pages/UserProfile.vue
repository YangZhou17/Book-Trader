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
            <el-row :gutter="20">
                <el-col :span="10">
                    <h1>{{username}}</h1>
                </el-col>
                <el-col :span="4">
                    <p v-if="isCurrentUser" @click="showFollowers" style="cursor: pointer;">
                        {{numFollowers}} followers
                    </p>
                    <p v-else>
                        {{numFollowers}} followers
                    </p>
                </el-col>
                <el-col :span="4">
                    <p v-if="isCurrentUser" @click="showFollowing" style="cursor: pointer;">
                        {{numFollowing}} following
                    </p>
                    <p v-else>
                        {{numFollowing}} following
                    </p>
                </el-col>
                <el-col :span="4">
                    <p v-if="isCurrentUser" @click="showTransactions" style="cursor: pointer;">
                        Total {{numTransactions}} transactions
                    </p>
                    <p v-else>
                        Total {{numTransactions}} transactions
                    </p>
                </el-col>
            </el-row>

            <!-- follow and contact button -->
            <el-row :gutter="20" style="width: 80%; margin-top: 20px; margin-left:10%;">
                <el-col :span="12">
                    <el-button v-if="!isCurrentUser" type="primary" @click="follow" style="width: 100%;">Follow</el-button>
                </el-col>
                <el-col :span="12">
                    <el-button v-if="!isCurrentUser" type="primary" @click="contact" style="width: 100%;">Contact</el-button>
                </el-col>
            </el-row><br><br>

            <!-- Bookshelf: selling or renting-->
            <el-row>
                <el-col :span="2" :offset="21">
                    <el-select v-model="transactionType" class="m-2" placeholder="Selling" style="width: 100px" @change="fetchBooks">
                        <el-option
                            v-for="item in transactionTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-row><br>

            <!-- Bookshelf: displaying books --> 
            <el-empty v-if="fetchedBooks.length === 0" description="No book uploaded" />
            <el-table v-if="fetchedBooks.length != 0" :data="fetchedBooks" height="400" style="width: 100%" border>
                <el-table-column prop="name" label="Name" />
                <el-table-column prop="price" label="Price" width="180" align="center"/>
                <el-table-column prop="uploaded_at" label="Uploaded At" width="180" align="center">
                    <template v-slot="scope">
                        {{ formatDate(scope.row.uploaded_at) }}
                    </template>
                </el-table-column>
                <el-table-column v-if="transactionType === 'renting'" prop="rent_duration" label="Duration (days)" width="180" align="center"/>
            </el-table>
        </el-main>
    </el-container>
</template>

<script>
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        components:{
            Breadcrumb,
        },
        computed: {
            isCurrentUser() {
                return this.username === localStorage.getItem("username");
            }
        },
        props: ['username'],
        data(){
            return{
                //username: localStorage.getItem("username") || "",
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
            // Navigate to followers, following, transactions page if clicked 
            showFollowers(){
                console.log("showing followers"); 
                this.$router.push("/followers");
            }, 

            showFollowing(){
                console.log("showing following"); 
                this.$router.push("/following");
            },

            showTransactions(){
                console.log("showing Transactions"); 
                this.$router.push("/transactions");
            },

            // Fetch number of followers, followings, total transactions
            fetchFollowers(){
                console.log("fetching number of followers"); 
                let url = "http://localhost:5001/api/" + this.username + "/followers" ; 

                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    this.numFollowers = data.length;
                })
                .catch(err => console.error(err));
            }, 

            fetchFollowing(){
                console.log("fetching number of followings"); 
                let url = "http://localhost:5001/api/" + this.username + "/following" ; 

                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    this.numFollowing = data.length;
                })
                .catch(err => console.error(err));
            }, 

            fetchTransactions(){
                console.log("fetching number of transactions"); 
                let url = "http://localhost:5001/api/transactions/" + this.username; 

                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if(!data.success){
                        console.log(data.message);
                    }
                    else{
                        this.numTransactions = data.transactions.length;
                    }
                })
                .catch(err => console.error(err));
            }, 


            // Fetch selling/renting books by user selection
            fetchBooks(){
                console.log("Fetching data for", this.transactionType, "of user", this.username);
                let url = "http://localhost:5001/api/books/" + this.transactionType + "/" + this.username; 

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

            follow() {
                const currentUser = localStorage.getItem("username");
                const userToFollow = this.username; // Username of the profile being viewed

                if (currentUser === userToFollow) {
                console.error("Cannot follow yourself.");
                return;
                }

                console.log("Trying to follow:", userToFollow);

                const url = "http://localhost:5001/api/follow";
                const data = {
                follower_name: currentUser,  // Current logged-in user
                followed_name: userToFollow, // User that current user is trying to follow
                };

                fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if (data.success) {
                        console.log(data.message);
                        // Optional: Update local UI state to reflect follow status
                    } else {
                        console.error(data.message);
                    }
                })
                .catch(err => console.error(err));
            },

            contact(){
                //TO BE IMPLEMENTED
            }

        },
            
        mounted() {
            this.fetchFollowers();
            this.fetchFollowing(); 
            this.fetchTransactions();
            this.fetchBooks();
        }

    }
</script>
