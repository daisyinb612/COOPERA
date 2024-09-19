<template>
  <el-container class="main-container">
    <el-main class="dialogue">
      <el-header class="header">
        <div>Creating dialogue</div>
      </el-header>
      <el-main class="dialogue" v-loading="loading">
        <el-header class="button-container-up">
          <el-scrollbar class="plot-name-list">
            <el-button v-for="(plot, index) in plots" :key="index" class="plot-name-button" @click="selectPlot(index)">
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
                  <div class="scene-name">Plot Name: {{ selectedPlot.plotName }}</div>
                  <el-button @click="generate_dialogue" class="confirm-button">Generacte</el-button>
                  <!-- <el-button @click="save_dialogue" class="confirm-button">保存</el-button> -->
                  <!-- <div class="location">{{ selectedPlot.location }}</div> -->
                </div>
                <el-row>
                  <el-col :span="3">
                    <img v-if="selectedPlot.scene.image" class="scene-image" :src="selectedPlot.scene.image"
                      alt="Asset Image" />
                  </el-col>
                  <el-col :span="1">
                  </el-col>
                  <el-col :span="20">
                    <div>Plot Name: : {{ selectedPlot.plotStage }}</div>
                    <div>Scene: {{ selectedPlot.scene.name }}</div>
                    <div>Description: {{ selectedPlot.scene.content }}</div>
                    <div>Appearing Characters:
                      <span v-for="character in selectedPlot.characters" :key="character">{{ character.name }},</span>
                    </div>
                    <div>introduction: {{ selectedPlot.beat }}</div>
                  </el-col>
                </el-row>
              </el-card>
              
              <!-- 根据对话编号显示角色和对话内容 -->
              <el-card class="dialogue-item" v-for="(dialogue, index) in dialogues" :key="index">
                <!-- <div class="dialogue-header">
                  <div class="dialogue-number">Dialogue {{ index + 1 }}</div>
                </div>
                <div v-for="dialogue in filteredDialogues(dialogueNumber)" :key="dialogue.character" class="character-dialogue"></div> -->
                <el-row align="middle">
                  <div style="position: absolute; right: 0%; top: 1%"><el-icon @click="del_one_dialogue(index)"><CloseBold /> </el-icon></div>
                  <el-col :span="4">
                  <div class="character">{{ dialogue.character }}: </div>
                 </el-col>
                  <el-col :span="2">
                    <svg @click="generate_audio(dialogue.content, dialogue.character, selectedPlotIndex, index)"
                      xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24">
                      <g fill="none">
                        <path fill-rule="evenodd" clip-rule="evenodd"
                          d="M5.08 9H5a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h.08a2 2 0 0 1 1.519.698l3.642 4.25c.604.704 1.759.277 1.759-.651V4.703c0-.928-1.155-1.355-1.76-.65L6.6 8.301A2 2 0 0 1 5.08 9zm13.556-4.725a1 1 0 1 0-1.377 1.45c3.655 3.472 3.655 9.078 0 12.55a1 1 0 1 0 1.377 1.45c4.485-4.26 4.485-11.19 0-15.45zm-2.947 2.8a1 1 0 1 0-1.378 1.45c2.027 1.925 2.027 5.025 0 6.95a1 1 0 1 0 1.378 1.45c2.857-2.714 2.857-7.136 0-9.85z"
                          fill="currentColor" />
                      </g>
                    </svg>
                  </el-col>
                  <el-col :span="18">
                    <audio ref="audioPlayer" controls v-if="dialogue.audio" style="height: 15px">
                      <source :src="dialogue.audio" type="audio/wav">
                      Your browser does not support the audio element.
                    </audio>
                  </el-col>
                </el-row>
                <br>
                <el-row align="middle">
                  <el-col :span="24">
                    <el-input type="textarea" v-model="dialogue.content" placeholder="Enter beat here..."
                      class="beat-input"></el-input>
                  </el-col>
                </el-row>
                <el-row align="middle">
                  <el-col :span="2">
                    <el-icon @click=""><CaretTop /></el-icon>
                  </el-col>
                  <el-col :span="2">
                    <el-icon @click=""><CaretBottom /></el-icon>
                  </el-col>
                  <el-col :span="2">
                  </el-col>
                </el-row>
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
import { useStore } from 'vuex';
import * as diff from 'diff';

