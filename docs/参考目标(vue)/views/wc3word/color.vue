<template>
  <div class="app-container">
    <el-form ref="form" :model="colorConfig" label-width="110px">
      <el-col :span="11" class="example-box">
        <spell
          v-if="e.name === exampleSpell"
          v-for="(e,i) in exampleSpellList"
          :spell-data="e"
          :color-config="colorConfig"
          :module="effectExample"
        />
      </el-col>
      <el-col :span="12" :offset="1" class="example-setting">
        <el-row style="text-align:left;">
          <el-divider content-position="left">示例设置</el-divider>
          <p>
            <el-radio-group v-model="effectExample" size="mini">
              <el-radio-button label="学习"></el-radio-button>
              <el-radio-button label="普通"></el-radio-button>
            </el-radio-group>
          </p>
          <p>
            <el-radio-group v-model="exampleSpell" size="mini" @change="handleExampleChange">
              <el-radio-button v-for="(e,i) in exampleSpellList" :label="e.name"></el-radio-button>
            </el-radio-group>
          </p>
          <p>
            <el-radio-group v-model="exampleLevel" size="mini" @change="handleExampleLevelChange">
              <el-radio-button
                v-for="(e,i) in exampleLevelList"
                :label="(i+1)"
              >{{ (1 + i) + '级' }}
              </el-radio-button>
            </el-radio-group>
          </p>
        </el-row>
        <el-row style="margin-top: 15px;">
          <el-form-item label="热键：" style="margin-bottom: 0;">
            <el-col :span="5">
              <el-color-picker size="mini" v-model="colorConfig.hotKey"/>
            </el-col>
            <el-col :span="7">{{ colorConfig.hotKey }}</el-col>
          </el-form-item>
          <el-form-item label="学习等级：" style="margin-bottom: 0;">
            <el-col :span="5">
              <el-color-picker size="mini" v-model="colorConfig.learnLevel"/>
            </el-col>
            <el-col :span="7">{{ colorConfig.learnLevel }}</el-col>
          </el-form-item>
          <el-form-item label="技能属性：" style="margin-bottom: 0;">
            <el-col :span="5">
              <el-color-picker size="mini" v-model="colorConfig.property"/>
            </el-col>
            <el-col :span="7">{{ colorConfig.property }}</el-col>
          </el-form-item>
          <el-form-item label="升级等级前缀：" style="margin-bottom: 0;">
            <el-col :span="5">
              <el-color-picker size="mini" v-model="colorConfig.learnUpdateLevel"/>
            </el-col>
            <el-col :span="7">{{ colorConfig.learnUpdateLevel }}</el-col>
          </el-form-item>
          <el-form-item label="特殊描述：" style="margin-bottom: 0;">
            <el-col :span="5">
              <el-color-picker size="mini" v-model="colorConfig.nature"/>
            </el-col>
            <el-col :span="7">{{ colorConfig.nature }}</el-col>
          </el-form-item>
          <div style="text-align:right;margin-top: 15px;margin-bottom: 15px;">
            <el-button size="mini" type="primary" plain @click="resetColorConfig">恢复默认</el-button>
            <el-button size="mini" type="success" plain @click="saveColorConfig">保存</el-button>
            <el-button size="mini" type="warning" plain @click="loadColorConfig">读取</el-button>
            <el-button size="mini" type="danger" plain @click="removeColorConfig">删除</el-button>
          </div>
        </el-row>
      </el-col>
    </el-form>

  </div>
</template>

<script>
import Spell from "@/views/wc3word/spell";
import {createObjs, defaultColorConfig} from "@/utils/tools";


