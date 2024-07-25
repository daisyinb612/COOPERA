export default {
  state: () => ({
    dialogues: [],
  }),
  mutations: {
    setDialogues(state, dialogues) {
      state.dialogues = dialogues;
    },
    addDialogue(state, dialogue) {
      state.dialogues.push(dialogue);
    },
    updateDialogue(state, { index, dialogue }) {
      state.dialogues.splice(index, 1, dialogue);
    },
    deleteDialogue(state, index) {
      state.dialogues.splice(index, 1);
    },
  },
  actions: {
    setDialogues({ commit }, dialogues) {
      commit('setDialogues', dialogues);
    },
    addDialogue({ commit }, dialogue) {
      commit('addDialogue', dialogue);
    },
    updateDialogue({ commit }, payload) {
      commit('updateDialogue', payload);
    },
    deleteDialogue({ commit }, index) {
      commit('deleteDialogue', index);
    },
  },
  getters: {
    dialogues: (state) => state.dialogues,
  },
};