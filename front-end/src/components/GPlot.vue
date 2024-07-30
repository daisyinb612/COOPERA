<template>
  <el-container class="main-container">
    <el-main class="plot">
      <el-header class="header">
        <div>PLOT</div>
      </el-header>
      <el-main class="plot">
        <el-header class="button-container-up">
          <el-button class="button" @click="generatePlot">生成</el-button>
          <el-button class="button" @click="AddPlot">添加</el-button>
        </el-header>
        <el-main class="plot-list-container">
          <el-scrollbar class="plots-list">
            <el-card v-for="(plot, index) in plots" :key="index" class="plot-item" @click="editPlot(index)">
              <div class="plot-header">
                <div class="scene-name">{{ plot.plotName }}</div>
                <div class="plot-element">{{ plot.plotStage }}</div>
                <div class="location">{{ plot.scene }}</div>
                <div class="characters">
                  <span v-for="character in plot.characters" :key="character">{{ character.name }}</span>
                </div>
              </div>
              <el-input type="textarea" v-model="plot.beat" placeholder="输入情节梗概..." class="beat-input"></el-input>
            </el-card>
          </el-scrollbar>
        </el-main>
        <el-footer class="button-container-down">
          <el-button class="button" @click="UploadPlot">保存</el-button>
        </el-footer>
      </el-main>
    </el-main>

    <el-dialog title="添加情节" v-model="addDialogVisible" custom-class="dialog-content">
      <el-form :model="newPlot" label-width="100px" class="add-plot-form">
        <el-form-item label="情节名称">
          <el-input v-model="newPlot.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="情节元素">
          <el-radio-group v-model="newPlot.plotElement">
            <el-radio value="Exposition">展示</el-radio>
            <el-radio value="Inciting Incident">激励事件</el-radio>
            <el-radio value="Conflict">冲突</el-radio>
            <el-radio value="Rising Action">上升动作</el-radio>
            <el-radio value="Climax">高潮</el-radio>
            <el-radio value="Resolution">解决</el-radio>
            <el-radio value="Dénouement">结局</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="场景">
          <el-select v-model="newPlot.scene" placeholder="请选择场景" allow-create filterable>
            <el-option v-for="scene in allScenes" :key="scene.value" :label="scene.label" :value="scene.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="newPlot.characters" multiple placeholder="请选择角色">
            <el-option v-for="character in allCharacters" :key="character.name" :label="character.name" :value="character.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="情节梗概">
          <el-input type="textarea" v-model="newPlot.beat" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button">取消</el-button>
          <el-button type="primary" @click="addNewPlot" class="confirm-button">确认</el-button>
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog title="编辑情节" v-model="editDialogVisible" custom-class="dialog-content">
      <el-form :model="editPlotData" label-width="100px" class="add-plot-form">
        <el-form-item label="情节名称">
          <el-input v-model="editPlotData.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="情节元素">
          <el-radio-group v-model="editPlotData.plotElement">
            <el-radio value="Exposition">展示</el-radio>
            <el-radio value="Inciting Incident">激励事件</el-radio>
            <el-radio value="Conflict">冲突</el-radio>
            <el-radio value="Rising Action">上升动作</el-radio>
            <el-radio value="Climax">高潮</el-radio>
            <el-radio value="Resolution">解决</el-radio>
            <el-radio value="Dénouement">结局</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="场景">
          <el-select v-model="editPlotData.scene" placeholder="请选择场景">
            <el-option v-for="scene in allScenes" :key="scene.name" :label="scene.name" :value="scene.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editPlotData.characters" multiple placeholder="请选择角色">
            <el-option v-for="character in allCharacters" :key="character.name" :label="character.name" :value="character.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="情节梗概">
          <el-input type="textarea" v-model="editPlotData.beat" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleEditDialogClose" class="cancel-button">取消</el-button>
          <el-button type="primary" @click="saveEditedPlot" class="confirm-button">确认</el-button>
        </el-footer>
      </el-form>
    </el-dialog>
  </el-container>
</template>

