<template>
  <div class="app-container">
    <el-tabs type="border-card" style="min-height: 50vh;">
      <!--      <el-tab-pane>-->
      <!--        <span slot="label">简介</span>-->
      <!--        <div>这是一个wc3编辑器文本生成器，它还在制作中。</div>-->
      <!--      </el-tab-pane>-->
      <el-tab-pane>
        <span slot="label"><i class="el-icon-edit"></i>编辑文本</span>
        <edit :color-config="colorConfig"/>
      </el-tab-pane>
      <el-tab-pane>
        <span slot="label"><i class="el-icon-setting"></i>色彩</span>
        <color :color-default-config="colorConfig" style="padding-left: 3%;padding-right: 3%;"
               @updateCfg="updateCfg"/>
      </el-tab-pane>
      <el-tab-pane>
        <span slot="label"><i class="el-icon-tickets"></i>更新日志</span>
        <update-record/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Color from "@/views/wc3word/color";
import Edit from "@/views/wc3word/edit";
import {defaultColorConfig} from '@/utils/tools'
import UpdateRecord from "@/views/wc3word/updateRecord";
import version from '@/views/wc3word/dialog/version';


export default {
  name: 'Word',
  components: {UpdateRecord, Edit, Color},
  data() {
    return {
      colorConfig: Object.assign({}, defaultColorConfig),
      version: '1.0.0'
    }
  },
  computed: {},
  watch: {},
  created() {
  },
  mounted() {
    const latestVersion = Object.entries(version).pop() // 获取最后一个版本号码
    const latestSubVersion = Object.keys(latestVersion[1]).pop() // 获取最后一个子版本号码
    this.version = `${latestVersion[0]}.${latestSubVersion}`
    const h = this.$createElement;
    this.$notify({
      title: '来自Soul2的提示',
      message: h('span', {style: 'color: teal'}, `当前正在使用的生成器版本是${this.version}。`),
      position: 'bottom-right',
      duration: 4000,
      // showClose: false
    });
  },
  methods: {
    updateCfg(cfg) {
      this.colorConfig = cfg
    }
  }
}
</script>

<style scoped lang="scss">
.app-container {
  padding-left: 15%;
  padding-right: 15%;
}
</style>
