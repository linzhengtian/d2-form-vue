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
    pageOptions: {

    },
    selectionRow: {
      align: 'center',
      width: 40
    },
    rowHandle:
      // 无权限则隐藏，需要将下文的权限进行汇总
      vm.hasPermi("['admin:qform:myform:{id}:put','admin:qform:myform:{id}:delete']")
      && {
      width: 320,
      view: {
        size: "small",
        order: 1
      },
      edit: {
        show: false
      },
      remove: {
        size: "small",
        order: 4,
        disabled: () => {
          return !vm.hasPermi("['admin:qform:myform:{id}:delete']");
        }
      },
      custom: [
        {
          text: "设计",
          type: "info",
          size: "small",
          icon: 'el-icon-edit',
          emit: "edit-click",
          order: 2,
          show: (index, ele) => {
            return vm.hasPermi("['admin:qform:myform:{id}:put']") && ele.design_permission === "1";
          }
        },
        {
          text: "表单",
          type: "info",
          size: "small",
          icon: 'el-icon-tickets',
          order: 3,
          emit: "statistics-click"
        },
      ]
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
        title: "表单名称",
        key: "name",
        sortable: "custom",
        search: {
          order: 1
        },
        form: {
          rules: [{ required: true, message: "请填写表单名称" }],
        }
      },
      {
        title: "表单描述",
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
        title: "发布状态",
        key: "publish_choice",
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select", // 支持任何v-model组件
            props: {
              multiple: true
            }
          },
          order: 2 // 查询字段排序，数字越小越靠前
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: {
          disabled: true
        },
        valueBuilder(row, key) {
          // 解决多选显示异常
          row.publish_choice = row.publish_choice || null;
        },
        valueResolve(row, key) {
          // 适配多选搜索方式
          if (_.isArray(row.publish_choice)) {
            row.publish_choice = _.join(row.publish_choice, ",") || null;
          }
        },
        dict: { // 数据字典配置
          url: "/admin/system/dict/get/type/publish_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "是否问卷模式",
        key: "questionnaire_choice",
        type: "select", // 字段类型为选择框
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select" // 支持任何v-model组件
          },
          order: 3 // 查询字段排序，数字越小越靠前
        },
        form: {
          rules: [{ required: true, message: "请选择" }],
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            props: { // 配置自定义组件的属性
              filterable: true, // 可过滤选择项
              clearable: true // 可清除
            }
          }
        },
        dict: { // 数据字典配置
          url: "/admin/system/dict/get/type/questionnaire_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
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
          width: 260,
          component: {
            props: {
              "picker-options": { shortcuts: shortcuts }
            }
          },
          order: 4 // 查询字段排序，数字越小越靠前
        } // 启用查询
      },
      {
        title: "更新日期",
        key: "update_datetime",
        sortable: "custom",
        type: "date", // 字段类型为时间选择器datepicker,根据类型可自动生成默认配置
        form: { // form表单的配置
          addDisabled: true // 是否仅在添加编辑框中关闭该字段
        }
      },
    ]
  };
};
