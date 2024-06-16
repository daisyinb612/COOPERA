<template>
  <el-container>
    <el-main class="CHAT">
      <div class="chat">
        <el-header class="header">
          <div class="asset-name">“CHAT”</div>
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
    </el-main>
    <el-footer>Footer</el-footer>
  </el-container>

</template>

<script>
  export default {
    name: "LogLine"
  }
</script>

<style scoped>

  .CHAT {
    flex: 3;
    background-color: #FFFFFF;
    display: flex;
    flex-direction: column;
    border-radius: 20px;
    overflow: hidden;
    box-sizing: border-box;
  }

</style>