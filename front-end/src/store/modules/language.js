export default {
  state() {
    return {
      language: "zh_CN",
    };
  },
  mutations: {
    setLanguage(state, language) {
      state.language = language;
    },
  },
  actions: {
    setLanguage({ commit }, language) {
      commit('setLanguage', language);
    },
  },
  getters: {
    language: (state) => state.language,
  },
};
