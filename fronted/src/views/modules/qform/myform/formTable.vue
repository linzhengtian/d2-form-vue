<template>
  <div>
    <el-form ref="queryForm" :model="queryParams" :inline="true">
      <template v-if="templateDatas.scheme" >
        <template v-for="item in initialData">
          <template v-if="['input', 'textarea', 'number', 'rate', 'slider'].includes(item.type) && item.isTable">
            <el-form-item :label="item.label">
              <el-input
                v-model="searchFilter[item.model]"
                placeholder="请输入"
                clearable
                size="small"
                style="width: 240px"
                @input="forceUpdate"
              />
            </el-form-item>
          </template>
          <template v-else-if="['select', 'radio', 'checkbox'].includes(item.type) && item.isTable">
            <el-form-item :label="item.label">
              <el-select
                v-model="searchFilter[item.model]"
                placeholder="请选择"
                :multiple="true"
                clearable
                size="small"
                style="width: 240px"
                @input="forceUpdate"
              >
                <el-option
                  v-for="dict in item.options.options"
                  :key="dict.value"
                  :label="dict.label"
                  :value="dict.value"
                />
              </el-select>
            </el-form-item>
          </template>
          <template v-else-if="['datePicker', 'date'].includes(item.type) && item.isTable">
            <el-form-item :label="item.label">
              <el-date-picker
                v-model="searchFilter[item.model]"
                size="small"
                style="width: 240px"
                value-format="yyyy-MM-dd"
                type="daterange"
                range-separator="-"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @input="forceUpdate"
              />
            </el-form-item>
          </template>
          <template v-else-if="['cascader'].includes(item.type) && item.isTable">
            <el-form-item :label="item.label">
              <el-cascader
                v-model="searchFilter[item.model]"
                :options="item.options.options"
                :props="{ expandTrigger: 'hover' }"
                @input="forceUpdate">
              </el-cascader>
            </el-form-item>
          </template>
        </template>
      </template>
      <el-form-item label="最新提交时间" label-width="100px">
        <el-date-picker
          v-model="updateDatetimeRange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetSort">清空排序</el-button>
      </el-form-item>
    </el-form>
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5" v-if="formInfo.publish_choice ==='1' && (formInfo.create_permission === '1' || formInfo.questionnaire_choice === '1' || formInfo.designpermission === '1')">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5" v-if="formInfo.modify_permission === '1' || formInfo.designpermission === '1'">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5" v-if="formInfo.delete_permission === '1' || formInfo.designpermission === '1'">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete(null)"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-dropdown>
          <el-button type="warning" size="mini">
            导出<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="handleExport"><i class="el-icon-download" />导出所有信息</el-dropdown-item>
            <el-dropdown-item @click.native="handleSelectedExport"><i class="el-icon-download" />导出勾选信息</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-col>
    </el-row>
    <el-row>
      <vxe-table
        border
        show-overflow
        :loading="loading"
        :column-config="{resizable: true}"
        :data="dataList"
        remote-sort
        ref="vxTable"
        @sort-change="sortChanged"
        @checkbox-change="handleSelectionChange"
        @checkbox-all="handleSelectionChange"
      >
        <vxe-column type="checkbox" width="60"></vxe-column>
        <vxe-column field="id" title="序号" width="60"></vxe-column>
        <vxe-column field="update_datetime" title="最新提交时间" sortable></vxe-column>
        <vxe-column v-for="item in headerTeamList" :field="item.key" :key="item.key" :title="item.label" sortable>
          <template slot-scope="scope">
            <template v-if="item.type === 'uploadImg'">
              <template v-for="file in scope.row.fill_data[item.key]">
                <el-button size="mini" @click="downloadFile(file, true)" class="mini-size-download-button">
                  <i class="el-icon-download" />
                </el-button>&nbsp&nbsp
              </template>
            </template>
            <template v-else-if="item.type === 'uploadFile'">
              <template v-for="file in scope.row.fill_data[item.key]">
                <el-button size="mini" @click="downloadFile(file, false)" class="mini-size-download-button">
                  <i class="el-icon-download" />
                </el-button>&nbsp&nbsp
              </template>
            </template>
            <template v-else>
              {{ scope.row[item.key] }}
            </template>
          </template>
        </vxe-column>
        <vxe-column field="handle" title="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="text"
              icon="el-icon-edit"
              @click="handleUpdate(scope.row.id)"
              v-if="formInfo.modify_permission === '1' || formInfo.designpermission === '1' || scope.row.creator_name === currentUserName"
            >修改</el-button>
            <el-button
              size="mini"
              type="text"
              icon="el-icon-edit"
              @click="handleView(scope.row.id)"
            >查看</el-button>
            <el-button
              size="mini"
              type="text"
              icon="el-icon-delete"
              @click="handleDelete(scope.row.id)"
              v-if="formInfo.delete_permission === '1' || formInfo.designpermission === '1' || scope.row.creator_name === currentUserName"
            >删除</el-button>
          </template>
        </vxe-column>
      </vxe-table>
      <vxe-pager
        border
        icon-prev-page="vxe-icon-arrow-left"
        icon-jump-prev="vxe-icon-arrow-double-left"
        icon-jump-next="vxe-icon-arrow-double-right"
        icon-next-page="vxe-icon-arrow-right"
        icon-jump-more="vxe-icon-ellipsis-h"
        :loading="loading"
        :current-page="queryParams.pageNum"
        :page-size="queryParams.pageSize"
        :total="total"
        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
        @page-change="handlePageChange"
      >
      </vxe-pager>
    </el-row>
    <!-- 表单类dialog-->
    <formDataDetail
      v-if="openModal"
      :dialog-title="dialogTitle"
      modal-width="900px"
      :open-modal="openModal"
      :formId="formId"
      :dataId="dataId"
      :handleType="handleType"
      @closeFormDialog="closeFormDialog"
    />
  </div>
