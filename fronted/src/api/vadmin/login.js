import request from "@/utils/request";

// 登录方法
export function login(username, password, code, uuid, publicId) {
  const data = {
    username,
    password,
    idValueC: code,
    idKeyC: uuid,
    publicId: publicId
  };
  return request({
    url: "/admin/login/",
    method: "post",
    data: data
  });
}

// 获取用户详细信息
export function getInfo() {
  return request({
    url: "/admin/getInfo/",
    method: "get"
  });
}

// 退出方法
export function logout() {
  return request({
    url: "/admin/logout/",
    method: "post"
  });
}

// 获取验证码
export function getCodeImg() {
  return request({
    url: "/admin/captcha/refresh/",
    method: "get"
  });
}

// 获取公钥
export function getPublicKey() {
  return request({
    url: "/admin/public/refresh/",
    method: "get"
  });
}
