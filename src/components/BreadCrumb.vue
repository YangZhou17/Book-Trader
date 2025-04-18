<!-- BreadCrumb -->
<template>
    <el-breadcrumb separator=">">
        <el-breadcrumb-item :to="{ path: '/main', query: { pageType: 'recommend' } }">Home</el-breadcrumb-item>
        <template v-for="(item, index) in breadList">
          <el-breadcrumb-item
            v-if="item.name"
            :key="index"
            :to="item.path"
          >{{ item.name }}</el-breadcrumb-item>
        </template>
    </el-breadcrumb>
</template>

<script>
export default {
  data() {
    return {
      breadList: [],
    }
  },
  methods: {
    getMatched() {
      this.breadList = this.$route.matched;
    },
  },
  created() {
    this.getMatched()
  },
  watch: {
    $route() {
      this.breadList = this.$route.matched;
    }
  }
}
</script>

<style scoped>
    .el-breadcrumb{
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 0.9rem;
        margin-top: 18px;
        margin-left: 15px;
    }
</style>