<template>
  <ng-form-build
    ref="formbuild"
    :formTemplate="formTemplate"
    :models="value"
    :config="config"
    :customComponents="customComponents"
    :renderPreview="renderPreview"
  />
</template>

<script>
import customComponents from "./config";

export default {
  name: "Build",
  props: {
    formTemplate: {
      type: Object, default: () => {}
    },
    config: {
      type: Object, default: () => {}
    },
    value: {
      type: Object, default: () => {}
    },
    renderPreview: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      customComponents: customComponents
    };
  },
  methods: {
    validator() {
      return this.$refs.formbuild.validator();
    }
  }
};
</script>

<style scoped>

</style>
