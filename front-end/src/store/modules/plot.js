// store/modules/plot.js
export default {
  state: () => ({
    plots: [],
  }),
  mutations: {
    setPlot(state, plot) {
      const index = state.plots.findIndex(p => p.id === plot.id);
      if (index !== -1) {
        state.plots.splice(index, 1, plot);
      }
    },
    addPlot(state, plot) {
      if (Array.isArray(plot)) {
        state.plots.push(...plot);
        return;
      }
      state.plots.push(plot);
    },
    updatePlot(state, { index, plot }) {
      state.plots.splice(index, 1, plot);
    },
    deletePlot(state, index) {
      state.plots.splice(index, 1);
    },
  },
  actions: {
    setPlot({ commit }, plot) {
      commit('setPlot', plot);
    },
    addPlot({ commit }, plot) {
      commit('addPlot', plot);
    },
    updatePlot({ commit }, payload) {
      commit('updatePlot', payload);
    },
    deletePlot({ commit }, index) {
      commit('deletePlot', index);
    },
  },
  getters: {
    plots: (state) => state.plots,
  },
};