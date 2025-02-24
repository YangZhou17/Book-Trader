<template>
  <main> 
    <section id="login"> 
      <h2>Welcome to Book Trader!</h2>

      <label for="username">Username: </label>
      <input type="text" id="username" placeholder="Username" v-model="username"><br><br>

      <label for="password">Password: </label>
      <input type="text" id="password" placeholder="Password" v-model="password"><br><br>

      <div id="loginButton" @click="login">Login</div><br><br>

      <p>Don't have an account?</p>
      <router-link to="/register" >Register</router-link>

      <p>{{message}}</p>
    </section>
  </main>
</template>

<!--VUE-->
<script>
export default {
  name: 'UserLogin',

  data() {
    return {
      username: "",
      password: "",
      message: "",
    };
  },

  methods: {
    login() {
      const data = {
        'username': this.username, 
        'password': this.password
        };
      console.log(data);

      fetch("http://localhost:8080/api/login", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'content-type': 'application/json' }
      })
      .then(response => response.json())
      .then((data) => {
        if(data.success){
          console.log("You have logged in successfully!");
          this.$router.push('/main');
        }
        else if (data.userExists){
          this.message = "Login failed! Incorrect password.";
          console.log("Login failed! Incorrect password.");
        }
        else{
          this.message = "Login failed! Have not registered yet.";
          console.log("Login failed! Have not registered yet.");
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
  text-align: center;
}
#loginButton{
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