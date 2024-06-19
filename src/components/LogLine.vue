<template>
  <el-container class="main-container">
    <el-main class="up-panel">
      <el-header class="header">
        <div>“editlogline”</div>
      </el-header>
      <el-main class="editlogline">
        <el-input v-model="textarea" :rows="5" type="textarea"  placeholder="Please input" />
      </el-main>

      <el-footer class="button-container">
        <el-button class="upload-button" @click="UploadLogLine">Upload</el-button>
      </el-footer>
    </el-main>

    <el-footer class="down-panel">
      <div class="chat">
        <el-header class="header">
          <div class="asset-name">“chat”</div>
        </el-header>
        <el-main>
          <el-card class="message" v-for="(message, index) in messages" :key="index">
            <template #header>
              <div class="message-header">{{ message.prompt }}</div>
            </template>
            <el-contanier>
              <el-aside width="100px">
                <el-avatar icon="el-icon-user" class="llm"></el-avatar>
              </el-aside>
              <el-main width="200px">
                <el-row class="llm-wrapper">
                  <el-icon v-if="message.downloadIcon" :size="15" class="generated-icon">
                    <Download @click="saveAsset('content', message.content)" />
                  </el-icon>
                  <div class="message-content">{{ message.content }} </div>
                </el-row>
              </el-main>
            </el-contanier>
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
    </el-footer>
  </el-container>

</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'LogLine',


  setup() {
    const inputMessage = ref('');
    const messages = ref([]);
    const textarea = ref('');

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

    
    return {
      inputMessage,
      messages,
      textarea,
      sendMessage,
      generateContent,
    }
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

</style>