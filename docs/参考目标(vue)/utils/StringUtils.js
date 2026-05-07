/**
 * 调用示例：
 *
 * var template1="我是{0}，今年{1}了";
 * var template2="我是{name}，今年{age}了";
 * var result1=template1.format("loogn",22);
 * var result2=template1.format({name:"loogn",age:22});
 */

String.prototype.format = function (args) {
  if (arguments.length > 0) {
    var result = this;
    if (arguments.length == 1 && typeof (args) == "object") {
      for (var key in args) {
        var reg = new RegExp("({" + key + "})", "g");
        result = result.replace(reg, args[key]);
      }
    } else {
      for (var i = 0; i < arguments.length; i++) {
        if (arguments[i] == undefined) {
          return "";
        } else {
          var reg = new RegExp("({[" + i + "]})", "g");
          result = result.replace(reg, arguments[i]);
        }
      }
    }
    return result;
  } else {
    return this;
  }
}

// chatGPT的 2.0 改进建议
// String.prototype.format = function (...args) {
//   const pattern = /\{(\d*|\w*)\}/g;
//   return this.replace(pattern, (match, p1) => {
//     if (p1 === '') {
//       throw new Error('占位符不能为空');
//     }
//
//     if (isNaN(p1)) {
//       if (!args[0] || typeof args[0] !== 'object') {
//         throw new Error('需要传入一个对象作为参数');
//       }
//
//       const value = args[0][p1];
//       if (value === undefined) {
//         throw new Error(`对象中没有名为${p1}的属性`);
//       }
//
//       return value;
//     }
//
//     const index = parseInt(p1);
//     if (index >= args.length) {
//       throw new Error(`占位符{${p1}}没有对应的参数`);
//     }
//
//     return args[index];
//   });
// };

/**
 * 取出所有a到b中间的字符串
 *
 * @param a
 * @param b
 */
String.prototype.between = function (a, b) {
  if (arguments.length > 0) {
    var results = [];
    var reg = new RegExp(`\\${a}([^\\${b}]+)\\${b}`, "g");
    var match;
    while ((match = reg.exec(this)) !== null) {
      results.push(match[1]);
    }
    return results;
  } else {
    return this.between("{", "}");
  }
}

