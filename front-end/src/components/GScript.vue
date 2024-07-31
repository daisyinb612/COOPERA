<template>
  <el-container class="main-container">
    <el-main class="script">
      <el-header class="header">
        <div>剧本</div>
      </el-header>
        <el-button @click="generate_script" class="confirm-button">生成</el-button>
        <div class="script-header">
          <el-scrollbar class="script-content">
          <div class="script-name">Title</div>
          {{ script.storylines }}
          <div v-for="plot in script.dialogues" :key="plot.plotName">
            <h3>{{ plot.plotName }}</h3>
            scene: {{ plot.scene }}
            <div v-for="dialogue in plot.dialogue" :key="dialogue.character">
              <div>{{ dialogue.character }}: {{ dialogue.content }}</div>
              </div>
          </div>
          </el-scrollbar>
        </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
import { defineComponent} from 'vue';
import { ref } from 'vue';

export default defineComponent({
  name: 'GScript',
  setup() {
    const script = ref({
      storylines: "",
      dialogues: "",
    })
    async function generate_script(){
      const res = await axios.get('http://localhost:8000/generate_script')
      script.value.dialogues = res.data['dialogues']
      script.value.storylines = res.data['storylines']
      console.log(script.value);
    }
    return {generate_script, script};
  },
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

.script-header {
  height: 100%;
  overflow-y: auto;
  padding-left: 20px;
}


</style>