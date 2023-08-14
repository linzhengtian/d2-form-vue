<template>
  <div class="app-container">
    <el-tabs v-model="activePage" @tab-click="handleClick" v-if="!noPermission">
      <el-tab-pane label="基础配置" name="basic">
        <formSetting @resetFormInfo="reset" :formInfo="formInfo"></formSetting>
      </el-tab-pane>
      <el-tab-pane
        label="表单设计"
        name="editor"
        v-if="formInfo.designpermission === '1'"
        lazy
      >
        <editor @resetFormInfo="reset" @resetTemplateDatas="resetTemplateDatas" :formInfo.sync="formInfo" :templateDatas.sync="templateDatas"></editor>
      </el-tab-pane>
      <el-tab-pane
        label="数据统计"
        name="datas"
        v-if="formInfo.form_info"
        lazy
      >
        <formTable :templateDatas="templateDatas" :formInfo="formInfo"></formTable>
      </el-tab-pane>
      <el-tab-pane
        label="发布"
        name="publish"
        lazy
        v-if="formInfo.form_info && formInfo.publish_choice === '1' && formInfo.questionnaire_choice === '1'"
      >
        <publishPanel @linkToEdit="linkToEdit" :formInfo="formInfo"></publishPanel>
      </el-tab-pane>
    </el-tabs>
    <noPanel v-else></noPanel>
  </div>
</template>

<script>
  import editor from "./editor";
  import formSetting from "./formSetting";
  import formTable from "./formTable";
  import publishPanel from "./publishPanel";
  import noPanel from "./noPanel";
  import {
    getData,
    getTemplateData
  } from "@/api/modules/qform/myform";
  import _ from "lodash";

    export default {
      name: "formEdit",
      components: {
        editor,
        formSetting,
        formTable,
        publishPanel,
        noPanel
      },
      props: {
        formId: {
          type: String
        },
        activeTab: {
          type: String,
          default: 'editor'
        },
      },
      data() {
        return {
          activePage: this.activeTab,
          templateDatas: {
            scheme: {}
          },
          formInfo: {},
          noPermission: false
        };
      },
      watch: {
        formId(val) {
          this.reset();
        },
        activeTab: {
          handler: function(newValue) {
            this.activePage = newValue;
          },
          immediate: true
        }
      },
      mounted() {
        this.getInfoDataById();
      },
      methods: {
        async getInfoDataById() {
          const res1 = await getData(this.formId);
          let res2 = null;
          if (res1.data.form_info) {
            res2 = await getTemplateData(res1.data.form_info);
          }
          this.formInfo = res1.data;
          const { designpermission, create_permission, modify_permission, questionnaire_choice, delete_permission } = this.formInfo;
          this.noPermission = (designpermission !== "1" && create_permission !== "1" && modify_permission !== "1" && questionnaire_choice === "0" && delete_permission !== "1");
          if (res2) {
            this.templateDatas = res2.data;
          }
        },
        reset() {
          this.formInfo = {};
          this.templateDatas = {
            scheme: {}
          };
          this.getInfoDataById();
        },
        async resetTemplateDatas() {
          this.templateDatas = {
            scheme: {}
          };
          const res = await getTemplateData(this.formInfo.form_info);
          if (res.code !== 200) { return; }
          this.templateDatas = res.data;
        },
        linkToEdit(name) {
          this.activeTab = this.activePage = name;
        },
        handleClick(tab, event) {
          this.activeTab = tab.name; // 防止切换tab后，再次进入跳转错误
          switch(tab.name)
          {
            case "editor":
              this.reset();
              // console.log(this.formInfo)
              break;
            case "datas":

              break;
            default:

          }
        }
      }
    }
</script>

<style scoped>

</style>