export default {
  name: 'Color',
  props: {
    colorDefaultConfig: Object
  },
  components: {Spell, defaultColorConfig},
  data() {
    return {
      colorCfg: {},
      exampleSpell: null,
      exampleLevel: 1,
      effectExample: '学习',
      exampleSpellList: [
        {
          id: "Ahtb",
          lv: "1",
          name: "风暴之锤",
          hotKey: "T",
          effect: "向目标投掷一巨大的魔法锤，对其造成一定伤害并使其陷入眩晕。",
          pros: [
            {name: '法力消耗', val: '75'},
            {name: '施法距离', val: '800'},
            {name: '冷却时间', val: '6'},
          ],
          updateWord: {
            text: "{d}点伤害，{t}秒的晕眩时间",
            vals: createObjs(5, i => ({d: 100 + i * 110, t: 3 + i}))
          },
          nature: "",
          normalWord: {
            text: '向目标投掷一巨大的魔法锤，对其造成{d}点伤害并使其{t}秒内处于眩晕状态。',
            vals: createObjs(5, i => ({d: 100 + i * 110, t: 3 + i}))
          }
        },
        {
          id: "Ahbz",
          lv: "1",
          name: "暴风雪",
          hotKey: "F",
          effect: "能召唤出若干次冰片攻击，对目标区域内的单位造成一定的伤害。",
          pros: [
            {name: '法力消耗', val: '75'},
            {name: '施法距离', val: '600'},
            {name: '冷却时间', val: '9'},
          ],
          updateWord: {
            text: "召唤{c}次，每次{d}点伤害。",
            vals: createObjs(6, i => ({c: i * 2 + 6, d: i * 10 + 30}))
          },
          nature: "需要持续施法",
          normalWord: {
            text: '召唤出{c}次的冰片攻击，每一次攻击能对一小块区域内的单位造成{d}的伤害值。',
            vals: createObjs(6, i => ({c: i * 2 + 6, d: i * 10 + 30}))
          }
        },
      ],
    }
  },
  computed: {
    exampleLevelList() {
      return this.exampleSpellList.filter(e => e.name === this.exampleSpell)[0].updateWord.vals.length
    },
    colorConfig() {
      return this.colorCfg
    }
  },
  watch: {
    colorCfg() {
      this.$emit("updateCfg", this.colorCfg)
    }
  },
  created() {
    this.colorCfg = Object.assign({}, this.colorDefaultConfig)
    this.exampleSpell = this.exampleSpellList[0].name
  },
  mounted() {
  },
  methods: {
    saveColorConfig() {
      // console.log('saving')
      let colorConfigList = JSON.parse(localStorage.getItem('color-config-list') || '[]')
      let colorCfgNames = colorConfigList.map(e => e.name)
      this.$prompt('取个名字吧!\n会覆盖同名的方案。', '提示', {
        confirmButtonText: '确定',
        // cancelButtonText: '取消',
        showCancelButton: false,
        showClose: false,
      }).then(({value}) => {
        let index = colorCfgNames.indexOf(value)
        if (index === -1) {
          colorConfigList.push({name: value, cfg: this.colorConfig})
        } else {
          colorConfigList[index].cfg = this.colorConfig
        }
        localStorage.setItem('color-config-list', JSON.stringify(colorConfigList))
        this.$message({type: 'success', message: '保存成功！'});
      }).catch(() => {
      });
    },
    loadColorConfig() {
      let colorConfigList = JSON.parse(localStorage.getItem('color-config-list') || '[]')
      if (colorConfigList.length > 0) {
        let colorCfgNames = colorConfigList.map(e => e.name)
        this.$prompt('你要读取哪个方案？\n已保存方案：\n' + colorCfgNames, '提示', {
          confirmButtonText: '确定',
          // cancelButtonText: '取消',
          showCancelButton: false,
          showClose: false,
        }).then(({value}) => {
          let index = colorCfgNames.indexOf(value)
          if (index === -1) {
            this.$message({type: 'error', message: '方案不存在！'});
          } else {
            this.colorConfig = colorConfigList[index].cfg
            this.$message({type: 'success', message: '读取成功！'});
          }
        }).catch(() => {
        });
      } else {
        this.$message({type: 'error', message: '没有已保存的方案！'});
      }
    },
    removeColorConfig() {
      let colorConfigList = JSON.parse(localStorage.getItem('color-config-list') || '[]')
      if (colorConfigList.length > 0) {
        let colorCfgNames = colorConfigList.map(e => e.name)
        this.$prompt('你要删除哪个方案？\n已保存方案的名称有：\n' + colorCfgNames,
          '提示', {
            confirmButtonText: '确定',
            // cancelButtonText: '取消',
            showCancelButton: false,
            showClose: false,
          }).then(({value}) => {
          let index = colorCfgNames.indexOf(value)
          if (index === -1) {
            this.$message({type: 'error', message: '方案不存在！'});
          } else {
            colorConfigList = colorConfigList.filter(e => e !== colorConfigList[index])
            localStorage.setItem('color-config-list', JSON.stringify(colorConfigList))
            this.$message({type: 'success', message: '操作成功！'});
          }
        }).catch(() => {
        });
      } else {
        this.$message({type: 'error', message: '没有已保存的方案！'});
      }
    },
    resetColorConfig() {
      // console.log('reset')
      this.colorCfg = Object.assign({}, defaultColorConfig)
    },
    handleExampleChange() {
      this.exampleSpellList.map(e => e.lv = 1)
      this.exampleLevel = 1
    },
    handleExampleLevelChange() {
      this.exampleSpellList.map(e => e.lv = this.exampleLevel)
    }
  }
}
</script>

<style scoped lang="scss">

.example-setting el-form-item {
  el-color-picker {
    min-width: 80px;
  }

  margin-bottom: 0;
}

.example-setting p {
  margin-top: 15px;
}

.example-box {
  max-height: 40vh;
}

.example-box p {
  font-size: 12px !important;
  font-weight: bold !important;
  overflow-y: auto;
  max-height: 30vh;
}
</style>
