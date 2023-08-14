<template>
  <el-select
    v-model="copyValue"
    :multiple="multiple"
    filterable
    remote
    reserve-keyword
    :clearable="true"
    :placeholder="placeholder"
    :remote-method="filterMethod"
    :loading="loading"
    @change="updateValue"
    @focus="focusMethod"
    @visible-change="visibleSelect"
    :style="selectStyle"
    :disabled="disabled"
    >
    <el-option
      v-for="item in copyLabel"
      :key="item[labelValue]"
      :label="item[labelName]"
      :value="item[labelValue]"
      style="display: none;">
    </el-option>
    <el-option
      v-for="item in options"
      :key="item[labelValue]"
      :label="item[labelName]"
      :value="item[labelValue]">
    </el-option>
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="pageNum"
      :page-size="pageSize"
      layout="prev, pager, next, total"
      :total="total">
    </el-pagination>
  </el-select>
</template>

<script>
import request from "@/utils/request";
import _ from "lodash";

export default {
  name: "SearchSelectPagination",
  props: {
    url: { type: String },
    multiple: { type: Boolean },
    method: { type: String, default: "get" },
    value: [Number, String, Array],
    // 用于赋默认值，String为value的label值，Array为默认值的键值对表达形式的列表,如[{labelValue:XX,labelName:XX}...]
    label: { type: [Number, String, Array], default: ()=>[] },
    labelName: { type: String },
    labelValue: { type: String },
    selectStyle: { type: Object },
    pageSize: { type: Number, default: 5 },
    defaultParams: { type: Object, default: ()=>{} },
    placeholder: { type: String, default: "请输入关键词" },
    disabled: { type: Boolean, default: false },
    // 默认的搜索值，如{ queryName: value }
  },
  data() {
    return {
      copyValue: this.value, // 防止子组件双向绑定报错
      loading: false,
      total: 0,
      pageNum: 1,
      options: [],
      query: ""
    };
  },
  watch: {
    value: {
      handler: function(val) {
        this.copyValue = val;
      },
      deep: true
    },
    label: {
      handler: function(val) {
        this.copyLabel = _.isArray(val) ? _.cloneDeep(val) :
          [{[this.labelValue]: this.value, [this.labelName]: val}];
        this.options = [];
      },
      immediate: true
    },
    options(val){
      let labelValues = val.map( v => v[this.labelValue]);
      let tmpLabels = [];
      for( const l of this.copyLabel){
        if (!labelValues.includes(l[this.labelValue])) {
          tmpLabels.push(l);
        }
      }
      this.copyLabel = tmpLabels;
    }
  },
  mounted() {
    this.remoteMethod();
  },
  methods: {
    async filterMethod(query) {
      this.query = query;
      this.pageNum = 1;
      await this.remoteMethod();
    },
    async remoteMethod() {
      const queryParams = {
        pageNum: this.pageNum,
        pageSize: this.pageSize,
        [this.labelName]: this.query
      };
      const { data } = await request({
        url: this.url,
        method: this.method,
        params: { ...queryParams, ...this.defaultParams}
      });
      this.options = data.results;
      this.total = data.count;
    },
    updateValue() {
      this.$emit("input", this.copyValue);
      this.$emit("update:value", this.copyValue); // 父组件需要.sync装饰
    },
    async visibleSelect(flag) {
      if (flag) {
        await this.filterMethod();
      }
    },
    async focusMethod() {
      if (!this.options || (this.options && this.options.length === 0)) {
        await this.remoteMethod();
      }
    },
    async handleCurrentChange(val) {
      this.pageNum = val;
      await this.remoteMethod();
    }
  }
};
</script>

<style scoped>

</style>
