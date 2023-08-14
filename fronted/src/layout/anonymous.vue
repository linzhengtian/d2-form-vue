<template>
  <div>
    <app-main />
  </div>
</template>

<script>
import { AppMain } from "./components";

export default {
  name: "anonymous",
  components: {
    AppMain
  },
}
</script>

<style lang="scss" scoped>
  .app-main {
    min-height: calc(100vh);
  }
</style>
