<template>
  <footer class="footer" v-show="is_home">
    <div>
      <span class="text-muted">Place sticky footer content here.</span>
    </div>
  </footer>
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
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  /* Set the fixed height of the footer here */
  height: 60px;
  line-height: 60px; /* Vertically center the text there */
  background-color: #f5f5f5;
}
</style>
