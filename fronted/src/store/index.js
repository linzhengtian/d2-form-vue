import Vue from "vue";
import Vuex from "vuex";
import app from "./modules/app";
import user from "./modules/user";
import tagsView from "./modules/tagsView";
import permission from "./modules/permission";
import settings from "./modules/settings";
import winSize from "./modules/winSize";
import modelSelect from "./modules/modelSelect";
import getters from "./getters";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    app,
    user,
    tagsView,
    permission,
    settings,
    modelSelect,
    winSize
  },
  getters
});

store.dispatch("winSize/setWinSize", {
  height: window.innerHeight,
  width: window.innerWidth
});

window.addEventListener("resize", () => {
  store.dispatch("winSize/setWinSize", {
    height: window.innerHeight,
    width: window.innerWidth
  });
});

export default store;
