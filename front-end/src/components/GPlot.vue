<template>
  <el-container class="main-container">
    <el-main class="plot">
      <el-header class="header">
        <div>Create the Plots</div>
      </el-header>
      <el-main class="plot">
        <el-header class="button-container-up">
          <el-button class="button" @click="generatePlot">Generate</el-button>
          <el-button class="button" @click="AddPlot">Add New Plot</el-button>
        </el-header>
        <el-main class="plot-list-container" v-loading="loading">
          <el-scrollbar class="plots-list">
            <el-card
              v-for="(plot, index) in plots"
              :key="index"
              class="plot-item"
              @click="editPlot(index)"
            >
              <div class="plot-header">
                <div class="plot-name">
                  <div>Plot{{ index + 1 }}:</div>
                  {{ plot.plotName }}
                </div>
                <div class="plot-element">
                  <div>Plot Stage:</div>
                  {{ plot.plotStage }}
                </div>
                <div class="location">
                  <div>Scene:</div>
                  {{ plot.scene.name }}
                </div>
                <div class="characters">
                  <div>Appearing Characters:</div>
                  <span v-for="character in plot.characters" :key="character">
                    <span style="padding: 3px">{{ character.name }}</span>
                  </span>
                </div>
              </div>
              <el-input
                type="textarea"
                v-model="plot.beat"
                placeholder="输入情节梗概..."
                class="beat-input"
              ></el-input>
            </el-card>
          </el-scrollbar>
        </el-main>
        <el-footer class="button-container-down">
          <el-button class="button" @click="UploadPlot">Upload</el-button>
        </el-footer>
      </el-main>
    </el-main>

    <el-dialog
      title="Add New Plot"
      v-model="addDialogVisible"
      custom-class="dialog-content"
    >
      <el-form :model="newPlot" label-width="100px" class="add-plot-form">
        <el-form-item label="Name">
          <el-input v-model="newPlot.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Plot Stage">
          <el-radio-group v-model="newPlot.plotStage">
            <el-radio
              v-for="stage in stageList"
              :key="stage"
              :label="stage"
              :value="stage"
              >{{ stage }}</el-radio
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Scene">
          <el-select
            v-model="newPlot.scene"
            placeholder="please select or create a scene"
            allow-create
            filterable
            value-key="name"
          >
            <el-option
              v-for="scene in allScenes"
              :key="scene.value"
              :label="scene.name"
              :value="scene"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Characters">
          <el-select
            v-model="newPlot.characters"
            multiple
            placeholder="please select the appearing characters"
            value-key="name"
          >
            <el-option
              v-for="character in allCharacters"
              :key="character.name"
              :label="character.name"
              :value="character"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="introduction">
          <el-input type="textarea" v-model="newPlot.beat" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button"
            >cancel</el-button
          >
          <el-button type="primary" @click="addNewPlot" class="confirm-button"
            >confirm</el-button
          >
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog
      title="Edit The Plot"
      v-model="editDialogVisible"
      custom-class="dialog-content"
    >
      <el-form :model="editPlotData" label-width="100px" class="add-plot-form">
        <el-form-item label="Number">
          <el-input v-model="editPlotData.No" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="editPlotData.plotName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Plot Stage">
          <el-radio-group v-model="editPlotData.plotStage">
            <el-radio
              v-for="stage in stageList"
              :key="stage"
              :label="stage"
              :value="stage"
              >{{ stage }}</el-radio
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Scene">
          <el-select
            v-model="editPlotData.scene"
            placeholder="please select or create a scene"
            value-key="name"
            clearable
            filterable
            allow-create
          >
            <el-option
              v-for="(scene, index) in allScenes"
              :key="scene"
              :label="scene.name"
              :value="scene"
            >
              <span style="float: left">{{ scene.name }}</span>
              <el-tag
                size="mini"
                effect="dark"
                type="danger"
                style="float: right; margin-top: 8px; margin-left: 3px"
                @click.stop="handleDelete(index)"
              >
                Delete
              </el-tag>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Characters">
          <el-select
            v-model="editPlotData.characters"
            multiple
            placeholder="please select the appearing characters"
            value-key="name"
          >
            <el-option
              v-for="character in allCharacters"
              :key="character.name"
              :label="character.name"
              :value="character"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="introduction">
          <el-input
            type="textarea"
            v-model="editPlotData.beat"
            autocomplete="off"
          />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleEditDialogClose" class="cancel-button"
            >Cancel</el-button
          >
          <el-button
            type="danger"
            @click="showDeleteDialog"
            class="delete-button"
            >Delete</el-button
          >
          <el-button
            type="primary"
            @click="saveEditedPlot"
            class="confirm-button"
            >Confirm</el-button
          >
        </el-footer>
        <el-dialog v-model="showDeleteConfirm">
          <div>Are you sure to remove the plot?</div>
          <span class="dialog-footer">
            <el-button @click="cancelDelete" class="cancel-button"
              >Cancel</el-button
            >
            <el-button
              type="danger"
              @click="confirmDelete"
              class="confirm-button"
              >Confirm</el-button
            >
          </span>
        </el-dialog>
      </el-form>
    </el-dialog>
  </el-container>
