const wwbTools = {
  dyeing: (str, color) => {
    const prefix = '|cfff'
    const suffix = '|r'
    return color ? (prefix + color.replace('#', "") + str + suffix) : str
  },
}
export default wwbTools
