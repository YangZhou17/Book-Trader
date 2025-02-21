<template>
  <el-container>
  <HelloWorld msg="Welcome to Your Vue.js App"/>
    <router-view />
  </el-container>
</template>

<script>
import HelloWorld from './components/index.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-container{
  margin-bottom: -10px;
  margin-right: -10px;
  height: 100vh;
}

</style>
