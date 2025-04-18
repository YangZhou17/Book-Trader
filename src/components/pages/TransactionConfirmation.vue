<template>
  <main> 
    <section id="confirmation"> 
      <h2>Confirm Your Action</h2>

        <!-- Book Information -->
        <div>
            <h3>{{ this.book_name }}</h3>
            <p><strong>Price:</strong> {{ this.book_price }}</p>
            <p><strong>Owner:</strong> {{ this.book_owner }}</p>
            <p><strong>Uploaded At:</strong> {{ formatDate(this.book_uploaded) }}</p>
            <p v-if="this.transaction_type == 'rent'"><strong>Rent Duration:</strong> {{ this.book_rent_duration }} days</p>
        </div><br>

        <!-- Checkbox with understanding statement -->
        <div>
            <input type="checkbox" v-model="checkboxChecked">
            I understand that by clicking the 'Confirm and Contact Owner' button below, 
            I will automatically reach out to the owner of this book and initiate the transaction confirmation process.
        </div><br>

        <!-- Contact Button -->
        <button  id="confirmButton" :disabled="!checkboxChecked" type="primary" @click="confirmTransaction">Confirm and Contact Owner</button >
        <!-- Back Button -->
        <button  id="cancelButton" type="secondary" @click="cancel">Cancel</button >
    </section>
  </main>
</template>

<script>
export default {
    name: 'TransactionConfirm',
    
    data() {
        return {
            checkboxChecked: false,
            book_id:"",
            book_name: "", 
            book_price: "",
            book_owner: "",
            book_uploaded: "", 
            book_rent_duration: "",
            transaction_type: ""
        };
    },

    methods: {
        formatDate(datetime) {
        if (!datetime) return '';
        return datetime.split('T')[0];
        },

        confirmTransaction() {
            console.log("contact button clicked");
            this.buyOrRent(); 
            this.contact();
        }, 

        buyOrRent(){
            // buy book
            if(this.transaction_type == 'buy'){
                const data = {
                    'username': localStorage.getItem("username") || "",
                    'book_id': this.book_id
                };
                console.log(data);

                fetch("http://localhost:5001/api/buy", {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if(data.success){
                        console.log("You have successfully bought this book");
                    }
                    else{
                        console.log(data.message);
                    }
                })
                .catch(err => console.error(err));
            }
            //rent book
            else{
                 const data = {
                    'username': localStorage.getItem("username") || "",
                    'book_id': this.book_id
                };
                console.log(data);

                fetch("http://localhost:5001/api/rent", {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: { 'content-type': 'application/json' }
                })
                .then(response => response.json())
                .then((data) => {
                    if(data.success){
                        console.log("You have successfully rent this book");
                    }
                    else{
                        console.log(data.message);
                    }
                })
                .catch(err => console.error(err));
            }
        }, 

        contact() {
                console.log("Contacting user:", this.book_owner);
                const url = `http://localhost:5001/api/user/${this.book_owner}`;

                fetch(url, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.email) {
                    console.log("User's email:", data.email);
                    // Open system email client
                    window.location.href = `mailto:${data.email}`;
                    } else {
                    console.error('Could not fetch email:', data.message || data);
                    }
                })
                .catch(err => console.error('Error contacting backend:', err));
            },

        cancel(){
            this.$router.push({ 
                    path: '/main', 
                    query: { 
                        pageType: "recommend",
                    }
                });
        }
    }, 

    mounted() {
        this.book_id = this.$route.query.book_id;
        this.book_name = this.$route.query.book_name;
        this.book_price = this.$route.query.book_price;
        this.book_owner = this.$route.query.book_owner;
        this.book_uploaded = this.$route.query.book_uploaded;
        this.transaction_type = this.$route.query.transaction_type;
        if(this.transaction_type == 'rent'){
            this.book_rent_duration = this.$route.query.book_rent_duration;
        }
    },
};
</script>

<style> 
main {
    height: 100vh;
}

#confirmation {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    text-align: left;
    z-index: 10;
    width: 100%; 
    max-width: 500px;
    box-sizing: border-box; 
}

h2 {
    margin-bottom: 20px;
    text-align: center;
}

h3 {
    font-size: 20px;
    font-weight: bold;
    word-wrap: break-word;
}

p {
    margin: 5px 0;
    word-wrap: break-word; 
}

#confirmButton {
    background-color:#1D7874;
    margin-top: 20px;
    width: 50%;
    height: 30px;
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;
    margin-left: 25%;
    border: none;
}

#cancelButton {
    background-color:lightgray;
    margin-top: 10px;
    width: 50%;
    height: 30px;
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;
    margin-left: 25%; 
    border: none;
}
</style> 