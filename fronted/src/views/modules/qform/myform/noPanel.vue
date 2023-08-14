<template>
  <div class="publish-container">
    <div class="publish-view">
      <el-row type="flex" justify="center">
        <el-col :span="12">
          <div class="publish-picture">
            <div class="icon-view">
              <i class="el-icon-close fail-icon"></i>
            </div>
          </div>
          <div>
            <p class="success-title">您没有操作权限！</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  export default {
    name: "noPanel",
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
      background-color: #ff0000;

      .fail-icon {
        text-align: center;
        color: #ffffff;
        font-size: 30px;
      }
    }
  }
</style>
