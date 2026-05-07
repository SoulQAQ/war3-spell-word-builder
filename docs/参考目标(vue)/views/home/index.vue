<template>
  <div id="home" :style="screenPadding">
    <el-card shadow="always">
      <el-collapse :accordion="false" v-model="expand" style="text-align: left">
        <el-collapse-item name="openShow">
          <template slot="title">
            关于灵魂演示
          </template>
          <div>
            <p>
              这是一套你不能错过的魔兽地图编辑器入门教程。
            </p>
            <p>
              灵魂演示是灵魂所制作的一套强大的
              <el-link
                href='https://xywiki.com/%E9%AD%94%E5%85%BD%E5%9C%B0%E5%9B%BE%E7%BC%96%E8%BE%91%E5%99%A8'
                target='_blank'
                type="primary"
                style="font-size: 12px"
              >
                魔兽地图编辑器
              </el-link>
              系统演示地图，涵盖了许多新手入门所关注和需要的内容。
            </p>
            <p>
              灵魂演示地图基于
              <el-link
                href='https://xywiki.com/YDWE'
                target='_blank'
                type="primary"
                style="font-size: 12px"
              >
                YDWE
              </el-link>
              1.27.5 制作，请使用 YDWE 1.27.5 或以上的版本打开灵魂演示地图，否则可能会导致
              <el-link
                href='https://xywiki.com/WE%E5%85%BC%E5%AE%B9%E6%80%A7%E9%94%99%E8%AF%AF'
                target='_blank'
                type="primary"
                style="font-size: 12px"
              >
                WE兼容性错误
              </el-link>
              。
            </p>
            <p>
              你可以选择
              <el-link
                href='http://next.soul2.cn/download/soul-demo/%E5%90%88%E9%9B%86.zip'
                target='_blank'
                type="primary"
                style="font-size: 12px"
                icon="el-icon-download"
              >
                点击这里
              </el-link>
              一次性下载所有演示地图，也可以通过点击下方各个按钮以你希望的方式下载你所需要的特定演示地图。
            </p>
            <div id="dl-btn">
              <el-button size="mini" class="el-icon-position"
                         @click="goto('https://wow8.org/soul-demo/')"
              >
                Wow8
              </el-button>
              <el-button size="mini" class="el-icon-position"
                         @click="goto('https://tieba.baidu.com/p/4575301644')"
              >
                贴吧
              </el-button>
              <el-button size="mini" class="el-icon-cloudy"
                         @click="goto('https://share.weiyun.com/5YXLT4L')"
              >
                微云
              </el-button>
              <el-button size="mini" class="el-icon-cloudy"
                         @click="goto('https://pan.baidu.com/s/1bGeoOm#list/path=%2F')"
              >
                百度云
              </el-button>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item name="soui">
          <template slot="title">
            关于SoUI
          </template>
          <div>
            <p>SoUI是基于魔兽争霸III地图编辑器的一个扩展性Mod, 仅使用编辑器原有的函数为使用者增加一些更方便的功能。</p>
            <p>当前最新版本的SoUI版本是
              <el-link href="http://bbs.mvprpg.com/forum.php?mod=viewthread&tid=465517"
                       type="primary" :underline="false">
                <el-tag size="mini">0.4.6</el-tag>
              </el-link>
            </p>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script>

import {mapGetters} from "vuex";

export default {
  name: "Home",
  components: {},
  computed: {
    ...mapGetters([
      "screenPadding"
    ]),
    expand() {
      return ['openShow', 'soui']
    },
  },
  methods: {
    goto(where) {
      location.href = where
    }
  }
}
</script>

<style scoped>
#home {
  padding-top: 20px;
}

#dl-btn .el-button {
  margin-top: 7px;
}
</style>
