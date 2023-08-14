import _ from "lodash";
import { parseTime } from "@/utils/ruoyi";

function addDays(date, days) {
  date.setTime(date.getTime() + 3600 * 1000 * 24 * days);
}

function addDataRange(params, dataRange) {
  const as = JSON.parse(_.get(params, "as", "{}"));
  for (const d in dataRange) {
    as[d] = dataRange[d];
    params["as"] = JSON.stringify(as);
  }
  return params;
}

const shortcuts = [
  {
    text: "今明两天",
    onClick(picker) {
      const start = new Date();
      const end = new Date();
      addDays(end, 1);
      picker.$emit("pick", [start, end]);
    }
  }
];

export const crudOptions = (vm) => { // vm即this
  return {
    pageOptions:{
      export: vm.hasPermi("['admin:case:casemaincrud:export:get']")
        && {
        local: true, //本地导出，false为服务端导出
        title: "数据导出", //导出的文件名
        type: "excel", //导出文件类型，可选： [ csv | excel ]
      },
    },
    // options: {
    //   events:{ //el-table事件监听
    //     'sort-change':(event)=>{
    //       // 处理排序回调，直接doSearch会二次请求
    //     }
    //   },
    //   fetchDetail(index,row,mode){ return row },// 打开对话框前调用，获取form详情数据
    // },
    selectionRow: {
      align: 'center',
      width: 40
    },
    rowHandle:
      // 无权限则隐藏，需要将下文的权限进行汇总
      vm.hasPermi("['admin:case:casemaincrud:{id}:get','admin:case:casemaincrud:{id}:post','admin:case:casemaincrud:{id}:delete']")
      && {
      width: 250,
      // width: 270,
      // dropdown: {
      //   atLeast: 3, // 至少2个以上才收入下拉框中
      //   text: "更多"
      // },
      show: false,
      view: {
        size: "small",
        disabled: () => {
          return !vm.hasPermi("['admin:case:casemaincrud:{id}:get']");
        }
      },
      edit: {
        show: "small",
        disabled: () => {
          return !vm.hasPermi("['admin:case:casemaincrud:{id}:post']");
        }
      },
      remove: {
        show: "small",
        disabled: () => {
          return !vm.hasPermi("['admin:case:casemaincrud:{id}:delete']");
        }
      }
    },
    columns: [
      {
        title: "ID",
        key: "id",
        width: 70,
        form: {
          disabled: true
        }
      },
      {
        title: "任务名称",
        key: "name",
        sortable: "custom",
        form: {
          rules: [{ required: true, message: "请填写任务名称" }],
        }
      },
      {
        title: "关联角色",
        key: "role_name",
        type: "text", // 字段类型为选择框
        form: {
          disabled: true
        }
      },
      {
        title: "关联角色",
        key: "case_role",
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "D2pSearchSelectPagination", // 支持任何v-model组件
            events: {
              "input": (e) => {
                // 自定义事件，会覆盖原监听取值，用于自动触发搜索
                const value = e.component.copyValue;
                const f = _.cloneDeep(vm.getSearch().form);
                f.case_role = _.isArray(value)?_.join(value, ","):value;
                vm.doSearch(f);
              }
            },
            props: { // 配置自定义组件的属性
              url: "/admin/case/caserole/",
              multiple: false,
              labelName: "role_name",
              labelValue: "id"
            }
          },
          order: 1 // 查询字段排序，数字越小越靠前
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: {
          rules: [{ required: true, message: "请选择关联角色" }],
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            name: "D2pSearchSelectPagination",
            props: { // 配置自定义组件的属性
              url: "/admin/case/caserole/",
              multiple: false,
              labelName: "role_name",
              selectStyle: { width: "100%" },
              labelValue: "id"
            }
          }
        },
        disabled: true,
        view: {
          disabled: true
        }
      },
      {
        title: "执行计划",
        key: "plan"
      },
      {
        title: "员工类型",
        key: "employee_choice",
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select" // 支持任何v-model组件
          },
          order: 2 // 查询字段排序，数字越小越靠前
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: {
          rules: [{ required: true, message: "请选择员工类型" }],
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            props: { // 配置自定义组件的属性
              filterable: true, // 可过滤选择项
              clearable: true // 可清除
            }
          }
        },
        dict: { // 数据字典配置
          url: "/admin/system/dict/get/type/case_employee_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "城市",
        key: "multi_cities",
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select", // 支持任何v-model组件
            props: {
              multiple: true
            }
          },
          order: 3 // 查询字段排序，数字越小越靠前
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: {
          rules: [{ required: true, message: "请选择城市" }],
          valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            // 将多选数组转化为字符串列表，用于后端存储
            if (_.isArray(value)) {
              form[key] = _.join(form[key], ",") || null;
            }
          },
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            name: "dict-select",
            props: { // 配置自定义组件的属性
              filterable: true, // 可过滤选择项
              multiple: true, // 支持多选
              clearable: true // 可清除
            }
          }
        },
        valueBuilder(row, key) {
          // 解决多选显示异常
          row.multi_cities = row.multi_cities || null;
        },
        valueResolve(row, key) {
          // 适配多选搜索方式
          if (_.isArray(row.multi_cities)) {
            row.multi_cities = _.join(row.multi_cities, ",") || null;
          }
        },
        dict: { // 数据字典配置
          url: "/admin/system/dict/get/type/case_cities/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "状态",
        key: "status",
        search: {
          disabled: false,
          order: 6
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: { // 配置添加和编辑，根据form的配置自动生成addTemplate和editTemplate
          rules: [// 【可选】添加和修改时的校验规则，不配置则不校验
            { required: true, message: "请选择状态" }
          ]
        },
        valueBuilder(row, key) {
          row.status = row.status.toString();
        },
        dict: { // 数据字典配置
          url: "/admin/system/dict/get/type/case_status/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "新建日期范围",
        key: "create_datetime__range",
        type: "daterange", // 字段类型为时间选择器datepicker,根据类型可自动生成默认配置
        form: { // form表单的配置
          disabled: true // 禁止添加输入与修改输入【可选】默认false
        },
        disabled: true,
        view: {
          disabled: true
        },
        valueResolve(row, key) {
          if (_.isArray(row.create_datetime__range) && row.create_datetime__range.length === 2) {
            addDataRange(row, { "create_datetime__range": [parseTime(row.create_datetime__range[0], "{y}-{m}-{d}"), parseTime(row.create_datetime__range[1], "{y}-{m}-{d}")] });
          }
        },
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: {
            props: {
              "picker-options": { shortcuts: shortcuts }
            }
          },
          order: 4 // 查询字段排序，数字越小越靠前
        } // 启用查询
      },
      {
        title: "更新日期范围",
        key: "update_datetime__range",
        type: "daterange", // 字段类型为时间选择器datepicker,根据类型可自动生成默认配置
        form: { // form表单的配置
          disabled: true // 禁止添加输入与修改输入【可选】默认false
        },
        disabled: true,
        view: {
          disabled: true
        },
        valueResolve(row, key) {
          if (_.isArray(row.update_datetime__range) && row.update_datetime__range.length === 2) {
            addDataRange(row, { "update_datetime__range": [parseTime(row.update_datetime__range[0], "{y}-{m}-{d}"), parseTime(row.update_datetime__range[1], "{y}-{m}-{d}")] });
          }
        },
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: {
            props: {
              "picker-options": { shortcuts: shortcuts }
            }
          },
          order: 5 // 查询字段排序，数字越小越靠前
        } // 启用查询
      },
      {
        title: "新建日期",
        key: "create_datetime",
        sortable: "custom",
        type: "date", // 字段类型为时间选择器datepicker,根据类型可自动生成默认配置
        form: { // form表单的配置
          addDisabled: true // 是否仅在添加编辑框中关闭该字段
        }
      },
      {
        title: "备注",
        key: "description",
        type: "text-area",
        form: { // form表单的配置
          component: {
            props: { // 配置自定义组件的属性
              rows: 4
            }
          }
        }
      },
      {
        title: "附件",
        key: "attachments",
        view: {
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            name: "D2pAttachmentsDetail",
            span: 24 // 显示宽度，12表示一半，24表示整行
          }
        },
        form: {
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            name: "D2pFileUpload",
            span: 24, // 显示宽度，12表示一半，24表示整行
            props: { // 配置自定义组件的属性
              fileType: ["ALL"],
              autoUpload: true,
              showFileList: false,
              multiple: true,
              limit: 3,
              fileSize: 10
            }
          }
        },
        valueResolve(row, key) {
          // form内容变动，提交时会触发，将附件数组转化为提交需要的字符串格式
          if (_.isArray(row.attachments)) {
            row.attachments = _.join(row.attachments.map(a => a.id), ",");
          }
        },
        disabled: true
      }
    ]
  };
};
