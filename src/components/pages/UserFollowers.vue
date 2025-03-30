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
                <el-col :span="4">
                    <h1>Followers of {{username}}</h1>
                </el-col>
            </el-row>

            <!-- Display list of users followed by the current user --> 
            <el-empty v-if="followers.length === 0" description="No followers" />
            <el-table v-if="followers.length != 0" :data="followers" :show-header="false" height="400" style="width: 100%" border>
                <!-- First column: Name -->
                <el-table-column prop="name">
                <template #default="scope">
                    {{ scope.row.name }}
                </template>
                </el-table-column>

                <!-- Second column: Follow button -->
                <el-table-column>
                <template #default="scope">
                    <el-button type="primary" size="mini" @click="follow(scope.row)">Follow</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>

<script>
// import { ref } from "vue"
import Breadcrumb from "../BreadCrumb.vue"
    export default{
        name: 'UserFollowers',
        components:{
            Breadcrumb,
        },
        data(){
            return{
                username: localStorage.getItem("username") || "",
                followers: [], 
            }
        },

        methods:{
             fetchFollowers(){
                console.log("fetching followers"); 
                this.followers = [
                                        { name: 'Alice' },
                                        { name: 'Bob' },
                                        { name: 'Charlie' }
                                    ]; 
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

            follow(user){
                console.log("Trying to follow: " + user);
            }
        },
            
        mounted() {
            this.fetchFollowers(); 
        }

    }
</script>
