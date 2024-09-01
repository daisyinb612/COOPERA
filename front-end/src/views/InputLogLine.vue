<template>
   <el-container class="main-container">
    <el-main class="up-panel">
      <el-header class="header">
        <div>INPUT YOUR lOGLINE </div>
      </el-header>
      <el-main class="editlogline" v-loading="loading">
        <el-scrollbar>
        <el-input v-model="loglineData" :rows="3" type="textarea" placeholder="Please write down your playwriting summary with two or three sentences " />
        </el-scrollbar>
      </el-main>

      <el-footer class="button-container">
        <el-button class="upload-button" @click="FreshBackend">Refresh</el-button>
        <el-button class="upload-button" @click="UploadLogLine">Upload</el-button>
      </el-footer>
    </el-main>

    <el-footer class="down-panel">
      <div class="chat">
        <el-header class="header">
          <div class="asset-name">LOGLINE Intelligent Assistant</div>
        </el-header>
        <el-main>
          <div class="message" v-for="(message, index) in messages" :key="index">
            <el-row :gutter="5" align="middle">
              <el-col :span="message.prompt.length > 35 ?0: 24-message.prompt.length"></el-col>
              <el-col :span="message.prompt.length > 35 ?24: message.prompt.length">
                <div class="human-iutput-container">
                  <div class="human-iutput" >
                  {{ message.prompt }}
                 </div>
                </div>
              </el-col>
            </el-row>
            <br>
            <el-row align="middle">
              <el-col :span="2"><el-avatar :src="require('@/assets/images/operalogo.jpg')" class="llm"></el-avatar></el-col>
              <el-col :span="22"><div class="AI-output" v-html="message.content"></div></el-col>
            </el-row>
          </div>
        </el-main>
        <el-footer>
          <el-input placeholder="You can ask LOGLINE Intelligent Assistant for help here..." v-model="inputMessage"
            @keyup.enter="sendMessage" clearable>
            <template #append>
              <el-button @click="sendMessage"><img class="upload-image" :src="require('@/assets/images/upload.png')"/></el-button>
            </template>
          </el-input>
        </el-footer>
      </div>
    </el-footer>
  </el-container>
</template>

<script>

import { defineComponent, ref } from 'vue';
import { mapState, mapActions } from 'vuex';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { useStore } from 'vuex';
import { computed } from 'vue';

export default defineComponent({
  name: 'LogLine',
  computed: {
    ...mapState({ 
      loglineData: state => state.logline.loglineData,
    }),
  },
  methods: {
    ...mapActions(['updateLoglineData']),
    async sendMessage() {
      if (!this.inputMessage) {
        ElMessage({
          message: '输入不能为空',
          type: 'warning',
        });
        return;
      }

      const userMessage = {
        role: 'user',
        content: this.inputMessage
      };
      this.history.push(userMessage);


      const requestBody = {
        action: 'get_storyline_help',
        data: {
          storyline: this.loglineData,
          history: this.history.map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          user_input: this.inputMessage
        }
      };
      const assistantMessage = {
            role: 'assistant',
            prompt: this.inputMessage,
            content: "loading...",
            image: 'logo.png',
            downloadIcon: true,
          };
      this.messages.push(assistantMessage);

      try {
        console.log("Sending request...");
        const response = await axios.post('http://localhost:8000/get_storyline_help', requestBody);
        console.log("Request successful");
        if (response.status === 200) {
          const assistantMessage = {
            role: 'assistant',
            prompt: this.inputMessage,
            content: response.data.answer,
            image: "test_asset.png",
            downloadIcon: true
          };
          this.messages.splice(this.messages.length - 1, 1, assistantMessage);
          this.history.push(assistantMessage);
          this.inputMessage = '';
        } else {
          ElMessage({
            message: '请求失败',
            type: 'error',
          });
        }
      } catch (error) {
        console.log("Request failed:", error);
        if (error.code === 'ECONNABORTED') {
          ElMessage({
            message: '请求超时',
            type: 'error',
          });
        } else {
          ElMessage({
            message: '请求失败',
            type: 'error',
          });
        }
      }
    },
    async FreshBackend(){
      const Response = await axios.get('http://localhost:8000/fresh_backend');
      if (Response.data.result === true) {
        ElMessage({
          message: '刷新成功，文件名：' + Response.data.filename,
          type: 'success',
        });
        return;
      }
      else {
        ElMessage({
          message: '刷新失败',
          type: 'error',
        });
        return;
      }

    },
    async UploadLogLine() {
      this.loading = true;
      if (!this.loglineData) {
        ElMessage({
          message: '输入不能为空',
          type: 'warning',
        });
        return;
      }
      
      const requestBody = {
        action: 'upload_storyline',
        data: {
          storyline: this.loglineData
        }
      };

      try {
        const response = await axios.post('http://localhost:8000/upload_storyline', requestBody);
        this.$store.dispatch('addCharacter', response.data);
        if (response.status === 200) {
          this.loading = false;
          ElMessage({
            message: '保存成功',
            type: 'success',
          });
        } else {
          ElMessage({
            message: '保存失败',
            type: 'error',
          });
        }
      } catch (error) {
        if (error.code === 'ECONNABORTED') {
          ElMessage({
            message: '请求超时',
            type: 'error',
          });
        } else {
          ElMessage({
            message: '请求失败',
            type: 'error',
          });
          }
        }
      }
  },




  setup() {
    const store=useStore()
    const inputMessage = ref('');
    const messages = ref([
            {
            role: 'assistant',
            prompt: '',
            content: `hello, I'm an Intelligent Assistant who can help you with logline writing.
                You can try asking me like the following questions:<br>
                What should I pay attention to when writing logline?<br>
                How can I summarize a specific story in two or three sentences?`,
            image: 'logo.png',
            downloadIcon: true,
          }
    ]);
    const loading = ref(false);
    const history = ref([]);
    const loglineData = computed({
      get: () => store.getters.loglineData,
      set: (value) => store.dispatch('updateLoglineData', value)
    });
    console.log(store);

    return {
      inputMessage,
      messages,
      loading,
      history,
      loglineData, // 返回 loglineData
    }
  }
});
</script>

<style scoped>

.upload-image {
  width: 15px;
  height: auto;
}

.llm{
  height: 80px;
  width: 80px;
}

.human-iutput-container {
  display: flex;
  justify-content: flex-end;
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

.up-panel {
  display: flex;
  flex: 1;
  background-color: #FFFFFF;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
}

.editlogline {
  height: 80px;
  overflow-y: scroll;
  overflow-y: auto;
}

.header {
  background-color: #5973FF;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
}

.down-panel {
  display: flex;
  flex: 2;
  background-color: #FFFFFF;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
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

.upload-button {
  margin: 0 5px;
  padding: 10px 20px;
  background-color: white;
  border: 2px solid #5973FF;
  color: #BCCFFF;
  cursor: pointer;
  border-radius: 10px !important;
  transition: background-color 0.2s, color 0.2s;
}
.upload-button:hover {
  background-color: #93a2f7;
  color: white;
}

.upload-button:active {
  background-color: #3a51d4;
  color: white;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  padding: 5px;
  gap: 20px;
  text-align: center;
  box-sizing: border-box;
}

.textarea-input {
  background-color: EEEEEE;
  width: 100%;
  height: 100%;
}


.human-iutput{
  max-width: 90%;
  display: inline-block;
  word-wrap:break-word;
  padding: 15px;
  line-height: 20px;
  border-radius: 10px;
  background-color: #D5DCFF;
}

.AI-output{
  padding: 15px;
  line-height: 20px;
  border-radius: 10px;
}

</style>