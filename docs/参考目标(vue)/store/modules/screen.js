const state = {
  screenWidth: document.body.clientWidth
}

const mutations = {
  UPDATE_SCREEN_WIDTH(state, value) {
    state.screenWidth = value
  }
}

const actions = {}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
