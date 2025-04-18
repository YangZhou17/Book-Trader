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
                <el-table-column prop="name" align="center">
                <template #default="scope">
                    {{ scope.row.name }}
                </template>
                </el-table-column>

                <!-- Second column: Follow button -->
                <el-table-column align="center">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="follow(scope.row)" :disabled="scope.row.followed">Follow</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>

<script>
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
                followings: []
            }
        },

        methods:{
            // fetch all followers
            fetchFollowers(){
                console.log("fetching followers"); 

                let url = "http://localhost:5001/api/" + this.username + "/followers" ; 

                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    this.followers = data.map(user => ({
                        ...user,
                        followed: false
                    }));
                    this.markAlreadyFollowed();
                })
                .catch(err => console.error(err));
            }, 

            // fetch all followings
            fetchFollowing(){
                console.log("fetching followings"); 

                let url = "http://localhost:5001/api/" + this.username + "/following" ; 

                fetch(url, {
                    method: 'GET',
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    this.followings = data;
                })
                .catch(err => console.error(err));
            }, 

            // check if the current followers is already followed by current user (in following list)
            markAlreadyFollowed() {
                const followingNames = this.followings.map(user => user.name.toLowerCase());
                this.followers.forEach(follower => {
                    if (followingNames.includes(follower.name.toLowerCase())){
                        follower.followed = true;
                    }
                });
            }, 

            // follow the selected user on follow button clicked
            follow(user){
                console.log("Trying to follow: " + user.name);

                let url = "http://localhost:5001/api/follow" ; 
                const data = {
                    'follower_name': this.username, //current user
                    'followed_name': user.name, //new user current user trying to follow
                };

                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if(data.success){
                        console.log(data.message);
                        user.followed = true;
                    }
                    else{
                        console.log(data.message);
                    }
                })
                .catch(err => console.error(err));
            }
        },
            
        mounted() {
            this.fetchFollowing();
            this.fetchFollowers(); 
        }

    }
</script>
