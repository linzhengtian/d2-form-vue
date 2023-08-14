<template>
  <el-dialog
    :title="dialogTitle"
    :visible="openDetailModal"
    :width="modalWidth"
    append-to-body
    @close="closeDetailFormDialog"
  >
    <el-form
      ref="form"
      :model="formValue"
      :label-width="labelWidth"
      :size="formSize"
    >
      <el-row>
        <template v-for="(item,index) in formItem">
          <el-col :key="index" :span="item.singleLine? 24:12">
            <el-form-item :key="item.index" :label="`${item.label}：`">
              <template v-if="item.customRender">
                <slot :name="item.key" :item="item" />
              </template>
              <template v-else-if="item.attachment">
                <div class="image" v-for="file in formValue[item.key]" :key="file.id">
                  <el-image
                    style="width: 100px; height: 100px"
                    :src="file.file_url ? baseUrl + file.file_url : file.file"
                    fit="contain"></el-image>
                  <div>
                    <span title="预览" style="padding-right: 10px;" @click.stop="dialogVisible = true; previewUrl = (file.file_url ? baseUrl + file.file_url : file.file)">
                      <i class="el-icon-zoom-in" />
                    </span>
                    <span title="下载" @click.stop="downloadFile(file);">
                      <i class="el-icon-download" />
                    </span>
                  </div>
                  <div style="margin-top: -5px;">{{ file.name }}</div>
                </div>
              </template>
              <template v-else>
                {{ formValue[item.key] }}
              </template>
            </el-form-item>
          </el-col>
        </template>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="closeDetailFormDialog">关 闭</el-button>
    </div>
    <el-dialog :visible.sync="dialogVisible" title="预览" width="600" append-to-body>
      <img :src="previewUrl" style="display: block; max-width: 100%; max-height: 600px; margin: 0 auto;">
    </el-dialog>
  </el-dialog>
</template>

<script>
import { parseTime } from "../../utils/ruoyi";
import _ from "lodash";
import request from "@/utils/request";
import { getFileList } from "@/api/vadmin/system/savefile";
import { downloadAuth } from "@/utils/ruoyi";

const labelTypeToFunction = {
  time: (item, formData) => {
    return parseTime(formData[item.key]);
  },
  labels: (item, formData) => {
    return item.choice.labels[formData[item.key]];
  }
};

export default {
  name: "DetailFormDialog",
  props: {
    dialogTitle: { type: String, required: true },
    openDetailModal: { type: Boolean, required: true },
    modalWidth: { type: String, default: "720px" },
    labelWidth: { type: String, default: "100px" },
    formSize: { type: String, default: "mini" },
    formData: { type: Object, default: {}},
    formItem: { type: Array, default: [] },
    //是否支持后台直接根据id匹配下载
    directDownload: { type: Boolean, default: false }
  },
  data() {
    return {
      previewUrl: "",
      dialogVisible: false,
      baseUrl: process.env.VUE_APP_BASE_API,
      formValue: _.cloneDeep(this.formData)
    }
  },
  created() {
    this.parseFormItemContent();
  },
  methods: {
    parseFormItemContent() {
      for (const item of this.formItem) {
        const choice = item.choice;
        if (choice) {
          const key = _.get(Object.keys(choice), 0, "");
          switch (key)
          {
            case "time":
            case "labels":
              this.formValue[item.key] = labelTypeToFunction[key](item, this.formValue);
              break;
            case "dict":
              this.getDicts(choice["dict"]).then(response => {
                this.formValue[item.key] = this.selectDictLabels(response.data, this.formValue[item.key], ",");
              });
              break;
            case "search":
              /**
               填入搜索结果第一条记录
               url: 搜索地址，格式如/admin/case/caserole/,
               queryName: 搜索条件字段,
               queryValue: 搜索结果字段
               请求地址为：http://127.0.0.1:8000/.../?queryName=2
               请求结果格式为：
               {
                  "code": 200,
                  "data": {
                      "results": [
                          {
                              "queryName": 2,
                              "queryValue": "test002",
                          }
                      ]
                  },
                  "msg": "success",
                  "status": "success"
              }
             */
              const search = item.choice.search;
              request({
                url: search.url,
                method: _.get(search, "method", "GET"),
                params: {
                  [search.queryName]: this.formValue[item.key]
                }
              }).then(response => {
                this.formValue[item.key] = response.data.results[0][search.queryValue];
              });
              break;
          }
        }
        /**
         默认由/admin/system/savefilelist/载入附件
         需要设置attachment: true
         */
        if (item.attachment) {
          const attachments_ids = this.formValue[item.key];
          if (attachments_ids) {
            getFileList(attachments_ids).then(response => {
              const files = response.data.results;
              files.forEach(f => {
                f.percentage = 100;
                f.status = "success";
                f.file_url = "/" + _.trimStart(f.file_url, "/");
              });
              this.formValue[item.key] = files;
            });
          }
        }
      }
    },
    closeDetailFormDialog() {
      this.$emit("closeDialog", false);
    },
    downloadFile(file) {
      if (this.directDownload) {
        this.download(file.file, file.name, true);
      } else {
        downloadAuth("/admin/system/savefile/download_file/?id=" + file.id, file.name);
      }
    }
  }

};
/**
  输入格式形如：
 [{
    index: 1,
    label: "编号",
    key: "id"
  },
 {
    index: 2,
    label: "角色", //根据搜索条件获取单选值
    key: "case_role",
    choice: {
      search: {
        url: "/admin/case/caserole/",
        queryName: "id",
        queryValue: "role_name"
      }
    }
  },
 {
    index: 3,
    label: "文本",
    key: "plan",
    singleLine: true
  },
 {
    index: 4,
    label: "类型", //根据数据字典获取值
    key: "employee_choice",
    choice: { dict: "case_employee_choice" }
  },
 {
    index: 5,
    label: "状态",
    key: "status", //根据自定义对象获取值
    choice: {
      labels: {
        false: "失败",
        true: "正常"
      }
    }
  },
 {
    index: 9,
    label: "日期",
    key: "create_datetime",
    choice: "time",
    singleLine: true
  },
 {
    index: 10,
    label: "附件", //默认附件方法
    key: "attachments",
    attachment: true,
    singleLine: true
  }]
 */
</script>

<style scoped lang="scss">
.image {
  padding: 10px 0;
  text-align: center;
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}
</style>

