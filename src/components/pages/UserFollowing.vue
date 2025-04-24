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
                <el-col :span="8" align="left">
                    <h1>Followings of {{username}}</h1>
                </el-col>
            </el-row>

            <!-- Display list of users followed by the current user --> 
            <el-empty v-if="followings.length === 0" description="No following" />
            <el-table v-if="followings.length != 0" :data="followings" :show-header="false" height="400" style="width: 100%" border>
                <el-table-column prop="name">
                    <template v-slot="scope">
                        <span
                        @click="$router.push(`/profile/${scope.row.name}`)"
                        style="color: #409EFF; cursor: pointer;"
                        >
                        {{ scope.row.name }}
                        </span>
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
        name: 'UserFollowing',
        components:{
            Breadcrumb,
        },
        data(){
            return{
                username: localStorage.getItem("username") || "",
                followings: [], 
            }
        },

        methods:{
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
        },
            
        mounted() {
            this.fetchFollowing(); 
        }

    }
</script>
