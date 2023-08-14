<template>
  <div class="app-container">
    <div v-loading="loading" style="padding: 10px;">
      <el-divider>表单信息</el-divider>
      <el-form :model="formInfo" label-width="80px">
        <el-form-item label="表单名称" style="margin-bottom: 10px;">
          <span> {{ formInfo.name }} </span>
        </el-form-item>
        <el-form-item label="表单描述">
          <span> {{ formInfo.description }} </span>
        </el-form-item>
      </el-form>
      <el-divider>表单内容</el-divider>
      <Build ref="formbuild" v-if="!loading" :form-template="templateDatas.scheme" v-model="models" />
      <div>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="reset">重置</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getTemplateData,
  getData,
  addFormData
} from "@/api/modules/qform/myform";
import _ from "lodash";
import Build from "@/components/NgForm/build";

export default {
  name: "Detail",
  components: {
    Build
  },
  props: {
    formId: {
      type: String
    }
  },
  data() {
    return {
      loading: false,
      templateDatas: { scheme: { }},
      formDatas: { },
      formInfo: { },
      models: { }
    };
  },
  mounted() {
    this.reset();
  },
  methods: {
    async reset() {
      this.templateDatas = { scheme: { }};
      this.formDatas = { };
      this.models = { };
      this.formInfo = { };
      await this.getTemplateDatas();
    },

    async getTemplateDatas() {
      this.loading = true;
      let res = await getData(this.formId);
      if (res.code !== 200) { return; }
      this.formInfo = res.data;
      res = await getTemplateData(this.formInfo.form_info);
      if (res.code !== 200) { return; }
      this.templateDatas = res.data;
      this.loading = false;
    },

    onSubmit() {
      this.$refs.formbuild.validator().then((valid) => {
        if (valid) {
          this.loading = true;
          this.formDatas = {
            "form_template": this.templateDatas.id,
            "fill_data": this.models
          };
          addFormData(this.formDatas).then((res) => {
            if (res.code === 200) {
              this.msgSuccess("提交成功");
            } else {
              this.msgError(res.msg);
            }
          }).finally(() => {
            this.loading = false;
          });
        }
      });
    }
  }
};
</script>

<style scoped>

</style>
