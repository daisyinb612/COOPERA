// store/modules/scene.js
export default {
  state: () => ({
    scenes: [],
  }),
  mutations: {
    setScenes(state, scenes) {
      state.scenes = scenes;
    },
    addScene(state, scene) {
      if (Array.isArray(scene)) {
        scene.forEach((s) => {
          if (!state.scenes.includes(s)) {
            state.scenes.push(s);
          }
        });
        
        return;
      }
      state.scenes.push(scene);
    },
    updateScene(state, { index, scene }) {
      state.scenes.splice(index, 1, scene);
    },
    deleteScene(state, index) {
      state.scenes.splice(index, 1);
    },
  },
  actions: {
    setScenes({ commit }, scenes) {
      commit('setScenes', scenes);
    },
    addScene({ commit }, scene) {
      commit('addScene', scene);
    },
    updateScene({ commit }, payload) {
      commit('updateScene', payload);
    },
    deleteScene({ commit }, index) {
      commit('deleteScene', index);
    },
  },
  getters: {
    scenes: (state) => state.scenes,
  },
};
