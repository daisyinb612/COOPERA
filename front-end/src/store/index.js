import { createStore } from 'vuex';
import character from './modules/character';
import dialogue from './modules/dialogue';
import logline from './modules/logline';
import plot from './modules/plot';
import scene from './modules/scene';
import script from './modules/script';

export default createStore({
  modules: {
    character,
    dialogue,
    logline,
    plot,
    scene,
    script,
  },
});
