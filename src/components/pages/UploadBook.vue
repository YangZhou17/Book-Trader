<template>
    <el-container>
        <!-- Header Section -->
        <el-header>
            <Breadcrumb></Breadcrumb>
        </el-header>
        <el-divider />

        <!-- Main Section -->
        <el-main>

            <!-- Form to Upload Book -->
            <el-form label-width="120px" style="max-width: 650px">
                <!-- book name --> 
                <el-form-item label="Book Name">
                    <el-input id="input_book_name" v-model="bookName" placeholder="Enter book name "/>
                </el-form-item>

                <!-- transaction type --> 
                <el-form-item label="Transaction Type">
                    <el-radio-group id="input_transaction_type" v-model="transactionType">
                        <el-radio label="sell">Sell</el-radio>
                        <el-radio label="rent">Rent</el-radio>
                    </el-radio-group>
                </el-form-item>

                <!-- Price --> 
                <el-form-item label="Price">
                    <el-input id="input_price" v-model="price" placeholder="Enter price" @input="validatePrice()"/>
                </el-form-item>
                <p v-if="priceError" style="color: red;">{{ priceError }}</p>

                <!-- Rent duration -->
                <el-form-item v-if="transactionType === 'rent'" label="Duration">
                    <el-input id="input_duration" v-model="duration" placeholder="Enter rental duration" @input="validateDuration()"/>
                </el-form-item>
                <p v-if="durationError" style="color: red;">{{ durationError }}</p>
            </el-form>

            <el-row class="mb-4">
                <el-button type="success" @click="upload">Upload</el-button>
                <el-button type="warning" @click="cancel">Cancel</el-button>
            </el-row>

            <p>{{message}}</p>
        </el-main>
    </el-container>
</template>

<script>
import Breadcrumb from "../BreadCrumb.vue"

export default{
    components: {
        Breadcrumb,
    },

    data() {
        return {
            bookName: "",
            transactionType: "",
            price: "",
            duration: "",

            priceError: "",
            durationError: "",
            message: "",
        };
    },

    methods: {
        // input Validation
        validatePrice() {
            if (isNaN(this.price) || this.price === "") {
                this.priceError = "Price must be a number.";
                return false
            } 
            else if (Number(this.price) <= 0) {
                this.priceError = "Price cannot be zero or negative.";
                return false;
            } else {
                this.priceError = "";
                return true
            }
        },

        validateDuration() {
            if(this.transactionType == "sell"){
                this.durationError = "";
                return true
            }
            if (isNaN(this.duration) || this.duration === "") {
                this.durationError = "Duration must be a number.";
                return false
            } 
            else if (Number(this.duration) < 0) {
                this.durationError = "Duration cannot be negative.";
                return false;
            } else {
                this.durationError = "";
                return true
            }
        },

        // cancel button 
        cancel(){
            this.$router.push({ 
                    path: '/main', 
                    query: { 
                        pageType: "recommend",
                    }
                });
        },

        // Upload book
        upload() {
            if(!this.validatePrice() || !this.validateDuration()){
                this.message = "There exists some invalid input";
                console.log("There exists some invalid input");
                return;
            }

            const data = {
                'username': localStorage.getItem("username") || "",
                'book_name': this.bookName, 
                'transaction_type': this.transactionType, 
                'price': this.price, 
                'rent_duration': this.duration
            };
            console.log(data);

            fetch("http://localhost:5001/api/upload", {
                method: 'POST',
                body: JSON.stringify(data),
                headers: { 'content-type': 'application/json' }
            })
            .then(response => response.json())
            .then((data) => {
                console.log(data);
                if(data.success){
                    console.log("You have uploaded a book successfully");
                    this.$router.push({ 
                        path: '/main', 
                        query: { 
                            pageType: "recommend",
                        }
                    });
                }
                else{
                    this.message = "Upload failed!";
                    console.log("Upload failed!");
                }
            })
            .catch(err => console.error(err));
        }
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
</style>