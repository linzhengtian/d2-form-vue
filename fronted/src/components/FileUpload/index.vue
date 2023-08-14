<template>
  <div class="upload-file">
    <el-upload
      ref="upload"
      :action="uploadFileUrl"
      :before-upload="handleBeforeUpload"
      :on-change="handleChange"
      :on-remove="removeChange"
      :file-list="fileLists"
      :auto-upload="autoUpload"
      :limit="limit"
      :multiple="multiple"
      :on-error="handleUploadError"
      :on-exceed="handleExceed"
      :on-success="handleUploadSuccess"
      :show-file-list="showFileList"
      :headers="headers"
      class="upload-file-uploader"
    >
      <!-- 上传按钮 -->
      <el-button size="mini" type="primary">选取文件</el-button>
      <!-- 上传提示 -->
      <div v-if="showTip" slot="tip" class="el-upload__tip">
        请上传
        <template v-if="fileSize"> 大小不超过 <b style="color: #f56c6c">{{ fileSize }}MB</b> </template>
        <template v-if="fileType"> 格式为 <b style="color: #f56c6c">{{ fileType.join("/") }}</b> </template>
        的文件
      </div>
    </el-upload>

    <!-- 文件列表 -->
    <slot name="fileGroup">
      <transition-group v-if="!showFileList" class="upload-file-list el-upload-list el-upload-list--text" name="el-fade-in-linear" tag="ul">
        <li v-for="(file, index) in list" :key="file.uid" class="el-upload-list__item ele-upload-list__item-content">
          <el-link :href="file.url" :underline="false" target="_blank">
            <span class="el-icon-document"> {{ getFileName(file.name) }}
              <template v-if="file.status ===`success`">
                <i class="el-icon-upload-success el-icon-circle-check"></i>
              </template>
              <template v-else-if="file.status ===`fail`">
                <i class="el-icon-error"></i>
              </template>
            </span>
          </el-link>
          <div class="ele-upload-list__item-content-action">
            <el-link v-if="previewStatus" :underline="false" type="primary" @click="handlePreview(index)">预览</el-link>
            <el-link :underline="false" type="primary" @click="handleDownload(index)">下载</el-link>
            <el-link :underline="false" type="danger" @click="handleDelete(index)">删除</el-link>
          </div>
        </li>
      </transition-group>
    </slot>
    <el-dialog :visible.sync="dialogVisible" title="预览" width="600" append-to-body>
      <img :src="previewUrl" style="display: block; max-width: 100%; max-height: 600px; margin: 0 auto;">
    </el-dialog>
  </div>
</template>

<script>
import { getToken } from "@/utils/auth";
import { delSaveFile } from "@/api/vadmin/system/savefile";
import { downloadAuth } from "@/utils/ruoyi";
import _ from "lodash";

