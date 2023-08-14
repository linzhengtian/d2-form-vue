<template>
  <el-dialog
    :title="dialogTitle"
    :visible="openModal"
    :width="modalWidth"
    append-to-body
    :close-on-click-modal="false"
    @close="closeFormDialog"
  >
    <el-form :model="models" label-position="top" id="copyForm" :rules="rules" ref="copyForm">
      <el-form-item label="表单名称" style="margin-bottom: 0px;">
        <span> {{ models.name }} </span>
      </el-form-item>
      <el-form-item label="新表单名称" prop="newName" style="margin-bottom: 10px;">
        <el-input v-model="models.newName" placeholder="填写表单名称" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="onSubmit">提交</el-button>
      <el-button @click="closeFormDialog">关闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {
  getData,
  copyForm
} from "@/api/modules/qform/myform";
import _ from "lodash";
import Build from "@/components/NgForm/build";

export default {
  name: "formCopy",
  components: {
    Build
  },
  props: {
    formId: {
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
  },
  data() {
    return {
      models: {
        name: "",
        newName: ""
      },
      rules: {
        newName: [
          { required: true, message: "表单名称不能为空", trigger: "blur" },
          { max: 256, message: "表单名称不能超过256个字符", trigger: "blur" }
        ]
      },
    };
  },
  mounted() {
    this.reset();
  },
  methods: {
    async reset() {
      this.models = {
        name: "",
        newName: ""
      };
      await this.getFormName();
    },

    async getFormName() {
      const res = await getData(this.formId);
      if (res.code !== 200) { return; }
      this.models.name = res.data.name;
      this.models.newName = res.data.name + "-新";
    },

    onSubmit() {
      this.$refs["copyForm"].validate(valid => {
        if (valid) {
          copyForm({
            id: this.formId,
            new_name: this.models.newName
          }).then(response => {
            this.$message.success("创建表单“" + response.data.name + "”成功");
            this.closeFormDialog();
          });
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
  ::v-deep #copyForm .el-form-item__label {
    margin-bottom: 0px;
    padding-bottom: 0px;
  }
</style>
