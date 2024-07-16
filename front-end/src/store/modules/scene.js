export default {
    state() {
      return {
        sceneData: null,
      };
    },
    mutations: {
      setSceneData(state, data) {
        state.sceneData = data;
      },
    },
    actions: {
      updateSceneData({ commit }, data) {
        commit('setSceneData', data);
      },
    },
    getters: {
      sceneData: (state) => state.sceneData,
    },
  };
  