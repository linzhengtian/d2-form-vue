<template>
  <div>
    <el-image
      v-for="(item,index) in record.options.imageUrl"
      :key="index"
      :style="record.options.style ? record.options.style : null"
      :src="item.file_url ? baseUrl + item.file_url : item.file"
      fit="scale-down"
    ></el-image>
  </div>
</template>
<script>
import _ from "lodash";

export default {
  props: {
	    record: { // 组件数据
	      type: Object,
	      required: true
	    },
	    models: { // 表单数组
	      type: Object,
	      required: true
	    },
	    disabled: { // 是否禁用
	      type: Boolean,
	      default: false
	    },
	    preview: { // 是否当前是预览
	      type: Boolean,
	      default: false
	    }
  },
  data() {
    return {
      baseUrl: process.env.VUE_APP_BASE_API
    };
  },
  methods: {
  }
};
</script>
