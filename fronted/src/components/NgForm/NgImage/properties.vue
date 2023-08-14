<template>
  <!-- 自定义组件的属性配置 -->
  <el-form v-show="selectItem.key" size="mini" :disabled="disabled">
    <template v-if="selectItem.type == 'NgImage'">
      <!-- 开关的label -->
      <el-form-item label="图片地址">
        <FileUpload
          ref="saveFile"
          v-model="selectItem.options.imageUrl"
          :file-type="['png', 'jpg', 'jpeg']"
          :auto-upload="true"
          :show-file-list="false"
          :multiple="true"
          :limit="3"
          :file-size="10"
        />
      </el-form-item>
      <el-form-item label="图片样式">
        <el-input v-model="selectItem.options.style" type="textarea" placeholder="请输入" />
      </el-form-item>
    </template>
  </el-form>
</template>
<script>
import FileUpload from "@/components/FileUpload/index";

export default {
  components: {
    FileUpload
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
  }
};
</script>
