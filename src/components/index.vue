<!-- index page -->
<template>
  <div class="book_trader">
    <div id="leftnav" v-if="showSidebar">
      <el-aside width="230px">

      <div id="navtop" @click="toggleCollapse">
          <span id="navlogo"  class="mb-2">Book Trader</span>
      </div>

      <el-menu
        :default-active="$route.path"
        router 
        background-color="rgb(235, 231, 231)"
        text-color="#rgb(0,0,0)"
        class="el-menu-vertical-demo"
        mode="vertical"
      >
        <el-menu-item :index="'main'" @click="navToRecommend">
          <el-icon><Star /></el-icon>
          <span>Recommended Books</span>
        </el-menu-item>

        <el-menu-item index="/main?pageType=nearby">
          <el-icon><Location /></el-icon>
          <span>Nearby Books</span>
        </el-menu-item>

        <el-menu-item index="/main?pageType=following">
          <el-icon><User /></el-icon>
          <span>Books By Following</span>
        </el-menu-item> 

        <el-menu-item index="/upload">
          <el-icon><Upload /></el-icon>
          <span>Upload Book</span>
        </el-menu-item>

        <el-menu-item :index="'profile'" @click="navToProfile">
          <el-icon><UserFilled /></el-icon>
          <span>Profile</span>
        </el-menu-item>

        <div class="logout-button">
          <el-button type="danger" @click="logout" plain>Logout</el-button>
        </div>
      </el-menu>
      </el-aside>
    </div>
  </div>
</template>
<script>

export default {
  name: 'SidePanel',
  props: {
    msg: String
  },

  methods: {
    logout(){
      localStorage.removeItem("username");
      console.log("You have successfully logged out. ")
      this.$router.push("/login");
    },

    navToProfile(){
      const username = localStorage.getItem("username");
      if (username) {
        this.$router.push(`/profile/${username}`);
      } else {
        console.error("No username found in local storage");
        this.$router.push("/login");
      }
    }, 

    navToRecommend(){
      this.$router.push({ 
        path: '/main', 
        query: { 
          pageType: 'recommend', 
          t: Date.now()  
        }
      });
    }
  },

  computed: {
    showSidebar() {
      return !['/login', '/register'].includes(this.$route.path);
    }
  },
  
}
</script>

<style scoped>
  .el-divider--horizontal{
    margin: 0;
    background: 0 0;
    border-top: 1px solid rgb(222, 219, 219);
  }
  #leftnav{
    background-color: rgb(235, 231, 231);
    height: 100vh;
    margin-left: -8px;
    margin-bottom: -10px;
    padding-top: 20px;
  }
  .submenu{
    font-weight: bold;
    color: rgb(91, 92, 92);
  }
  .mb-2{
    text-align: left;
    margin-left: 10px;
    height: 20px;
    font-size: 1.2rem;
    font-weight: bold;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  }
</style>