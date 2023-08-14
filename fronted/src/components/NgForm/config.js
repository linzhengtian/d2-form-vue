import NgImage from "./NgImage/index";
import NgCode from "./NgCode/index";

const customComponents = [
  {
    type: "NgImage",
    label: "图片展示", // 标题文字
    component: NgImage,
    options: {
      style: "width:100px;height:100px",
      imageUrl: ""
    },
    rules: [
      {
        required: false,
        message: "必填项"
      }
    ]
  },
  {
    type: "NgCode",
    label: "代码", // 标题文字
    component: NgCode,
    options: {
      code: "ace/mode/sh",
      fontSize: 14,
      minLines: 10,
      maxLines: 25
    },
    rules: [
      {
        required: false,
        message: "必填项"
      }
    ]
  }
];

export default customComponents;
