<template>
  <el-container class="main-container">
    <el-container class="scene-panel">
      <el-header class="art-asset-header">
        <div class="art-asset">艺术资产-场景</div>
      </el-header>
      <el-container class="rightcontainer">
<!--        <el-button-group class="button-container">-->
<!--          <el-button class="asset-button" @click="selectTab('scene')"-->
<!--                     :class="{ active: selectedTab === 'scene' }">场景</el-button>-->
<!--        </el-button-group>-->

        <el-scrollbar class="assets-list">
          <el-card v-for="(asset, index) in sceneList" :key="index" 
           class="asset-item" 
           shadow="hover"
          @click="editAsset(index)">
           <el-row :gutter="10" style="width: 100%;" align="middle">
              <el-col :span="10" style="text-align: center">
                <img v-if="asset.image" class="asset-image" :src="asset.image" >
                <img v-else class="asset-image" :src="require('@/assets/images/empty.png')">
              </el-col>
              <el-col :span="14"><div>{{ asset.name }}</div></el-col>
           </el-row>
          </el-card>
        </el-scrollbar>

        <el-footer class="add-button-container">
          <el-button class="addasset-button" @click="upload">保存</el-button>
        </el-footer>
      </el-container>
    </el-container>

    <el-aside class="chat-panel">
      <div class="chat">
        <el-header class="header">
          <div>【场景】智能助手</div>
        </el-header>
        <el-main>
          <div class="message" v-for="(message, index) in messages" :key="index">
            <el-row :gutter="5" align="middle">
              <!-- <el-col :span="message.prompt.length > 0 ?0: 19-message.prompt.length"></el-col>
              <el-col :span="message.prompt.length > 0 ?24: 5+message.prompt.length"> -->
                <div class="human-iutput" >
                {{ message.prompt }} </div>
              <!-- </el-col> -->
            </el-row>
            <br>
            <el-row align="top">
              <el-col :span="4"><el-avatar :src="require('@/assets/images/operalogo.jpg')" class="llm"></el-avatar></el-col>
              <el-col :span="20"><div class="AI-output">{{ message.content }}</div></el-col>
            </el-row>
          </div>
        </el-main>
        <el-footer class="inputfooter">
          <el-input placeholder="向【场景】智能助手提问吧..." v-model="inputMessage" class="input-field"
                    @keyup.enter="sendMessage" clearable>
            <template #append>
              <el-button @click="sendMessage"><img class="upload-image" :src="require('@/assets/images/upload.png')"/></el-button>
            </template>
          </el-input>
         </el-footer>
      </div>
    </el-aside>

    <el-dialog title="编辑资产" v-model="showEditDialog" custom-class="dialog-content">
      <el-form-item label="分组" :label-width="formLabelWidth">
        场景
      </el-form-item>

      <el-form-item label="资产名" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="描述" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.content" autocomplete="off" />
      </el-form-item>

      <el-form-item label="图片" :label-width="formLabelWidth">
        <div v-loading="loading">
        <el-upload :http-request="uploadFile"
                   list-type="picture-card"
                   :on-success="handleUploadSuccess"
                   v-model:file-list="fileList"
                   :on-preview="handlePictureCardPreview"
                   :on-remove="handleRemove"
                   :on-exceed="handleExceed">
          <i class="el-icon-plus"></i>
        </el-upload>
        <el-button @click="generate_image" class="confirm-button">生成</el-button>
        <el-button @click="save_image" class="confirm-button">保存</el-button>
        </div>
      </el-form-item>

      <el-footer class="dialog-footer">
        <el-button @click="handleEditClose" class="cancel-button">取消</el-button>
<!--        <el-button type="danger" @click="showDeleteDialog" class="delete-button">删除</el-button>-->
        <el-button type="primary" @click="saveEditedAsset" class="confirm-button">确定</el-button>
      </el-footer>

      <el-dialog v-model="showDeleteConfirm">
        <div>你确认删除该资产吗？</div>
        <span class="dialog-footer">
          <el-button @click="cancelDelete" class="cancel-button">取消</el-button>
          <el-button type="danger" @click="confirmDelete" class="confirm-button">确定</el-button>
        </span>
      </el-dialog>
    </el-dialog>
  </el-container>
</template>


