export default {
  state() {
    return {
      loglineData: null,
    };
  },
  mutations: {
    setLoglineData(state, data) {
      state.loglineData = data;
    },
  },
  actions: {
    updateLoglineData({ commit }, data) {
      commit('setLoglineData', data);
    },
  },
  getters: {
    loglineData: (state) => state.loglineData,
  },
};
