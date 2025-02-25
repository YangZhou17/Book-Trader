<template>
  <main> 
    <section id="register"> 
      <h2>Please Register</h2>

      <label for="username">Username: </label>
      <input type="text" id="username" placeholder="Username" v-model="username"><br><br>

      <label for="password">Password: </label>
      <input type="text" id="password" placeholder="Password" v-model="password"><br><br>

      <div id="registerButton" @click="register">Register!</div><br><br>
      <div id="backButton" @click="back">Back</div>

      <p>{{message}}</p>
    </section>
  </main>
</template>

<!--VUE-->
<script>
export default {
  name: 'UserRegister',

  data() {
    return {
      username: "",
      password: "",
      message: "",
    };
  },

  methods: {
    back(){
      this.$router.push('/login');
    },

    register() {
      const data = {
        'username': this.username, 
        'password': this.password
        };
        console.log(data);

      fetch("http://localhost:5001/api/register", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'content-type': 'application/json' }
      })
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        if(data.success){
          console.log("You have registered successfully");
          this.$router.push('/login');
        }
        else if (data.userExists){
          this.message = "User already exist! Please login.";
          console.log("User already exist! Please login.");
        }
        else{
          this.message = "Registration failed!";
          console.log("Registration failed!");
        }
      })
      .catch(err => console.error(err));
    }
  }
};
</script>

<style> 
body{
  background-color: beige;
}
#registerButton{
  color: white;
  background-color: burlywood;
  border-radius: 25px;
  padding-left: 10px;
  padding-right: 10px;
  margin-left: 5px;
  margin-right: 5px;
  display: inline;
}
#backButton{
  color: white;
  background-color: burlywood;
  border-radius: 25px;
  padding-left: 10px;
  padding-right: 10px;
  margin-left: 5px;
  margin-right: 5px;
  display: inline;
}
</style> 