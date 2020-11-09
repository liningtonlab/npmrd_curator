<template>
  <div class="container">
    <div>
      <h1 class="title">npmrd_curator</h1>
      <h3 class="subtitle">
        Tools for accelerating NMR data curation from the Literature
      </h3>
      <h3>Select your Input:</h3>
      <div class="links">
        <nuxt-link class="button--green" to="/textparser">
          Text Block
        </nuxt-link>
        <nuxt-link class="button--grey" to="/tableparser">
          HTML Table
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
