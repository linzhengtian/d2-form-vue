<template>
  <div class="app-container">
    <el-form v-show="showSearch" ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="任务名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入任务名称"
          clearable
          size="small"
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="城市" prop="multi_cities">
        <el-select
          v-model="queryParams.multi_cities"
          placeholder="请选择"
          :multiple="true"
          clearable
          size="small"
          style="width: 240px"
        >
          <el-option
            v-for="dict in multiCitiesOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select
          v-model="queryParams.status"
          placeholder="请选择"
          clearable
          size="small"
          style="width: 240px"
        >
          <el-option
            v-for="dict in statusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="dateRange"
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
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['admin:case:casemain:post']"
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['admin:case:casemain:{id}:post']"
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['admin:case:casemain:{id}:delete']"
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['admin:case:casemain:export:get']"
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
        >导出</el-button>
      </el-col>
      <right-toolbar :show-search.sync="showSearch" @queryTable="getList" />
    </el-row>

    <el-table ref="dataTable" v-loading="loading" :data="dataList" @selection-change="handleSelectionChange" @sort-change="sortChanged">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="编号" align="center" prop="id" width="100" sortable="custom" />
      <el-table-column label="任务名称" align="center" prop="name" :show-overflow-tooltip="true" sortable="custom">
        <template slot-scope="scope">
          <a v-if="hasPermi(['admin:case:casemain:{id}:get'])" href="javascript:void(0);" @click="handleView(scope.row);" style="text-decoration: underline; color: #1890ff;">{{ scope.row.name }}</a>
          <span v-else>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="执行计划" align="center" prop="plan" :show-overflow-tooltip="true" />
      <el-table-column label="员工类型" align="center" prop="employee_choice" :formatter="employeeChoiceFormat" />
      <el-table-column label="城市" align="center" prop="multi_cities" :formatter="multiCitiesFormat" />
      <el-table-column label="状态" align="center" prop="status" :formatter="statusFormat" />
      <el-table-column label="备注" align="center" prop="description" :show-overflow-tooltip="true" />
      <el-table-column label="创建时间" align="center" prop="create_datetime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        v-if="hasPermi(['admin:case:casemain:{id}:post','admin:case:casemain:{id}:delete'])"
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="scope">
          <el-button
            v-hasPermi="['admin:case:casemain:{id}:post']"
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
          >修改</el-button>
          <el-button
            v-hasPermi="['admin:case:casemain:{id}:delete']"
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="填写任务名称" />
        </el-form-item>
        <el-form-item label="执行计划" prop="plan">
          <el-input v-model="form.plan" placeholder="填写执行计划" />
        </el-form-item>
        <el-form-item label="关联角色" prop="case_role">
          <SearchSelectPagination
            v-model="form.case_role"
            :label="form.role_name"
            labelName="role_name"
            labelValue="id"
            :multiple="false"
            url="/admin/case/caserole/"
            style="width: 100%;"
          >
          </SearchSelectPagination>
        </el-form-item>
        <el-form-item label="员工类型" prop="employee_choice">
          <el-radio-group v-model="form.employee_choice">
            <el-radio
              v-for="dict in employeeChoiceOptions"
              :key="dict.dictValue"
              :label="dict.dictValue"
            >{{ dict.dictLabel }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="城市" prop="multi_cities">
          <el-select
            v-model="form.multi_cities"
            placeholder="请选择"
            :multiple="true"
            clearable
            size="small"
            style="width: 100%;"
          >
            <el-option
              v-for="dict in multiCitiesOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="dict in statusOptions"
              :key="dict.dictValue==='true'"
              :label="dict.dictValue==='true'"
            >{{ dict.dictLabel }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="附件" prop="attachments">
          <FileUpload
            v-model="attachments"
            ref="saveFile"
            :file-type="['ALL']"
            :autoUpload="true"
            :showFileList="false"
            :multiple="true"
            :limit="3"
            :fileSize="10"/>
        </el-form-item>
        <el-form-item label="备注" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 表单类详情dialog-->
    <DetailFormModal
      v-if="openDetailModal"
      dialog-title="详情"
      modal-width="700px"
      :open-detail-modal="openDetailModal"
      :form-data="form"
      :form-item="formItem"
      @closeDialog="value=>{openDetailModal=value}"
    />
  </div>
</template>

<script>
import { listData, getData, delData, addData, updateData, exportData } from "@/api/modules/case/casemain";
import { getFileList } from "@/api/vadmin/system/savefile";
import SearchSelectPagination from "@/components/SearchSelectPagination/Index";
import _ from "lodash";
import FileUpload from "@/components/FileUpload/index";
import DetailFormModal from "@/components/Modal/DetailFormModal";
import { downloadAuth } from "@/utils/ruoyi";

const FORM_DETAIL_ITEM = [
  {
    index: 1,
    label: "编号",
    key: "id"
  },
  {
    index: 2,
    label: "任务名称",
    key: "name"
  },
  {
    index: 3,
    label: "关联角色",
    key: "case_role",
    choice: {
      search: {
        url: "/admin/case/caserole/",
        queryName: "id",
        queryValue: "role_name"
      }
    }
  },
  {
    index: 4,
    label: "执行计划",
    key: "plan",
    singleLine: true
    // width: "auto"
  },
  {
    index: 5,
    label: "员工类型",
    key: "employee_choice",
    choice: { dict: "case_employee_choice" }
  },
  {
    index: 6,
    label: "城市",
    key: "multi_cities",
    choice: { dict: "case_cities" }
  },
  {
    index: 7,
    label: "状态",
    key: "status",
    choice: {
      labels: {
        false: "失败",
        true: "正常"
      }
    }
  },
  {
    index: 8,
    label: "备注",
    key: "description",
    singleLine: true
  },
  {
    index: 9,
    label: "执行日期",
    key: "create_datetime",
    choice: "time",
    singleLine: true
  },
  {
    index: 10,
    label: "附件",
    key: "attachments",
    attachment: true,
    singleLine: true
  }
];

export default {
  name: "CaseMain",
  components: {
    SearchSelectPagination,
    FileUpload,
    DetailFormModal
  },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 表格数据
      dataList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 数据字典 -改
      statusOptions: [],
      employeeChoiceOptions: [],
      multiCitiesOptions: [],
      // 日期范围
      dateRange: [],
      // 查询参数 -改
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        name: undefined,
        multi_cities: undefined,
        status: undefined,
        ordering: ""
      },
      // 排序
      ordering: "",
      // 表单参数
      form: {},
      // 附件 -改
      attachments: [],
      // 是否显示详细模态框
      openDetailModal: false,
      formItem: FORM_DETAIL_ITEM,
      // 表单校验 -改
      rules: {
        name: [
          { required: true, message: "任务名称不能为空", trigger: "blur" },
          { max: 256, message: "任务名称不能超过256个字符", trigger: "blur" }
        ],
        plan: [
          { max: 1024, message: "执行计划不能超过1024个字符", trigger: "blur" }
        ],
        case_role: [
          { required: true, message: "关联角色不能为空", trigger: "blur" }
        ],
        employee_choice: [
          { required: true, message: "员工类型不能为空", trigger: "blur" }
        ],
        status: [
          { required: true, message: "运行状态不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
    // 获取数据字典 -改
    this.getDicts("case_status").then(response => {
      this.statusOptions = response.data;
    });
    this.getDicts("case_employee_choice").then(response => {
      this.employeeChoiceOptions = response.data;
    });
    this.getDicts("case_cities").then(response => {
      this.multiCitiesOptions = response.data;
    });
  },
  methods: {
    /** 处理查询条件 -改 */
    handleQueryParams() {
      const search = this.addDateRange(this.queryParams, this.dateRange);
      search.multi_cities = _.join(this.queryParams.multi_cities, ",");
      search.ordering = this.ordering;
      return search;
    },
    /** 查询列表 */
    getList() {
      this.loading = true;
      listData(this.handleQueryParams()).then(response => {
        this.dataList = response.data.results;
        this.total = response.data.count;
        this.loading = false;
      });
    },
    // 数据字典 -改
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 数据字典 -改
    employeeChoiceFormat(row, column) {
      return this.selectDictLabel(this.employeeChoiceOptions, row.employee_choice);
    },
    // 数据字典 -改
    multiCitiesFormat(row, column) {
      return this.selectDictLabels(this.multiCitiesOptions, row.multi_cities, ",");
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置 -改
    reset() {
      this.form = {
        id: undefined,
        name: undefined,
        plan: undefined,
        employee_choice: this.selectDictDefault(this.employeeChoiceOptions),
        multi_cities: undefined,
        case_role: undefined,
        status: this.selectDictDefault(this.statusOptions) === "true",
        remark: undefined,
        attachments: ""
      };
      this.resetForm("form");
      this.attachments = [];
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = [];
      this.resetForm("queryForm");
      this.ordering = "";
      this.$refs.dataTable.clearSort();
      this.handleQuery();
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加";
    },
    /** 详细按钮操作 */
    handleView(row) {
      this.openDetailModal = true;
      this.form = row;
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id);
      this.single = selection.length !== 1;
      this.multiple = !selection.length;
    },
    /** 修改按钮操作 -改 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids;
      getData(id).then(response => {
        this.form = response.data;
        this.form.multi_cities = response.data.multi_cities ? response.data.multi_cities.split(",") : [];
        const attachments_ids = this.form.attachments;
        this.title = "修改";
        if (attachments_ids) {
          getFileList(attachments_ids).then(response => {
            const files = response.data.results;
            files.forEach(f => {
              f.percentage = 100;
              f.status = "success";
              f.file_url = "/" + _.trimStart(f.file_url, "/");
            });
            this.attachments = files;
          });
        }
        this.open = true;
      });
    },
    /** 提交按钮 -改 */
    submitForm: function() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          this.form.attachments = this.attachments.map(v => v.id).join(",");
          // 数据二次处理
          const form = _.cloneDeep(this.form);
          form.multi_cities = _.join(this.form.multi_cities, ",");
          if (this.form.id !== undefined) {
            updateData(form).then(response => {
              this.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addData(form).then(response => {
              this.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$confirm('是否确认删除编号为"' + ids + '"的数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return delData(ids);
      }).then(() => {
        this.getList();
        this.msgSuccess("删除成功");
      });
    },
    // 排序
    sortChanged({ column, prop, order }) {
      this.ordering = order ? ((order === "descending" ? "-" : "") + prop) : "";
      this.getList();
    },
    // 清空排序
    resetSort() {
      this.ordering = "";
      this.$refs.dataTable.clearSort();
      this.getList();
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm("是否确认导出所有数据项?", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return exportData(queryParams);
      }).then(response => {
        downloadAuth("/admin/system/savefile/download_file/?id=" + response.data.id, response.data.name);
      });
    }
  }
};
</script>
