import Vue from "vue";
import VueRouter from "vue-router";
import Layout from "@/layout";

Vue.use(VueRouter)

export const routes = [
  {
    path: '',
    component: Layout,
    children: [{
      path: '/',
      name: 'Home',
      component: () => import('@/views/home/index'),
      meta: {title: '首页', icon: 'dashboard'}
    }]
  },
  {
    path: '',
    component: Layout,
    children: [{
      path: '/soui',
      name: 'SoUI',
      component: () => import('@/views/soui/index'),
      meta: {title: 'SoUI', icon: 'dashboard'}
    }]
  },
  {
    path: '',
    component: Layout,
    children: [{
      path: '/demo',
      name: 'SoDemo',
      component: () => import('@/views/sodemo/index'),
      meta: {title: '灵魂演示', icon: 'dashboard'}
    }]
  },
  {
    path: '',
    component: Layout,
    children: [{
      path: '/wc3/word',
      name: 'Word',
      component: () => import('@/views/wc3word/index'),
      meta: {title: '文本生成', icon: 'dashboard'}
    }]
  },
  // {
  //   path: '',
  //   component: Layout,
  //   meta: {title: '多菜单测试', icon: 'dashboard'},
  //   children: [{
  //     path: '/a',
  //     name: 'a',
  //     component: () => import('@/views/sodemo/index'),
  //     meta: {title: '菜单1', icon: 'dashboard'}
  //   },{
  //     path: '/b',
  //     name: 'b',
  //     component: () => import('@/views/sodemo/index'),
  //     meta: {title: '菜单2', icon: 'dashboard'}
  //   }]
  // },
]

const createRouter = () => new VueRouter({
  base: process.env.VUE_APP_CONTEXT_PATH || '/',
  mode: 'history', // require service support
  scrollBehavior: () => ({y: 0}),
  routes: routes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router


