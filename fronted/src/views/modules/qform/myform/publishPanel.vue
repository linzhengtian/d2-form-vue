<template>
  <div class="publish-container">
    <div class="publish-view">
      <el-row type="flex" justify="center">
        <el-col :span="12">
          <div class="publish-picture">
            <div class="icon-view">
              <i class="el-icon-check success-icon"></i>
            </div>
          </div>
          <div>
            <p class="success-title">问卷已成功发布！</p>
          </div>
          <div>
            <p class="link-text">{{ publishUrl }}</p>
          </div>
          <template v-if="formInfo.designpermission === '1'">
            <el-row>
              <el-col :span="6" :offset="6">
                <el-button type="primary" @click="copyUrl">复制链接</el-button>
              </el-col>
              <el-col :span="6" :offset="1">
                <el-button type="danger" @click="linkToEdit">修改问卷</el-button>
              </el-col>
            </el-row>
          </template>
          <template v-else>
            <el-row>
              <div style="text-align: center; margin-left: 30px;">
                <el-button type="primary" @click="copyUrl">复制链接</el-button>
              </div>
            </el-row>
          </template>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  export default {
    name: "publishPanel",
    props: {
      formInfo: {
        type: String
      }
    },
    computed: {
      publishUrl() {
        return document.location.host + `/paper?formId=${this.formInfo.id}`;
      }
    },
    methods: {
      copyUrl() {
        let inputNode = document.createElement('input'); // 创建input
        inputNode.value = this.publishUrl; // 赋值给 input 值
        document.body.appendChild(inputNode); // 插入进去
        inputNode.select(); // 选择对象
        document.execCommand('Copy'); // 原生调用执行浏览器复制命令
        inputNode.style.display = 'none'; // 隐藏
      },

      linkToEdit() {
        this.$emit("linkToEdit", "editor");
      }
    },
  }
</script>

<style lang="scss" scoped>
  .publish-container {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    min-height: 90vh;

    .publish-view {
      text-align: center;
      width: 800px;
      height:200px;
      margin: 0 auto;
      padding-top: 200px;

      .success-title {
        padding-left: 50px;
        color: #1e1e1e;
        font-size: 28px;
      }

      .link-text {
        padding-left: 30px;
        color: #1e1e1e;
        font-size: 14px;
      }
    }
  }

  .publish-picture {
    display: flex;
    justify-content: center;
    text-align: center;
    align-items: center;
    padding-left: 30px;

    .icon-view {
      width: 60px;
      height: 60px;
      border-radius: 100px;
      display: flex;
      align-items: center;
      align-content: center;
      justify-content: center;
      justify-items: center;
      background-color: #1c84c6;

      .success-icon {
        text-align: center;
        color: #ffffff;
        font-size: 30px;
      }
    }
  }
</style>
