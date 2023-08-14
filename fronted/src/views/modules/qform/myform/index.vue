<template>
  <crud-container :class="{'page-compact':crud.pageOptions.compact}" :style="{ height: height }">
    <template slot="header">我的表单</template>
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @edit-click="editTo"
      @statistics-click="statisticsClick"
    >
      <!-- 自动绑定参数与事件 -->
      <!-- 包含详细参数见：https://gitee.com/greper/d2-crud-plus/blob/master/packages/d2-crud-plus/src/lib/mixins/crud.js#L164-->
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch" />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow" v-hasPermi="['admin:qform:myform:post']"><i class="el-icon-plus" /> 新增</el-button>
          <el-button size="small" type="primary" @click="copyRow" v-hasPermi="['admin:qform:myform:post']"><i class="el-icon-postcard" /> 复制</el-button>
          <!--<el-button size="small" type="danger" @click="batchDelete" v-hasPermi="['admin:case:casemaincrud:{id}:delete']"><i class="el-icon-delete"></i> 批量删除</el-button>-->
          <!--<el-button size="small" type="primary" @click="customHandle"><i class="el-icon-s-shop"></i> 自定义按钮</el-button>-->
        </el-button-group>
        <!-- 列设置存在bug -->
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" :columns="undefined"/>
      </div>
    </d2-crud-x>
    <!-- 表单复制dialog-->
    <formCopy
      v-if="openModal"
      dialog-title="复制表单"
      modal-width="900px"
      :open-modal="openModal"
      :formId="copyFormId"
      @closeFormDialog="closeFormDialog"
    />
  </crud-container>
</template>

<script>
import { crudOptions } from "./crud"; // 上文的crudOptions配置
import { d2CrudPlus } from "d2-crud-plus";
import { listData, getData, delData, addData, updateData } from "@/api/modules/qform/myform";
import { getFileList } from "@/api/vadmin/system/savefile";
import _ from "lodash";
import formCopy from "./formCopy";

export default {
  name: "MyFormCrud",
  data() {
    return {
      openModal: false,
      copyFormId: ""
    };
  },
  components: {
    formCopy
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
      if(!_.isEmpty(orderProp)){
        query.ordering = (orderAsc ? "" : "-") + orderProp;
      }
      return listData(query);
    },
    addRequest(row) {
      return addData(row).then(res => {
        this.$router.push({
          path: "/qform/formEdit/",
          query: {
            formId: res.data.id,
            activeTab: "editor"
          }
        });
      });
    }, // 添加请求
    // updateRequest(row) { return updateData(row); }, // 修改请求
    delRequest(row) { return delData(row.id); }, // 删除请求
    addAfter(row) {
      // 避免新增成功后重复搜索，因为重新激活页面后会进行搜索
      // this.doAfterRowChange(row);
    },
    copyRow() {
      const table = this.getD2CrudTable();
      if (_.isEmpty(table.selection)) {
        this.$message.error("请选择条目");
      } else if (table.selection.length === 1) {
        this.openModal = true;
        this.copyFormId = table.selection[0].id;
      } else {
        this.$message.error("只能选择一条");
      }
    },
    // 关闭数据弹窗
    closeFormDialog(val) {
      this.openModal = val;
      this.doLoad();
    },
    async batchDelRequest(ids) {
      // 批量删除
      for (const i of ids) {
        await delData(i);
      }
      this.doLoad();
    },
    editTo(context) {
      this.$router.push({
        path: "/qform/formEdit/",
        query: {
          formId: context.row.id,
          activeTab: (context.row.publish_choice === "1" && context.row.questionnaire_choice === "1") ? "publish" : "editor",
        }
      });
    },
    statisticsClick(context) {
      if (!context.row.form_info) {
        this.editTo(context);
      } else {
        this.$router.push({
          path: "/qform/formEdit/",
          query: {
            formId: context.row.id,
            activeTab: "datas",
          }
        });
      }
    },
    doDialogOpened(context) {
      // 组件插入除value外其余参数
      if (context.mode === "edit") {
        // this.$set(this.getEditFormTemplate("XXX").component.props, "label", context.row.XXX);
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
