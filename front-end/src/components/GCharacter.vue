<template>
  <el-container class="main-container">
    <el-container class="character_panel">
      <el-header class="art-asset-header">
        <div class="art-asset">{{ this.$t('characters') }}</div>
      </el-header>
      <el-container class="rightcontainer">
        <el-tabs
          v-model="activeName"
          type="card"
          @tab-click="handleClick"
        >
        <el-tab-pane :label="this.$t('cha')" name="first" >
            <el-scrollbar class="assets-list">
              <el-card
                v-for="(asset, index) in charList"
                :key="index"
                class="asset-item"
                shadow="hover"
                @click="editAsset(index)">
                <el-row :gutter="10" style="width: 100%" align="middle">
                    <el-col :span="4" style="text-align: center">
                      <img
                        v-if="asset.image"
                        class="asset-image"
                        :src="asset.image"
                      />
                      <img
                        v-else
                        class="asset-image"
                        :src="require('@/assets/images/empty.png')"
                      />
                    </el-col>
                    <el-col :span="20"
                      ><div>{{ asset.name }}</div></el-col
                    >
                </el-row>
              </el-card>
            </el-scrollbar>
            <el-footer class="add-button-container">
              <el-button class="addasset-button" @click="showAddDialog"
                >{{ this.$t('cha_add') }}</el-button>
            </el-footer>
        </el-tab-pane>
        <el-tab-pane :label="this.$t('cha_vis')" name="second">
              <iframe :src=htmlContent width="100%" frameborder="0"></iframe>
        </el-tab-pane>
        </el-tabs>
      </el-container>
    </el-container>
    <el-container class="chatgpt_panel">
      <div class="chat">
        <el-header class="header">
          <div>{{ this.$t('cha_AI') }}</div>
        </el-header>
        <el-main>
          <div
            class="message"
            v-for="(message, index) in messages"
            :key="index"
          >
            <el-row :gutter="5" align="middle">
              <div v-if="message.prompt" class="human-iutput">
                {{ message.prompt }}
              </div>
              <!-- </el-col> -->
            </el-row>
            <br />
            <el-row align="top">
              <el-col :span="4"
                ><el-avatar
                  :src="require('@/assets/images/operalogo.jpg')"
                  class="llm"
                ></el-avatar
              ></el-col>
              <el-col :span="20"
                ><div class="AI-output" v-html="message.content"></div
              ></el-col>
            </el-row>
          </div>
        </el-main>
        <el-footer>
          <el-input
            :placeholder="$t('AI_input')"
            v-model="inputMessage"
            class="input-field"
            @keyup.enter="sendMessage"
            clearable
          >
            <template #append>
              <el-button @click="sendMessage"
                ><img
                  class="upload-image"
                  :src="require('@/assets/images/upload.png')"
              /></el-button>
            </template>
          </el-input>
        </el-footer>
      </div>
    </el-container>

    <el-dialog
      :title="$t('cha_add')"
      v-model="addDialogVisible"
      custom-class="dialog-content"
    >
      <el-form :model="newAsset" label-width="100px" class="add-asset-form">
        <el-form-item :label="this.$t('C_name')" :label-width="formLabelWidth">
          <el-input v-model="newAsset.name" autocomplete="off" />
        </el-form-item>

        <el-form-item
          v-if="newAsset.group === 'characters'"
          :label="this.$t('C_de')"
          :label-width="formLabelWidth"
        >
          <el-input v-model="newAsset.content" autocomplete="off" />
        </el-form-item>

        <el-form-item :label="this.$t('C_re')" >
          <el-select
            v-model="newAsset.characters"
            multiple
            :placeholder="this.$t('C_reh')"
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

        <el-form-item :label="this.$t('C_voice')">
          <el-select
            v-model="newAsset.per"
            :placeholder="this.$t('voice')"
          >
            <el-option
              v-for="audio in audios"
              :key="audio"
              :label="audio"
              :value="audio"
            />
          </el-select>
        </el-form-item>

        <el-form-item
          v-if="newAsset.group === 'characters'"
          :label="this.$t('C_p')"
          :label-width="formLabelWidth"
        >
          <div v-loading="loading">
            <el-upload
              :http-request="uploadFile"
              list-type="picture-card"
              :on-success="handleUploadSuccess"
              v-model:file-list="fileList"
              :on-remove="handleRemove"
              :on-preview="handlePictureCardPreview"
              :on-exceed="handleExceed"
            >
              <i class="el-icon-plus"></i>
            </el-upload>
            <el-button @click="generate_new_image" class="confirm-button"
              >{{ this.$t('C_Genp') }}</el-button
            >
          </div>
        </el-form-item>

        <el-footer class="dialog-footer">
          <el-button @click="handleAddDialogClose" class="cancel-button"
            >{{ this.$t('cancel') }}</el-button
          >
          <el-button type="primary" @click="addNewAsset" class="confirm-button"
            >{{ this.$t('confirm') }}</el-button
          >
        </el-footer>
      </el-form>
    </el-dialog>

    <el-dialog
      :title="'保存 ' + curSaveType"
      v-model="showSaveDialog"
      custom-class="dialog-content"
    >
      <el-form-item label="类型">
        {{ curSaveType }}
      </el-form-item>

      <el-form-item label="分组">
        <el-select
          v-model="newAsset.group"
          placeholder="选择分组"
          @change="changeGroup"
        >
          <el-option label="角色" value="characters" />
        </el-select>
      </el-form-item>
      <el-form-item label="资产名" :label-width="formLabelWidth">
        <el-select
          v-if="newAsset.group"
          v-model="newAsset.name"
          placeholder="选择名字"
        >
          <el-option
            v-for="(asset, index) in curGroup"
            :key="index"
            :label="asset.name"
            :value="asset.name"
          />
        </el-select>
        <el-input v-model="newAsset.name" autocomplete="off" />
      </el-form-item>

      <el-footer class="dialog-footer">
        <el-button @click="handleSaveClose" class="cancel-button"
          >取消</el-button
        >
        <el-button
          type="primary"
          @click="saveAssetConfirm(newAsset.group, newAsset.name)"
          class="confirm-button"
          >确认</el-button
        >
      </el-footer>
    </el-dialog>

    <el-dialog
     :title="$t('cha_edit')"
      v-model="showEditDialog"
      custom-class="dialog-content"
    >

      <el-form-item :label="this.$t('C_name')" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.name" autocomplete="off" />
      </el-form-item>

      <el-form-item :label="this.$t('C_de')" :label-width="formLabelWidth">
        <el-input v-model="currentEditAsset.content" autocomplete="off" />
      </el-form-item>

      <el-form-item :label="this.$t('C_voice')" >
        <el-select v-model="currentEditAsset.per" placeholder="choose voice">
          <el-option
            v-for="audio in audios"
            :key="audio"
            :label="audio"
            :value="audio"
          />
        </el-select>
      </el-form-item>

      <el-form-item :label="this.$t('C_p')" :label-width="formLabelWidth">
        <div v-loading="loading">
          <el-upload
            :http-request="uploadFile"
            list-type="picture-card"
            :on-success="handleUploadSuccess"
            :file-list="fileList"
            show-file-list="true"
            :on-remove="handleEditRemove"
            :on-exceed="handleExceed"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-button @click="generate_image" class="confirm-button"
            >{{ this.$t('C_Genp') }}</el-button
          >
        </div>
      </el-form-item>

      <el-footer class="dialog-footer">
        <el-button @click="handleEditClose" class="cancel-button"
          > {{ this.$t('cancel') }} </el-button
        >
        <el-button type="danger" @click="showDeleteDialog" class="delete-button"
          > {{ this.$t('delete') }} </el-button
        >
        <el-button
          type="primary"
          @click="saveEditedAsset"
          class="confirm-button"
          > {{ this.$t('confirm') }} </el-button
        >
      </el-footer>

      <el-dialog v-model="showDeleteConfirm">
        <div>Are you sure to remove the character?</div>
        <span class="dialog-footer">
          <el-button @click="cancelDelete" class="cancel-button"
            >Cancel</el-button
          >
          <el-button type="danger" @click="confirmDelete" class="confirm-button"
            >Confirm</el-button
          >
        </span>
      </el-dialog>
    </el-dialog>
    
  </el-container>
