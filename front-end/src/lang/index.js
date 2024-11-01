import { createI18n } from "vue-i18n";

// import { language } from "@/store/modules/language"
import zh_CN from "./zh_CN";
import en_US from "./en_US";
// import {computed} from "vue";
// import { ref } from 'vue'


const i18n = createI18n({
  legacy: false,
  globalInjection: true,
    // 此处则利用store获取项目中当前语言环境,
  locale: localStorage.getItem('lang') || 'zh_CN',
  messages: {
    zh_CN,
    en_US,
  },
});

export default i18n;