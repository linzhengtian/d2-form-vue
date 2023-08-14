import request from "@/utils/request";

// 查询列表
export function listCaseRole(query) {
  return request({
    url: "/admin/case/caserole/",
    method: "get",
    params: query
  });
}
