<template>
  <div class="paper-container">
    <div class="project-form-wrapper" v-if="fillin">
      <div class="project-form">
        <div class="form-name-text">
          {{ formInfo.name }}
        </div>
        <div class="describe-html" v-if="formInfo.description">
          {{ formInfo.description }}
        </div>
        <div class="project-body">
          <Build
            ref="formbuild"
            v-if="loading"
            :form-template="templateDatas.scheme"
            v-model="formDatas"
            :config="httpConfig"
          />
          <div class="project-handler">
            <el-button type="primary" @click="onSubmit">提交</el-button>
            <el-button @click="reset">重置</el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="write-container" v-else>
      <div class="title-icon-view">
        <div class="el-result">
          <div class="el-result__icon">
            <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" class="icon-success">
              <path d="M24,4 C35.045695,4 44,12.954305 44,24 C44,35.045695 35.045695,44 24,44 C12.954305,44 4,35.045695 4,24 C4,12.954305 12.954305,4 24,4 Z M34.5548098,16.4485711 C33.9612228,15.8504763 32.9988282,15.8504763 32.4052412,16.4485711 L32.4052412,16.4485711 L21.413757,27.5805811 L21.413757,27.5805811 L21.4034642,27.590855 C21.0097542,27.9781674 20.3766105,27.9729811 19.9892981,27.5792711 L19.9892981,27.5792711 L15.5947588,23.1121428 C15.0011718,22.514048 14.0387772,22.514048 13.4451902,23.1121428 C12.8516033,23.7102376 12.8516033,24.6799409 13.4451902,25.2780357 L13.4451902,25.2780357 L19.6260786,31.5514289 C20.2196656,32.1495237 21.1820602,32.1495237 21.7756472,31.5514289 L21.7756472,31.5514289 L34.5548098,18.614464 C35.1483967,18.0163692 35.1483967,17.0466659 34.5548098,16.4485711 Z"></path>
            </svg>
          </div><div class="el-result__title"><p>提交成功</p></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getAnonymousTemplateData,
  getAnonymousData,
  addAnonymousFormData
} from "@/api/modules/qform/myform";
import Build from "@/components/NgForm/build";
import _ from "lodash";

export default {
  name: "Detail",
  components: {
    Build
  },
  props: {
    formId: {
      type: String
    }
  },
  data() {
    return {
      loading: false,
      templateDatas: {
        list: []
      },
      fillin: true,
      httpConfig: {
        uploadPath: process.env.VUE_APP_BASE_API + "/admin/qform/anonymoussavefile/",
        baseUrl: process.env.VUE_APP_BASE_API // 用于拼接下载地址，nginx需要配置对media目录的重定向
      },
      formDatas: { },
      formInfo: { }
    };
  },
  created() {
    this.reset();
  },
  methods: {
    async reset() {
      this.templateDatas = { scheme: { }};
      this.formDatas = { };
      this.formInfo = { };
      await this.getAnonymousTemplateDatas();
    },

    async getAnonymousTemplateDatas() {
      this.loading = false;
      let res = await getAnonymousData(this.formId);
      this.formInfo = res.data;
      res = await getAnonymousTemplateData(res.data.form_info);
      this.templateDatas = res.data;
      this.loading = true;
    },

    onSubmit() {
      this.$refs.formbuild.validator().then((valid) => {
        if (valid) {
          this.loading = true;
          this.formDatas = {
            "form_template": this.templateDatas.id,
            "fill_data": this.formDatas
          };
          addAnonymousFormData(this.formDatas).then((res) => {
            if (res.code === 200) {
              this.fillin = false;
              // this.msgSuccess("提交成功");
            } else {
              this.msgError(res.msg);
            }
          }).finally(() => {
            this.loading = false;
          });
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
  .paper-container {
    width: 100%;
    height: 100%;

    .project-form-wrapper {
      width: 100%;
      min-width: 950px;
      min-height: 100vh;
      padding: 20px 10px;
      background: hsla(0, 0%, 83.5%, .2784313725490196);
      height: 100%;
      background-position: center 0 !important;
      background-size: cover !important;
      overflow: auto;

      .project-form {
        margin: 0 auto;
        min-width: 800px;
        width: 70%;
        background-repeat: repeat;
        background-color: #fff;
        -webkit-box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
        box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
        border-radius: 10px;

        .form-name-text {
          padding: 30px 30px 10px;
          border: 1px dashed transparent;
          line-height: 30px;
          margin: 0;
          text-align: center;
          font-size: 28px;
          font-weight: 700;
        }

        .project-body {
          padding: 20px;

          .project-handler {
            padding-top: 20px;
            text-align: center;
          }
        }

        .describe-html {
          padding: 5px 30px;
          border: 1px dashed transparent;
        }
      }
    }

    .write-container {
      margin: 0;
      padding: 0;
      height: 100%;
      width: 100%;
      overflow-x: hidden;

      .title-icon-view {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        align-content: center;
        -webkit-box-pack: center;
        justify-content: center;
        -ms-flex-align: center;
        -ms-flex-line-pack: center;
        -ms-flex-pack: center;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        height: 100%;
        width: 100%;

        .el-result {
          display: -webkit-box;
          display: -ms-flexbox;
          display: flex;
          -webkit-box-pack: center;
          -ms-flex-pack: center;
          justify-content: center;
          -webkit-box-align: center;
          -ms-flex-align: center;
          align-items: center;
          -webkit-box-orient: vertical;
          -webkit-box-direction: normal;
          -ms-flex-direction: column;
          flex-direction: column;
          text-align: center;
          -webkit-box-sizing: border-box;
          box-sizing: border-box;
          padding: 40px 30px;

          .icon-success {
            fill: #13ce66;
          }
          .el-result__icon svg {
            width: 64px;
            height: 64px;
          }

          .el-result__title {
            margin-top: 20px;
          }
        }
      }
    }
  }
</style>
