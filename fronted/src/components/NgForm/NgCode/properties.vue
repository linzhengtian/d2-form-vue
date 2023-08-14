<template>
  <!-- 自定义组件的属性配置 -->
  <el-form v-show="selectItem.key" size="mini" :disabled="disabled">
    <template v-if="selectItem.type == 'NgCode'">
      <el-form-item label="设置语言">
        <el-select
          v-model="selectItem.options.code"
          placeholder="请输入"
          size="small"
          style="width: 100%;"
        >
          <el-option
            v-for="dict in aceCodeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="字体大小">
        <el-input-number v-model="selectItem.options.fontSize" :min="14" :max="50"></el-input-number>
      </el-form-item>
      <el-form-item label="行数">
        <el-input-number v-model="selectItem.options.maxLines" :min="selectItem.options.minLines" :max="100"></el-input-number>
      </el-form-item>
    </template>
  </el-form>
</template>
<script>

export default {
  components: {
  },
  data() {
    return {
      aceCodeOptions: []
    };
  },
  props: {
    selectItem: { // 当前选择的组件
      type: Object,
      required: true
    },
    disabled: { // 是否禁用
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.getDicts("ace_code").then(response => {
      this.aceCodeOptions = response.data;
    });
  }
};
</script>
