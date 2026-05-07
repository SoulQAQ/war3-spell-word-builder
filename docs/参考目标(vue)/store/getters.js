const getters = {
  routes: state => state.menu.routes,
  screenWidth: state => state.screen.screenWidth,
  screenPadding: state => {
    let width = state.screen.screenWidth
    if (width >= 600) {
      if (width >= 1000) {
        return {paddingLeft: '15%', paddingRight: '15%'}
      } else {
        return {paddingLeft: '5%', paddingRight: '5%'}
      }
    } else {
      return {}
    }
  }
}

export default getters
