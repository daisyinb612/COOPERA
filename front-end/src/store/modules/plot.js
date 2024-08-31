// store/modules/plot.js
export default {
  state: () => ({
    plots: [],
  }),
  mutations: {
    setPlots(state, plots) {
      state.plots = plots
      // const index = state.plots.findIndex(p => p.id === plot.id);
      // if (index !== -1) {
      //   state.plots.splice(index, 1, plot);
      // }
    },
    movePlot(state, {fromIndex, toIndex}){
      for (let i = 0; i < state.plots.length; i++) {
          let item = state.plots[i];
          if (i === fromIndex) {
              state.plots.splice(i, 1);
              state.plots.splice(toIndex, 0, item);
              break;
          }
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
    setPlots({ commit }, plots) {
      commit('setPlot', plots);
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
    movePlot({ commit }, payload) {
      commit('movePlot', payload);
    },
  },
  getters: {
    plots: (state) => state.plots,
  },
};