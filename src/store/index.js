// src/store/index.js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      characterData: null,
      plotData: null,
      sceneData: null,
      dialogueData: null,
      scriptData: null,
    };
  },
  mutations: {
    setCharacterData(state, data) {
      state.characterData = data;
    },
    setPlotData(state, data) {
      state.plotData = data;
    },
    setSceneData(state, data) {
      state.sceneData = data;
    },
    setDialogueData(state, data) {
      state.dialogueData = data;
    },
    setScriptData(state, data) {
      state.scriptData = data;
    },
  },
  actions: {
    updateCharacterData({ commit }, data) {
      commit('setCharacterData', data);
    },
    updatePlotData({ commit }, data) {
      commit('setPlotData', data);
    },
    updateSceneData({ commit }, data) {
      commit('setSceneData', data);
    },
    updateDialogueData({ commit }, data) {
      commit('setDialogueData', data);
    },
    updateScriptData({ commit }, data) {
      commit('setScriptData', data);
    },
  },
  getters: {
    characterData: (state) => state.characterData,
    plotData: (state) => state.plotData,
    sceneData: (state) => state.sceneData,
    dialogueData: (state) => state.dialogueData,
    scriptData: (state) => state.scriptData,
  },
});

export default store;