export default {
  name: "FileUpload",
  props: {
    // 值
    value: [String, Object, Array],
    // 大小限制(MB)
    fileSize: {
      type: Number,
      default: 5
    },
    // 文件类型, 例如['png', 'jpg', 'jpeg']
    fileType: {
      type: Array,
      default: () => ["doc", "xls", "ppt", "txt", "pdf"]
    },
    // 是否显示提示
    isShowTip: {
      type: Boolean,
      default: true
    },
    // 文件限制个数
    limit: {
      type: Number,
      default: 1
    },
    // 是否多选
    multiple: {
      type: Boolean,
      default: false
    },
    // 是否自动上传
    autoUpload: {
      type: Boolean,
      default: true
    },
    // 是否自定义文件框
    showFileList: {
      type: Boolean,
      default: false
    },
    // 是否支持预览
    previewStatus: {
      type: Boolean,
      default: false
    },
    // 是否支持后台直接根据id匹配下载
    directDownload: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      uploadFileUrl: process.env.VUE_APP_BASE_API + "/admin/system/savefile/", // 上传的图片服务器地址
      headers: {
        Authorization: "Bearer " + getToken()
      },
      dialogVisible: false,
      previewUrl: "",
      baseUrl: process.env.VUE_APP_BASE_API,
      fileLists: Array.isArray(this.value) ? this.value : (this.value ? [this.value] : [])
    };
  },
  computed: {
    // 是否显示提示
    showTip() {
      return this.isShowTip && (this.fileType || this.fileSize);
    },
    // 列表
    list() {
      let temp = 1;
      if (this.fileLists) {
        // 首先将值转为数组
        const list = this.fileLists;
        // 然后将数组转为对象数组
        return list.map((item) => {
          if (typeof item === "string") {
            item = { name: item, url: item };
          }
          item.uid = item.uid || new Date().getTime() + temp++;
          return item;
        });
      } else {
        this.fileLists = [];
        return [];
      }
    }
  },
  watch: {
    value: {
      handler: function(val) {
        this.fileLists = val;
      },
      deep: true
    }
  },
  created() {
  },
  methods: {
    // 提交
    submit() {
      if (this.fileLists.length > 0) {
        this.$refs.upload.submit();
      }
    },
    handleChange(file, fileLists, i) {
      // 解决自动上传关闭后,上传校验不生效
      if (!this.autoUpload && !this.handleBeforeUpload(file)) {
        fileLists = fileLists.filter(v => v.name !== file.name);
      }
      this.fileLists = fileLists;
    },
    async removeChange(file, fileLists) {
      try {
        if (this.autoUpload && "id" in file) {
          await delSaveFile(file.id);
        }
        this.fileLists = fileLists;
        if (this.showFileList) {
          this.$emit("input", this.fileLists);
        }
      } catch (err) {
        this.$message.error("删除失败, 请重试");
      }
    },
    // 上传前校检格式和大小
    handleBeforeUpload(file) {
      // 校检文件类型
      if (this.fileType && this.fileType[0] !== "ALL") {
        let fileExtension = "";
        if (file.name.lastIndexOf(".") > -1) {
          fileExtension = file.name.slice(file.name.lastIndexOf(".") + 1);
        }
        const isTypeOk = this.fileType.some((type) => {
          if ("type" in file && file.type.indexOf(type) > -1) return true;
          if (fileExtension && fileExtension.indexOf(type) > -1) return true;
          return false;
        });
        if (!isTypeOk) {
          this.$message.error(`${file.name}文件格式不正确, 请上传${this.fileType.join("/")}格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < this.fileSize;
        if (!isLt) {
          this.$message.error(`上传${file.name}文件大小不能超过 ${this.fileSize} MB!`);
          return false;
        }
      }
      return true;
    },
    // 文件个数超出
    handleExceed() {
      this.$message.error(`只允许上传${this.limit}个文件`);
    },
    // 上传失败
    handleUploadError() {
      this.$message.error("上传失败, 请重试");
    },
    // 上传成功回调
    handleUploadSuccess(res, file) {
      if (res.code === 200) {
        this.fileLists.forEach(f => {
          if (Object.hasOwnProperty.call(f, "response") && !Object.hasOwnProperty.call(f, "id") && Object.hasOwnProperty.call(f.response.data, "id")) {
            f.id = f.response.data.id;
            f.file = f.response.data.file;
            if (f.response.data.file_url) {
              f.file_url = "/" + _.trimStart(f.response.data.file_url, "/");
            }
          }
        });
        this.$message.success(`${file.name}上传成功`);
        // this.$emit("input", res.data.file);
        if (this.fileLists.every(file => file.status === "success")) {
          // 全部完成传输后，父组件接收closeUpload方法，用于控制窗口关闭, fileList可以获取上传成功后的返回信息
          this.$emit("closeUpload", [true, this.fileLists]);
          this.$emit("input", this.fileLists);
        }
      } else {
        this.$message.error(res.msg);
      }
    },
    // 删除文件
    async handleDelete(index) {
      try {
        if (this.autoUpload) {
          const file = this.fileLists[index];
          await delSaveFile(file.id);
        }
        this.fileLists.splice(index, 1);
        this.$emit("input", this.fileLists);
      } catch (err) {
        this.$message.error("删除失败, 请重试");
      }
    },
    // 下载文件
    handleDownload(index) {
      const file = this.fileLists[index];
      if (this.directDownload) {
        this.download(file.file, file.name, true);
      } else {
        downloadAuth("/admin/system/savefile/download_file/?id=" + file.id, file.name);
      }
    },
    // 预览图片
    handlePreview(index) {
      const file = this.fileLists[index];
      this.dialogVisible = true;
      this.previewUrl = file.file_url ? this.baseUrl + file.file_url : file.file;
    },
    // 获取文件名称
    getFileName(name) {
      if (name.lastIndexOf("/") > -1) {
        return name.slice(name.lastIndexOf("/") + 1).toLowerCase();
      } else {
        return name || "";
      }
    }
  }
};
</script>

<style scoped lang="scss">
.upload-file-uploader {
  margin-bottom: 5px;
}
.upload-file-list .el-upload-list__item {
  border: 1px solid #e4e7ed;
  line-height: 2;
  margin-bottom: 10px;
  position: relative;
}
.upload-file-list .ele-upload-list__item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: inherit;
}
.ele-upload-list__item-content-action .el-link {
  margin-right: 10px;
}
</style>
