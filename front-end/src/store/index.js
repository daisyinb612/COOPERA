import { createStore } from 'vuex';
import character from './modules/character';
import plot from './modules/plot';
import scene from './modules/scene';
import dialogue from './modules/dialogue';
import script from './modules/script';

const store = createStore({
  modules: {
    character,
    plot,
    scene,
    dialogue,
    script,
  },
});

export default store;
