<template>
  <el-container class="main-container">
    <el-main class="script">
      <el-header class="header">
        <div>剧本</div>
      </el-header>
    </el-main>
  </el-container>
</template>

<script>
import { defineComponent} from 'vue';
export default defineComponent({
  name: 'GScript',
});
</script>


<style scoped>
.main-container {
  display: flex;
  height: 88vh;
  width: 100%;
  gap: 20px;
  padding: 30px;
  overflow: hidden;
  box-sizing: border-box;
  background-color: #F4F4F4;
}

.header {
  background-color: #5973FF;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.script {
  display: flex;
  background-color: #FFFFFF;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
}

</style>