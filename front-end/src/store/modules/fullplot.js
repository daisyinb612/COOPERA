export default {
  state: () => ({
    fullplots: [],
  }),
  mutations: {
    setFullplots(state, fullplots) {
      state.fullplots = fullplots;
    },
    addFullplot(state, fullplots) {
      state.fullplots.push(fullplots);
    },
    updateFullplot(state, { index, fullplots }) {
      state.fullplots.splice(index, 1, fullplots);
    },
    deleteFullplot(state, index) {
      state.fullplots.splice(index, 1);
    },
  },
  actions: {
    setFullplots({ commit }, fullplots) {
      commit('setFullplots', fullplots);
    },
    addFullplots({ commit }, fullplots) {
      commit('addFullplot', fullplots);
    },
    updateFullplot({ commit }, payload) {
      commit('updateFullplot', payload);
    },
    deleteFullplot({ commit }, index) {
      commit('deleteFullplot', index);
    },
  },
  getters: {
    fullplots: (state) => state.fullplots,
  },
};