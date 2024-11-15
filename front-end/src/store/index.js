import { createStore } from 'vuex';
import logline from './modules/logline';
import character from './modules/character';
import plot from './modules/plot';
import scene from './modules/scene';
import script from './modules/script';
import language from './modules/language'

export default createStore({
  modules: {
    logline,
    character,
    plot,
    scene,
    script,
    language
  },
});
