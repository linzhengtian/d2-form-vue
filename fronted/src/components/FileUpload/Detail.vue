<template>
  <div>
    <el-col :key="index" :span="span">
        <div class="image" v-for="file in formItem" :key="file.id">
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
    </el-col>
    <el-dialog :visible.sync="dialogVisible" title="预览" width="600" append-to-body>
      <img :src="previewUrl" style="display: block; max-width: 100%; max-height: 600px; margin: 0 auto;">
    </el-dialog>
  </div>
</template>

<script>
  import { parseTime } from "../../utils/ruoyi";
  import _ from "lodash";
  import request from "@/utils/request";
  import { getFileList } from "@/api/vadmin/system/savefile";
  import { downloadAuth } from "@/utils/ruoyi";

  export default {
    name: "AttachmentsDetail",
    props: {
      index: { type: [Number, String], default: "attachments" },
      value: { type: String }, // 格式为附件id的组合，如：11,12,13,
      span: { type: Number, default: 24 },
      // 是否支持后台直接根据id匹配下载
      directDownload: { type: Boolean, default: false }
    },
    data() {
      return {
        previewUrl: "",
        dialogVisible: false,
        attachments: [],
        baseUrl: process.env.VUE_APP_BASE_API,
        formItem: []
      }
    },
    watch: {
      value: {
        handler: function (val) {
          this.attachments = val;
        },
        immediate: true
      },
    },
    created() {
      this.parseFormItemContent();
    },
    methods: {
      parseFormItemContent() {
        if (this.attachments) {
          getFileList(this.attachments).then(response => {
            const files = response.data.results;
            files.forEach(f => {
              f.percentage = 100;
              f.status = "success";
              f.file_url = "/" + _.trimStart(f.file_url, "/");
            });
            this.formItem = files;
          });
        }
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
   {
    index: 10,
    label: "附件", //默认附件方法
    key: "attachments",
    attachment: true,
    singleLine: true
  }
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

