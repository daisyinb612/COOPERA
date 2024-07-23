// store/modules/plot.js
export default {
  state: () => ({
    plots: [],
  }),
  mutations: {
    setPlot(state, plot) {
      state.plots.push(plot);
    },
    addPlot(state, plot) {
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
      commit('addPlot', plot);
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