import { d2CrudPlus } from "d2-crud-plus";
// import d2Crud from '@d2-projects/d2-crud' 【d2-crud官方已停止维护，推荐使用增强版d2-crud-x】
// 推荐将d2-crud替换为d2-crud-x【使用方式基本与d2-crud一致】
import d2CrudX from "d2-crud-x";
import Vue from "vue";
import Cookies from "js-cookie";
import Element from "element-ui";
import VueI18n from 'vue-i18n';
import VueEditor from 'vue2-editor';
import VXETable from 'vxe-table';
import 'vxe-table/lib/style.css';

// 自定义表格工具扩展
import "./assets/styles/element-variables.scss";
import "@/assets/styles/index.scss"; // global css
import "@/assets/styles/ruoyi.scss"; // ruoyi css
import App from "./App";
import store from "./store";
import router from "./router";
import permission from "./directive/permission";
import "./assets/icons"; // icon
import "./permission"; // permission control
import { getDicts } from "@/api/vadmin/system/dict/data";
import { getConfigKey } from "@/api/vadmin/system/config";
import {
  addDateRange,
  download,
  handleTree,
  parseTime,
  resetForm,
  selectDictLabel,
  selectDictDefault,
  selectDictLabels
} from "@/utils/ruoyi";
import Pagination from "@/components/Pagination";
import RightToolbar from "@/components/RightToolbar";
import SmallDialog from "@/components/SmallDialog";
import DeptTree from "@/components/DeptTree";
import UsersTree from "@/components/UsersTree";
import ModelDisplay from "@/components/ModelDisplay";
import CommonIcon from "@/components/CommonIcon";
import CommonStaticTable from "@/components/CommonStaticTable";
import { getCrontabData, getIntervalData } from "./utils/validate"; // 通用图标组件
import { getModelSelect } from "@/utils/modelSelect";
import request from "@/utils/request";
import { D2pAreaSelector, D2pFileUploader, D2pIconSelector, D2pTreeSelector, D2pFullEditor, D2pUploader, D2pDemoExtend } from 'd2p-extends'; // 组件支持懒加载
import SearchSelectPagination from "@/components/SearchSelectPagination/Index";
import FileUpload from "@/components/FileUpload/index";
import AttachmentsDetail from "@/components/FileUpload/Detail";
import 'normalize.css/normalize.css';
// ng-form
import NgForm from '@linzhengtian/ng-form-element';
import '@linzhengtian/ng-form-element/lib/ng-form-element.css';
import pluginExport from '@d2-projects/vue-table-export';
// 按需引入vue-awesome图标
import Icon from 'vue-awesome/components/Icon';
import 'vue-awesome/icons/chart-bar.js';
import 'vue-awesome/icons/chart-area.js';
import 'vue-awesome/icons/chart-pie.js';
import 'vue-awesome/icons/chart-line.js';
import 'vue-awesome/icons/align-left.js';
import dataV from '@jiaminghi/data-view';
import echarts from 'echarts';

Vue.use(d2CrudX, { name: "d2-crud-x" });
Vue.use(d2CrudPlus, {
  // 获取数据字典的请求方法
  // 可在dict中配置getData方法覆盖此全局方法
  getRemoteDictFunc(url, dict) {
    return request({ // 用你项目中的http请求
      url: url,
      method: "get"
    }).then(ret => {
      return ret.data; // 返回字典数组
    });
  },
  commonOption() { // d2-crud option 全局配置，每个页面的crudOptions会以全局配置为基础进行覆盖
    return {
      format: {
        page: { // page接口返回的数据结构配置，
          request: { // 请求参数
            current: "pageNum", // 当前
            size: "pageSize"
          },
          response: { // 返回结果
            current: (data) => { return Number(data.pageNum) }, // 当前页码 ret.data.pageNum
            size: (data) => { return Number(data.pageSize) }, // 每页条数，ret.data.pageSize,
            // current: "pageNum", // 当前页码 ret.data.pageNum
            // size: "pageSize", // 每页条数，ret.data.pageSize,
            // size: (data) => { return data.size }, //你也可以配置一个方法，自定义返回
            total: "count", // 总记录数 ret.data.count
            records: "results" // 列表数组 ret.data.results
          }
        }
      },
      formOptions: {
        nullToBlankStr: true,
        defaultSpan: 12 // 默认的表单 span
      },
      options: {
        height: "100%" // 表格高度100%，此时d2-crud-x外部容器必须有高度, 使用toolbar必须设置
      },
      pageOptions: {
        compact: true // 是否紧凑型页面
      },
      viewOptions: {
        disabled: false // 开启查看按钮
      }
    };
  }
});

// 全局方法挂载
Vue.prototype.getDicts = getDicts;
Vue.prototype.getConfigKey = getConfigKey;
Vue.prototype.getModelSelect = getModelSelect;
Vue.prototype.parseTime = parseTime;
Vue.prototype.resetForm = resetForm;
Vue.prototype.addDateRange = addDateRange;
Vue.prototype.selectDictLabel = selectDictLabel;
Vue.prototype.selectDictDefault = selectDictDefault;
Vue.prototype.selectDictLabels = selectDictLabels;
Vue.prototype.getCrontabData = getCrontabData;
Vue.prototype.getIntervalData = getIntervalData;
Vue.prototype.download = download;
Vue.prototype.handleTree = handleTree;
Vue.prototype.hasPermi = function(values) {
  const permissions = store.getters && store.getters.permissions;
  return permissions.some(permission => {
    return permission === "*:*:*" || values.includes(permission);
  });
};
Vue.prototype.msgSuccess = function(msg) {
  this.$message({ showClose: true, message: msg, type: "success" });
};
Vue.prototype.msgError = function(msg) {
  this.$message({ showClose: true, message: msg, type: "error" });
};
Vue.prototype.msgInfo = function(msg) {
  this.$message.info(msg);
};

// 自定义组件
Vue.component("SmallDialog", SmallDialog);
Vue.component("DeptTree", DeptTree);
Vue.component("UsersTree", UsersTree);
Vue.component("ModelDisplay", ModelDisplay);
// 全局组件挂载
Vue.component("Pagination", Pagination);
Vue.component("RightToolbar", RightToolbar);
Vue.component("CommonIcon", CommonIcon);
Vue.component("CommonStaticTable", CommonStaticTable);
Vue.component("D2pSearchSelectPagination", SearchSelectPagination);
Vue.component("D2pFileUpload", FileUpload);
Vue.component("D2pAttachmentsDetail", AttachmentsDetail);
Vue.component("icon", Icon);

// 安装扩展插件
Vue.use(VueI18n);
Vue.use(VueEditor);
Vue.use(permission);
Vue.use(D2pTreeSelector);
Vue.use(D2pAreaSelector);
Vue.use(D2pIconSelector);
Vue.use(D2pFullEditor);
Vue.use(D2pFileUploader);
Vue.use(D2pDemoExtend);
Vue.use(pluginExport);
Vue.use(VXETable);
// Vue.use(D2pUploader, {
//   ... //文件上传有额外配置,请看下方链接
// })

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */
Vue.use(NgForm);

Vue.use(Element, {
  size: Cookies.get("size") || "medium" // set element-ui default size
});

Vue.use(dataV);

Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
});
