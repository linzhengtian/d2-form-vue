<template>
  <crud-container :class="{'page-compact':crud.pageOptions.compact}" :style="{ height: height }">
    <template slot="header">测试页面</template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
    >
      <!-- 自动绑定参数与事件 -->
      <!-- 包含详细参数见：https://gitee.com/greper/d2-crud-plus/blob/master/packages/d2-crud-plus/src/lib/mixins/crud.js#L164-->
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch" />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow" v-hasPermi="['admin:case:casemaincrud:post']"><i class="el-icon-plus" /> 新增</el-button>
          <el-button size="small" type="danger" @click="batchDelete" v-hasPermi="['admin:case:casemaincrud:{id}:delete']"><i class="el-icon-delete"></i> 批量删除</el-button>
          <!--<el-button size="small" type="primary" @click="customHandle"><i class="el-icon-s-shop"></i> 自定义按钮</el-button>-->
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
  </crud-container>
</template>

<script>
import { crudOptions } from "./crud"; // 上文的crudOptions配置
import { d2CrudPlus } from "d2-crud-plus";
import { listData, delData, addData, updateData } from "@/api/modules/case/casemain";
import { getFileList } from "@/api/vadmin/system/savefile";
import _ from "lodash";

export default {
  name: "CaseMainCrud",
  components: {
  },
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  computed: {
    height() {
      return this.$store.state.winSize.winheight - 100 + "px !important";
    }
  },
  methods: {
    getCrudOptions() { return crudOptions(this); },
    pageRequest(query) {
      // 数据请求
      const { orderProp, orderAsc } = query;
      if( !_.isEmpty(orderProp) ){
        query.ordering = (orderAsc ? "" : "-" ) + orderProp;
      }
      return listData(query);
    },
    addRequest(row) { return addData(row); }, // 添加请求
    updateRequest(row) { return updateData(row); }, // 修改请求
    delRequest(row) { return delData(row.id); }, // 删除请求
    doServerExport (context) {
      // 默认导出方法
      const table = this.getD2CrudTable();
      if(!_.isEmpty(table.selection)){
        this.$message("导出ID为"+_.join(table.selection.map(v=>v.id), ",")+"的数据");
      } else {
        this.$message("导出检索的所有数据");
      }
    },
    async batchDelRequest (ids) {
      // 批量删除
      for (const i of ids){
        await delData(i);
      }
      this.doLoad();
    },
    // handleCurrentChange (currentRow, oldCurrentRow) {
    //   // 单选某行调用
    //   this.$message('单选' + currentRow.id)
    // },
    // customHandle (){
    //   // 自定义操作
    //   this.getD2CrudTable().toggleRowSelection(this.getD2CrudTableData()[0]); // 选择第一行
    //   this.getD2Crud().$refs.elTable.toggleRowSelection(this.getD2Crud().d2CrudData[1]); // 选择第二行
    // },
    doDialogOpened(context) {
      // 组件插入除value外其余参数
      if (context.mode === "edit") {
        this.$set(this.getEditFormTemplate("case_role").component.props, "label", context.row.role_name);
        if (context.form.attachments) {
          getFileList(context.form.attachments).then(response => {
            const files = response.data.results;
            files.forEach(f => {
              f.percentage = 100;
              f.status = "success";
              f.file_url = "/" + _.trimStart(f.file_url, "/");
            });
            context.form.attachments = files;
          });
        }
      }
    }
  }
};
</script>

<style scoped>

</style>
