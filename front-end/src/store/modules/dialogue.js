export default {
    state() {
      return {
        dialogueData: null,
      };
    },
    mutations: {
      setDialogueData(state, data) {
        state.dialogueData = data;
      },
    },
    actions: {
      updateDialogueData({ commit }, data) {
        commit('setDialogueData', data);
      },
    },
    getters: {
      dialogueData: (state) => state.dialogueData,
    },
  };
  