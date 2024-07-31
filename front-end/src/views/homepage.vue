<template>
  <el-container class="full-height-container">
    <el-header class="custom-header">
      <WebTitle />
    </el-header>
    <el-container class="inner-container">
      <el-aside width="300px" class="aside-menu">
        <MenuGuide />
      </el-aside>
      <el-main class="main-content">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import WebTitle from '../components/WebTitle.vue'
import MenuGuide from '../components/MenuGuide.vue'

export default {
  name: 'HomePage',
  components: {
    WebTitle,
    MenuGuide
  }
}
</script>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.full-height-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.inner-container {
  height: 100%;
  display: flex;
  flex: 1;
}

.aside-menu {
  width: 300px;
  height: 100%;
  background-color: #F1F1F1;
  padding: 0px;
}

.custom-header {
  height: 80px;
  padding: 0px;
}

.main-content {
  flex: 1;
  background-color: #F1F1F1;
}

</style>