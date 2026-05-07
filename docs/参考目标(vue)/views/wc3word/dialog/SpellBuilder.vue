<template>
  <el-dialog ref="dialog" width="50%" :title="title" :visible.sync="visible" @close="closeDialog"
             :append-to-body="true" :show-close="false" :transition="dialogTransition">
    <div class="builder-dialog">
      <el-col :span="12" style="padding-right: 20px;">
        <el-divider content-position="center">结果展示</el-divider>
        <spell :spell-data="spell" :module="spellModule" :color-config="color"/>
      </el-col>
      <el-col :span="11" :offset="1" class="cp-rect">
        <el-divider content-position="left">结果展示设置</el-divider>
        <el-radio-group v-model="spellModule" size="mini">
          <el-radio-button label="学习"></el-radio-button>
          <el-radio-button label="普通"></el-radio-button>
        </el-radio-group>
        <el-row class="cp-item">
          <el-radio-group v-model="spellData.lv" size="mini">
            <el-radio-button
              v-for="(e,i) in exampleLevelList"
              :label="(i+1)"
            >{{ (1 + i) + '级' }}
            </el-radio-button>
          </el-radio-group>
        </el-row>
        <el-row class="cp-item">
          <el-divider content-position="left">点击复制</el-divider>
          <el-button-group>
            <el-button type="success" plain size="mini"
                       @click="handleBuilder('title')">学习标题
            </el-button>
            <el-button type="success" plain size="mini"
                       @click="handleBuilder('export')">学习扩展
            </el-button>
          </el-button-group>
        </el-row>
        <el-row class="cp-item" v-for="(e,i) in spell.updateWord.vals">
          <el-button-group>
            <el-button :type="i%2===1?'success':'primary'" plain size="mini"
                       @click="handleBuilder('title', (i+1))">
              {{ (i + 1) }}级标题
            </el-button>
            <el-button :type="i%2===1?'success':'primary'" plain size="mini"
                       @click="handleBuilder('export', (i+1))">
              {{ (i + 1) }}级扩展
            </el-button>
          </el-button-group>
        </el-row>
      </el-col>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button @click="visible = false" size="mini">关闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import Spell from "@/views/wc3word/spell";
import {copyToClipboard} from "@/utils/tools";

export default {
  name: 'SpellBuilderDialog',
  props: {
    spellData: {
      type: Object,
      default: () => false
    },
    colorConfig: Object,
    show: {
      type: Boolean,
      default: () => false
    }
  },
  components: {Spell},
  data() {
    return {
      visible: this.show,
      spellModule: '学习',
      dialogTransition: 'dialog-fade'
    }
  },
  computed: {
    spell() {
      return this.spellData
    },
    exampleLevelList() {
      return this.spellData.updateWord.vals.length || 1
    },
    color() {
      return this.colorConfig
    },
    title() {
      return '技能文本生成结果'
    }
  },
  watch: {
    visible() {
      this.$emit('update:show', false)
    }
  },
  created() {

  },
  mounted() {
  },
  methods: {
    closeDialog() {
      // 关闭
    },
    handleSave() {
    },
    dyeing(str, color) {
      const prefix = '|cff'
      const suffix = '|r'
      return color ? (prefix + color.replace('#', "") + str + suffix) : str
    },
    handleBuilder(module, lv) {
      const {learnLevel, property, hotKey, level, learnUpdateLevel, nature} = this.color
      const sp = this.spell
      let result = ''
      if (!lv) {
        // 无lv 是学习文本
        lv = '%d'
        if (module === 'title') {
          result = `学习 ${this.dyeing(lv + ' 级', learnLevel)} ${sp.name}(${this.dyeing(sp.hotKey, hotKey)})`
        } else if (module === 'export') {
          result += sp.effect + '\n'
          result += sp.natual ? (sp.natual + '\n') : ''
          sp.pros.forEach(e => {
            result += `\n${this.dyeing(e.name, property)}：${e.val}`
          })
          if (sp.updateWord.text && sp.updateWord.vals) {
            result += "\n"
            sp.updateWord.vals.forEach((v, i) => {
              let w = sp.updateWord.text.format(v)
              w = w.endsWith("。") ? w : w + "。"
              result += `\n${this.dyeing((i + 1) + '级', learnUpdateLevel)} - ${w}`
            })
          }
        }
      } else {
        // 有lv 是普通文本
        if (module === 'title') {
          result = `${sp.name}(${this.dyeing(sp.hotKey, hotKey)}) - [${this.dyeing(lv + ' 级', learnLevel)}]`
        } else if (module === 'export') {
          let n = sp.normalWord
          let ps = sp.pros.filter(e => e.name !== '法力消耗')
          result += n.text.format(n.vals[lv - 1])
          result += sp.natual ? (sp.natual + '\n') : ''
          if (ps && ps.length > 0) {
            result += '\n'
            ps.forEach(p => {
              result += `\n${this.dyeing(p.name, property)}：${p.val}`
            })
          }
        }
      }
      // console.log('result -> ', result)
      // return result
      copyToClipboard(result)
      const h = this.$createElement;
      this.$notify({
        title: '来自Soul2的提示',
        message: h('span', {style: 'color: teal'}, '生成的文本已输出到剪切板。'),
        position: 'bottom-right',
        duration: 3000,
        // showClose: false
      });
    }
  }
}
</script>

<style scoped lang="scss">
.builder-dialog {
  overflow-y: auto;
  min-height: 35vh;
  padding-left: 5%;
  padding-right: 5%;

  .cp-rect .cp-item {
    margin-top: 8px;
    margin-bottom: 8px;
  }
}
</style>
