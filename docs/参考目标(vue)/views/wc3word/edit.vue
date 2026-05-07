<template>
  <div class="edit-container">
    <el-col :span="9" style="padding-top: 2vh;text-align:left;">
      <el-row class="spell-info-setting">
        <el-radio-group v-model="spellInfo.module" size="mini">
          <el-radio-button label="学习"></el-radio-button>
          <el-radio-button label="普通"></el-radio-button>
        </el-radio-group>
      </el-row>
      <el-row class="spell-info-setting">
        <el-radio-group v-model="spellData.lv" size="mini">
          <el-radio-button
            v-for="(e,i) in exampleLevelList"
            :label="(i+1)"
          >{{ (1 + i) + '级' }}
          </el-radio-button>
        </el-radio-group>
      </el-row>
      <el-row class="spell-info-setting">
        <el-button size="mini" type="success" plain @click="handleBuilder">生成</el-button>
        <el-button size="mini" type="primary" plain @click="handleResetSpellData">恢复默认</el-button>
      </el-row>
      <spell :module="spellInfo.module" :spell-data="spellData" :color-config="colorConfig"/>
    </el-col>
    <el-col :span="14" :offset="1">
      <el-card shadow="always">
        <el-form class="edit-form" size="mini" ref="editForm" v-model="spellData" label-width="90px">
          <el-divider content-position="left">在此填写</el-divider>
          <el-row>
            <el-col :span="18">
              <el-form-item label="名称">
                <el-col :span="21">
                  <el-input v-model="spellData.name" placeholder="技能名称"/>
                </el-col>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="热键" label-width="45px">
                <el-input v-model="spellData.hotKey" placeholder="热键"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-form-item label="技能描述">
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 3}"
                        placeholder="例：能召唤出若干次冰片攻击，对目标区域内的单位造成一定的伤害。"
                        v-model="spellData.effect"/>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="特点">
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 3}" placeholder="例：需要持续施法"
                        v-model="spellData.nature"/>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item>
              <template slot="label">
                <span>升级描述</span>
                <el-tooltip placement="top" effect="light">
                  <template slot="content">
                    用{}来标记数值的位置，{}内用<span style="color:#f00;">各不相同</span>的小写abcd来区分。<br>
                    例：{a}点伤害，晕眩时间{b}秒。<br>
                    数值的语法:<br>
                    [lv=3][a=1,2,3][b=20+10]<br>
                    其中a、b与上述数值的标记对应；lv=3表示一共有3个等级 <br>
                    [b=20+10]中 20+10表示公式，意思是1级是20，后面每级+10；而[a=1,2,3]表示每个等级的数值
                  </template>
                  <i class="el-icon-question" style="cursor:pointer;"></i>
                </el-tooltip>
              </template>
              <el-input placeholder="学习技能时显示的“1级 - xx伤害，xx秒时间。”"
                        v-model="spellData.updateWord.text" @change="handleTempDataForUpdate"/>
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}"
                        placeholder="数值"
                        v-model="tempData.updateWord" @change="handleTempDataForUpdate"/>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item>
              <template slot="label">
                <span>普通描述</span>
                <el-tooltip placement="top" effect="light">
                  <template slot="content">
                    用{}来标记数值的位置，{}内用<span style="color:#f00;">各不相同</span>的小写abcd来区分。<br>
                    例：造成{a}点伤害并使其{b}秒内陷入晕眩。
                    数值的语法:<br>
                    [lv=3][a=1,2,3][b=20+10]<br>
                    其中a、b与上述数值的标记对应；lv=3表示一共有3个等级 <br>
                    [b=20+10]中 20+10表示公式，意思是1级是20，后面每级+10；而[a=1,2,3]表示每个等级的数值
                  </template>
                  <i class="el-icon-question" style="cursor:pointer;"></i>
                </el-tooltip>
              </template>
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}"
                        placeholder="向目标投掷一巨大的魔法锤，对其造成100点伤害并使其3秒内处于眩晕状态。"
                        v-model="spellData.normalWord.text" @change="handleTempDataForNormal"/>
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4}"
                        placeholder="数值"
                        v-model="tempData.normalWord" @change="handleTempDataForNormal"/>
            </el-form-item>
          </el-row>
          <el-divider content-position="left">技能属性</el-divider>
          <el-row v-for="(e,i) in spellData.pros" style="margin-bottom: 12px;">
            <el-col :span="2" style="line-height: 40px;text-align:right;">
              <i class="el-icon-remove" style="font-size: 18px; margin-right: 5px;cursor: pointer;color:#F56C6C;"
                 @click="spellData.pros = spellData.pros.filter(f=>f!==e)"></i>
            </el-col>
            <el-col :span="13">
              <el-autocomplete class="inline-input" v-model="e.name" placeholder="请输入名称"
                               :fetch-suggestions="querySearch"></el-autocomplete>
            </el-col>
            <el-col :span="9">
              <el-input v-model="e.val" placeholder="请输入值"/>
            </el-col>
          </el-row>
          <div style="text-align:left;padding-left: 50px;margin-bottom: 20px;">
            <el-link type="primary" @click="addSpellPro">添加...</el-link>
          </div>
        </el-form>
      </el-card>
    </el-col>
    <spell-builder-dialog v-if="spellBuilderCfg.show" :show.sync="spellBuilderCfg.show"
                          :spell-data="spellBuilderCfg.data" :color-config="colorConfig"/>
  </div>
