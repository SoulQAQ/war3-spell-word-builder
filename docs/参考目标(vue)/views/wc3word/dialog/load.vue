<template>
  <el-dialog ref="dialogForm" width="30%" :title="title" :visible.sync="visible" @close="closeDialog"
             :append-to-body="true">
    <div style="padding-left: 10%;padding-right: 10%;">
      <el-radio-group v-model="checked" size="mini">
        <el-radio v-for="(e,i) in spellLoadList" :label="e" border>
          {{ e !== spellMap[e].name ? e + `<${spellMap[e].name}>` : e }}
        </el-radio>
      </el-radio-group>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button size="mini" @click="visible = false">取消</el-button>
      <el-button size="mini" type="primary" @click="handleLoad">读取</el-button>
      <el-button size="mini" type="warning" @click="handleRemove">删除</el-button>
      <el-button size="mini" type="danger" @click="handleRemoveAll">删除全部</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'LoadSpellDialog',
  props: {
    spellMap: {
      type: Object,
      require: true
    },
    spellList: {
      type: Array
    },
    show: {
      type: Boolean,
      default: () => false
    }
  },
  components: {},
  data() {
    return {
      visible: this.show,
      checked: null
    }
  },
  computed: {
    title() {
      return '你要读取哪个'
    },
    spellLoadList() {
      return this.spellList || Object.keys(this.spellMap)
    },
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
    handleLoad() {
      if (this.checked) {
        this.$emit('load', this.spellMap[this.checked])
        // console.log('checked -> ', this.checked)
        this.visible = false
      } else {
        this.$message({type: 'info', message: '你还没选择！'});
      }
    },
    handleRemove() {
      if (this.checked) {
        this.$confirm('此操作将永久删除这个记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$emit('remove', this.checked)
          // console.log('checked -> ', this.checked)
          this.visible = false
        }).catch(() => {
        })
      } else {
        this.$message({type: 'info', message: '你还没选择！'});
      }
    },
    handleRemoveAll() {
      this.$confirm('此操作将永久删除所有保存记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        localStorage.removeItem('spell-list')
        this.$message({type: 'success', message: '记录已清空!'});
        this.visible = false
      }).catch(() => {
      })
    },
  }
}
</script>

<style scoped lang="scss">

</style>
