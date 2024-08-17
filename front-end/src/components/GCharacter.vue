<template>
  <el-container class="main-container">
    <el-container class="character_panel">
      <el-header class="art-asset-header">
        <div class="art-asset">艺术资产-角色</div>
      </el-header>
      <el-container class="rightcontainer">
        <!-- <el-button-group class="button-container">
          <el-button class="asset-button" @click="selectTab('characters')"
                     :class="{ active: selectedTab === 'characters' }">角色</el-button>
        </el-button-group> -->
        <el-scrollbar class="assets-list">
          <el-card v-for="(asset, index) in charList" :key="index" 
            class="asset-item" 
            shadow="hover"
           @click="editAsset(index)" >
         <el-row :gutter="10" style="width: 100%;" align="middle">
              <el-col :span="4" style="text-align: center">
                <img v-if="asset.image" class="asset-image" :src="asset.image" />
                <img v-else class="asset-image" :src="require('@/assets/images/empty.png')"/>
              </el-col>
              <el-col :span="20"><div>{{ asset.name }}</div></el-col>
         </el-row>
          </el-card>
        </el-scrollbar>

        <el-footer class="add-button-container">
          <el-button class="addasset-button" @click="showAddDialog">新增</el-button>
          <el-button class="addasset-button" @click="upload">保存</el-button>
        </el-footer>
      </el-container>
    </el-container>

    <el-aside class="chatgpt_panel">
      <div class="chat">
        <el-header class="header">
          <div>【角色】智能助手</div>
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
        <el-footer>
          <el-input placeholder="向【角色】智能助手提问吧..." v-model="inputMessage" class="input-field"
                    @keyup.enter="sendMessage" clearable>
            <template #append>
              <el-button @click="sendMessage"><img class="upload-image" :src="require('@/assets/images/upload.png')"/></el-button>
            </template>
          </el-input>
        </el-footer>
      </div>
    </el-aside>

    <el-dialog title="新增资产" v-model="addDialogVisible" custom-class="dialog-content" v-loading="loading">
      <el-form :model="newAsset" label-width="100px" class="add-asset-form">
        <el-form-item label="分组">
          角色
        </el-form-item>
        <el-form-item label="资产名" :label-width="formLabelWidth">
          <el-input v-model="newAsset.name" autocomplete="off" />
        </el-form-item>

        <el-form-item v-if="newAsset.group === 'characters'" label="描述" :label-width="formLabelWidth">
          <el-input v-model="newAsset.content" autocomplete="off" />
        </el-form-item>

        <el-form-item label="音色">
          <el-select v-model="newAsset.per" placeholder="请选择角色音色">
            <el-option v-for="audio in audios" :key="audio" :label="audio" :value="audio" />
         </el-select>
       </el-form-item>
        
        <el-form-item v-if="newAsset.group === 'characters'" label="图片" :label-width="formLabelWidth">
          <div>
            <el-upload :http-request="uploadFile"
                       list-type="picture-card"
                       :on-success="handleUploadSuccess"
                       v-model:file-list="fileList"
                       :on-remove="handleRemove"
                        :on-preview="handlePictureCardPreview"
                       :on-exceed="handleExceed">
              <i class="el-icon-plus"></i>
            </el-upload>
            <el-button @click="generate_image" class="confirm-button">生成</el-button>
            <el-button @click="save_image" class="confirm-button">保存</el-button>
          </div>
        </el-form-item>

        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button">取消</el-button>
          <el-button type="primary" @click="addNewAsset" class="confirm-button">确定</el-button>
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog :title="'保存 ' + curSaveType" v-model="showSaveDialog" custom-class="dialog-content">
      <el-form-item label="类型">
        {{ curSaveType }}
      </el-form-item>

      <el-form-item label="分组">
        <el-select v-model="newAsset.group" placeholder="选择分组" @change="changeGroup">
          <el-option label="角色" value="characters" />
        </el-select>
      </el-form-item>
      <el-form-item label="资产名" :label-width="formLabelWidth">
        <el-select v-if="newAsset.group" v-model="newAsset.name" placeholder="选择名字">
          <el-option v-for="(asset, index) in curGroup" :key="index" :label="asset.name" :value="asset.name" />
        </el-select>
        <el-input v-model="newAsset.name" autocomplete="off" />
      </el-form-item>

      <el-footer class="dialog-footer">
        <el-button @click="handleSaveClose" class="cancel-button">取消</el-button>
        <el-button type="primary" @click="saveAssetConfirm(newAsset.group, newAsset.name)"
                   class="confirm-button">确认</el-button>
      </el-footer>
    </el-dialog>


    <el-dialog title="编辑资产" v-model="showEditDialog" custom-class="dialog-content">
      <el-form-item label="分组" :label-width="formLabelWidth">
        角色
      </el-form-item>

      <el-form-item label="资产名" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="描述" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.content" autocomplete="off" />
      </el-form-item>

      <el-form-item label="音色">
          <el-select v-model="currentEditAsset.per" placeholder="请选择角色音色">
            <el-option v-for="audio in audios" :key="audio" :label="audio" :value="audio" />
          </el-select>
        </el-form-item>


      <el-form-item label="图片" :label-width="formLabelWidth" >
        <div v-loading="loading">
        <el-upload :http-request="uploadFile"
                   list-type="picture-card"
                   :on-success="handleUploadSuccess"
                   :file-list="fileList"
                   show-file-list="true"

                   :on-remove="handleEditRemove"
                   :on-exceed="handleExceed">
          <i class="el-icon-plus"></i>

        </el-upload>
        <el-button @click="generate_image" class="confirm-button">生成</el-button>
        </div>
      </el-form-item>

      <el-footer class="dialog-footer">
        <el-button @click="handleEditClose" class="cancel-button">取消</el-button>
        <el-button type="danger" @click="showDeleteDialog" class="delete-button">删除</el-button>
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
import { useStore } from 'vuex';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import * as diff from 'diff';

