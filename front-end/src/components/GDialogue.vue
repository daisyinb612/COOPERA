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
          <template v-if="selectedPlot">
            <!-- 显示选中情节的剧情卡片 -->
            <el-card class="plot-item">
              <div class="plot-header">
                <div class="scene-name">{{ selectedPlot.plotName }}</div>
                <div class="plot-element">{{ selectedPlot.plotElement }}</div>
                <div class="location">{{ selectedPlot.location }}</div>
                <div class="characters">
                  <span v-for="character in selectedPlot.characters" :key="character">{{ character }}</span>
                </div>
              </div>
              <el-input
                type="textarea"
                v-model="selectedPlot.beat"
                placeholder="Enter beat here..."
                class="beat-input"
              ></el-input>
            </el-card>
            <!-- 根据对话编号显示角色和对话内容 -->
            <el-card class="dialogue-item" v-for="(dialogueNumber, index) in dialogueNumbers" :key="index">
              <div class="dialogue-header">
                <div class="dialogue-number">Dialogue {{ dialogueNumber }}</div>
              </div>
              <div v-for="dialogue in filteredDialogues(dialogueNumber)" :key="dialogue.character" class="character-dialogue">
                <div class="character">{{ dialogue.character }}: </div>
                <div class="dialogue-content">{{ dialogue.content }}</div>
              </div>
            </el-card>
          </template>
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
import { useStore } from 'vuex';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'GDialogue',

  setup() {
    const store = useStore();

    const examplePlots = [
      {
        plotName: 'Plot 1',
        plotElement: 'Conflict',
        location: 'Location 1',
        characters: ['Character 1', 'Character 2'],
        beat: 'This is the beat for plot 1.',
        dialogue: [
          { number: 1, character: 'Character 1', content: 'Dialogue 1 for Character 1' },
          { number: 2, character: 'Character 2', content: 'Dialogue 1 for Character 2' }
        ]
      },
      {
        plotName: 'Plot 2',
        plotElement: 'Climax',
        location: 'Location 2',
        characters: ['Character 3', 'Character 4'],
        beat: 'This is the beat for plot 2.',
        dialogue: [
          { number: 1, character: 'Character 3', content: 'Dialogue 1 for Character 3' },
          { number: 2, character: 'Character 4', content: 'Dialogue 1 for Character 4' }
        ]
      }
    ];

    const plots = computed(() => {
      const storePlots = store.getters['plot/plots'];
      return storePlots.length > 0 ? storePlots : examplePlots;
    });

    const selectedPlotIndex = ref(null);

    const selectedPlot = computed(() => {
      return selectedPlotIndex.value !== null ? plots.value[selectedPlotIndex.value] : null;
    });

    const dialogueNumbers = computed(() => {
      return selectedPlot.value ? [...new Set(selectedPlot.value.dialogue.map(d => d.number))] : [];
    });

    function selectPlot(index) {
      selectedPlotIndex.value = index;
    }

    async function UploadDialogue() {
      const payload = {
        action: 'update_dialogue',
        data: plots.value.map(plot => ({
          章节名: plot.plotName,
          故事阶段: plot.plotElement,
          情节梗概: plot.beat,
          对话内容: plot.dialogue,
          参与人物: plot.characters.map(character => ({ 角色名字: character }))
        }))
      };

      try {
        await axios.post('http://localhost:8000', payload);
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

    function filteredDialogues(dialogueNumber) {
      return selectedPlot.value ? selectedPlot.value.dialogue.filter(d => d.number === dialogueNumber) : [];
    }

    return {
      plots,
      selectedPlot,
      dialogueNumbers,
      selectedPlotIndex,
      filteredDialogues,
      selectPlot,
      UploadDialogue
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
  background-color: #F4F4F4;
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
  display: flex;
}

.dialogue-content {
  margin-left: 5px;
}
</style>
