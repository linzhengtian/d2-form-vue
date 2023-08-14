<template>
  <div>
    <Screen style="height: 100vh; overflow-y: scroll;"></Screen>
  </div>
</template>

<script>
import Screen from "./index";

export default {
  components: {
    Screen
  },
}
</script>

<style scoped lang="scss" >
::v-deep #index .bg {
  height: auto;
}
</style>
