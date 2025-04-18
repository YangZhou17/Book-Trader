<template>
  <main> 
    <section id="register"> 
      <h2>Please Register</h2>

      <label for="username">Username: </label>
      <input type="text" id="username" placeholder="Username" v-model="username"><br><br>

      <label for="email">E-mail: </label>
      <input type="text" id="email" placeholder="E-mail" v-model="email"><br><br>
      
      <!-- University field with dropdown -->
      <div class="university-input">
        <label for="school">University: </label>
        <input type="text" id="school" placeholder="University" v-model="schoolInput" @input="onUniversityInput">
        <!-- Dropdown list, only show if there are search results -->
        <div v-if="universities.length > 0" class="dropdown">
          <ul>
            <li v-for="uni in universities" :key="uni" @click="selectUniversity(uni)">
              {{ uni }}
            </li>
          </ul>
        </div>
      </div>
      <p>{{uniMessage}}</p>

      <label for="password">Password: </label>
      <input type="text" id="password" placeholder="Password" v-model="password"><br><br>

      <p style="color: red">{{registerMessage}}</p>

      <div id="registerButton" @click="register">Register!</div><br><br>
      <div id="backButton" @click="back">Back</div>

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
      email: "",
      schoolInput: "", 
      selectedSchool: "",
      password: "",
      registerMessage: "",
      universities: [],
      debounceTimer: null,
      uniMessage: "",
    };
  },

  methods: {
    back(){
      this.$router.push('/login');
    },

    inputCheck(){
      // check if any field is empty
      if (this.username == "" || this.email == "" || this.selectedSchool == "" || this.password == ""){
        this.registerMessage = "All fields must be filled."
        return false;
      }
      //check if email is correct form 
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)){
        this.registerMessage = "Please enter a correct email. "
        return false;
      }
      return true;
    },

    register() {
      if (!this.inputCheck()){
        return;
      }

      const data = {
        'username': this.username,
        'email': this.email, 
        'school': this.selectedSchool, 
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
          this.registerMessage = "User already exist! Please login.";
          console.log("User already exist! Please login.");
        }
        else{
          this.registerMessage = "Registration failed!";
          console.log("Registration failed!");
        }
      })
      .catch(err => console.error(err));
    },

    // Univeristy input handling
    onUniversityInput() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        if (this.schoolInput.length >= 3) {
          this.fetchUniversities(this.schoolInput);
        } else {
          this.universities = [];
        }
      }, 300);
    },

    fetchUniversities(input){
      const url = "https://api.data.gov/ed/collegescorecard/v1/schools?api_key=FWE9F9Rq01meBDpkjqd5sQDIOR7fYRIi2Udniod4&per_page=100&school.name=" + input;
      console.log(input);
      fetch(url)
      .then(response => {
        if (!response.ok) {
          this.uniMessage = "University server unavailable. \n Please try again later."
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        this.uniMessage = "";
        this.universities = (data.results || [])
        .map(result => result.school?.name)
        .filter(name => !!name);
        console.log(this.universities);
      })
      .catch(error => console.error('Error:', error));
    },

    selectUniversity(uni) {
      this.selectedSchool = uni || "";
      this.schoolInput = uni || "";
      this.universities = [];
    }
  }, 
};
</script>

<style> 
main {
  height: 100vh;
}

#register {
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

.university-input {
  position: relative;
  width: 100%;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 150px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  font-size: 14px;
}

.dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown li {
  padding: 8px 10px;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown li:hover {
  background-color: #f0f0f0;
}
</style> 