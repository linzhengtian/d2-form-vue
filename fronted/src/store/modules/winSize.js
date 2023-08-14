const state = {
  winheight: 0,
  winWidth: 0
};

const mutations = {
  setWinSize(state, { height, width }) {
    state.winheight = height;
    state.winWidth = width;
  }
};

const actions = {
  setWinSize({ commit }, data) {
    commit("setWinSize", data);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};

