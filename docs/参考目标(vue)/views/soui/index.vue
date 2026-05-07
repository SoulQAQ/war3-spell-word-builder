<template>
  <div id="soui" style="text-align: left;" :style="screenPadding">
    <el-card shadow="always">
      <div class="title" slot="header" style="text-align: center">
        关于SoUI
      </div>
      <p>这是一个基于YDWEv1.31.8(+网易DzAPI 1.2.9a)打包的魔兽争霸3地图编辑器扩展包.</p>
      <p>该扩展包添加了一些减少重复劳动的编辑器额外动作UI.</p>
      <p>扩展包部分内容仍处于测试阶段,其功能可能存有未知BUG.</p>
      <p>已提供部分额外功能的演示地图,安装后可以在安装目录\example(演示地图)\SoUI文件夹内找到.</p>
      <p>未经本人许可擅自将SoUI在网上散播者将承担盗版乱传的相关法律责任,并且传播者将承担所有使用者使用本UI带来的所有负面后果,Soul本人不承担任何责任.</p>
      <p>SoUI仅对编辑器功能进行扩展,不涉及编辑器原有功能的修改.</p>
    </el-card>

    <el-card shadow="always" style="margin-top: 20px;">
      <div slot="header" style="text-align: center">关于版本</div>
      <div>
        <p>最新的版本是
          <el-tag size="mini">0.4.6</el-tag>
          。
        </p>
        <p>可能会有
          <el-tag size="mini">0.5.0</el-tag>
          (也许)
        </p>
      </div>
    </el-card>

    <el-card shadow="always" style="margin-top: 20px;">
      <div slot="header" style="text-align: center">下载</div>
      <div>
        <el-button size="mini" class="el-icon-cloudy"
                   @click="goto('https://share.weiyun.com/dlM6m0EE')"
        >
          微云
        </el-button>
        <el-button size="mini" class="el-icon-cloudy"
                   @click="goto('https://pan.baidu.com/s/1bL96VxXYSCW8pSsVZ5rzrw#awsl')"
        >
          百度云
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "SoUi",
  computed: {
    ...mapGetters([
      "screenPadding"
    ]),
  },
  methods: {
    goto(where) {
      location.href = where
    }
  }
}
</script>

<style scoped>
#soui {
  padding-top: 20px;
}
</style>
