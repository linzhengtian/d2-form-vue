<template>
  <div style="padding: 10px;">
    <el-tabs tab-position="left">
      <el-tab-pane label="基本信息">
        <el-row>
          <el-form ref="formInfo" :model="formInfo" :rules="rules" label-width="120px" :disabled="onlyView">
            <el-form-item label="表单名称" prop="name">
              <el-input v-model="formInfo.name" placeholder="填写表单名称" />
            </el-form-item>
            <el-form-item label="启动状态" prop="publish_choice" v-if="formInfo.publish_choice !== '0'">
              <el-radio-group v-model="formInfo.publish_choice">
                <el-radio
                  v-for="dict in startChoiceOptions"
                  :key="dict.dictValue"
                  :label="dict.dictValue"
                >{{ dict.dictLabel }}</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="表单描述" prop="description">
              <el-input v-model="formInfo.description" type="textarea" placeholder="请输入内容" :autosize="{ minRows: 5}"/>
            </el-form-item>
            <el-form-item label="是否问卷模式" prop="questionnaire_choice">
              <el-radio-group v-model="formInfo.questionnaire_choice">
                <el-radio
                  v-for="dict in questionnaireChoiceOptions"
                  :key="dict.dictValue"
                  :label="dict.dictValue"
                >{{ dict.dictLabel }}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </el-row>
        <el-row>
          <div v-if="formInfo.designpermission === '1'">
            <el-button type="primary" @click="submitForm">保 存</el-button>
          </div>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="权限配置">
        <el-form :model="formInfo" :rules="rules" label-width="120px">
          <el-form-item label="负责人" prop="design_users">
            <div>{{formInfo.design_users}}</div>
            <template v-if="!onlyView">
              <el-button type="primary" @click="openDesign">
                编 辑
              </el-button>
            </template>
          </el-form-item>
          <el-form-item label="角色权限">
            <el-button type="primary" @click="openRole">
              <template v-if="onlyView">
                查 看
              </template>
              <template v-else>
                编 辑
              </template>
            </el-button>
          </el-form-item>
          <el-form-item label="用户权限">
            <el-button type="primary" @click="openUser">
              <template v-if="onlyView">
                查 看
              </template>
              <template v-else>
                编 辑
              </template>
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <el-dialog
      title="表单角色权限列表"
      :visible="openRoleModal"
      width="835px"
      v-if="openRoleModal"
      append-to-body
      @close="closeRoleDialog"
      :destroy-on-close=true
      class="permissionDialog"
    >
      <formRole :formId="formInfo.id" :height="height" :onlyView="onlyView"></formRole>
    </el-dialog>
    <el-dialog
      title="表单用户权限列表"
      :visible="openUserModal"
      width="835px"
      v-if="openUserModal"
      append-to-body
      @close="closeUserDialog"
      :destroy-on-close=true
      class="permissionDialog"
    >
      <formUser :formId="formInfo.id" :height="height" :onlyView="onlyView"></formUser>
    </el-dialog>
    <el-dialog
      title="修改负责人"
      :visible="openDesignModal"
      width="500px"
      v-if="openDesignModal"
      append-to-body
      @close="closeDesignDialog"
      :destroy-on-close=true
    >
      <SearchSelectPagination
        v-model="designPermissionList"
        :label="designPermissionLabels"
        labelName="all_name"
        labelValue="id"
        :multiple=true
        url="/admin/qform/formuser/"
        style="width: 100%;"
      >
      </SearchSelectPagination>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitDesignForm">确 定</el-button>
        <el-button @click="closeDesignDialog">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import formRole from "./permissions/formRole";
  import formUser from "./permissions/formUser";
  import {
    updateData,
    getDesignData,
    patchDesignData
  } from "@/api/modules/qform/myform";
  import SearchSelectPagination from "@/components/SearchSelectPagination/Index";
  import _ from "lodash";

    export default {
      name: "formSetting",
      props: {
        formInfo: {
          type: Object, default: () => {}
          },
      },
      data() {
        return {
          openRoleModal: false,
          openUserModal: false,
          openDesignModal: false,
          // 数据字典 -改
          templateFlagOptions: [],
          startChoiceOptions: [],
          questionnaireChoiceOptions: [],
          permissionChoiceOptions: [],
          // 负责人表
          designPermissionList: [],
          designPermissionLabels: [],
          // 表单校验 -改
          rules: {
            name: [
              { required: true, message: "表单名称不能为空", trigger: "blur" },
              { max: 256, message: "表单名称不能超过256个字符", trigger: "blur" }
            ],
            description: [
              { max: 8000, message: "表单描述不能超过8000个字符", trigger: "blur" }
            ],
            publish_choice: [
              { required: true, message: "发布状态不能为空", trigger: "blur" }
            ],
            questionnaire_choice: [
              { required: true, message: "是否问卷模式不能为空", trigger: "blur" }
            ],
          }
        };
      },
      components: {
        SearchSelectPagination,
        formRole,
        formUser
      },
      computed: {
        height() {
          return Math.max(Math.min(this.$store.state.winSize.winheight - 100, 720), 500);
        },
        onlyView() {
          return this.formInfo.designpermission !== "1";
        }
      },
      created() {
        // 获取数据字典 -改
        this.getDicts("start_flag").then(response => {
          this.startChoiceOptions = response.data;
        });
        this.getDicts("questionnaire_choice").then(response => {
          this.questionnaireChoiceOptions = response.data;
        });
        this.getDicts("permission_choice").then(response => {
          this.permissionChoiceOptions = response.data;
        });
      },
      mounted() {

      },
      methods: {
        /** 提交按钮 -改 */
        submitForm: function() {
          this.$refs["formInfo"].validate(valid => {
            if (valid) {
                updateData(this.formInfo).then(response => {
                  this.msgSuccess("修改成功");
                });
              }
          });
        },
        openRole() {
          this.openRoleModal = true;
        },
        closeRoleDialog() {
          this.openRoleModal = false;
          if (!this.onlyView) {
            this.$emit("resetFormInfo");
          }
        },
        openUser() {
          this.openUserModal = true;
        },
        closeUserDialog() {
          this.openUserModal = false;
          if (!this.onlyView) {
            this.$emit("resetFormInfo");
          }
        },
        openDesign() {
          getDesignData(this.formInfo.id).then(response => {
            this.designPermissionLabels = response.data.designers;
            this.designPermissionLabels.forEach(v => v.id=v.form_user);
            this.designPermissionList = this.designPermissionLabels.map(v => v.id=v.form_user);
            this.openDesignModal = true;
          });

        },
        closeDesignDialog() {
          this.openDesignModal = false;
        },
        submitDesignForm: function() {
          if (this.designPermissionList.length > 0) {
            const data = {
              id: this.formInfo.id,
              ids: this.designPermissionList.join(",")
            };
            patchDesignData(data).then(response => {
              this.msgSuccess("修改成功");
              this.$emit("resetFormInfo");
              this.closeDesignDialog();
            });
          } else {
            this.msgError("负责人不能为空");
          }
        },
      }
    }
</script>

<style scoped>

</style>