export default defineComponent({
  name: 'GCharacter',

  setup() {
    const { proxy } = getCurrentInstance();

    // State and reactive properties
    const addDialogVisible = ref(false);
    const showSaveDialog = ref(false);
    const showEditDialog = ref(false);
    const curSaveType = ref('');
    const curSaveThing = ref('');
    const loading = ref(false);
    const curEditAssetIndex = ref('');
    const fileList = ref([]);
    const inputMessage = ref('');
    const selectedTab = ref('characters');
    const history = ref([]);
    const messages = ref([]);
    const showDeleteConfirm = ref(false);
    const newAsset = reactive({
      group: 'characters',
      name: '',
      content: '',
      image: '',
    });
    const beforeEditAsset = reactive({
      name: '',
      content: '',
    });
    const store=useStore()
    const audios = {
      0:"标准女音",
      1:"标准男音",
      // 3:"斯文男音",
      // 4:"小萌萌",
      // 5:"知性女音",
      // 6:"老教授",
      // 9:"播音员",
      // 10:"京腔",
      // 11:"温柔大叔",
    }
    const currentEditAsset = reactive({
      name: '',
      content: '',
      per: '',
      image: '',
    });
    const tableData = [
  {
    date: '2016-05-02',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]
    // Computed properties
    // const currentEditAsset = computed(() => {
    //   return charList[curEditAssetIndex.value] || { name: '', content: '', image: '' };
    // });

    const filteredAssets = computed(() => {
      return charList;
    });


    const charList=computed(()=>{
      console.log(store.state.character.characters);
      return store.state.character.characters
    })


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
        action: 'get_character_help',
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
        const response = await axios.post('http://localhost:8000/get_character_help', requestBody);
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

          // const imageRequestBody = {
          //   action: 'get_character_image_help',
          //   data: {
          //     history: history.value.map((msg) => ({
          //       role: msg.role,
          //       content: msg.content,
          //     })),
          //     user_input: inputMessage.value,
          //   },
          // };

        //   const imageResponse = await axios.post('http://localhost:8000/get_character_image_help', imageRequestBody);
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

    function handlePictureCardPreview(file){
      charList.value[curEditAssetIndex.value].image = file.url;
    }

    function handleAddDialogClose() {
      newAsset.group = 'characters';
      newAsset.name = '';
      newAsset.content = '';
      newAsset.image = '';
      fileList.value = [];
      addDialogVisible.value = false;
    }

    const handleRemove = () => {
      newAsset.image = '';
    };

    const handleEditRemove = () => {
      currentEditAsset.image = '';
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

    function addNewAsset() {
      let charactersList=store.state.character.characters
      if (!newAsset.name) {
        proxy.$message.warning('资产名不能为空');
        return;
      }
      if (charactersList.some((asset) => asset.name === newAsset.name)) {
        proxy.$message.warning('资产名已存在');
        return;
      }
      if (!newAsset.per) {
        proxy.$message.warning('请选择音色');
        return;
      }

      const character = {
        name: newAsset.name,
        content: newAsset.content,
        image: newAsset.image || null,
        per: newAsset.per,
      };
      store.dispatch('addCharacter',character)
      handleAddDialogClose();
      proxy.$message.success('资产新增成功');
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

      const assetIndex = charList.value.findIndex((asset) => asset.name === name);
      if (assetIndex !== -1) {
        if (curSaveType.value === 'image') {
          charList[assetIndex].image = curSaveThing.value;
        } else {
          charList[assetIndex].content = curSaveThing.value;
        }
        store.dispatch('updateCharacter', { index: assetIndex, character: charList[assetIndex] });
        proxy.$message.success('资产更新成功');
      } else {
        console.log(curSaveThing.value);
        const newAsset = {
          name: name,
          image: curSaveType.value === 'image' ? curSaveThing.value : null,
          content: curSaveType.value === 'content' ? curSaveThing.value : '',
        };
        store.dispatch('addCharacter',newAsset)
        proxy.$message.success('新资产添加成功');
      }
      // showSaveDialog.value = false;
    }

    function editAsset(index) {
      if(charList.value[index].image){
        fileList.value = [{
          name: charList.value[index].name,
          url: charList.value[index].image,
        }]
      }

      curEditAssetIndex.value = index;
      currentEditAsset.name = charList.value[index].name;
      currentEditAsset.content = charList.value[index].content;
      currentEditAsset.per = charList.value[index].per;
      currentEditAsset.image = charList.value[index].image;
      beforeEditAsset.name = charList.value[index].name;
      beforeEditAsset.content = charList.value[index].content;
    
      console.log(currentEditAsset);
      showEditDialog.value = true;
    }

    const uploadFile = (options) => {
      const formData = new FormData();
      formData.append('action', 'save_character_asset_image');
      formData.append('character_name', newAsset.name);
      formData.append('character_image', options.file);

      axios.post('http://localhost:8000/update_character_asset_image', formData)
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
      const name = charList.value[curEditAssetIndex.value].name;
      store.dispatch('deleteCharacter',curEditAssetIndex.value)
      await axios.post('http://localhost:8000/delete_character', {
        action: 'delete_character',
        data: {
          index: curEditAssetIndex.value,
        },
      });
      showDeleteConfirm.value = false;
      handleEditClose();
      ElMessage({
        type: 'success',
        message: `成功删除资产 "${name}"`,
      });
    }

    function getImageSrc(image) {
      return image ? image : '@/assets/images/logo.png';
    }

    function handleUploadSuccess(response) {
      if (response.success) {
        charList[curEditAssetIndex.value].image = response.filePath;
        store.dispatch('updateCharacter', { index: curEditAssetIndex.value, character: charList[curEditAssetIndex.value] });
      }
    }

    

    async function saveEditedAsset() {
      console.log(beforeEditAsset);
      // add的用[]包裹, remove的用{}包裹
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
      const editedAsset = JSON.parse(JSON.stringify(currentEditAsset));
      if (!editedAsset.name) {
        proxy.$message.warning('资产名不能为空');
        return;
      }
      if (!editedAsset.content) {
        proxy.$message.warning('描述不能为空');
        return;
      }
      if (!editedAsset.per) {
        proxy.$message.warning('请选择音色');
        return;
      }
      // if (!editedAsset.image) {
      //   proxy.$message.warning('请上传图片');
      //   return;
      // }
      store.dispatch('updateCharacter', { index: curEditAssetIndex.value, character: editedAsset });
      await axios.post('http://localhost:8000/update_character', {
        action: 'update_character',
        data: {
          index: curEditAssetIndex.value, character: editedAsset 
        },
      });
      proxy.$message.success('资产更新成功');
      showEditDialog.value = false;   
    }

    async function generate_image() {
      loading.value = true;
      const imageRequestBody = {
            action: 'create_character_picture',
            data: {
              name: currentEditAsset.name,
              content: currentEditAsset.content,
            },
          };
          const imageResponse = await axios.post('http://localhost:8000/create_character_picture', imageRequestBody);
          fileList.value.push({
            name: currentEditAsset.name,
            url: imageResponse.data.image,
          });
          loading.value = false;
          console.log(fileList.value);
          newAsset.image = imageResponse.data.image;
          currentEditAsset.image = imageResponse.data.image;
          charList.value[curEditAssetIndex.value].image = imageResponse.data.image;
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
      curSaveThing,
      showEditDialog,
      curEditAssetIndex,
      showDeleteConfirm,
      handleSaveClose,
      handleRemove,
      handleEditRemove,
      tableData,
      handleExceed,
      sendMessage,
      showAddDialog,
      handleAddDialogClose,
      addNewAsset,
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
      handlePictureCardPreview,
      generate_image,
      loading,
      charList,
      audios,
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

.llm{
  display: flex;
  align-items: top;
  margin: 10px 0;
  gap: 10px;
  height: 40px;
  width: 40px;
}

.el-main {
  padding:10px;
}

.main-container {
  display: flex;
  height: 88vh;
  width: 100%;
  gap: 20px;
  padding: 30px;
  overflow: hidden;
  box-sizing: border-box;
  background-color: #F1f1f1;
}

.chatgpt_panel {
  flex: 1;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.character_panel {
  flex: 3;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  width: 100%;
}

.rightcontainer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.upload-image {
  width: 15px;
  height: auto;
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
  gap: 10px
}

.llm {
  margin-right: 10px;
}

.character-image {
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
.upload-button:hover {
  background-color: #93a2f7;
  color: white;
}

.upload-button:active {
  background-color: #3a51d4;
  color: white;
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
.asset-button.hover {
  background-color: #939dd3;
  border-radius: 10px;
  color: white;
}
.asset-button.active {
  background-color: #5973FF;
  border-radius: 10px;
  color: white;
}

.assets-list {
  height: 100%;
  width:100%;
  flex: 1;
  overflow: hidden;
  padding: 20px;
  box-sizing: border-box;
}

.asset-item {
  /* display: flex; */
  align-items: center; 
  margin: 15px;
  padding: 10px;
  height: 80px;
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

.asset-image {
  border-radius: 50%;
  width: 50px;
  height: 50px; 
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
.addasset-button:hover {
  background-color: #BCCFFF;
  color: white;
}

.addasset-button:active {
  background-color: #5973FF;
  color: white;
  transform: scale(0.95);
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

body {
  margin: 0;
}
.example-showcase .el-loading-mask {
  z-index: 9;
}
</style>