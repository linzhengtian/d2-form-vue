<template>
  <div>
    <div ref="ace"></div>
  </div>
</template>
<script>
import ace from 'ace-builds';
import 'ace-builds/src-noconflict/snippets/javascript';
import 'ace-builds/src-noconflict/snippets/sql';
import 'ace-builds/src-noconflict/snippets/html';
import 'ace-builds/src-noconflict/snippets/java';
import 'ace-builds/src-noconflict/snippets/python';
import 'ace-builds/src-noconflict/snippets/json';
import 'ace-builds/src-noconflict/snippets/golang';
import 'ace-builds/src-noconflict/snippets/sh';
import 'ace-builds/webpack-resolver';
import 'ace-builds/src-noconflict/ext-language_tools';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-sql';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-json';
import 'ace-builds/src-noconflict/mode-golang';
import 'ace-builds/src-noconflict/mode-sh';

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
      value: "",
      aceEditor: null,
      wrap: true, // 是否自动换行
      themePath: "ace/theme/monokai" // 黑色主题，默认为白色
    };
  },
  mounted() {
    this.aceEditor =
      ace.edit(this.$refs.ace, {
        maxLines: this.record.options.maxLines,
        minLines: this.record.options.minLines,
        fontSize: this.record.options.fontSize,
        value: this.value ? this.value : "", // 初始显示内容
        theme: this.themePath,
        mode: this.record.options.code,
        wrap: this.wrap,
        tabSize: 4
      });
    // 激活自动提示
    this.aceEditor.setOptions({
      enableSnippets: true,
      enableLiveAutocompletion: true,
      enableBasicAutocompletion: true
    });
    this.aceEditor.getSession().on("change", this.change);
    this.aceEditor.getSession().setValue(this.models[this.record.model]);
  },
  watch: {
    "record.options.code"(val) {
      this.handleModelPathChange(val);
    },
    "record.options.fontSize"(val) {
      this.handleFontSizeChange(val);
    },
    "record.options.maxLines"(val) {
      this.handleFontSizeLine(val);
    },
  },
  methods: {
    // 获取值
    change() {
      this.models[this.record.model] = this.aceEditor.getSession().getValue();
    },
    // 切换语言
    handleModelPathChange(modelPath) {
      this.aceEditor.getSession().setMode(modelPath);
    },
    // 修改字体大小
    handleFontSizeChange(value) {
      this.aceEditor.setFontSize(value);
    },
    handleFontSizeLine(value) {
      this.aceEditor.getSession().setWrapLimitRange(this.record.options.minLines, value);
    },
  }
};
</script>
