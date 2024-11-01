<template>
  <div style="display: flex; background: linear-gradient(162.86deg, #a1b0ff, #f472ff);
">
    <div :class="$style.title">
      <div :class="$style.ellipseParent">
        <div :class="$style.frameChild"></div>
        <div :class="$style.coOpera">CO-OPERA</div>
      </div>
    </div>
  <div class="right-bar">
      <el-switch
      v-model="language"
      inline-prompt
      style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
      active-text="ZH"
      active-value="zh_CN"
      inactive-text="EN"
      inactive-value="en_US"
      @change="change_language"
  />
  </div>
  </div>
  </template>
  
  <script>
  // import { useStore } from "vuex";
  import { ref } from 'vue'
 import { useI18n } from "vue-i18n";
import { computed } from "vue";
  export default {
    name: "WebTitle",

    setup() {
      // const store = useStore()
      const language = ref(localStorage.lang || 'zh_CN')
      const { t, locale } = useI18n();

      function change_language(){
        locale.value = language.value;
        localStorage.setItem('lang', language.value)
        location.reload()
      }
      const getCurrentLang = computed(() => {
        return locale.value;
      });

      console.log(getCurrentLang.value);
      console.log(t("message.hello"));

      // const language = ref(store.getters['language']);

      // function change_language() {
      //   store.dispatch("setLanguage", language.value).then(()=>{
      //     locale.value = language
      //   })
      // }

    return{
      language,
      change_language
    }
  }

  }


  </script>
  
  <style module>
  .right-bar {
    position: absolute;
    right: 10px;
    padding: 10px;

  }

  .frameChild {
    width: 50px;
    position: relative;
    box-shadow: 0px 4px 4px 4px rgba(0, 0, 0, 0.1) inset, 0px 4px 4px 4px rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    background: linear-gradient(162.86deg, #a1b0ff, #f472ff);
    border: 4px solid rgba(255, 255, 255, 1);
    box-sizing: border-box;
    height: 50px;
  }
  
  .coOpera {
    position: relative;
    font-weight: 800;
  }
  
  .ellipseParent {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 20px;
  }
  
  .title {
    width: 100%;
    position: relative;
    height: 80px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 17px 20px;
    box-sizing: border-box;
    text-align: left;
    font-size: 36px;
    color: #fff;
    font-family: var(--font-jetbrains-mono);
  }
  
  </style>  