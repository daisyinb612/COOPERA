<template>
  <el-container class="main-container">
    <el-main class="dialogue">
      <el-header class="header">
        <div>Dialogue</div>
      </el-header>
      <el-main class="dialogue">
        <el-header class="button-container-up">
          <el-scrollbar class="plot-name-list">
            <el-button
              v-for="(plot, index) in plots"
              :key="index"
              class="plot-name-button"
              @click="selectPlot(index)"
            >
              {{ plot.plotName }}
            </el-button>
          </el-scrollbar>
        </el-header>

        <el-main class="dialogue-list-container">
          <el-scrollbar class="plots-list">
          <template v-if="selectedPlot">
            <!-- 显示选中情节的剧情卡片 -->
            <el-card class="plot-item">  
              <div class="plot-header">
                <div class="scene-name">{{ selectedPlot.plotName }}</div>
                <el-button @click="generate_dialogue" class="confirm-button">生成</el-button>
            <!-- <el-button @click="save_dialogue" class="confirm-button">保存</el-button> -->
                <!-- <div class="location">{{ selectedPlot.location }}</div> -->
                
              </div>
              <el-row>
                <el-col :span="3">
                  <img v-if="selectedPlot.scene.image" class="scene-image" :src="selectedPlot.scene.image" alt="Asset Image" />
                </el-col>
                <el-col :span="3">
                 </el-col>
                <el-col :span="12">
                  <div>plotElement: {{ selectedPlot.plotStage }}</div>
                  <div>Scene name: {{ selectedPlot.scene.name }}</div>
                  <div>Scene discription: {{ selectedPlot.scene.content }}</div>
                  <div>Character:
                  <span v-for="character in selectedPlot.characters" :key="character">{{ character }},</span>
                </div>
                <div>Plot beat: {{ selectedPlot.beat }}</div>
                </el-col>
              </el-row>
              
                  
            </el-card>
            <!-- 根据对话编号显示角色和对话内容 -->
            <el-card class="dialogue-item" v-for="(dialogue, index) in dialogues" :key="index">
              <div class="dialogue-header">
                <div class="dialogue-number">Dialogue {{ index+1 }}</div>
              </div>
              <!-- <div v-for="dialogue in filteredDialogues(dialogueNumber)" :key="dialogue.character" class="character-dialogue"> -->
                <div class="character">{{ dialogue.character }}: </div>
                <el-input
                type="textarea"
                v-model="dialogue.content"
                placeholder="Enter beat here..."
                class="beat-input"
              ></el-input>
              <!-- </div> -->
            </el-card>
          </template>
        </el-scrollbar>
        </el-main>
        
        <el-footer class="button-container-down">
          <el-button class="button" @click="UploadDialogue">Upload</el-button>
        </el-footer>
      </el-main>
    </el-main>
  </el-container>
</template>

<script>
import { defineComponent, ref, computed } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import {useStore} from 'vuex';

export default defineComponent({
  name: 'GDialogue',

  setup() {
    const store = useStore();
    const plots = computed(() => store.state.plot.plots);
    console.log(plots.value);
    const selectedPlotIndex = ref(null);

    const selectedPlot = computed(() => {
      return selectedPlotIndex.value !== null ? plots.value[selectedPlotIndex.value] : null;
    });
    const dialogues = computed(() => {
      return selectedPlot.value.dialogue ?? [];
    });


    function selectPlot(index) {
      selectedPlotIndex.value = index;
    }

    async function generate_dialogue(){
      const payload = {
        action: 'generate_dialogue',
        data: {
          plotName: selectedPlot.value.plotName,
          plotStage: selectedPlot.value.plotStage,
          scene: selectedPlot.value.scene,
          beat: selectedPlot.value.beat,
          characters: selectedPlot.value.characters
        }
      };
      try {
        const response = await axios.post('http://localhost:8000/generate_dialogue', payload);
        console.log(response.data);
        selectedPlot.value.dialogue = response.data;
        ElMessage({
          message: '对话生成成功',
          type: 'success'
        });
      } catch (error) {
        ElMessage({
          message: '对话生成失败',
          type: 'error'
        });
      }
    }

    async function UploadDialogue() {
      const payload = {
        action: 'upload_dialogue',
        data: plots.value
      };

      try {
        await axios.post('http://localhost:8000/upload_dialogue', payload);
        ElMessage({
          message: '上传成功',
          type: 'success'
        });
      } catch (error) {
        ElMessage({
          message: '上传失败',
          type: 'error'
        });
      }
    }
    // function filteredDialogues(dialogueNumber) {
    //   return selectedPlot.value ? selectedPlot.value.dialogue.filter(d => d.number === dialogueNumber) : [];
    // }
    return {
      plots,
      selectedPlot,
      // dialogueNumbers,
      dialogues,
      selectedPlotIndex,
      // filteredDialogues,
      selectPlot,
      UploadDialogue,
      generate_dialogue
    };
  }
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
  background-color: #F1F1F1;
}

.header {
  background-color: #5973FF;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.dialogue {
  display: flex;
  background-color: #FFFFFF;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
}

.button-container-up {
  display: flex;
  justify-content: flex-start;
  padding: 5px;
  gap: 20px;
  text-align: center;
  box-sizing: border-box;
}

.plot-name-list {
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.plot-name-button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: white;
  border: 2px solid #5973FF;
  color: #BCCFFF;
  cursor: pointer;
  border-radius: 10px !important;
  transition: background-color 0.2s, color 0.2s;
}

.plot-name-button:hover {
  background-color: #93a2f7;
  color: white;
}

.plot-name-button:active {
  background-color: #3a51d4;
  color: white;
}

.dialogue-list-container {
  flex: 1;
  overflow: hidden;
  padding: 10px;
  box-sizing: border-box;
}

.dialogue-item {
  margin-bottom: 10px;
  padding: 20px;
  border-radius: 10px;
  background-color: #e6e6e6;
}

.dialogue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.plot-name {
  font-size: 18px;
  font-weight: bold;
}

.dialogue-element,
.location,
.characters {
  font-size: 14px;
}

.dialogue-input {
  width: 100%;
  margin-top: 10px;
}

.button-container-down {
  display: flex;
  justify-content: flex-end;
  padding: 5px;
  gap: 20px;
  text-align: center;
  box-sizing: border-box;
}

.button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: white;
  border: 2px solid #5973FF;
  color: #BCCFFF;
  cursor: pointer;
  border-radius: 10px !important;
  transition: background-color 0.2s, color 0.2s;
}

.button:hover {
  background-color: #93a2f7;
  color: white;
}

.button:active {
  background-color: #3a51d4;
  color: white;
}
.plot-item {
    margin-bottom: 10px;
    padding: 20px;
    border-radius: 10px;
    background-color: #e6e6e6;
}
.plot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.character-dialogue {
  display: flex; /* 使用flex布局使角色和对话内容横排 */
}
.dialogue-content {
  margin-left: 5px; /* 添加左边距，确保对话内容和冒号之间有足够的空间 */
}
.plots-list {
  height: 100%;
  overflow-y: auto;
}

.scene-image{
  width: 100%;
  margin: 10px;
}

</style>