</template>

<script>
import {
  defineComponent,
  ref,
  reactive,
  computed,
  getCurrentInstance,
} from "vue";
import { useStore } from "vuex";
import axios from "axios";
import { ElMessage } from "element-plus";
import * as diff from "diff";

export default defineComponent({
  name: "GCharacter",

  setup() {
    const { proxy } = getCurrentInstance();

    // State and reactive properties
    const addDialogVisible = ref(false);
    const showSaveDialog = ref(false);
    const showEditDialog = ref(false);
    const curSaveType = ref("");
    const curSaveThing = ref("");
    const loading = ref(false);
    const curEditAssetIndex = ref("");
    const fileList = ref([]);
    const inputMessage = ref("");
    const selectedTab = ref("characters");
    const history = ref([]);
    const messages = ref([
      {
        role: "assistant",
        prompt: "",
        content: `你好，我是辅助角色创作的智能助手。你可以尝试问我以下问题：<br>
在角色创作中，我应该考虑哪些方面的适合性？<br>
      对于特定角色，你有什么创意方向和建议？`,

        // content: `hello, I'm an Intelligent Assistant who can help you with character crafting.You can try asking me like the following questions:<br>
        //         What aspects should I consider in terms of suitability for character creation?<br>
        //         What are your creative directions and suggestions for a specific character?`,

        image: "logo.png",
        downloadIcon: true,
      },
    ]);
    const showDeleteConfirm = ref(false);
    const newAsset = reactive({
      group: "characters",
      name: "",
      content: "",
      image: "",
    });
    const beforeEditAsset = reactive({
      name: "",
      content: "",
    });
    const store = useStore();
    const audios = {
      0: "女音",
      1: "男音",
      // 3:"斯文男音",
      // 4:"小萌萌",
      // 5:"知性女音",
      // 6:"老教授",
      // 9:"播音员",
      // 10:"京腔",
      // 11:"温柔大叔",
    };
    const allCharacters = computed(() => store.state.character.characters);

    const currentEditAsset = reactive({
      name: "",
      content: "",
      per: "",
      image: "",
    });

    // Computed properties
    const filteredAssets = computed(() => {
      return charList;
    });

    const charList = computed(() => {
      console.log(store.state.character.characters);
      return store.state.character.characters;
    });
    const activeName = ref('first');
    const htmlContent = ref('');

    const fetchHtmlContent = async () => {
      try {
        const response = await axios.post('/api/get_vis');
        
        let path = '/api/get_vis/get_html'
        console.log('response', path, response)
        htmlContent.value = path;
      } catch (error) {
        console.error('Error fetching HTML:', error);
      }
    };

    const handleClick = (tab) => {
      console.log('handelClick')
      if (tab.paneName === 'first' && !htmlContent.value) {
        fetchHtmlContent();
      }
    };

    // Functions
    async function sendMessage() {
      if (!inputMessage.value) {
        ElMessage({
          message: "输入不能为空",
          type: "warning",
        });
        return;
      }

      const userMessage = {
        role: "user",
        content: inputMessage.value,
      };
      history.value.push(userMessage);

      const requestBody = {
        action: "get_character_help",
        data: {
          history: history.value.map((msg) => ({
            role: msg.role,
            content: msg.content,
          })),
          user_input: inputMessage.value,
        },
      };
      const assistantMessage = {
        role: "assistant",
        prompt: inputMessage.value,
        content: "loading...",
        image: "logo.png",
        downloadIcon: true,
      };
      messages.value.push(assistantMessage);

      try {
        const response = await axios.post(
          "/api/get_character_help",
          requestBody
        );
        if (response.status === 200) {
          const assistantMessage = {
            role: "assistant",
            prompt: inputMessage.value,
            content: response.data.answer,
            image: "logo.png",
            downloadIcon: true,
          };
          messages.value.splice(messages.value.length - 1, 1, assistantMessage);
          history.value.push(assistantMessage);
          inputMessage.value = "";
        }
      } catch (error) {
        ElMessage({
          message: "请求失败",
          type: "error",
        });
      }
    }

    function selectTab(tab) {
      selectedTab.value = tab;
    }

    function showAddDialog() {
      fileList.value = [];
      addDialogVisible.value = true;
    }

    function handlePictureCardPreview(file) {
      charList.value[curEditAssetIndex.value].image = file.url;
    }

    function handleAddDialogClose() {
      newAsset.group = "characters";
      newAsset.name = "";
      newAsset.content = "";
      newAsset.image = "";
      newAsset.characters = [];
      fileList.value = [];
      addDialogVisible.value = false;
    }

    const handleRemove = () => {
      newAsset.image = "";
    };

    const handleEditRemove = () => {
      currentEditAsset.image = "";
    };

    const handleExceed = () => {
      proxy.$message.warning("只能上传一个附件");
    };

    function handleSaveClose() {
      newAsset.group = "";
      newAsset.name = "";
      newAsset.content = "";
      newAsset.image = "";
      newAsset.characters = [];
      fileList.value = [];
      showSaveDialog.value = false;
    }

    function addNewAsset() {
      let charactersList = store.state.character.characters;
      if (!newAsset.name) {
        proxy.$message.warning("资产名不能为空");
        return;
      }
      if (charactersList.some((asset) => asset.name === newAsset.name)) {
        proxy.$message.warning("资产名已存在");
        return;
      }
      if (!newAsset.per) {
        proxy.$message.warning("请选择音色");
        return;
      }

      const character = {
        name: newAsset.name,
        content: newAsset.content,
        image: newAsset.image || null,
        per: newAsset.per,
        re: newAsset.re,
      };
      store.dispatch("addCharacter", character);
      axios.post("/api/add_character", {
        action: "add_character",
        data: character,
      });
      handleAddDialogClose();
      proxy.$message.success("资产新增成功");
    }

    function saveAsset(Type, content) {
      curSaveType.value = Type;
      curSaveThing.value = content;
      showSaveDialog.value = true;
    }

    function saveAssetConfirm(group, name) {
      if (!name) {
        proxy.$message.warning("资产名为空");
        return;
      }

      const assetIndex = charList.value.findIndex(
        (asset) => asset.name === name
      );
      if (assetIndex !== -1) {
        if (curSaveType.value === "image") {
          charList[assetIndex].image = curSaveThing.value;
        } else {
          charList[assetIndex].content = curSaveThing.value;
        }
        store.dispatch("updateCharacter", {
          index: assetIndex,
          character: charList[assetIndex],
        });
        proxy.$message.success("资产更新成功");
      } else {
        console.log(curSaveThing.value);
        const newAsset = {
          name: name,
          image: curSaveType.value === "image" ? curSaveThing.value : null,
          content: curSaveType.value === "content" ? curSaveThing.value : "",
        };
        store.dispatch("addCharacter", newAsset);
        proxy.$message.success("新资产添加成功");
      }
      // showSaveDialog.value = false;
    }

    function editAsset(index) {
      console.log(charList.value);
      console.log(index);
      if (charList.value[index].image) {
        fileList.value = [
          {
            name: charList.value[index].name,
            url: charList.value[index].image,
          },
        ];
      } else {
        fileList.value = [];
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
      formData.append("action", "save_character_asset_image");
      formData.append("character_name", newAsset.name);
      formData.append("character_image", options.file);

      axios
        .post("/api/update_character_asset_image", formData)
        .then((response) => {
          if (response.data.success) {
            newAsset.image = response.data.filePath;
            options.onSuccess(response.data, options.file);
          } else {
            options.onError(new Error("Upload failed"));
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
      store.dispatch("deleteCharacter", curEditAssetIndex.value);
      await axios.post("/api/delete_character", {
        action: "delete_character",
        data: {
          index: curEditAssetIndex.value,
        },
      });
      showDeleteConfirm.value = false;
      handleEditClose();
      ElMessage({
        type: "success",
        message: `成功删除资产 "${name}"`,
      });
    }

    function getImageSrc(image) {
      return image ? image : "@/assets/images/logo.png";
    }

    function handleUploadSuccess(response) {
      if (response.success) {
        charList[curEditAssetIndex.value].image = response.filePath;
        store.dispatch("updateCharacter", {
          index: curEditAssetIndex.value,
          character: charList[curEditAssetIndex.value],
        });
      }
    }

    async function saveEditedAsset() {
      console.log(beforeEditAsset);
      // add的用[]包裹, remove的用{}包裹
      let changes = "";
      diff
        .diffChars(beforeEditAsset.content, currentEditAsset.content)
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
      const editedAsset = JSON.parse(JSON.stringify(currentEditAsset));
      if (!editedAsset.name) {
        proxy.$message.warning("资产名不能为空");
        return;
      }
      if (!editedAsset.content) {
        proxy.$message.warning("描述不能为空");
        return;
      }
      if (!editedAsset.per) {
        proxy.$message.warning("请选择音色");
        return;
      }
      // if (!editedAsset.image) {
      //   proxy.$message.warning('请上传图片');
      //   return;
      // }
      store.dispatch("updateCharacter", {
        index: curEditAssetIndex.value,
        character: editedAsset,
      });
      await axios.post("/api/update_character", {
        action: "update_character",
        data: {
          index: curEditAssetIndex.value,
          character: editedAsset,
        },
      });
      proxy.$message.success("资产更新成功");
      showEditDialog.value = false;
    }

    async function generate_image() {
      loading.value = true;
      const imageRequestBody = {
        action: "create_character_picture",
        data: {
          name: currentEditAsset.name,
          content: currentEditAsset.content,
        },
      };
      const imageResponse = await axios.post(
        "/api/create_character_picture",
        imageRequestBody
      );
      const pic_url =
        "/api/get_image?filename=" +
        imageResponse.data.image +
        "&path=character";
      fileList.value.push({
        name: currentEditAsset.name,
        url: pic_url,
      });
      loading.value = false;
      console.log(fileList.value);
      newAsset.image = pic_url;
      currentEditAsset.image = pic_url;
      charList.value[curEditAssetIndex.value].image = pic_url;
    }

    async function generate_new_image() {
      loading.value = true;
      const imageRequestBody = {
        action: "create_character_picture",
        data: {
          name: newAsset.name,
          content: newAsset.content,
        },
      };
      const imageResponse = await axios.post(
        "/api/create_character_picture",
        imageRequestBody
      );
      const pic_url =
        "/api/get_image?filename=" +
        imageResponse.data.image +
        "&path=character";
      fileList.value.push({
        name: newAsset.name,
        url: pic_url,
      });
      loading.value = false;
      console.log(fileList.value);
      newAsset.image = pic_url;
      newAsset.image = pic_url;
    }

    return {
      loading,
      charList,
      audios,
      allCharacters,
      activeName,
      htmlContent,
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
      generate_new_image,
      handleSaveClose,
      handleRemove,
      handleEditRemove,
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
      handleClick,
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

.llm {
  display: flex;
  align-items: top;
  margin: 10px 0;
  gap: 10px;
  height: 40px;
  width: 40px;
}

.el-main {
  padding: 10px;
}

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

.chatgpt_panel {
  flex: 2;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.character_panel {
  flex: 2;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  width: 100%;
}

.rightcontainer {
  width: 100%;
  height: 100vh; /* 使父容器填满整个视口高度 */
  display: flex;
  flex-direction: column;
}

/* .tabs >  {
  flex: 1;
  padding: 32px;
}

.demo-tabs >  {
  flex: 1;
  padding: 32px;
} */


.el-tabs--card {
  height: calc(100vh - 110px);
  /* overflow-y: auto; */
}
.el-tab-pane {
  height: calc(100vh - 110px);
  overflow-y: auto;
}

iframe {
  width: 100%;
  height: 100%; 
}

.assets-list {
  height: auto;
  width: 100%;
  overflow: hidden;
  padding: 20px;
  box-sizing: border-box;
}

.upload-image {
  width: 15px;
  height: auto;
}

.header {
  background-color: #5973ff;
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
  background-color: #5973ff;
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
  background-color: #bccfff;
  color: white;
  border: 2px solid #5973ff;
  cursor: pointer;
  border-radius: 10px !important;
  transition:
    background-color 0.2s,
    color 0.2s;
}
.asset-button.hover {
  background-color: #939dd3;
  border-radius: 10px;
  color: white;
}
.asset-button.active {
  background-color: #5973ff;
  border-radius: 10px;
  color: white;
}

.asset-item {
  /* display: flex; */
  align-items: center;
  margin: 15px;
  padding: 10px;
  height: 80px;
}

.human-iutput {
  display: inline-flex;
  justify-content: flex-start;
  word-wrap: break-word;
  padding: 10px;
  line-height: 20px;
  border-radius: 5px;
  min-width: 90%;
  background-color: #d5dcff;
}

.AI-output {
  padding: 5px;
  line-height: 20px;
  border-radius: 10px;
}

.asset-image {
  border-radius: 50%;
  width: 46px;
  height: 46px;
  border: 2px solid #ddd;
}

.add-button-container {
  display: flex;
  position: relative;
  bottom: 0;
  justify-content: right;
  padding: 10px;
}

.addasset-button {
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
.addasset-button:hover {
  background-color: #bccfff;
  color: white;
}

.addasset-button:active {
  background-color: #5973ff;
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
  background-color: #f1f1f1;
  color: #333;
}

.confirm-button {
  background-color: #5973ff;
  color: white;
}

body {
  margin: 0;
}
.example-showcase .el-loading-mask {
  z-index: 9;
}
</style>
