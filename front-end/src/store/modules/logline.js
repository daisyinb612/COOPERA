// store/modules/logline.js
const state = {
    storyline: '', // 初始值
  };
  
  const mutations = {
    setStoryline(state, storyline) {
      state.storyline = storyline;
    }
  };
  
  const actions = {
    updateStoryline({ commit }, storyline) {
      commit('setStoryline', storyline);
    }
  };
  
  const getters = {
    getStoryline(state) {
      return state.storyline;
    }
  };
  
  export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
  };
  