export default {
    state() {
      return {
        characterData: null,
      };
    },
    mutations: {
      setCharacterData(state, data) {
        state.characterData = data;
      },
    },
    actions: {
      updateCharacterData({ commit }, data) {
        commit('setCharacterData', data);
      },
    },
    getters: {
      characterData: (state) => state.characterData,
    },
  };