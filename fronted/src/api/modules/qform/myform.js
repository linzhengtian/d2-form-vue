import request from "@/utils/request";
import { downloadBlob } from "@/utils/ruoyi";

// 查询列表
export function listData(query) {
  return request({
    url: "/admin/qform/forminfolist/",
    method: "get",
    params: query
  });
}

// 查询详细
export function getData(id) {
  return request({
    url: "/admin/qform/forminfo/" + id + "/",
    method: "get"
  });
}

// 查询详细
export function getAnonymousData(id) {
  return request({
    url: "/admin/qform/anonymousforminfo/" + id + "/",
    method: "get"
  });
}

// 新增
export function addData(data) {
  return request({
    url: "/admin/qform/forminfo/",
    method: "post",
    data: data
  });
}

// 修改
export function updateData(data) {
  return request({
    url: "/admin/qform/forminfo/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 局部修改
export function patchData(data) {
  return request({
    url: "/admin/qform/forminfo/" + data.id + "/",
    method: "patch",
    data: data
  });
}

// 删除
export function delData(id) {
  return request({
    url: "/admin/qform/forminfo/" + id + "/",
    method: "delete"
  });
}

// 查询详细
export function getAnonymousTemplateData(id) {
  return request({
    url: "/admin/qform/anonymousformtemplate/" + id + "/",
    method: "get"
  });
}

// 查询详细
export function getTemplateData(id) {
  return request({
    url: "/admin/qform/formtemplate/" + id + "/",
    method: "get"
  });
}

// 新增
export function addTemplateData(data) {
  return request({
    url: "/admin/qform/formtemplate/",
    method: "post",
    data: data
  });
}

// 修改
export function updateTemplateData(data) {
  return request({
    url: "/admin/qform/formtemplate/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 删除
export function delTemplateData(id) {
  return request({
    url: "/admin/qform/formtemplate/" + id + "/",
    method: "delete"
  });
}

// 查询详细
export function getFormData(id) {
  return request({
    url: "/admin/qform/formdata/" + id + "/",
    method: "get"
  });
}

// 新增
export function addFormData(data) {
  return request({
    url: "/admin/qform/formdata/",
    method: "post",
    data: data
  });
}

// 新增
export function addAnonymousFormData(data) {
  return request({
    url: "/admin/qform/anonymousformdata/",
    method: "post",
    data: data
  });
}

// 修改
export function updateFormData(data) {
  return request({
    url: "/admin/qform/formdata/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 查询列表
export function listFormData(query) {
  return request({
    url: "/admin/qform/formdata/",
    method: "get",
    params: query
  });
}

// 删除
export function delFormData(id) {
  return request({
    url: "/admin/qform/formdata/" + id + "/",
    method: "delete"
  });
}

// 查询列表
export function listRolePermissions(query) {
  return request({
    url: "/admin/qform/forminforolepermissions/",
    method: "get",
    params: query
  });
}

// 新增
export function addRolePermissions(data) {
  return request({
    url: "/admin/qform/forminforolepermissions/",
    method: "post",
    data: data
  });
}

// 修改
export function updateRolePermissions(data) {
  return request({
    url: "/admin/qform/forminforolepermissions/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 删除
export function delRolePermissions(id) {
  return request({
    url: "/admin/qform/forminforolepermissions/" + id + "/",
    method: "delete"
  });
}

// 查询列表
export function listUserPermissions(query) {
  return request({
    url: "/admin/qform/forminfouserpermissions/",
    method: "get",
    params: query
  });
}

// 新增
export function addUserPermissions(data) {
  return request({
    url: "/admin/qform/forminfouserpermissions/",
    method: "post",
    data: data
  });
}

// 修改
export function updateUserPermissions(data) {
  return request({
    url: "/admin/qform/forminfouserpermissions/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 删除
export function delUserPermissions(id) {
  return request({
    url: "/admin/qform/forminfouserpermissions/" + id + "/",
    method: "delete"
  });
}

// 查询详细
export function getDesignData(id) {
  return request({
    url: "/admin/qform/forminfodesignpermissions/" + id + "/",
    method: "get"
  });
}

// 局部修改
export function patchDesignData(data) {
  return request({
    url: "/admin/qform/forminfodesignpermissions/" + data.id + "/",
    method: "patch",
    data: data
  });
}

// 导出
export function exportFormData(query) {
  return request({
    url: "/admin/qform/formdata/export/",
    method: "get",
    params: query,
    responseType: "arraybuffer" // 解决乱码
  }).then((res) => {
    downloadBlob(res, "结果.xlsx");
  });
}

// 新增
export function copyForm(data) {
  return request({
    url: "/admin/qform/formcopy/copy/",
    method: "post",
    data: data
  });
}