export default defineComponent({
  name: 'GDialogue',

  setup() {
    const store = useStore();
    const loading = ref(false);
    const plots = computed(() => store.state.plot.plots);
    const selectedPlotIndex = ref(null);
    const selectedPlot = computed(() => {
      return selectedPlotIndex.value !== null ? plots.value[selectedPlotIndex.value] : null;
    });
    const dialogues = computed(() => {
      return selectedPlot.value.dialogue ?? [];
    });
    const beforeEditAssets = ref([])
    const audios = {
      "Female Voice": 0,
      "Male Voice": 1,
      // "斯文男音": 3,
      // "小萌萌": 4,
      // "知性女音": 5,
      // "老教授": 6,
      // "播音员": 9,
      // "京腔": 10,
      // "温柔大叔": 11,
    }

    async function generate_audio(content, character, scene, index) {
      const filename = `scene${scene}_${index}.wav`;
      console.log(character);
      let id_speaker = store.state.character.characters.find(c => c.name === character).per;
      // 忽略（）中的内容
      content = content.replace(/\(.*?\)/g, '');
      // per是字符串，需要通过audios转换成数字
      dialogues.value[index].audio = ''
      id_speaker = audios[id_speaker];
      const payload = {
        action: 'do_tts',
        data: {
          filename: filename,
          text: content,
          id_speaker: id_speaker
        }
      };
      try {
        // dialogues.value[index].audio = 'init';
        await axios.post('http://localhost:8000/do_tts', payload);
        // console.log(response.data);
        dialogues.value[index].audio = 'http://localhost:8000/get_audio?filename=' + filename;
        console.log('dialogues.value[index].audio', dialogues.value[index].audio)
        ElMessage({
          message: '音频生成成功',
          type: 'success'
        });
      } catch (error) {
        ElMessage({
          message: '音频生成失败',
          type: 'error'
        });
      }
    }


    function selectPlot(index) {
      selectedPlotIndex.value = index;
    }

    async function generate_dialogue() {
      loading.value = true;
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
      console.log(payload);
      try {
        const response = await axios.post('http://localhost:8000/generate_dialogue', payload);
        console.log(response.data);
        loading.value = false;
        selectedPlot.value.dialogue = response.data;
        // 深拷贝对话，用于上传对话时比较对话的差异
        beforeEditAssets.value = [...beforeEditAssets.value, ...JSON.parse(JSON.stringify(selectedPlot.value.dialogue))]
        console.log('beforeEditAssets', beforeEditAssets.value);
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
      // 比较beforeEditAssets和plots的差异
      // beforeEditAssets都是数组，元素为对象，对象的属性有character, content, audio
      // plots是数组，元素为对象，对象的属性有plotName, plotStage, scene, beat, characters, dialogue
      // dialogue是数组，元素为对象，对象的属性有character, content, audio
      // 对比beforeEditAssets的content和plots的dialogue的content
      const beforEditDialogues = beforeEditAssets.value.map(d => d.content);
      const currentDialogues = plots.value.flatMap(p => p.dialogue ? p.dialogue.map(d => d.content) : []);
      console.log('beforeEditDialogues', beforEditDialogues);
      console.log('currentDialogues', currentDialogues);
      beforEditDialogues.forEach(async (d, i) => {
        let changes = '';
        diff.diffChars(d, currentDialogues[i]).forEach(part => {
          const value = part.value.replace(/\n/g, '');
          if (part.added) {
            changes += `[${value}]`;
          } else if (part.removed) {
            changes += `{${value}}`;
          } else {
            changes += value;
          }
        });
        // 保存修改的记录,
        await axios.post('http://localhost:8000/save_changes', {
          action: 'save_changes',
          data: {
            changes: changes,
          },
        });
      });


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
    // const delOneDialogue = (payload) => store.dispatch('delOneDialogue', payload);
    function del_one_dialogue(index){
      // let payload = {
      //   plotIndex: selectedPlotIndex.value,
      //   dialogueIndex: index
      // }
      // delOneDialogue(payload)

      selectedPlot.value.dialogue.splice(index, 1)
    }

    return {
      plots,
      selectedPlot,
      // dialogueNumbers,
      dialogues,
      selectedPlotIndex,
      loading,
      // filteredDialogues,
      selectPlot,
      UploadDialogue,
      generate_audio,
      generate_dialogue,
      del_one_dialogue
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
  align-items: center;
  display: flex;
  padding: 10px;
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
  box-sizing: border-box;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 20px;
  padding-right: 20px;
}

.dialogue-item {
  margin-bottom: 20px;
  padding: 5px;
  border-radius: 5px;
  background-color: #F1F1F1
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
  margin-bottom: 40px;
  padding: 5px;
  border-radius: 10px;
  background-color: #D5DCFF;
}

.plot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.character-dialogue {
  display: flex;
  /* 使用flex布局使角色和对话内容横排 */
}

.dialogue-content {
  margin-left: 5px;
  /* 添加左边距，确保对话内容和冒号之间有足够的空间 */
}

.plots-list {
  height: 100%;
  overflow-y: auto;
}

.scene-image {
  border-radius: 10px;
  width: 120px;
  height: 120px;
  border: 2px solid #ddd
}

.del-button{
  height: 100%;
}

</style>