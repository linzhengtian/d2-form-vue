import _ from "lodash";


export const crudOptions = (vm) => { // vm即this
  return {
    selectionRow: {
      align: 'center',
      width: 40
    },
    rowHandle:
      // 无权限则隐藏，需要将下文的权限进行汇总
      vm.hasPermi("['admin:qform:myform:{id}:put','admin:qform:myform:{id}:delete']")
      && {
      width: 240,
      view: {
        size: "mini",
      },
      edit: {
        size: "mini",
        show: () => {
          return vm.hasPermi("['admin:qform:myform:{id}:put']") && !vm.onlyView;
        }
      },
      remove: {
        size: "mini",
        show: () => {
          return vm.hasPermi("['admin:qform:myform:{id}:delete']") && !vm.onlyView;
        }
      },
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
        title: "关联表单",
        key: "form_info",
        type: "text", // 字段类型为选择框
        disabled: true,
        form: {
          disabled: true
        },
        view: {
          disabled: true
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
        key: "form_role",
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "D2pSearchSelectPagination", // 支持任何v-model组件
            events: {
              "input": (e) => {
                // 自定义事件，会覆盖原监听取值，用于自动触发搜索
                const value = e.component.copyValue;
                const f = _.cloneDeep(vm.getSearch().form);
                f.form_role = _.isArray(value)?_.join(value, ","):value;
                vm.doSearch(f);
              }
            },
            props: { // 配置自定义组件的属性
              url: "/admin/qform/formrole/",
              multiple: false,
              labelName: "roleName",
              placeholder: "请输入",
              labelValue: "id"
            }
          },
          order: 1 // 查询字段排序，数字越小越靠前
        }, // 启用查询
        type: "select", // 字段类型为选择框
        form: {
          rules: [{ required: true, message: "请选择" }],
          component: { // 添加和修改时form表单的组件，支持任何v-model组件
            name: "D2pSearchSelectPagination",
            props: { // 配置自定义组件的属性
              url: "/admin/qform/formrole/",
              multiple: false,
              labelName: "roleName",
              placeholder: "请输入",
              selectStyle: { width: "100%" },
              labelValue: "id"
            }
          }
        },
        disabled: true,
        view: {
          disabled: true
        },
        editForm: {
          component: {
            disabled: true
          }
        }
      },
      {
        title: "是否有新增权限",
        key: "create_permission",
        type: "select", // 字段类型为选择框
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select" // 支持任何v-model组件
          },
          order: 2 // 查询字段排序，数字越小越靠前
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
          url: "/admin/system/dict/get/type/permission_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "是否有修改权限",
        key: "modify_permission",
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
          url: "/admin/system/dict/get/type/permission_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
      {
        title: "是否有删除权限",
        key: "delete_permission",
        type: "select", // 字段类型为选择框
        search: {
          disabled: false, // 是否禁用该字段的查询，默认false
          component: { // 查询框组件配置，默认根据form配置生成
            name: "dict-select" // 支持任何v-model组件
          },
          order: 4 // 查询字段排序，数字越小越靠前
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
          url: "/admin/system/dict/get/type/permission_choice/?status=1", // 远程获取数据字典
          label: "dictLabel",
          value: "dictValue"
        }
      },
    ]
  };
};