<script>
import { defineComponent, ref, reactive, computed, getCurrentInstance } from 'vue';
import { mapActions,useStore } from 'vuex';
import axios from 'axios';
import * as diff from 'diff';
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'GScene',

  setup() {
    const { proxy } = getCurrentInstance();

    // State and reactive properties
    const addDialogVisible = ref(false);
    const showSaveDialog = ref(false);
    const showEditDialog = ref(false);
    const curSaveType = ref('');
    const curSaveThing = ref('');
    const curEditAssetIndex = ref('');
    const fileList = ref([]);
    const inputMessage = ref('');
    const selectedTab = ref('scene');
    const history = ref([]);
    const loading = ref(false);
    const messages = ref([]);
    const showDeleteConfirm = ref(false);
    const sceneList=computed(()=>{
      return store.state.scene.scenes
    })
    const newAsset = reactive({
      group: 'scenes',
      name: '',
      content: '',
      image: null,
    });
    const beforeEditAsset = reactive({
      name: '',
      content: '',
    });
    const store=useStore();
    const currentEditAsset = reactive({
      group: 'scenes',
      name: '',
      content: '',
      image: null,
    });

    // Computed properties
    // const currentEditAsset = computed(() => {
    //   return Scenedata[curEditAssetIndex.value] || { name: '', content: '', image: '' };
    // });

    const filteredAssets = computed(() => {
      return scenes;
    });

    const scenes=computed(()=>{
      return store.state.scene.scenes
    });

    
    function handlePictureCardPreview(file){
      sceneList.value[curEditAssetIndex.value].image = file.url;
    }


    const actions = mapActions('scene', [
      'addScene',
      'deleteScene',
    ]);

    // const addScene = (scene) => store.dispatch('addScene', scene);
    const updateScene = (payload) => store.dispatch('updateScene', payload);
    // const deleteScene = (index) => store.dispatch('updateScene', index);

    // Functions
    async function sendMessage() {
      if (!inputMessage.value) {
        ElMessage({
          message: '输入不能为空',
          type: 'warning',
        });
        return;
      }

      const userMessage = {
        role: 'user',
        content: inputMessage.value,
      };
      history.value.push(userMessage);

      const requestBody = {
        action: 'get_scene_help',
        data: {
          history: history.value.map((msg) => ({
            role: msg.role,
            content: msg.content,
          })),
          user_input: inputMessage.value,
        },
      };

      const assistantMessage = {
            role: 'assistant',
            prompt: inputMessage.value,
            content: "loading...",
            image: 'logo.png',
            downloadIcon: true,
          };
      messages.value.push(assistantMessage);

      try {
        const response = await axios.post('http://localhost:8000/get_scene_help', requestBody);
        if (response.status === 200) {
          const assistantMessage = {
            role: 'assistant',
            prompt: inputMessage.value,
            content: response.data.answer,
            image: 'logo.png',
            downloadIcon: true,
          };
          messages.value.splice(messages.value.length - 1, 1, assistantMessage);
          history.value.push(assistantMessage);

        //   const imageRequestBody = {
        //     action: 'get_scene_image_help',
        //     data: {
        //       history: history.value.map((msg) => ({
        //         role: msg.role,
        //         content: msg.content,
        //       })),
        //       user_input: inputMessage.value,
        //     },
        //   };

        //   const imageResponse = await axios.post('http://localhost:8000', imageRequestBody);
        //   if (imageResponse.status === 200 && imageResponse.data.image) {
        //     const index = messages.value.indexOf(assistantMessage);
        //     if (index !== -1) {
        //       messages.value[index].image = imageResponse.data.image;
        //     }
        //   }
        //   inputMessage.value = '';
        // } else {
        //   ElMessage({
        //     message: '请求失败',
        //     type: 'error',
        //   });
        }
      } catch (error) {
        ElMessage({
          message: '请求失败',
          type: 'error',
        });
      }
    }

    function selectTab(tab) {
      selectedTab.value = tab;
    }

    function showAddDialog() {
      addDialogVisible.value = true;
    }

    function handleAddDialogClose() {
      newAsset.group = 'scenes';
      newAsset.name = '';
      newAsset.content = '';
      newAsset.image = null;
      fileList.value = [];
      addDialogVisible.value = false;
    }

    const handleRemove = () => {
      newAsset.image = null;
    };

    const handleExceed = () => {
      proxy.$message.warning('只能上传一个附件');
    };

    function handleSaveClose() {
      newAsset.group = '';
      newAsset.name = '';
      newAsset.content = '';
      newAsset.image = '';
      fileList.value = [];
      showSaveDialog.value = false;
    }

    function saveAsset(Type, content) {
      curSaveType.value = Type;
      curSaveThing.value = content;
      showSaveDialog.value = true;
    }

    function saveAssetConfirm(group, name) {
      if (!name) {
        proxy.$message.warning('资产名为空');
        return;
      }

      const assetIndex = scenes.value.findIndex((asset) => asset.name === name);
      if (assetIndex !== -1) {
        if (curSaveType.value === 'image') {
          scenes[assetIndex].image = curSaveThing.value;
        } else {
          scenes[assetIndex].content = curSaveThing.value;
        }
        actions.updateScene({ index: assetIndex, scene: scenes[assetIndex] });

        proxy.$message.success('资产更新成功');
      } else {
        const newAsset = {
          name: name,
          url: curSaveType.value === 'image' ? curSaveThing.value : 'empty.png',
          content: curSaveType.value === 'content' ? curSaveThing.value : '',
        };
        actions.addScene(newAsset);
        proxy.$message.success('新资产添加成功');
      }
      showSaveDialog.value = false;
    }

    function editAsset(index) {
      beforeEditAsset.name = scenes.value[index].name;
      beforeEditAsset.content = scenes.value[index].content;
      if(sceneList.value[index].image !== '') {
        fileList.value = [{
          name: sceneList.value[index].name,
          url: sceneList.value[index].image,
        }]
      }
      curEditAssetIndex.value = index
      currentEditAsset.name = scenes.value[index].name;
      currentEditAsset.content = scenes.value[index].content;
      currentEditAsset.image = scenes.value[index].image;
      showEditDialog.value = true;
    }

    const uploadFile = async (options) => {
      const formData = new FormData();
      formData.append('action', 'save_scene_asset_image');
      formData.append('scene_name', newAsset.name);
      formData.append('scene_content', newAsset.content);
      formData.append('scene_image', options.file);

      await axios.post('http://localhost:8000/save_scene_asset', formData)
        .then((response) => {
          if (response.data.success) {
            newAsset.image = response.data.filePath;
            options.onSuccess(response.data, options.file);
          } else {
            options.onError(new Error('Upload failed'));
          }
        })
        .catch((error) => {
          options.onError(error);
        });
    };

    function handleEditClose() {
      showEditDialog.value = false;
    }

    function showDeleteDialog() {
      showDeleteConfirm.value = true;
    }

    function cancelDelete() {
      showDeleteConfirm.value = false;
    }

    async function confirmDelete() {
      actions.deleteScene(curEditAssetIndex.value);
      await axios.post('http://localhost:8000/delete_scene_asset', {
        action: 'delete_scene_asset',
        data: {
          index: curEditAssetIndex.value,
        },
      });
      showDeleteConfirm.value = false;
      handleEditClose();
      ElMessage({
        type: 'success',
        message: `成功删除资产 "${currentEditAsset.value.name}"`,
      });
    }

    function getImageSrc(image) {
      return image ? image : '@/assets/images/logo.png';
    }

    function handleUploadSuccess(response) {
      if (response.success) {
        scenes[curEditAssetIndex.value].image = response.filePath;
        actions.updateScene({ index: curEditAssetIndex.value, scene: scenes[curEditAssetIndex.value] });
      }
    }

    async function saveEditedAsset() {
      // const editedAsset = Scenedata[curEditAssetIndex.value];
      let changes = ""
      diff.diffChars(beforeEditAsset.content, currentEditAsset.content).forEach((part) => {
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
      if (!currentEditAsset.name) {
        proxy.$message.warning('资产名不能为空');
        return;
      }
      if (!currentEditAsset.content) {
        proxy.$message.warning('描述不能为空');
        return;
      }
      // if (!currentEditAsset.image) {
      //   proxy.$message.warning('请上传图片');
      //   return;
      // }
      console.log(currentEditAsset)
      const currentPlot = store.state.plot.plots[curEditAssetIndex.value]
      console.log(currentPlot);
      currentPlot.scene = {...currentEditAsset}
      updateScene({ index: curEditAssetIndex.value, scene: { ...currentEditAsset } });
      store.dispatch('updatePlot', { index: curEditAssetIndex.value,  plot: currentPlot });
      await axios.post('http://localhost:8000/save_scene_asset', {
          action: 'save_scene_asset',
          data: {
            index: curEditAssetIndex.value, scene: currentEditAsset
          },
        });
      proxy.$message.success('资产更新成功');
      showEditDialog.value = false;
    }

    async function generate_image() {
      loading.value = true;
      const imageRequestBody = {
            action: 'create_scene_picture',
            data: {
              name: currentEditAsset.name,
              user_input: currentEditAsset.content,
            },
          };

          const imageResponse = await axios.post('http://localhost:8000/create_scene_picture', imageRequestBody);
          sceneList.value[curEditAssetIndex.value] = {
            name: currentEditAsset.name,
            url: imageResponse.data.image,
          }
          loading.value = false;
          currentEditAsset.image = imageResponse.data.image;
          fileList.value.push({
            name: currentEditAsset.name,
            url: imageResponse.data.image,
          });
          newAsset.image = imageResponse.data.image;
      }

    return {
      currentEditAsset,
      fileList,
      addDialogVisible,
      inputMessage,
      selectedTab,
      messages,
      newAsset,
      filteredAssets,
      showSaveDialog,
      curSaveType,
      loading,
      curSaveThing,
      showEditDialog,
      curEditAssetIndex,
      showDeleteConfirm,
      handleSaveClose,
      handleRemove,
      handleExceed,
      sendMessage,
      showAddDialog,
      handlePictureCardPreview,
      handleAddDialogClose,
      selectTab,
      saveAsset,
      saveAssetConfirm,
      editAsset,
      uploadFile,
      handleEditClose,
      handleUploadSuccess,
      saveEditedAsset,
      getImageSrc,
      showDeleteDialog,
      cancelDelete,
      confirmDelete,
      generate_image,
      ...actions,
      scenes,
      sceneList,
      // ...mapState('scene', ['scenes']),
    };
  },
});
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

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

