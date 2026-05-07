import Vue from 'vue'
import Vuex from 'vuex'
import getters from "@/store/getters";
import menu from "@/store/modules/menu";
import screen from "@/store/modules/screen";

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    menu,
    screen
  },
  getters
})

export default store
