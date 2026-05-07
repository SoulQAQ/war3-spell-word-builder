import wwbTools from '@/views/word_builder/tools/tools'
/* Spell */
const default_spell_module = {
  name: null, // 技能名称
  hotKey: null, // 热键
  learn: { // 学习文本设置
    title: null, // 学习标题
    tip: { // 学习扩展文本
      effect: null, // 效果描述
      attr: () => this.attrData.filter(e => !Array.isArray(e)), // 属性
      lvEffect: [ // 每个等级的效果描述
        // { text: '造成{a}点伤害和{b}秒眩晕', data: [100,3] }
      ],
    },
  },
  attrData: [
    /**
     * { name: '法力消耗', value: null }
     * or
     * { name: '法力消耗', value: [] }
     */
  ],
  normal: { // 普通技能文本
    attr: () => this.attrData.filter(e => e.name !== '法力消耗'),
    title: null, // 标题
    tip: [
      /** { text: '造成{a}点伤害和{b}秒眩晕', data: [100,3] } */
    ]
  },
  nature: null, // 特点
  toWord: (color, module, lv) => {
    let result = ''
    if (module) {
      if (module === 'title') {
        if (lv) {
          result += `${this.name}(${wwbTools.dyeing(this.hotKey, color.hotKey)})`
          result += ` - [${wwbTools.dyeing(lv + '级', color.level)}]`
        } else {
          lv = '%d'
          result += `学习 ${wwbTools.dyeing(lv + '级', color.level)} ${this.name}(${wwbTools.dyeing(this.hotKey, color.hotKey)})`
        }
      } else if (module === 'uberTip') {
        if (lv) { // 有lv，返回普通文本
          lv = Math.min(lv, this.normal.tip.length)
          let d = this.normal.tip[lv]
          result += d.text.format(...d.data)
          result += this.nature ? ('\n\n' + wwbTools.dyeing(this.nature, color.nature)) : ''
          if (this.normal.attr().length > 0) {
            result += ('\n')
            this.normal.attr().forEach((e) => {
              result += ('\n' + wwbTools.dyeing(e.name, color.property) + '：')
              try {
                result += (Array.isArray(e.value) ? e.value[lv] : e.value)
              } catch (e) {
                result += e.value[e.value.length - 1]
              }
            })
          }
        } else { // 无lv，返回学习文本
          result += (this.learn.tip.effect)
          result += this.nature ? ('\n\n' + wwbTools.dyeing(this.nature, color.nature)) : ''
          if (this.learn.tip.attr().length > 0) {
            result += '\n'
            this.learn.tip.attr().forEach((e) => {
              result += ('\n' + wwbTools.dyeing(e.name, color.property) + '：')
              try {
                result += (Array.isArray(e.value) ? e.value[lv] : e.value)
              } catch (e) {
                result += e.value[e.value.length - 1]
              }
            })
          }
          if (this.learn.tip.lvEffect?.length > 0) {
            result += '\n'
            this.learn.tip.lvEffect.forEach((e, i) => {
              result += ('\n' + wwbTools.dyeing((i + 1) + '级 - ', color.learnUpdateLevel))
              result += (e.text.format(...e.data))
            })
          }
        }
      }
    }
    return result
  },
}


/* Unit */
const default_unit_module = {
  name: null, // 单位名称
  desc: null, // 单位描述，可填充数据项
  descValues: null, // 单位描述数据
  hotKey: null, // 热键
  spells: [ // 技能列表，可以是对象列表，也可以是字符串列表
    {
      name: null, // 技能名称
      desc: null, // 技能简述，不可填充数据，可选项
    }, {
      name: null, // 技能名称
      desc: null, // 技能简述，不可填充数据，可选项
    },
  ],
  nature: null, // 特点
  attack: { // 攻击力设置
    max: null, // 攻击力上限
    min: null, // 攻击力下限
    dice: { // 骰子设置
      count: null, // 骰子个数
      sides: null, // 骰子面数
    },
    type: null, // 攻击力类型
    range: null, // 射程
  },
  hp: null, // 最大生命值
  mp: null, // 最大法力值
  armor: { // 护甲设置
    value: null, // 护甲值
    type: null // 护甲类型
  },
}

/* item */
const default_item_module = {
  overlapping: false, // 是否可叠加，默认否
  hotKey: null, // 热键
  uses: 0, // 使用次数，默认是0
  price: 125, // 价格，默认是125
  desc: { // 说明设置
    tip: null, // 放地上鼠标点击显示的文本提示
    title: null, // 标题
    uberTip: null, // 扩展
  },
  cd: { // 冷却时间，默认不显示
    show: false,
    value: 0
  },
  beLost: true, // 可以被丢弃
  beSold: true, // 可卖给商店
  attributes: [ // 属性
    {
      type: 'gain', // gain=增益；reduce=减损；spell=技能
      name: null, // 属性名称,类型为spell时为技能名
      tip: null, // 技能描述，类型是spell时显示
      value: null, // 属性值，类型是spell时不显示
    },
    /**
     * example: { type: gain, name: 力量, value: 3} -> result: 力量+3
     * example: { type: reduce, name: 力量, value: 3} -> result: |cffff0000力量-3|r
     * example: { type: spell, name: 能量冲击, tip: 召唤能量光柱攻击敌人，造成100点伤害和3秒眩晕。} ->
     *           result: |cff00ff00能量冲击|r|n召唤能量光柱攻击敌人，造成100点伤害和3秒眩晕。
     */
  ],
}
