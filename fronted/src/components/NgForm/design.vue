<template>
  <ng-form-design ref="formDesign" :custom-components="customComponents">
    <!-- 自定义属性配置 -->
    <template slot="custom-properties" slot-scope="{selectItem}">
      <Properties :select-item="selectItem" />
      <CodeProperties :select-item="selectItem" />
    </template>
  </ng-form-design>
</template>

<script>
import Properties from "./NgImage/properties";
import CodeProperties from "./NgCode/properties";
import customComponents from "./config";

export default {
  name: "Design",
  components: {
    Properties,
    CodeProperties
  },
  data() {
    return {
      customComponents: customComponents
    };
  },
  methods: {
    initModel(scheme) {
      this.$refs["formDesign"].initModel(scheme);
    },
    getModel() {
      return this.$refs["formDesign"].getModel();
    }
  }
};
</script>

<style scoped>

</style>
