export default {
    state() {
      return {
        plotData: null,
      };
    },
    mutations: {
      setPlotData(state, data) {
        state.plotData = data;
      },
    },
    actions: {
      updatePlotData({ commit }, data) {
        commit('setPlotData', data);
      },
    },
    getters: {
      plotData: (state) => state.plotData,
    },
  };
  