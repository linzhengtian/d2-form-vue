<template>
  <el-dialog
    :title="dialogTitle"
    :visible="openModal"
    :width="modalWidth"
    append-to-body
    @close="closeFormDialog"
  >
    <el-form :model="formInfo" label-position="top" id="detailForm">
      <el-form-item label="表单名称" style="margin-bottom: 0px;">
        <span> {{ formInfo.name }} </span>
      </el-form-item>
      <el-form-item label="表单描述" style="margin-bottom: 10px;">
        <span> {{ formInfo.description }} </span>
      </el-form-item>
    </el-form>
    <Build
      ref="formbuild"
      v-if="!loading"
      :form-template="templateDatas.scheme"
      v-model="models"
      :renderPreview="handleType === 'detail'"
      :config="httpConfig"/>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="onSubmit" v-if="handleType !== 'detail'">提交</el-button>
      <el-button @click="closeFormDialog" v-if="handleType === 'detail'">关闭</el-button>
      <el-button @click="reset" v-if="handleType === 'create'">重置</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {
  getTemplateData,
  getData,
  addFormData,
  getFormData,
  updateFormData
} from "@/api/modules/qform/myform";
import { getToken } from "@/utils/auth";
import _ from "lodash";
import Build from "@/components/NgForm/build";

export default {
  name: "formDataDetail",
  components: {
    Build
  },
  props: {
    formId: {
      type: [String, Number]
    },
    dataId: {
      type: [String, Number]
    },
    dialogTitle: {
      type: String,
      required: true
    },
    openModal: {
      type: Boolean,
      required: true
    },
    modalWidth: {
      type: String,
      default: "720px"
    },
    handleType: {
      type: String,
      default: "create"
    },
  },
  data() {
    return {
      loading: false,
      templateDatas: { scheme: { }},
      formDatas: { },
      formInfo: { },
      models: { },
      httpConfig: {
        uploadPath: process.env.VUE_APP_BASE_API + "/admin/system/savefile/",
        headers: [{ label: 'Authorization', value: "Bearer " + getToken() }],
        baseUrl: process.env.VUE_APP_BASE_API // 用于拼接下载地址，nginx需要配置对media目录的重定向
      },
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
      if (this.handleType === "create") {
        res = await getTemplateData(this.formInfo.form_info);
        if (res.code !== 200) { return; }
        this.templateDatas = res.data;
      } else {
        if (["detail", "edit"].includes(this.handleType)){
          res = await getFormData(this.dataId);
          if (res.code !== 200) { return; }
          this.models = res.data.fill_data;
          res = await getTemplateData(res.data.form_template);
          if (res.code !== 200) { return; }
          this.templateDatas = res.data;
        }
      }
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
          if (this.handleType === 'create') {
            addFormData(this.formDatas).then((res) => {
              if (res.code === 200) {
                this.msgSuccess("提交成功");
              } else {
                this.msgError(res.msg);
              }
            }).finally(() => {
              this.loading = false;
              this.closeFormDialog();
            });
          } else {
            this.formDatas["id"] = this.dataId;
              updateFormData(this.formDatas).then((res) => {
              if (res.code === 200) {
                this.msgSuccess("修改成功");
              } else {
                this.msgError(res.msg);
              }
            }).finally(() => {
              this.loading = false;
              this.closeFormDialog();
            });
          }
        }
      });
    },

    closeFormDialog() {
      this.$emit("closeFormDialog", false);
    }
  }
};
</script>

<style lang="scss" scoped>
  ::v-deep #detailForm .el-form-item__label {
    margin-bottom: 0px;
    padding-bottom: 0px;
  }
</style>
