export const defaultColorConfig = {
  learnLevel: '#33ccff',
  property: '#33cc33',
  hotKey: '#ffcc00',
  level: '#33ccff',
  learnUpdateLevel: '#ff9900',
  nature: '#ffcccc'
}

export function createObjs(len, fn) {
  let arr = [];
  for (let i = 0; i < len; i++) {
    let res = fn(i)
    arr.push(res)
  }
  return arr
}

export function formula2arr(str, keys = 'abcdefghijklmnopqrstuvwxyz'.split('')) {
  // 解析数量
  let formulas = str.split(';');
  const num = parseInt(formulas[0])
  // 解析参数
  formulas = formulas[1].split('/');
  // 构建返回
  const result = [];
  // 解析公式
  formulas = formulas.map((f) => {
    let formula = f.split("+")
    formula = formula.map(e => parseInt(e))
    return {
      base: formula[0],
      plus: formula[1]
    }
  })
  // 生成对象
  for (let i = 0; i < num; i++) {
    let obj = {}
    for (let j = 0; j < formulas.length; j++) {
      let key = keys[j]
      obj[key] = formulas[j].base + formulas[j].plus * i
    }
    result.push(obj)
  }
  return result;
}

function toCfg(s, c) {
  if (typeof s !== 'string') {
    return c
  }
  let items = s.split(", ")
  let cfg = c
  if (items.length > 0) {
    items.forEach((e) => {
      let p = e.split(":")
      cfg[p[0]] = p[1]
    })
  }
  return cfg
}

/**
 * 以[xxx]的形式分析数据，自定义配置使用{}在参数str内附带，没有指定自定义配置时会使用默认配置
 * 例：[a=2/3/4][b=16+8][lv=3]{ls:/, fs:,}
 * warning: 自定义配置以“， ”为分隔符，空格不可省略
 *
 * @param str
 * @param cfg <ul>配置:
 *                <li>fs：公式数据的分隔符</li>
 *                <li>ls：数值列表的分隔符</li>
 *                <li>es：属性的分隔符</li>
 *                <li>lv：等级的属性名</li>
 * </ul>
 * @returns {*[]}
 */
export function conversion(str, cfg = {fs: "+", ls: ",", es: "=", lv: "lv"}) {
  // 加载自定义配置
  cfg = toCfg(str.between()[0], cfg)
  // 过滤无效信息
  const pairs = checkValid((str).between("[", "]"))
  // 判断必备条件，否则返回空数组
  if (str.indexOf("[" + cfg.lv + cfg.es) === -1 || isNaN(parseInt((str).between("[" + cfg.lv + cfg.es, "]")))) {
    return []
  }
  const lv = parseInt((str).between("[" + cfg.lv + cfg.es, "]"))
  let items = {}
  let itemKeys = []
  const result = []
  pairs.forEach(pair => {
    let p = pair.split(cfg.es)
    itemKeys.push(p[0])
    if (p[1].indexOf(cfg.fs) !== -1) { // 有+号，是公式
      let fps = p[1].split(cfg.fs)
      let rules = {base: parseFloat(fps[0]), plus: parseFloat(fps[1])}
      items[p[0]] = createObjs(lv, i => rules.base + rules.plus * i)
    } else { // 没有+号，是数值list
      items[p[0]] = arrCut(p[1].split(cfg.ls).filter(e => !isNaN(parseFloat(e))).map(e => parseFloat(e)), lv)
    }
  })
  for (let i = 0; i < lv; i++) {
    let obj = {}
    itemKeys.forEach((k, n) => {
      obj[k] = items[k][i]
    })
    result.push(obj)
  }
  return result
}

/**
 * 检查输入的内容是否为a=b的形式，并返回合格的内容
 * a的通过规则：为a-z的其中一个
 * b可以是任意字符串
 *
 * @param arr
 * @returns {*[]}
 */
export function checkValid(arr) {
  const result = [];
  for (let i = 0; i < arr.length; i++) {
    const str = arr[i];
    const regex = /^[a-z]=[^\s]+$/;
    if (regex.test(str)) {
      result.push(str);
    }
  }
  return result;
}

export function copyToClipboard(text) {
  const textarea = document.createElement('textarea'); // 创建一个文本域元素
  textarea.value = text; // 将传入的文本内容赋值给文本域
  textarea.setAttribute('readonly', ''); // 设置文本域只读
  textarea.style.position = 'absolute';
  textarea.style.left = '-9999px'; // 将文本域定位到屏幕外
  document.body.appendChild(textarea); // 将文本域添加到页面上
  textarea.select(); // 选中文本域中的内容
  document.execCommand('copy'); // 将选中的内容复制到系统剪切板
  document.body.removeChild(textarea); // 移除文本域
}


/**
 * 如果a的长度超过b就返回a的前b项
 * 如果小于则添加字符串"null"使a的长度到达b
 * 如果相等则直接返回a
 *
 * @param arr
 * @param targetLength
 * @returns {*}
 */
function arrCut(arr, targetLength) {
  if (arr.length > targetLength) {
    return arr.slice(0, targetLength);
  } else if (arr.length < targetLength) {
    let nulls = new Array(targetLength - arr.length).fill("null");
    return arr.concat(nulls);
  } else {
    return arr;
  }
}

/**
 * 中文标点符号换成英文标点符号，以赋予输入中文符号不出错的能力
 *
 * @param str
 * @returns {*}
 * @constructor
 */
export function symbolCn2En(str) {
  if (Array.isArray(str)) {
    return str.map(s => symbolCn2En(s));
  }
  const map = {
    '，': ',',
    '。': '.',
    '？': '?',
    '！': '!',
    '：': ':',
    '；': ';',
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '（': '(',
    '）': ')',
    '【': '[',
    '】': ']',
    '《': '<',
    '》': '>',
    '、': ','
  };
  return str.replaceAll(/[\u4e00-\u9fa5]/g, c => map[c] || c);
}