</template>

<script>
import {
  listFormData,
  delFormData,
  exportFormData
} from "@/api/modules/qform/myform";
import _ from "lodash";
import formDataDetail from "./formDataDetail";
import { downloadAuth } from "@/utils/ruoyi";

export default {
  name: "FormTable",
  components: {
    formDataDetail
  },
  props: {
    formInfo: {
      type: Object, default: () => {}
    },
    templateDatas: {
      type: Object, default: () => {
        scheme: { }
      }
    }
  },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        ordering: ""
      },
      searchFilter: {},
      updateDatetimeRange: [],
      // 总条数
      total: 0,
      // 排序
      ordering: "",
      dataList: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 表单头
      headerTeamList: [],
      // 附件表头
      attachHeaderList: [],
      // 查询结果初始化
      initialData: [],
      // 列表展示内容
      arrayTypes: ["address", "checkbox", "select", "state", "cascader", "radio"],
      dialogTitle: "",
      openModal: false,
      formId: "",
      handleType: "create",
      dataId: "",
      isArray: _.isArray,
      baseUrl: process.env.VUE_APP_BASE_API
    };
  },
  computed: {
    currentUserName() {
      return this.$store.getters.name;
    }
  },
  watch: {
    "formInfo.form_info"(val) {
      if (val !== undefined && val !== null) {
        this.reset();
      } else {
        this.initialData = [];
        this.headerTeamList = [];
        this.attachHeaderList = [];
      }
    }
  },
  mounted() {
    this.reset();
  },
  methods: {
    reset() {
      this.initialData = [];
      this.headerTeamList = [];
      this.attachHeaderList = [];
      this.handleTemplateDatas(this.templateDatas.scheme);
      this.initialData.forEach(v => {
        this.searchFilter[v["model"]] = "";
      });
      this.handleHeader(this.initialData);
      this.resetQuery();
    },
    handleTemplateDatas(scheme) {
      if (this.isArray(scheme)) {
        scheme.forEach(s => this.handleTemplateDatas(s));
      } else if (Object.hasOwnProperty.call(scheme, "tds")) {
        scheme.tds.forEach(s => this.handleTemplateDatas(s));
      } else {
        scheme.list.forEach(d => {
          if (d.type === "control") {

          } else if (d.type === "grid") {
            this.handleTemplateDatas(d.columns);
          } else if (d.type === "table") {
            this.handleTemplateDatas(d.trs);
          } else {
            this.initialData.push(d);
          }
        });
      }
    },

    handleHeader(scheme) {
      scheme.filter(v => v.isTable).forEach(l => {
        if (["uploadImg", "uploadFile"].includes(l.type)) {
          this.attachHeaderList.push({ label: l.label, key: l.model, type: l.type });
        }
        this.headerTeamList.push({ label: l.label, key: l.model, type: l.type });
      });
    },
    /** 处理查询条件 -改 */
    handleQueryParams() {
      const search = this.addDateRange(this.queryParams, this.updateDatetimeRange);
      search.searchFilter = JSON.stringify(this.searchFilter);
      search.source_form_id = this.formInfo.id;
      search.ordering = this.ordering;
      return search;
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.updateDatetimeRange = [];
      this.searchFilter = {};
      this.resetSort();
    },
    /** 查询列表 */
    getList() {
      this.loading = true;
      listFormData(this.handleQueryParams()).then(response => {
        this.dataList = response.data.results;
        this.handleSchemeData();
        this.total = response.data.count;
        this.loading = false;
        this.single = true;
        this.multiple = true;
      });
    },
    // 处理分页
    handlePageChange({ currentPage, pageSize }) {
      this.queryParams.pageNum = currentPage;
      this.queryParams.pageSize = pageSize;
      this.getList();
    },
    handleSchemeData() {
      this.dataList.forEach(data => {
        // 选择框
        this.initialData.forEach(v => {
          if (this.arrayTypes.includes(v["type"])) {
            data[v["model"]] = data.fill_data[v["model"] + "_label"];
          } else {
            data[v["model"]] = data.fill_data[v["model"]];
          }
        });
      });
    },
    // 清空排序
    resetSort() {
      this.$refs.vxTable.clearSort();
      this.ordering = "";
      this.getList();
    },
    // 排序
    sortChanged({ column, prop, order }) {
      this.ordering = order ? ((order === "descending" ? "-" : "") + prop) : "";
      this.getList();
    },
    // 新增
    handleAdd() {
      this.openModal = true;
      this.dialogTitle = "添加";
      this.handleType = "create";
      this.formId = this.formInfo.id;
      this.dataId = "";
    },
    // 修改
    handleUpdate(rowId) {
      const checkRow = this.$refs.vxTable.getCheckboxRecords();
      if (checkRow.length == 1) {
        rowId = checkRow[0].id;
      }
      this.openModal = true;
      this.dialogTitle = "编辑";
      this.formId = this.formInfo.id;
      this.handleType = "edit";
      this.dataId = rowId;
    },
    handleView(rowId) {
      this.openModal = true;
      this.dialogTitle = "详情";
      this.formId = this.formInfo.id;
      this.handleType = "detail";
      this.dataId = rowId;
    },
    // 多选框选中数据
    handleSelectionChange() {
      const selection = this.$refs.vxTable.getCheckboxRecords();
      this.ids = selection.map(item => item.id);
      this.single = selection.length !== 1;
      this.multiple = !selection.length;
    },
    // 删除
    handleDelete(rowId) {
      const ids = rowId || this.ids.join(",");
      this.$confirm('是否确认删除编号为"' + ids + '"的数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return delFormData(ids);
      }).then(() => {
        this.getList();
        this.msgSuccess("删除成功");
      });
    },
    // 导出
    async handleSelectedExport() {
      if (_.isEmpty(this.ids)) {
        this.$message.error("请勾选数据行");
      } else {
        // window.location.href = process.env.VUE_APP_BASE_API + "/admin/qform/formdata/export/?id=" + _.join(this.ids, "%2C");
        await exportFormData({
          source_form_id: this.formInfo.id,
          ids: _.join(this.ids, ",")
        });
      }
    },
    async handleExport() {
      const search = this.addDateRange({}, this.updateDatetimeRange);
      search.searchFilter = JSON.stringify(this.searchFilter);
      search.source_form_id = this.formInfo.id;
      await exportFormData(search);
    },
    forceUpdate() {
      this.$forceUpdate();
    },
    // 关闭数据弹窗
    closeFormDialog(val) {
      this.openModal = val;
      this.getList();
    },
    // 下载文件
    downloadFile(file, directDownload) {
      if (directDownload) {
        window.open(file.url || (this.baseUrl + file.file_url));
      } else {
        downloadAuth("/admin/system/savefile/download_file/?id=" + file.id, file.name)
      }
    }
  }
};
</script>

<style lang="scss" scoped>
  ::v-deep .mini-size-download-button {
    padding: 8px 8px !important;
  }

</style>