</template>

<script>
import Spell from "@/views/wc3word/spell";
import {conversion} from "@/utils/tools";
import SpellBuilderDialog from "@/views/wc3word/dialog/SpellBuilder";

const default_spell_data = {
  id: "A000",
  lv: "1",
  name: null,
  hotKey: null,
  effect: null,
  pros: [{name: '法力消耗', val: null},],
  updateWord: {text: '', vals: []},
  nature: undefined,
  normalWord: {text: '', vals: []},
}
const default_spell_info = {
  module: '学习',
}
const default_spell_pro_list = [
  {name: '法力消耗', val: null},
  {name: '施法距离', val: null},
  {name: '冷却时间', val: null},
  {name: '持续时间', val: null},
  {name: '法术范围', val: null},
  {name: '吟唱时间', val: null},
]

export default {
  name: 'Edit',
  props: {
    colorConfig: Object
  },
  components: {SpellBuilderDialog, Spell},
  data() {
    return {
      tempData: {},
      spellBuilderCfg: {
        show: false,
        data: null
      },
      spellDataObj: Object.assign({}, default_spell_data),
      spellInfo: Object.assign({}, default_spell_info),
    }
  },
  computed: {
    spellData() {
      return this.spellDataObj
    },
    spellDefaultProNames() {
      return default_spell_pro_list.map(e => ({value: e.name}))
    },
    exampleLevelList() {
      return this.spellData.updateWord.vals.length || 1
    },
  },
  watch: {
    spellDataObj: {
      handler(newVal) {
        localStorage.setItem('lastSpellData', JSON.stringify(newVal));
      },
      deep: true // 监听嵌套属性的变化
    },
    tempData: {
      handler(newVal) {
        localStorage.setItem('lastTempData', JSON.stringify(newVal));
      },
      deep: true // 监听嵌套属性的变化
    },
  },
  created() {
    if (localStorage.getItem('lastSpellData') != null) {
      // console.log(localStorage.getItem('lastSpellData'))
      this.spellDataObj = JSON.parse(localStorage.getItem('lastSpellData'))
    }
    if (localStorage.getItem('lastTempData') != null) {
      // console.log(localStorage.getItem('lastTempData'))
      this.tempData = JSON.parse(localStorage.getItem('lastTempData'))
    }
  },
  mounted() {
  },
  methods: {
    querySearch(queryString, cb) {
      var restaurants = this.spellDefaultProNames;
      var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (restaurant) => {
        return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    addSpellPro() {
      this.spellData.pros.push({})
    },
    handleResolveTempData(s) {
      var sStrList = s.between("[", "]")
      var result = []
      sStrList.forEach((sStr, i) => {
        var vs = sStr.split(",")
        result.push(vs)
      })
      var minLv = result.minFor()
      if (!minLv) {
        return minLv
      }
      return result.startCut(minLv)
    },
    handleTempDataForNormal() {
      var ori = this.tempData.normalWord
      var ns = this.spellData.normalWord
      if (ori && ns.text) {
        ns.vals = conversion(ori)
      }
    },
    handleTempDataForUpdate() {
      var ori = this.tempData.updateWord
      var ns = this.spellData.updateWord
      if (ori && ns.text) {
        ns.vals = conversion(ori)
      }
    },
    handleBuilder() {
      // console.log('开始生成 -> ', this.spellData)
      this.spellBuilderCfg.show = true
      this.spellBuilderCfg.data = Object.assign({}, this.spellData)
    },
    handleResetSpellData() {
      this.spellDataObj = Object.assign({}, default_spell_data)
    }
  }
}
</script>

<style scoped lang="scss">
.edit-container {
  * {
    font-weight: bold;
    font-size: 12px;
  }

  .spell-info-setting {
    margin-bottom: 15px;
  }

  .edit-form {
    padding-right: 5%;
    padding-left: 5%;
    overflow-y: auto;
    max-height: 68vh;
  }

  padding-left: 5%;
  padding-right: 5%;
  max-height: 68vh;
}
</style>
