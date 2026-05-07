/**
 * chatGPT改进版
 */
interface StorageItem {
  value: any;
  lostTime?: Date;
}

const storageHelper = {
  /**
   *
   * @param name 保存名称
   * @param key 保存的key
   * @param value 保存的值
   * @param time 失活时间，默认无限
   */
  set: function (name: string, key: string, value: any, time?: Date): void {
    const str = localStorage.getItem(name);
    let storage: { [key: string]: StorageItem };
    try {
      storage = JSON.parse(str || '{}')
    } catch (e) {
      console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
      console.error('目标数据：\n' + str)
      return;
    }
    storage[key] = {
      value,
      lostTime: time,
    }
    localStorage.setItem(name, JSON.stringify(storage))
  },
  /**
   * 读取数据
   * @param name
   * @param key
   */
  get: function (name: string, key: string): any {
    const str = localStorage.getItem(name);
    let storage: { [key: string]: StorageItem };
    try {
      storage = JSON.parse(str)
    } catch (e) {
      console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
      console.error('目标数据：\n' + str)
      return;
    }
    this.clearLostTimeData(name)
    return storage[key]?.value;
  },
  /**
   * 删除目标数据
   * @param name
   * @param key
   */
  remove: function (name: string, key?: string | string[]) {
    if (!name) return;
    const str = localStorage.getItem(name);
    let storage: { [key: string]: StorageItem };
    try {
      storage = JSON.parse(str || '{}')
    } catch (e) {
      console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
      console.error('目标数据：\n' + str)
      return;
    }
    if (!key) {
      localStorage.removeItem(name);
      return;
    }
    const keys = Array.isArray(key) ? key : [key];
    for (const k of keys) {
      if (storage[k]) {
        storage[k] = undefined;
      }
    }
    localStorage.setItem(name, JSON.stringify(storage));
  },
  /**
   * 清除失活的数据
   * @param name
   */
  clearLostTimeData: function (name: string): boolean {
    const str = localStorage.getItem(name);
    let storage: { [key: string]: StorageItem };
    try {
      storage = JSON.parse(str || '{}');
    } catch (e) {
      return false;
    }
    const keys = Object.keys(storage);
    const now = new Date().getTime();
    let changed = false;
    for (const k of keys) {
      if (storage[k].lostTime && storage[k].lostTime.getTime() < now) {
        storage[k] = undefined;
        changed = true;
      }
    }
    if (changed) {
      const remainingKeys = Object.keys(storage).filter(k => storage[k]);
      if (remainingKeys.length > 0) {
        localStorage.setItem(name, JSON.stringify(storage));
      } else {
        localStorage.removeItem(name);
      }
    }
    return changed;
  },
};

export default storageHelper;


/**
 * 原始版本
 */
// const storageHelper = {
//   /**
//    *
//    * @param name 保存名称
//    * @param key 保存的key
//    * @param value 保存的值
//    * @param time 失活时间，默认无限
//    */
//   set: function (name: string, key: string, value: any, time: Date = undefined) {
//     const str = localStorage.getItem(name);
//     let storage: object;
//     try {
//       storage = JSON.parse(str || '{}')
//     } catch (e) {
//       console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
//       console.error('目标数据：\n' + str)
//       return;
//     }
//     storage[key] = {
//       value,
//       lostTime: time,
//     }
//     localStorage.setItem(name, JSON.stringify(storage))
//   },
//   get: function (name: string, key: string): any {
//     const str = localStorage.getItem(name);
//     let storage: object;
//     try {
//       storage = JSON.parse(str)
//     } catch (e) {
//       console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
//       console.error('目标数据：\n' + str)
//       return;
//     }
//     this.clearLostTimeData(name)
//     return storage[key].data
//   },
//   remove: function (name: string, key: any) {
//     if (name) {
//       if (key) {
//         const str = localStorage.getItem(name);
//         let storage: object;
//         try {
//           storage = JSON.parse(str)
//         } catch (e) {
//           console.error(`无法解析数据名称 "${name}" ，该数据可能已损坏。`)
//           console.error('目标数据：\n' + str)
//           return;
//         }
//         if (Array.isArray(key)) {
//
//         }
//       } else {
//         localStorage.removeItem(name)
//       }
//     }
//   },
//   clearLostTimeData: function (name: string) {
//     const str = localStorage.getItem(name);
//     let storage: object;
//     try {
//       storage = JSON.parse(str);
//     } catch (e) {
//       return false;
//     }
//     let keys = Object.keys(storage)
//     let now = new Date().getTime()
//     keys.forEach((key, i) => {
//       if (storage[key].lostTime && storage[key].lostTime.getTime() < now) {
//         storage[key] = undefined
//       }
//     })
//     keys = Object.keys(storage)
//     if (keys.length == 0) {
//       localStorage.removeItem(name)
//       return false;
//     } else {
//       return true;
//     }
//   },
// }
//
// export default storageHelper

