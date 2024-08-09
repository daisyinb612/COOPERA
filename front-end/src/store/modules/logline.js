export default {
  state() {
    return {
      loglineData: null,
      message: '',
    };
  },
  mutations: {
    setLoglineData(state, data) {
      state.loglineData = data;
    },
    setMessage(state, message) {
      state.message = message;
  },
},
  actions: {
    updateLoglineData({ commit }, data) {
      commit('setLoglineData', data);
    },
    updateMessage({ commit }, message) {
      commit('setMessage', message);
    },
  },
  getters: {
    loglineData: (state) => state.loglineData,
    message: (state) => state.message,
  },
};
