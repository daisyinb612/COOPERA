import { createStore } from 'vuex';
import logline from './modules/logline';
import character from './modules/character';
import plot from './modules/plot';
import fullplot from './modules/fullplot';
import scene from './modules/scene';
import script from './modules/script';

export default createStore({
  modules: {
    logline,
    character,
    plot,
    fullplot,
    scene,
    script,
  },
});
