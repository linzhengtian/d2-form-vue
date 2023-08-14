<template>
  <crud-container :class="{'page-compact':crud.pageOptions.compact}" :style="{ height: height + 'px', 'width': '800px' }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
    >
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch" />
        <el-button-group v-if="!onlyView">
          <el-button size="small" type="primary" @click="addRow" v-hasPermi="['admin:qform:myform:post']"><i class="el-icon-plus" /> 新增</el-button>
          <el-button size="small" type="danger" @click="batchDelete" v-hasPermi="['admin:qform:myform:{id}:delete']"><i class="el-icon-delete"></i> 批量删除</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" :columns="undefined"/>
      </div>
    </d2-crud-x>
  </crud-container>
</template>

<script>
import { crudOptions } from "./userCrud"; // 上文的crudOptions配置
import { d2CrudPlus } from "d2-crud-plus";
import { listUserPermissions, addUserPermissions, updateUserPermissions, delUserPermissions } from "@/api/modules/qform/myform";
import _ from "lodash";

export default {
  name: "formUser",
  props: {
    formId: {
      type: [String, Number]
    },
    height: {
      type: [String, Number]
    },
    onlyView: {
      type: Boolean,
      default: false
    }
  },
  components: {
  },
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  methods: {
    getCrudOptions() { return crudOptions(this); },
    pageRequest(query) {
      query.form_info = this.formId;
      return listUserPermissions(query);
    },
    addRequest(row) {
      row.form_info = this.formId;
      return addUserPermissions(row);
    }, // 添加请求
    updateRequest(row) { return updateUserPermissions(row); }, // 修改请求
    delRequest(row) { return delUserPermissions(row.id); }, // 删除请求
    async batchDelRequest(ids) {
      // 批量删除
      for (const i of ids) {
        await delUserPermissions(i);
      }
      this.doLoad();
    },
    doDialogOpened(context) {
      // 组件插入除value外其余参数
      if (context.mode === "edit") {
        this.$set(this.getEditFormTemplate("form_user").component.props, "label", context.row.name);
      }
    }
  }
};
</script>

<style scoped>

</style>
