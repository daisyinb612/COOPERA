// store/modules/script.js

export default {
    state: () => ({
      scripts: [],
    }),
    mutations: {
      setScripts(state, scripts) {
        state.scripts = scripts;
      },
      addScript(state, script) {
        state.scripts.push(script);
      },
      updateScript(state, { index, script }) {
        state.scripts.splice(index, 1, script);
      },
      deleteScript(state, index) {
        state.scripts.splice(index, 1);
      },
    },
    actions: {
      setScripts({ commit }, scripts) {
        commit('setScripts', scripts);
      },
      addScript({ commit }, script) {
        commit('addScript', script);
      },
      updateScript({ commit }, payload) {
        commit('updateScript', payload);
      },
      deleteScript({ commit }, index) {
        commit('deleteScript', index);
      },
    },
    getters: {
      scripts: (state) => state.scripts,
    },
  };
  