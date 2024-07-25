export default {
  state() {
    return {
      characters: [],
    };
  },
  mutations: {
    setCharacters(state, characters) {
      state.characters = characters;
    },
    addCharacter(state, character) {
      state.characters.push(character);
    },
    updateCharacter(state, { index, character }) {
      state.characters.splice(index, 1, character);
    },
    deleteCharacter(state, index) {
      state.characters.splice(index, 1);
    },
  },
  actions: {
    setCharacters({ commit }, characters) {
      commit('setCharacters', characters);
    },
    addCharacter({ commit }, character) {
      commit('addCharacter', character);
    },
    updateCharacter({ commit }, payload) {
      commit('updateCharacter', payload);
    },
    deleteCharacter({ commit }, index) {
      commit('deleteCharacter', index);
    },
  },
  getters: {
    characters: (state) => state.characters,
  },
};
