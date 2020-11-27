<template>
  <div>
    <router-link v-show="!is_home" :to="{ path: '/' }">Home</router-link>
    <!-- <a href="/" v-show="!is_home">Home</a> -->
    <router-link :to="{ path: '/demomol' }">JSmol Demo</router-link>
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
