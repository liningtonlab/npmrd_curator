<template>
  <div class="header">
    <a href="/" v-show="!is_home">Home</a>
    <a href="https://liningtonlab.github.io/npmrd_curator/" target="_blank">
      Documentation
    </a>
  </div>
</template>

<script>
export default {
  computed: {
    is_home: function () {
      return this.$route.path === '/'
    },
  },
}
</script>

<style scoped>
.header a {
  margin-right: 20px;
}
</style>
