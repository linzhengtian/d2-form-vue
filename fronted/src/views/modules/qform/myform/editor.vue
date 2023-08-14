<template>
  <div>
    <el-row :gutter="5">
      <el-col :span="8">
        <template v-if="!createFlag">
          <span style="margin-right: 5px;">版本号：{{templateDatas.version}}</span>
          <el-button size="small" type="primary" @click="openTemplateFormVersion" v-if="!createFlag && formInfo.publish_choice !== '2'"><i class="el-icon-plus" /> 切换版本</el-button>
        </template>
        <span style="margin-left: 5px;">
          <template v-for="dict in publishChoiceOptions">
            <el-tag v-if="dict.dictValue === formInfo.publish_choice">{{ dict.dictLabel }}</el-tag>
          </template>
        </span>
      </el-col>

      <el-col :offset="8" :span="8" style="text-align: right;">
        <el-button-group>
          <el-button size="small" type="primary" @click="createTemplateFormVersion" v-if="!createFlag && formInfo.publish_choice === '1'"><i class="el-icon-plus" /> 新建版本</el-button>
          <el-button size="small" type="primary" @click="submitCheck('save')" v-hasPermi="['admin:qform:myform:{id}:put']" v-if="createFlag || formInfo.publish_choice === '0'"><i class="el-icon-plus" /> 保存</el-button>
          <el-button size="small" type="primary" @click="submitCheck('create')" v-hasPermi="['admin:qform:myform:{id}:put']" v-if="createFlag"><i class="el-icon-plus" /> 发布</el-button>
          <el-button size="small" type="primary" @click="submitCheck('publish')" v-hasPermi="['admin:qform:myform:{id}:put']" v-if="!createFlag && formInfo.publish_choice === '0'"><i class="el-icon-plus" /> 发布</el-button>
          <el-button size="small" type="danger" v-hasPermi="['admin:qform:myform:{id}:delete']" v-if="createFlag"><i class="el-icon-delete" /> 删除</el-button>
          <el-button size="small" type="danger" @click="deleteForm" v-hasPermi="['admin:qform:myform:{id}:delete']" v-if="!createFlag"><i class="el-icon-delete"></i> 删除版本</el-button>
        </el-button-group>
      </el-col>
    </el-row>
    <el-row>
      <div id="app">
        <template v-if="formInfo.publish_choice === '0'">
          <Design ref="formDesign"></Design>
        </template>
        <template v-else>
          <Build :formTemplate="templateDatas.scheme" v-model="testModel"/>
        </template>
      </div>
    </el-row>
    <!-- 切换对话框 -->
    <el-dialog title="切换版本" :visible.sync="changeOpen" width="500px" append-to-body>
      <el-form ref="versionForm" :model="versionForm" :rules="changeRules" label-width="80px">
        <el-form-item label="版本号" prop="version">
          <SearchSelectPagination
            v-model="versionForm.version"
            labelName="version"
            labelValue="id"
            :multiple="false"
            url="/admin/qform/formtemplateversion/"
            :defaultParams="{source_form_id: templateDatas.source_form_id}"
            style="width: 100%;"
          >
          </SearchSelectPagination>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="changeTemplateFormVersion">确 定</el-button>
        <el-button @click="cancelVersionDialog">取 消</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="submitTitle" :visible.sync="submitOpen" width="500px" append-to-body>
      <div style="margin-top: 0px; margin-bottom: 15px; font-size: 15px; line-height: 20px;">
        <span>请设置用于列表显示的栏位，该栏位最多设置8条，目前已设置{{isTableNum}}条。</span>
        <span v-if="isTableNum > 8" style="color: red;">目前已超过{{isTableNum-8}}条，请修改。</span>
        <span>注意：弹性容器中列表展示选型无效。</span>
      </div>
      <vxe-table
        border
        show-overflow
        :column-config="{resizable: true}"
        :max-height="tableHeight"
        :data="this.checkTableList"
        ref="vxTable"
      >
        <vxe-column field="label" title="栏位名称"></vxe-column>
        <vxe-column field="isTable" prop="isTable" title="是否列表显示">
          <template slot-scope="scope">
            <template v-if="isTableList.includes(scope.row.type)">
              <el-switch
                v-model="scope.row.isTable"
                class="drawer-switch"
                active-text="是"
                inactive-text="否"
                @change="ChangeIsTable(scope.row)"
              />
            </template>
          </template>
        </vxe-column>
      </vxe-table>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitTable">确 定</el-button>
        <el-button @click="cancelSubmit">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  addTemplateData,
  updateTemplateData,
  updateData,
  patchData,
  delTemplateData
} from "@/api/modules/qform/myform";
  import _ from "lodash";
  import moment from "moment";
  import SearchSelectPagination from "@/components/SearchSelectPagination/Index";
  import Design from "@/components/NgForm/design";
  import Build from "@/components/NgForm/build";

    export default {
      name: "editor",
      components: {
        SearchSelectPagination,
        Design,
        Build
      },
      props: {
        formInfo: {
          type: Object, default: () => {}
        },
        templateDatas: {
          type: Object, default: () => {
            scheme: { }
          }
        },
      },
      data() {
        return {
          changeOpen: false,
          submitOpen: false,
          submitTitle: "",
          changeRules: {
            version: [
              { required: true, message: "版本号不能为空", trigger: "blur" },
            ]
          },
          versionForm: {},
          publishChoiceOptions: [],
          testModel: {},
          // 可列表化清单
          isTableList: ['input', 'textarea', 'number', 'rate','select', 'radio', 'checkbox','datePicker', 'date', 'time', 'uploadImg', 'slider', "uploadFile", "switch", "cascader", 'state', 'address'],
          // 展示标签列表
          checkTableList: [],
          // 表单验证类型标签
          flagType: "save",
          // 数据字段唯一校验
          uniqueNames: []
        }
      },
      computed: {
        isTableNum() {
          return this.templateDatas.scheme.list !== undefined ? this.checkTableList.filter(v => v.isTable === true).length : 0;
        },
        createFlag() {
          return !this.formInfo.form_info;
        },
        tableHeight() {
          return this.$store.state.winSize.winheight - 300 + "px !important";
        }
      },
      watch: {
        "formInfo.form_info"(val) {
          this.testModel = {};
          if(val !== undefined) {
            this.reset();
          }
        },
        templateDatas() {
          this.reset();
        },
      },
      created() {
        this.getDicts("publish_choice").then(response => {
          this.publishChoiceOptions = response.data;
        });
        this.reset();
      },
      methods: {
        // 强制修正弹性容器isTable属性
        fixControlIsTable(scheme) {
          scheme.list.forEach(v => {
            v.isTable = false;
          })
        },
        // 处理是否列表展示校验
        handleTemplateDatas(scheme) {
          if (_.isArray(scheme)) {
            scheme.forEach(s => this.handleTemplateDatas(s));
          } else if (Object.hasOwnProperty.call(scheme, "tds")) {
            scheme.tds.forEach(s => this.handleTemplateDatas(s));
          } else {
            scheme.list.forEach(d => {
              if (d.type === "control") {
                this.fixControlIsTable(d)
                // this.handleTemplateDatas(d);
              } else if (d.type === "grid") {
                this.handleTemplateDatas(d.columns);
              } else if (d.type === "table") {
                this.handleTemplateDatas(d.trs);
              } else if (this.isTableList.includes(d.type)) {
                // 强制避免数据字段重复
                if (this.uniqueNames.includes(d.model)) {
                  d.model = d.model + "1";
                }
                this.uniqueNames.push(d.model);
                this.checkTableList.push({
                  label: d.label,
                  type: d.type,
                  model: d.model,
                  isTable: d.isTable
                });
              }
            });
          }
        },

        changeIsTableData(scheme, model, flag) {
          if (_.isArray(scheme)) {
            scheme.forEach(s => this.changeIsTableData(s, model, flag));
          } else if (Object.hasOwnProperty.call(scheme, "tds")) {
            scheme.tds.forEach(s => this.changeIsTableData(s, model, flag));
          } else {
            scheme.list.forEach(d => {
              if (d.type === "control") {
                // this.changeIsTableData(d, model, flag);
              } else if (d.type === "grid") {
                this.changeIsTableData(d.columns, model, flag);
              } else if (d.type === "table") {
                this.changeIsTableData(d.trs, model, flag);
              } else if (d.model === model) {
                d.isTable = flag;
              }
            });
          }
        },

        ChangeIsTable(row) {
          this.changeIsTableData(this.templateDatas.scheme, row.model, row.isTable);
        },

        reset() {
          if (!this.createFlag) {
              if (this.formInfo.publish_choice === "0") {
                this.$nextTick(() => this.$refs["formDesign"].initModel(this.templateDatas.scheme));
              }
          }
        },

        async saveTemplateForm() {
          let res;
          if (this.createFlag) {
            this.templateDatas.version = moment().format("YYYYMMDDHHmmss");
            this.templateDatas.source_form_id = this.formInfo.id;
            this.templateDatas.scheme = this.$refs["formDesign"].getModel();
            res = await addTemplateData(this.templateDatas);
            if (res.code !== 200) { return; }
            this.$emit("update:templateDatas", res.data);
            this.formInfo.form_info = res.data.id;
            res = await updateData(this.formInfo);
            if (res.code !== 200) { return; }
            this.$emit("update:formInfo", res.data);
          } else {
            res = await updateTemplateData(this.templateDatas);
            if (res.code !== 200) { return; }
            this.$emit("update:templateDatas", res.data);
          }
          this.msgSuccess("修改成功");
        },

        async createTemplateFormVersion() {
          let res;
          let tmp = _.cloneDeep(this.templateDatas);
          tmp.id = null;
          const version = moment().format("YYYYMMDDHHmmss");
          tmp.version = version;
          res = await addTemplateData(tmp);
          if (res.code !== 200) { return; }
          this.$emit("update:templateDatas", res.data);
          this.formInfo.publish_choice = "0";
          this.formInfo.form_info = res.data.id;
          res = await updateData(this.formInfo);
          if (res.code !== 200) { return; }
          this.$emit("update:formInfo", res.data);
          this.msgSuccess("新建版本成功");
        },

        async publishTemplateForm() {
          let tmp = _.cloneDeep(this.formInfo);
          tmp.publish_choice = "1";
          let res = await updateData(tmp);
          if (res.code !== 200) { return; }
          this.$emit("update:formInfo", res.data);
          res = await updateTemplateData(this.templateDatas);
          if (res.code !== 200) { return; }
          this.$emit("update:templateDatas", res.data);
          this.msgSuccess("发布成功");
        },

        async saveAndPublishTemplateForm() {
          let res;
          this.templateDatas.version = moment().format("YYYYMMDDHHmmss");
          this.templateDatas.source_form_id = this.formInfo.id;
          this.templateDatas.scheme = this.$refs["formDesign"].getModel();
          res = await addTemplateData(this.templateDatas);
          if (res.code !== 200) { return; }
          this.$emit("update:templateDatas", res.data);
          this.formInfo.form_info = res.data.id;
          this.formInfo.publish_choice = "1";
          res = await updateData(this.formInfo);
          if (res.code !== 200) { return; }
          this.$emit("update:formInfo", res.data);
          this.msgSuccess("发布成功");
        },

        openTemplateFormVersion() {
          if (this.formInfo.publish_choice === "0") {
            this.msgError("切换版本前，请发布当前版本");
            return;
          }
          this.changeOpen = true;
          this.versionForm = {};
        },

        changeTemplateFormVersion(){
          this.$refs["versionForm"].validate(valid => {
            if (valid) {
              patchData({ id: this.formInfo.id, form_info: this.versionForm.version }).then(response => {
                this.msgSuccess("修改成功");
                this.$emit("update:formInfo", response.data);
                this.$emit("resetTemplateDatas");
              });
            }
          });
          this.changeOpen = false;
        },

        cancelVersionDialog() {
          this.changeOpen = false;
        },

        submitTable() {
          if (this.flagType === "save") {
            this.saveTemplateForm();
          } else if (this.flagType === "publish") {
            this.publishTemplateForm();
          } else {
            this.saveAndPublishTemplateForm();
          }
          this.submitOpen = false;
        },

        submitCheck(flag) {
          if (this.createFlag) {
            this.templateDatas.scheme = this.$refs["formDesign"].getModel();
          }
          if (this.templateDatas.scheme.list.length === 0) {
            this.msgError("表单内容不能为空");
            return;
          }
          this.submitOpen = true;
          this.checkTableList = [];
          this.handleTemplateDatas(this.templateDatas.scheme);
          this.uniqueNames = [];
          if (flag !== "save") {
            this.submitTitle = "发布确认";
          } else {
            this.submitTitle = "保存确认";
          }
          this.flagType = flag;
        },

        cancelSubmit() {
          this.submitOpen = false;
        },

        deleteForm() {
          this.$confirm('删除当前版本后，相关表单数据将被清空', "警告", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            return delTemplateData(this.templateDatas.id);
          }).then(() => {
            this.$emit("resetFormInfo");
            this.msgSuccess("删除版本成功");
          });
        },
      }
    }
</script>

<style lang="scss" scoped>
  #app {
    margin-top: 13px;
    background: #eef1f6;

    section {
      ::v-deep aside {
        margin-right: -15px !important;
        margin-left: 5px !important;
        margin-bottom: 0px !important;
      }
      ::v-deep main {
        div.form-design.el-row {
          margin-right: 0 !important;
          margin-left: 5px !important;
        }
      }
    }
  }


</style>