<script>
import { defineComponent, ref, reactive, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'GPlot',
  setup() {
    const store = useStore();

    const addDialogVisible = ref(false);
    const editDialogVisible = ref(false);
    const newPlot = reactive({
      plotName: '',
      plotElement: '',
      scene: '',
      characters: [],
      beat: '',
      dialogue: [],
    });
    const editPlotData = reactive({
      plotName: '',
      plotElement: '',
      scene: '',
      characters: [],
      beat: '',
      dialogue: [],
    });
    const plotToEditIndex = ref(null);

    // 使用 computed 从 Vuex store 中获取数据
    const plots = computed(() => store.getters['plots']);
    const allScenes = computed(() => store.state.scene.scenes);
    const allCharacters = computed(() => store.state.character.characters);

    const addPlot = (plot) => store.dispatch('addPlot', plot);
    const addScene = (scene) => store.dispatch('addScene', scene);
    const updatePlot = (payload) => store.dispatch('updatePlot', payload);

    function AddPlot() {
      addDialogVisible.value = true;
    }

    function handleAddDialogClose() {
      newPlot.plotName = '';
      newPlot.plotElement = '';
      newPlot.scene = '';
      newPlot.characters = [];
      newPlot.beat = '';
      editPlotData.dialogue = [];
      addDialogVisible.value = false;
    }

    function handleEditDialogClose() {
      editPlotData.plotName = '';
      editPlotData.plotElement = '';
      editPlotData.scene = '';
      editPlotData.characters = [];
      editPlotData.beat = '';
      editPlotData.dialogue = [];
      editDialogVisible.value = false;
    }

    function addNewPlot() {
      if (!newPlot.plotName) {
        ElMessage({
          message: '情节名称不能为空',
          type: 'warning',
        });
        return;
      }

      if (!newPlot.scene) {
        ElMessage({
          message: '场景不能为空',
          type: 'warning',
        });
        return;
      }

      if (newPlot.characters.length === 0) {
        console.log(newPlot)
        ElMessage({
          message: '角色不能为空',
          type: 'warning',
        });
        return;
      }

      const existingPlotIndex = plots.value.findIndex((plot) => plot.plotName === newPlot.plotName);
      if (existingPlotIndex !== -1) {
        updatePlot({ index: existingPlotIndex, plot: { ...newPlot } });

        ElMessage({
          message: '更新成功',
          type: 'success',
        });
      } else {
        addPlot({ ...newPlot });
        ElMessage({
          message: '添加成功',
          type: 'success',
        });
      }

      const newScene = {
        name: newPlot.scene,
        content: "",
        image: 'empty.png',
      };
      const existingSceneIndex = allScenes.value.findIndex((scene) => scene.name === newScene.name)
      if (existingSceneIndex === -1){
        addScene({...newScene})
      }

      handleAddDialogClose();
    }

    function editPlot(index) {
      const plotToEdit = plots.value[index];
      editPlotData.plotName = plotToEdit.plotName;
      editPlotData.plotElement = plotToEdit.plotElement;
      editPlotData.scene = plotToEdit.scene;
      editPlotData.characters = [...plotToEdit.characters];
      editPlotData.beat = plotToEdit.beat;
      editPlotData.dialogue = plotToEdit.dialogue;
      plotToEditIndex.value = index;
      editDialogVisible.value = true;
    }

    function saveEditedPlot() {

      if (!editPlotData.plotName) {
        ElMessage({
          message: '情节名称不能为空',
          type: 'warning',
        });
        return;
      }

      if (!editPlotData.scene) {
        ElMessage({
          message: '场景不能为空',
          type: 'warning',
        });
        return;
      }

      if (editPlotData.characters.length === 0) {
        ElMessage({
          message: '角色不能为空',
          type: 'warning',
        });
        return;
      }


      if (plotToEditIndex.value !== null) {
        const updatedPlot = {
          plotName: editPlotData.plotName,
          plotElement: editPlotData.plotElement,
          scene: editPlotData.scene,
          characters: [...editPlotData.characters],
          beat: editPlotData.beat,
        };
        updatePlot({ index: plotToEditIndex.value, plot: updatedPlot });
        ElMessage({
          message: '情节更新成功',
          type: 'success',
        });
        handleEditDialogClose();
      }
    }

    async function generatePlot() {
      try {
        const response = await axios.post('http://localhost:8000/init_plot_generation', {
          action: 'init_plot_generation',
          data: null,
        });
        console.log(response.data);
        addPlot(response.data);
        const scenes = response.data.map((plot) => {
          return {
            name: plot.scene,
            url: 'empty.png',
          }
        }
        )
        store.dispatch('addScene', scenes);
      } catch (error) {
        ElMessage({
          message: '请求失败',
          type: 'error',
        });
      }
    }

    async function UploadPlot() {
      const payload = {
        action: 'update_plot',
        data: plots.value.map((plot) => ({
          plotName: plot.plotName,
          plotStage: plot.plotStage,
          scene: plot.scene,
          情节梗概: plot.beat,
          characters: plot.characters.map((character) => ({ name: character })),
        })),
      };

      try {
        await axios.post('http://localhost:8000/update_plot', payload);
        ElMessage({
          message: '上传成功',
          type: 'success',
        });
      } catch (error) {
        ElMessage({
          message: '上传失败',
          type: 'error',
        });
      }
    }

    return {
      addDialogVisible,
      editDialogVisible,
      plots,
      newPlot,
      editPlotData,
      allScenes,
      allCharacters,
      AddPlot,
      handleAddDialogClose,
      handleEditDialogClose,
      addNewPlot,
      editPlot,
      saveEditedPlot,
      generatePlot,
      UploadPlot,
    };
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

.plot {
  display: flex;
  background-color: #FFFFFF;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
}

.button-container-up,
.button-container-down {
  display: flex;
  justify-content: flex-start;
  padding: 5px;
  gap: 20px;
  text-align: center;
  box-sizing: border-box;
}

.button-container-down {
  justify-content: flex-end;
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

.plot-list-container {
  flex: 1;
  overflow: hidden;
  padding: 10px;
  box-sizing: border-box;
}

.plots-list {
  height: 100%;
  overflow-y: auto;
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

.scene-name {
  font-size: 18px;
  font-weight: bold;
}

.plot-element,
.location,
.characters {
  font-size: 14px;
}

.beat-input {
  width: 100%;
  margin-top: 10px;
}

.add-plot-form {
  padding: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #333;
}

.confirm-button {
  background-color: #5973ff;
  color: white;
}

.character-tag {
  margin-right: 5px;
}
</style>