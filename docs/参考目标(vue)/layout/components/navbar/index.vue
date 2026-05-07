<template>
  <div id="navbar">
    <el-menu
      :default-active="activeMenu"
      :background-color="variables.menuBg"
      :text-color="variables.menuText"
      :active-text-color="variables.menuActiveText"
      :unique-opened="false"
      :collapse-transition="false"
      mode="horizontal"
      :router="true"
      :style="screenPadding"
    >
      <el-col :xs="menuItemSize.xs" :sm="menuItemSize.sm" :md="menuItemSize.md" :lg="menuItemSize.lg"
              :xl="menuItemSize.xl"
              v-for="(route, i) in routes" :key="i">
        <el-menu-item v-if="route.children.length === 1" :index="to(route.children[0])">
          {{ title(route.children[0]) }}
        </el-menu-item>
        <el-submenu v-else-if="route.children.length > 1" :index="route.path">
          <template slot="title">{{ route.meta.title || title(route.children[0]) }}</template>
          <el-menu-item v-for="(child) in route.children" :key="child.path" :index="to(child)">
            {{ child.meta.title }}
          </el-menu-item>
        </el-submenu>
      </el-col>
    </el-menu>
  </div>
</template>

<script>
import variables from '@/style/layout/variables.scss'
import {mapGetters} from "vuex";

export default {
  name: "Navbar",
  components: {},
  data() {
    return {
      screenWidth: document.body.clientWidth
    }
  },
  computed: {
    ...mapGetters([
      'routes',
    ]),
    menuItemSize() {
      return {
        xs: 6,
        sm: 5,
        md: 4,
        lg: 3,
        xl: 2
      }
    },
    screenPadding() {
      if (this.screenWidth >= 600) {
        if (this.screenWidth >= 1000) {
          return {
            paddingLeft: '15%',
            paddingRight: '15%'
          }
        } else {
          return {
            paddingLeft: '5%',
            paddingRight: '5%'
          }
        }
      } else {
        return {}
      }
    },
    activeMenu() {
      const route = this.$route
      const {meta, path} = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    variables() {
      return variables
    },
  },
  mounted() {
    window.onresize = () => {
      this.screenWidth = document.body.clientWidth
      this.$store.commit('screen/UPDATE_SCREEN_WIDTH', document.body.clientWidth)
    }
    // console.log('routes -> ', this.routes)
  },
  watch: {
    screenWidth(newValue) {
      // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
      if (!this.timer) {
        // 一旦监听到的screenWidth值改变，就将其重新赋给data里的screenWidth
        this.screenWidth = newValue;
        this.$store.commit('screen/UPDATE_SCREEN_WIDTH', newValue)
        this.timer = true;
        setTimeout(() => {
          //console.log(this.screenWidth);
          this.timer = false;
        }, 1250);
      }
    }
  },
  methods: {
    title(route) {
      return route.meta.title
    },
    to(route) {
      return route.path
    }
  },
}
</script>

<style scoped lang="scss">
@import "~@/style/layout/variables.scss";

#navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9;
}

.is-active {
  border-bottom: #{$subMenuActiveText} 3px solid;
}

.el-menu-item {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
