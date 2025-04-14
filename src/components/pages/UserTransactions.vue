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
                    <h1>Transactions of {{username}}</h1>
                </el-col>
            </el-row>

            <!-- displaying books --> 
            <el-empty v-if="transactions.length === 0" description="No Transactions" />
            <el-table v-if="transactions.length != 0" :data="transactions" height="400" style="width: 100%" border>
                <el-table-column prop="book_name" label="Book Name" />
                <el-table-column prop="transaction_type" label="Transaction Type" width="100" />
                <el-table-column prop="price" label="Price" width="100" />
                <el-table-column prop="seller" label="Seller" width="150">
                    <template v-slot="scope">
                        <el-link :underline="false" @click="goToUploaderProfile(scope.row.seller)">{{ scope.row.seller }}</el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="buyer_renter" label="Buyer/Renter" width="150" />
                <el-table-column prop="transaction_datetime" label="Transaction Date" width="150">
                    <template v-slot="scope">
                        {{ formatDate(scope.row.transaction_datetime) }}
                    </template>
                </el-table-column>
                <el-table-column prop="rent_duration" label="Rent Duration (days)" width="120" />
                <el-table-column prop="status" label="Status" width="180" />
            </el-table>
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
                username: localStorage.getItem("username") || "",
                transactions: [],
            }
        },

        methods:{
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
                        this.transactions = data.transactions;
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

            goToUploaderProfile(username) {
                this.$router.push(`/profile/${username}`);
            },
        },
            
        mounted() {
            this.fetchTransactions();
        }
    }
</script>

