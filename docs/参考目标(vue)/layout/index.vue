<template>
  <div id="layout">
    <!--    <div id="bg" :style="randomUrl" />-->
    <el-container style="height: 100%;">
      <el-header>
        <navbar/>
      </el-header>
      <el-main style="padding: 0;">
        <el-scrollbar>
          <app-main/>
        </el-scrollbar>
      </el-main>
      <el-footer style="height: 40px;">
        <app-footer/>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import AppMain from "@/layout/components/AppMain";
import Navbar from "@/layout/components/navbar";
import AppFooter from "@/layout/components/footer";
import Background from "@/layout/components/background";

export default {
  name: "Layout",
  components: {Background, Navbar, AppMain, AppFooter},
  computed: {
    randomUrl() {
      let n = Math.floor(Math.random() * 5 + 1)
      return {
        background: "url(http://soul2.cn/images/spi_a" + n + ".jpg) center no-repeat fixed"
      }
    }
  }
}
</script>

<style scoped lang="scss">
#layout {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  position: absolute;
  top: 0;
  left: 0;
}

#bg {
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  background-size: 100% 100%;
  -moz-background-size: 100% 100%;
  -webkit-background-size: 100% 100%;
}

el-container {
  padding-top: 0;
}
</style>
