<template>
  <div id="app-footer">
    Soul2 | <a class="record-number" href="http://beian.miit.gov.cn/">粤ICP备2020098994号</a>
  </div>
</template>

<script>
export default {
  name: "AppFooter"
}
</script>

<style scoped lang="scss">
@import "~@/style/layout/footer.scss";

#app-footer {
  width: 100%;
}

.record-number {
  color: #000;
  border-bottom: none;
  text-decoration: none;
}

.record-number:hover {
  border-bottom: #{$recordNumberHover} 1px solid;
  color: #{$recordNumberHover};
}
</style>
