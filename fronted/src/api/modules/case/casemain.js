import request from "@/utils/request";

// 查询列表
export function listData(query) {
  return request({
    url: "/admin/case/casemain/",
    method: "get",
    params: query
  });
}

// 查询详细
export function getData(id) {
  return request({
    url: "/admin/case/casemain/" + id + "/",
    method: "get"
  });
}

// 新增
export function addData(data) {
  return request({
    url: "/admin/case/casemain/",
    method: "post",
    data: data
  });
}

// 修改
export function updateData(data) {
  return request({
    url: "/admin/case/casemain/" + data.id + "/",
    method: "put",
    data: data
  });
}

// 删除
export function delData(id) {
  return request({
    url: "/admin/case/casemain/" + id + "/",
    method: "delete"
  });
}

// 导出字典类型
export function exportData(query) {
  return request({
    url: "/admin/case/casemain/export/",
    method: "get",
    params: query
  });
}
