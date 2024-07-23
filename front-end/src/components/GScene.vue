<template>
  <el-container class="main-container">
    <el-aside class="left-panel">
      <div class="chat">
        <el-header class="header">
          <div class="asset-name">“CHAT”</div>
        </el-header>
        <el-main>
          <el-card class="message" v-for="(message, index) in messages" :key="index">
            <template #header>
              <div class="message-header">{{ message.prompt }}</div>
            </template>
            <el-container>
              <el-aside width="100px">
                <el-avatar icon="el-icon-user" class="llm"></el-avatar>
              </el-aside>
              <el-main width="200px">
                <el-row class="llm-wrapper">
                  <el-icon v-if="message.downloadIcon" :size="15" class="generated-icon">
                    <Download @click="saveAsset('image', message.image)" />
                  </el-icon>
                  <img v-if="message.image" class="character-image" :src="require('@/assets/images/' + message.image)"
                    alt="Character" />
                  <div v-else class="loading-wrapper">
                    <el-loading :loading="true" text="loading......" />
                  </div>
                </el-row>
                <el-row class="llm-wrapper">
                  <el-icon v-if="message.downloadIcon" :size="15" class="generated-icon">
                    <Download @click="saveAsset('content', message.content)" />
                  </el-icon>
                  <div class="message-content">{{ message.content }} </div>
                </el-row>
              </el-main>
            </el-container>
          </el-card>
        </el-main>
        <el-footer class="inputfooter">
          <el-input placeholder="Type your message here..." v-model="inputMessage" class="input-field"
            @keyup.enter="sendMessage" clearable>
            <template #append>
              <el-button icon="el-icon-upload2" @click="sendMessage"></el-button>
            </template>
          </el-input>
        </el-footer>
      </div>
    </el-aside>
    <el-container class="right-panel">
      <el-header class="art-asset-header">
        <div class="art-asset">Art Asset</div>
      </el-header>
      <el-container class="rightcontainer">
        <el-button-group class="button-container">
          <el-button class="asset-button" @click="selectTab('locations')" :class="{ active: selectedTab === 'locations' }">Locations</el-button>
        </el-button-group>
        <el-main class="assets-list-container">
          <el-scrollbar class="assets-list">
            <el-card v-for="(asset, index) in filteredAssets" :key="index" class="asset-item" @click="editAsset(index)">
              <div class="asset-name">{{ asset.name }}</div>
              <img class="asset-image" :src="require('@/assets/images/' + asset.image)" alt="Asset Image" />
            </el-card>
          </el-scrollbar>
        </el-main>
        <el-footer class="add-button-container">
          <el-button class="addasset-button" @click="showAddDialog">Add</el-button>
          <el-button class="addasset-button">Upload</el-button>
        </el-footer>
      </el-container>
    </el-container>

    <el-dialog title="Add Asset" v-model="addDialogVisible" custom-class="dialog-content">
      <el-form :model="newAsset" :rules="rules" ref="addAssetForm" label-width="100px" class="add-asset-form">
        <el-form-item label="Group" prop="group">
          <el-select v-model="newAsset.group" placeholder="Select group">
            <el-option label="Characters" value="characters" />
            <el-option label="Locations" value="locations" />
          </el-select>
        </el-form-item>
        <el-form-item label="Asset Name" prop="name">
          <el-input v-model="newAsset.name" autocomplete="off" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button">Cancel</el-button>
          <el-button type="primary" @click="addNewAsset" class="confirm-button">Confirm</el-button>
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog :title="'Save ' + curSaveType" v-model="showSaveDialog" custom-class="dialog-content">
      <el-form-item label="type">
        {{ curSaveType }}
      </el-form-item>
      <el-form-item label="group">
        <el-select v-model="newAsset.group" placeholder="Select group" @change="changeGroup">
          <el-option label="Characters" value="characters" />
          <el-option label="Locations" value="locations" />
        </el-select>
      </el-form-item>
      <el-form-item label="Asset Name" :label-width="formLabelWidth">
        <el-select v-if="newAsset.group" v-model="newAsset.name" placeholder="Select Name">
          <el-option v-for="(asset, index) in curGroup" :key="index" :label="asset.name" :value="asset.name" />
        </el-select>
        <el-input v-model="newAsset.name" autocomplete="off" />
      </el-form-item>
      <el-footer class="dialog-footer">
        <el-button @click="handleSaveClose" class="cancel-button">Cancel</el-button>
        <el-button type="primary" @click="saveAssetConfirm(newAsset.group, newAsset.name)" class="confirm-button">Confirm</el-button>
      </el-footer>
    </el-dialog>

    <el-dialog title="Edit Asset" v-model="showEditDialog" custom-class="dialog-content">
      <el-form :model="curGroup[curEditAssetIndex]" :rules="rules" ref="editAssetForm" label-width="100px">
        <el-form-item label="Group">
          <el-input v-model="curGroup[curEditAssetIndex].group" autocomplete="off" disabled />
        </el-form-item>
        <el-form-item label="Asset Name" prop="name">
          <el-input v-model="curGroup[curEditAssetIndex].name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Description" prop="content">
          <el-input v-model="curGroup[curEditAssetIndex].content" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Image">
          <img class="asset-image" :src="require('@/assets/images/' + curGroup[curEditAssetIndex].image)" alt="Asset Image" />
        </el-form-item>
        <el-footer class="dialog-footer">
          <el-button @click="handleEditClose" class="cancel-button">Cancel</el-button>
          <el-button type="primary" @click="saveEditedAsset" class="confirm-button">Confirm</el-button>
        </el-footer>
      </el-form>
    </el-dialog>
  </el-container>