</template>

<script>
import { defineComponent, ref, reactive, computed } from "vue";
import { useStore } from "vuex";
import axios from "axios";
// eslint-disable-next-line no-unused-vars
import * as diff from "diff";
import { ElMessage } from "element-plus";

export default defineComponent({
  name: "GPlot",
  setup() {
    const store = useStore();
    const loading = ref(false);

    const addDialogVisible = ref(false);
    const editDialogVisible = ref(false);
    const showDeleteConfirm = ref(false);
    const newPlot = reactive({
      plotName: "",
      plotStage: "",
      scene: "",
      characters: [],
      beat: "",
      dialogue: [],
    });
    const beforeEditAsset = reactive({
      No: "",
      //   plotName: '',
      //   plotStage: '',
      //   scene: '',
      //   characters: [],
      beat: "",
      //   dialogue: [],
    });
    const editPlotData = reactive({
      No: "",
      plotName: "",
      plotStage: "",
      scene: "",
      characters: [],
      beat: "",
      dialogue: [],
    });
    const plotToEditIndex = ref(null);

    // 使用 computed 从 Vuex store 中获取数据
    const plots = computed(() => store.getters["plots"]);
    const allScenes = computed(() => store.state.scene.scenes);
    const allCharacters = computed(() => store.state.character.characters);
    const stageList = [
      "exposition",
      "incident",
      "conflict",
      "rising",
      "climax",
      "falling",
      "end",
    ];

    const delPlots = () => store.dispatch("delPlots");
    const delScenes = () => store.dispatch("delScenes");
    const addPlot = (plot) => store.dispatch("addPlot", plot);
    const addScene = (scene) => store.dispatch("addScene", scene);
    const updatePlot = (payload) => store.dispatch("updatePlot", payload);
    const movePlot = (payload) => store.dispatch("movePlot", payload);

    function AddPlot() {
      addDialogVisible.value = true;
    }

    function showDeleteDialog() {
      showDeleteConfirm.value = true;
    }

    function cancelDelete() {
      showDeleteConfirm.value = false;
    }

    function handleEditClose() {
      editDialogVisible.value = false;
    }

    function confirmDelete() {
      store.dispatch("deletePlot", plotToEditIndex.value);
      showDeleteConfirm.value = false;
      handleEditClose();
      ElMessage({
        type: "success",
        message: `成功删除情节`,
      });
    }

    async function handleDelete(index) {
      store.dispatch("deleteScene", index);

      await axios.post("/api/delete_scene_asset", {
        action: "delete_scene_asset",
        data: {
          index: index,
        },
      });
    }

    function handleAddDialogClose() {
      newPlot.plotName = "";
      newPlot.plotStage = "";
      newPlot.scene = "";
      newPlot.characters = [];
      newPlot.beat = "";
      newPlot.dialogue = [];
      addDialogVisible.value = false;
    }

    function handleEditDialogClose() {
      editPlotData.No = "";
      editPlotData.plotName = "";
      editPlotData.plotStage = "";
      editPlotData.scene = "";
      editPlotData.characters = [];
      editPlotData.beat = "";
      editPlotData.dialogue = [];
      editDialogVisible.value = false;
    }

    // eslint-disable-next-line no-unused-vars
    function changeSerial(No) {
      if (isNaN(Number(No, 10))) {
        ElMessage({
          message: "数字",
          type: "warning",
        });
        return;
      }
    }

    async function addNewPlot() {
      if (!newPlot.plotName) {
        ElMessage({
          message: "情节名称不能为空",
          type: "warning",
        });
        return;
      }

      if (!newPlot.scene) {
        ElMessage({
          message: "场景不能为空",
          type: "warning",
        });
        return;
      }

      console.log(newPlot.scene);

      if (newPlot.characters.length === 0) {
        console.log(newPlot);
        ElMessage({
          message: "角色不能为空",
          type: "warning",
        });
        return;
      }

      // 如果scene不是一个对象，说明是新建的场景
      if (typeof newPlot.scene !== "object") {
        const newScene = {
          name: newPlot.scene,
          content: "",
          image: null,
        };
        newPlot.scene = newScene;
        addScene({ ...newScene });
        await axios.post("/api/add_scene", {
          action: "add_scene",
          data: {
            scene: newScene,
          },
        });
      }

      const existingPlotIndex = plots.value.findIndex(
        (plot) => plot.plotName === newPlot.plotName
      );
      if (existingPlotIndex !== -1) {
        updatePlot({ index: existingPlotIndex, plot: { ...newPlot } });

        ElMessage({
          message: "更新成功",
          type: "success",
        });
      } else {
        addPlot({ ...newPlot });
        ElMessage({
          message: "添加成功",
          type: "success",
        });
      }

      handleAddDialogClose();
    }

    function editPlot(index) {
      beforeEditAsset.No = index + 1;
      // beforeEditAsset.plotName = plots.value[index].plotName;
      // beforeEditAsset.plotStage = plots.value[index].plotStage;
      // beforeEditAsset.scene = plots.value[index].scene;
      // beforeEditAsset.characters = plots.value[index].characters;
      beforeEditAsset.beat = plots.value[index].beat;
      // beforeEditAsset.dialogue = plots.value[index].dialogue;

      const plotToEdit = plots.value[index];
      editPlotData.No = index + 1;
      editPlotData.plotName = plotToEdit.plotName;
      editPlotData.plotStage = plotToEdit.plotStage;
      editPlotData.scene = plotToEdit.scene;
      editPlotData.characters = plotToEdit.characters;
      editPlotData.beat = plotToEdit.beat;
      editPlotData.dialogue = plotToEdit.dialogue;
      plotToEditIndex.value = index;
      editDialogVisible.value = true;
    }

    async function saveEditedPlot() {
      if (!editPlotData.plotName) {
        ElMessage({
          message: "情节名称不能为空",
          type: "warning",
        });
        return;
      }

      if (!editPlotData.scene) {
        ElMessage({
          message: "场景不能为空",
          type: "warning",
        });
        return;
      }

      if (editPlotData.characters.length === 0) {
        ElMessage({
          message: "角色不能为空",
          type: "warning",
        });
        return;
      }

      if (isNaN(Number(editPlotData.No, 10))) {
        ElMessage({
          message: "序号必须为数字",
          type: "warning",
        });
        return;
      }

      // plots.value[]
      let changes = "";
      diff
        .diffChars(beforeEditAsset.beat, editPlotData.beat)
        .forEach((part) => {
          const value = part.value.replace(/\n/g, "");
          if (part.added) {
            changes += `[${value}]`;
          } else if (part.removed) {
            changes += `{${value}}`;
          } else {
            changes += value;
          }
        });
      // 保存修改的记录,
      await axios.post("/api/save_changes", {
        action: "save_changes",
        data: {
          changes: changes,
        },
      });

      // 如果scene不是一个对象，说明是新建的场景
      if (typeof editPlotData.scene !== "object") {
        const newScene = {
          name: editPlotData.scene,
          content: "",
          image: null,
        };
        editPlotData.scene = newScene;
        addScene({ ...newScene });
        await axios.post("/api/add_scene", {
          action: "add_scene",
          data: {
            scene: newScene,
          },
        });
      }

      const updatedPlot = {
        plotName: editPlotData.plotName,
        plotStage: editPlotData.plotStage,
        scene: editPlotData.scene,
        characters: editPlotData.characters,
        beat: editPlotData.beat,
      };

      if (Number(editPlotData.No, 10) !== beforeEditAsset.No) {
        movePlot({
          fromIndex: beforeEditAsset.No - 1,
          toIndex: editPlotData.No - 1,
        });
        updatePlot({ index: editPlotData.No - 1, plot: updatedPlot });
      } else {
        updatePlot({ index: plotToEditIndex.value, plot: updatedPlot });
      }
      ElMessage({
        message: "情节更新成功",
        type: "success",
      });
      handleEditDialogClose();

      // if (plotToEditIndex.value !== null) {
      //   const updatedPlot = {
      //     plotName: editPlotData.plotName,
      //     plotStage: editPlotData.plotStage,
      //     scene: editPlotData.scene,
      //     characters: editPlotData.characters,
      //     beat: editPlotData.beat,
      //   };
      //   updatePlot({ index: plotToEditIndex.value, plot: updatedPlot });
      //   ElMessage({
      //     message: '情节更新成功',
      //     type: 'success',
      //   });
      //   handleEditDialogClose();
      // }
    }

    async function refreshData() {
      delPlots();
      delScenes();
    }

    async function generatePlot() {
      try {
        loading.value = true;
        const response = await axios.post("/api/init_plot_generation", {
          action: "init_plot_generation",
          data: {
            characters: store.state.character.characters,
          },
        });
        loading.value = false;
        await refreshData();
        addPlot(response.data);
        const scenes = response.data.reduce((acc, plot) => {
          if (!acc.find((scene) => scene.name === plot.scene.name)) {
            acc.push({
              name: plot.scene.name,
              content: plot.scene.content,
              image: null,
            });
          }
          return acc;
        }, []);
        store.dispatch("addScene", scenes);
      } catch (error) {
        ElMessage({
          message: "请求失败",
          type: "error",
        });
      }
    }

    async function UploadPlot() {
      const payload = {
        action: "update_plot",
        data: plots.value.map((plot) => ({
          plotName: plot.plotName,
          plotStage: plot.plotStage,
          scene: plot.scene,
          情节梗概: plot.beat,
          characters: plot.characters.map((character) => ({ name: character })),
        })),
      };

      try {
        await axios.post("/api/update_plot", payload);
        ElMessage({
          message: "上传成功",
          type: "success",
        });
      } catch (error) {
        ElMessage({
          message: "上传失败",
          type: "error",
        });
      }
    }

    return {
      addDialogVisible,
      editDialogVisible,
      plots,
      handleDelete,
      newPlot,
      stageList,
      editPlotData,
      showDeleteConfirm,
      allScenes,
      allCharacters,
      loading,
      AddPlot,
      handleAddDialogClose,
      handleEditDialogClose,
      addNewPlot,
      editPlot,
      saveEditedPlot,
      showDeleteDialog,
      cancelDelete,
      confirmDelete,
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
  background-color: #f1f1f1;
}

.header {
  background-color: #5973ff;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.plot {
  display: flex;
  background-color: #ffffff;
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
  border: 2px solid #5973ff;
  color: #bccfff;
  cursor: pointer;
  border-radius: 10px !important;
  transition:
    background-color 0.2s,
    color 0.2s;
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
  overflow: hidden;
  box-sizing: border-box;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 20px;
  padding-right: 20px;
}

.plots-list {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  border-radius: 20px;
  background-color: #f1f1f1;
}

.plot-item {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  background-color: #d5dcff;
}

.plot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.plot-name {
  display: flex;
  font-size: 18px;
  font-weight: bold;
}

.plot-element,
.location,
.characters {
  display: flex;
  align-items: center;
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
  background-color: #f1f1f1;
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
