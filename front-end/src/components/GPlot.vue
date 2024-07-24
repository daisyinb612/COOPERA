<template>
  <el-container class="main-container">
    <el-main class="plot">
      <el-header class="header">
        <div>PLOT</div>
      </el-header>
      <el-main class="plot">
        <el-header class="button-container-up">
          <el-button class="button" @click="generatePlot">Generate</el-button>
          <el-button class="button" @click="AddPlot">Add</el-button>
        </el-header>
        <el-main class="plot-list-container">
          <el-scrollbar class="plots-list">
            <el-card v-for="(plot, index) in plots" :key="index" class="plot-item" @click="editPlot(index)">
              <div class="plot-header">
                <div class="scene-name">{{ plot.plotName }}</div>
                <div class="plot-element">{{ plot.plotElement }}</div>
                <div class="location">{{ plot.scene }}</div>
                <div class="characters">
                  <span v-for="character in plot.characters" :key="character">{{ character }}</span>
                </div>
              </div>
              <el-input type="textarea" v-model="plot.beat" placeholder="Enter beat here..." class="beat-input"></el-input>
            </el-card>
          </el-scrollbar>
        </el-main>
        <el-footer class="button-container-down">
          <el-button class="button" @click="UploadPlot">Upload</el-button>
        </el-footer>
      </el-main>
    </el-main>

    <el-dialog title="Add Plot" v-model="addDialogVisible" custom-class="dialog-content">
      <el-form :model="newPlot" label-width="100px" class="add-plot-form">
        <el-form-item label="情节名称">
          <el-input v-model="newPlot.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Plot Element">
          <el-radio-group v-model="newPlot.plotElement">
            <el-radio value="Exposition">Exposition</el-radio>
            <el-radio value="Inciting Incident">Inciting Incident</el-radio>
            <el-radio value="Conflict">Conflict</el-radio>
            <el-radio value="Rising Action">Rising Action</el-radio>
            <el-radio value="Climax">Climax</el-radio>
            <el-radio value="Resolution">Resolution</el-radio>
            <el-radio value="Dénouement">Dénouement</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="场景">
          <el-input v-model="newPlot.scene" autocomplete="off" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="selectedCharacters" multiple placeholder="请选择角色">
            <el-option v-for="character in allCharacters" :key="character.name" :label="character.name" :value="character.name" />
          </el-select>
          <div class="characters">
            <el-tag v-for="(character, index) in selectedCharacters" :key="index" closable @close="removeCharacter(character)">
              {{ character }}
            </el-tag>
          </div>
        </el-form-item>
        <el-form-item label="Beat">
          <el-input type="textarea" v-model="newPlot.beat" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button">Cancel</el-button>
          <el-button type="primary" @click="addNewPlot" class="confirm-button">Confirm</el-button>
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog title="Edit Plot" v-model="editDialogVisible" custom-class="dialog-content">
      <el-form :model="editPlotData" label-width="100px" class="add-plot-form">
        <el-form-item label="情节名称">
          <el-input v-model="editPlotData.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Plot Element">
          <el-radio-group v-model="editPlotData.plotElement">
            <el-radio value="Exposition">Exposition</el-radio>
            <el-radio value="Inciting Incident">Inciting Incident</el-radio>
            <el-radio value="Conflict">Conflict</el-radio>
            <el-radio value="Rising Action">Rising Action</el-radio>
            <el-radio value="Climax">Climax</el-radio>
            <el-radio value="Resolution">Resolution</el-radio>
            <el-radio value="Dénouement">Dénouement</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="场景">
          <el-input v-model="editPlotData.scene" autocomplete="off" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editSelectedCharacters" multiple placeholder="请选择角色">
            <el-option v-for="character in allCharacters" :key="character.name" :label="character.name" :value="character.name" />
          </el-select>
          <div class="characters">
            <el-tag v-for="(character, index) in editSelectedCharacters" :key="index" closable @close="removeEditCharacter(character)">
              {{ character }}
            </el-tag>
          </div>
        </el-form-item>
        <el-form-item label="Beat">
          <el-input type="textarea" v-model="editPlotData.beat" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleEditDialogClose" class="cancel-button">Cancel</el-button>
          <el-button type="primary" @click="saveEditedPlot" class="confirm-button">Confirm</el-button>
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
    const showDeleteConfirm = ref(false);
    const selectedCharacters = ref([]);
    const editSelectedCharacters = ref([]);
    const newPlot = reactive({
      plotName: '',
      plotElement: '',
      scene: '',
      characters: [],
      beat: '',
    });
    const editPlotData = reactive({
      plotName: '',
      plotElement: '',
      scene: '',
      characters: [],
      beat: '',
    });
    const plotToDeleteIndex = ref(null);
    const plotToEditIndex = ref(null);

    const plots = computed(() => store.getters['plot/plots'] || []);
    const allCharacters = computed(() => store.state.character.characters); // 修改为 characters

    const addPlot = (plot) => store.dispatch('plot/addPlot', plot);
    const updatePlot = (payload) => store.dispatch('plot/updatePlot', payload);
    const deletePlot = (index) => store.dispatch('plot/deletePlot', index);

    function showDeleteDialog() {
      showDeleteConfirm.value = true;
    }

    function cancelDelete() {
      showDeleteConfirm.value = false;
    }

    function AddPlot() {
      addDialogVisible.value = true;
    }

    function confirmDelete() {
      if (plotToDeleteIndex.value !== null) {
        deletePlot(plotToDeleteIndex.value);
        ElMessage({
          message: '情节已删除',
          type: 'success',
        });
      }
      showDeleteConfirm.value = false;
      editDialogVisible.value = false;
    }

    function handleAddDialogClose() {
      newPlot.plotName = '';
      newPlot.plotElement = '';
      newPlot.scene = '';
      newPlot.characters = [];
      newPlot.beat = '';
      selectedCharacters.value = [];
      addDialogVisible.value = false;
    }

    function handleEditDialogClose() {
      editPlotData.plotName = '';
      editPlotData.plotElement = '';
      editPlotData.scene = '';
      editPlotData.characters = [];
      editPlotData.beat = '';
      editSelectedCharacters.value = [];
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
      handleAddDialogClose();
    }

    function removeCharacter(character) {
      const index = selectedCharacters.value.indexOf(character);
      if (index !== -1) {
        selectedCharacters.value.splice(index, 1);
      }
    }

    function removeEditCharacter(character) {
      const index = editSelectedCharacters.value.indexOf(character);
      if (index !== -1) {
        editSelectedCharacters.value.splice(index, 1);
      }
    }

    function editPlot(index) {
      const plotToEdit = plots.value[index];
      editPlotData.plotName = plotToEdit.plotName;
      editPlotData.plotElement = plotToEdit.plotElement;
      editPlotData.scene = plotToEdit.scene;
      editPlotData.characters = [...plotToEdit.characters];
      editSelectedCharacters.value = [...plotToEdit.characters];
      editPlotData.beat = plotToEdit.beat;
      plotToEditIndex.value = index;
      editDialogVisible.value = true;
    }

    function saveEditedPlot() {
      if (plotToEditIndex.value !== null) {
        const updatedPlot = {
          plotName: editPlotData.plotName,
          plotElement: editPlotData.plotElement,
          scene: editPlotData.scene,
          characters: [...editSelectedCharacters.value],
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
        const response = await axios.post('http://localhost:8000', {
          action: 'init_plot_generation',
          data: null,
        });
        const generatedPlot = response.data;
        addPlot({
          plotName: generatedPlot.plot,
          plotElement: '',
          scene: '',
          characters: [],
          beat: generatedPlot.plot_content,
        });
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
          章节名: plot.plotName,
          故事阶段: plot.plotElement,
          场景: plot.scene,
          情节梗概: plot.beat,
          参与人物: plot.characters.map((character) => ({ 角色名字: character })),
        })),
      };

      try {
        await axios.post('your-api-endpoint', payload);
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
      selectedCharacters,
      editSelectedCharacters,
      showDeleteConfirm,
      allCharacters, // 修改为 characters
      confirmDelete,
      showDeleteDialog,
      cancelDelete,
      AddPlot,
      handleAddDialogClose,
      handleEditDialogClose,
      addNewPlot,
      removeCharacter,
      removeEditCharacter,
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