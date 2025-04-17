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

      fetch("http://localhost:5001/api/login", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'content-type': 'application/json' }
      })
      .then(response => response.json())
      .then((data) => {
        if(data.success){
          localStorage.setItem("username", this.username);
          console.log("You have logged in successfully!");
          this.$router.push({ 
                    path: '/main', 
                    query: { 
                        pageType: "recommend",
                    }
                  });
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

main {
  height: 100vh;
}

#login {
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