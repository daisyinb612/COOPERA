<template>
  <el-container class="main-container">
    <el-main class="script">
      <el-header class="header">
        <div>Playwriting</div>
      </el-header>
      <el-header class="button-container-up">
        <el-button class="button" @click="generate_script">Generate</el-button>
      </el-header>
      <div class="script-header">
        <el-scrollbar class="script-content">
          <!-- <div class="script-name">Logline</div> -->
          {{ script.storylines }}
          <div v-for="plot in script.dialogues" :key="plot.plotName">
            <h3>{{ plot.plotName }}</h3>
            scene: {{ plot.scene.name }}
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
import axios from "axios";
import { defineComponent } from "vue";
import { ref } from "vue";

export default defineComponent({
  name: "GScript",
  setup() {
    const script = ref({
      storylines: "",
      dialogues: "",
    });
    async function generate_script() {
      const res = await axios.get("/api/generate_script");
      script.value.dialogues = res.data["dialogues"];
      script.value.storylines = res.data["storylines"];
      console.log(script.value);
    }
    return { generate_script, script };
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
  background-color: #f1f1f1;
}

.header {
  background-color: #5973ff;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.script {
  display: flex;
  background-color: #ffffff;
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

.button-container-up {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  display: flex;
  padding: 10px;
}

.button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: white;
  border: 2px solid #5973ff;
  color: #bccfff;
  cursor: pointer;
  border-radius: 10px !important;
  transition:
    background-color 0.2s,
    color 0.2s;
}
</style>
