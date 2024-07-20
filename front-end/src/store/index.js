// store/index.js
import { createStore } from 'vuex';
import character from './modules/character';
import plot from './modules/plot';
import scene from './modules/scene';
import dialogue from './modules/dialogue';
import script from './modules/script';
import logline from './modules/logline'; // 导入logline模块

const store = createStore({
  modules: {
    character,
    plot,
    scene,
    dialogue,
    script,
    logline, // 注册logline模块
  },
});

export default store;
