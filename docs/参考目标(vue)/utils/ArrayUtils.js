/**
 * 求出多个数组的最小长度
 * @returns {*|number}
 */
Array.prototype.minFor = function () {
  return this.reduce((min, arr) => Math.min(min, arr.length), Infinity);
}

/**
 * 让每个子数组只保留前n个元素
 * @param n
 * @returns {*[]}
 */
Array.prototype.startCut = function (n) {
  return this.map(arr => arr.slice(0, n));
}