.upload-image {
  width: 15px;
  height: auto;
}

.el-main {
  padding:10px;
}

.chat-panel {
  flex: 1;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.scene-panel {
  flex: 3;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.rightcontainer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.header {
  background-color: #5973FF;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.chat {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin: 10px;
}

.message-header {
  font-weight: bold;
}

.llm-wrapper {
  display: flex;
  align-items: center;
  margin: 10px 0;
  gap: 10px;
}

.llm {
  margin-right: 10px;
}

.scene-image {
  width: 100%;
  max-width: 400px;
  border-radius: 15px;
}

.loading-wrapper {
  width: 100%;
  text-align: center;
}

.input-field {
  width: 100%;
}

.art-asset-header {
  background-color: #5973FF;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.button-container {
  display: flex;
  justify-content: space-around;
  margin: 10px;
  padding: 10px;
  gap: 10px;
  text-align: center;
  box-sizing: border-box;
}

.asset-button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: #BCCFFF;
  color: white;
  border: 2px solid #5973FF;
  cursor: pointer;
  border-radius: 10px !important;
  transition: background-color 0.2s, color 0.2s;
}

.asset-button.active {
  background-color: #5973FF;
  border-radius: 10px;
  color: white;
}

.assets-list-container {
  flex: 1;
  height: calc(100vh - 200px);
  overflow: hidden;
  padding: 10px;
  box-sizing: border-box;
}

.assets-list {
  height: 100%;
  width:100%;
  flex: 1;
  overflow: hidden;
  padding: 20px;
  box-sizing: border-box;
}

.el-scrollbar__wrap {
  height: 100% !important;
  max-height: 300px;
  overflow-y: auto;
}

.asset-item {
  align-items: center; 
  margin: 15px;
  padding: 10px;
  height: auto;
}

.asset-image {
  border-radius: 5px;
  width: 200px;
  height: 80px; 
  border: 2px solid #ddd
}

.add-button-container {
  display: flex;
  position: relative;
  justify-content: right;
  padding: 10px;
}

.addasset-button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: white;
  border: 2px solid #5973FF;
  color: #BCCFFF;
  cursor: pointer;
  border-radius: 10px !important;
  transition: background-color 0.2s, color 0.2s;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  z-index: 1001;
  width: 30% !important;
  display: flex;
  justify-content: center;
  align-items: center;
}

.add-asset-form {
  padding: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
}

.cancel-button {
  background-color: #F1F1F1;
  color: #333;
}

.confirm-button {
  background-color: #5973FF;
  color: white;
}


.human-iutput{
  display: inline-flex;
  justify-content: flex-start; 
  word-wrap: break-all; 
  padding: 10px;
  line-height: 20px;
  border-radius: 5px;
  min-width: 90%;
  background-color: #D5DCFF;
}

.AI-output{
  padding: 5px;
  line-height: 20px;
  border-radius: 10px;
}

</style>