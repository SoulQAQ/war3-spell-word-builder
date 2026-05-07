<template>
  <el-collapse v-model="activeNames">
    <el-collapse-item class="version" v-for="v in versionList('1.0')" :name="v.v">
      <div slot="title" class="version-title">{{ v.v }}</div>
      <div class="version-line" v-for="line in v.l">[{{ line.type }}]{{ line.value }}</div>
    </el-collapse-item>
  </el-collapse>
</template>

<script>
import version from '@/views/wc3word/dialog/version'

export default {
  name: 'UpdateRecord',
  props: {
    version: String
  },
  components: {},
  data() {
    return {
      activeNames: [],
    }
  },
  computed: {},
  watch: {},
  created() {
    this.activeNames.push(this.versionList('1.0')[0].v)
  },
  mounted() {
  },
  methods: {
    versionList(pv) {
      let keys = Object.keys(version[pv]).sort((a, b) => b - a)
      return keys.map(e => ({v: pv + '.' + e, l: version[pv][e]}))
    }
  }
}
</script>

<style scoped lang="scss">
.version {
  &-title {
    font-size: 16px;
    font-weight: bold;
  }

  &-line {
    padding-left: 5%;
    padding-right: 5%;
    text-align: left;
    font-size: 16px;
    font-weight: bold;
  }
}
</style>
