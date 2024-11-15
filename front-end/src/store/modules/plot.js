// store/modules/plot.js
export default {
  state: () => ({
    plots: [],
  }),
  mutations: {
    setPlots(state, plots) {
      state.plots = plots
    },
    delPlots(state){
      state.plots = []
    },
    delOneDialogue(state, {plotIndex, dialogueIndex}){
      console.log(state.plots)
      console.log(plotIndex)
      console.log(dialogueIndex)
      state.plots[plotIndex]['dialogue'].splice(dialogueIndex, 1)
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
    swapDialogue(state, {plotIndex, dialogueIndex1, dialogueIndex2}){
      const dialogues = state.plots[plotIndex].dialogue;
      const temp = dialogues[dialogueIndex1];
      dialogues[dialogueIndex1] = dialogues[dialogueIndex2];
      dialogues[dialogueIndex2] = temp;
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
    delOneDialogue({ commit }, payload) {
      commit('delOneDialogue', payload);
    },
    swapDialogue({ commit }, payload) {
      commit('swapDialogue', payload);
    },
    delPlots({commit}){
      commit('delPlots');
    }
  },
  getters: {
    plots: (state) => state.plots,
  },
};