</template>

<script>
import { defineComponent, ref, reactive, computed } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'GCharacter',
  setup() {
    const store = useStore();
    const addDialogVisible = ref(false);
    const showSaveDialog = ref(false);
    const showEditDialog = ref(false);
    const curSaveType = ref('');
    const curSaveThing = ref('');
    const curGroup = ref([]);
    const curEditAssetIndex = ref('');
    const inputMessage = ref('');
    const selectedTab = ref('locations');
    const messages = ref([]);
    const newAsset = reactive({ group: '', name: '' });

    const rules = {
      group: [
        { required: true, message: 'Please select a group', trigger: 'change' },
      ],
      name: [
        { required: true, message: 'Please input the asset name', trigger: 'blur' },
      ],
    };

    const allAssets = computed(() => store.getters['scene/scenes'] || []);
    const filteredAssets = computed(() => {
      const assets = allAssets.value;
      return assets ? assets.filter(asset => asset.group === selectedTab.value) : [];
    });

    function sendMessage() {
      if (inputMessage.value) {
        messages.value.push({
          prompt: inputMessage.value,
          content: "Generating...",
          image: ""
        });
        generateContent(messages.value.length - 1);
        inputMessage.value = '';
      }
    }

    function generateContent(index) {
      const message = messages.value[index];
      setTimeout(() => {
        message.content = '等以后生成';
        message.image = "test_asset.png";
        message.downloadIcon = true;
      }, 1000);
    }

    function selectTab(tab) {
      selectedTab.value = tab;
    }

    function showAddDialog() {
      addDialogVisible.value = true;
    }

    function handleAddDialogClose() {
      newAsset.group = '';
      newAsset.name = '';
      addDialogVisible.value = false;
    }

    function handleSaveClose() {
      newAsset.group = '';
      newAsset.name = '';
      showSaveDialog.value = false;
    }

    function addNewAsset() {
      const addAssetForm = ref(null);
      addAssetForm.value.validate((valid) => {
        if (valid) {
          store.dispatch('scene/addScene', { group: newAsset.group, name: newAsset.name, image: 'empty.png', content: '' });
          handleAddDialogClose();
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    }

    function saveAsset(Type, content) {
      curSaveType.value = Type;
      curSaveThing.value = content;
      newAsset.group = '';
      newAsset.name = '';
      showSaveDialog.value = true;
    }

    function saveAssetConfirm(group, name) {
      if (!name) return;
      const assetIndex = allAssets.value.findIndex(asset => asset.name === name && asset.group === group);
      if (assetIndex !== -1) {
        const updatedAsset = { ...allAssets.value[assetIndex] };
        if (curSaveType.value === 'image') {
          updatedAsset.image = curSaveThing.value;
        } else {
          updatedAsset.content = curSaveThing.value;
        }
        store.dispatch('scene/updateScene', { index: assetIndex, scene: updatedAsset });
        handleSaveClose();
      }
    }

    function changeGroup() {
      curGroup.value = allAssets.value.filter(asset => asset.group === newAsset.group);
    }

    function editAsset(index) {
      curEditAssetIndex.value = index;
      curGroup.value = filteredAssets.value;
      showEditDialog.value = true;
    }

    function handleEditClose() {
      showEditDialog.value = false;
    }

    function saveEditedAsset() {
      const editAssetForm = ref(null);
      editAssetForm.value.validate((valid) => {
        if (valid) {
          const index = curEditAssetIndex.value;
          if (index !== null) {
            store.dispatch('scene/updateScene', { index, scene: curGroup.value[index] });
            handleEditClose();
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    }

    return {
      addDialogVisible,
      inputMessage,
      selectedTab,
      messages,
      newAsset,
      filteredAssets,
      showSaveDialog,
      curSaveType,
      curSaveThing,
      curGroup,
      showEditDialog,
      curEditAssetIndex,
      sendMessage,
      generateContent,
      showAddDialog,
      handleAddDialogClose,
      addNewAsset,
      selectTab,
      saveAsset,
      changeGroup,
      handleSaveClose,
      saveAssetConfirm,
      editAsset,
      handleEditClose,
      saveEditedAsset,
      rules,
    };
  }
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
  background-color: #F4F4F4;
}

.left-panel {
  flex: 3;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.right-panel {
  flex: 1;
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

.asset-name {
  font-size: 24px;
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

.character-image {
  width: 100%;
  max-width: 400px;
  border-radius: 15px;
}

.loading-wrapper {
  width: 100%;
  text-align: center;
}

.inputfooter {
  padding: 10px;
  border-top: 1px solid #ddd;
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
  flex: 1;
  overflow: hidden;
  padding: 10px;
  box-sizing: border-box;
}

.assets-list .el-scrollbar__wrap {
  height: 100% !important;
  max-height: 300px;
  overflow-y: auto;
}

.asset-item {
  margin-bottom: 10px;
  padding: 10px;
}

.asset-name {
  margin-bottom: 10px;
  font-weight: bold;
}

.asset-image {
  max-width: 100%;
  border-radius: 10px;
}

.add-button-container {
  display: flex;
  position: relative;
  justify-content: center;
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
  background-color: #f5f5f5;
  color: #333;
}

.confirm-button {
  background-color: #5973FF;
  color: white;
}
</style>