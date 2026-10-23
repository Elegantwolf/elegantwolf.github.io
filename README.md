# ElegantWolf — Academic Homepage

个人学术主页的筹备仓库，目标部署平台为 GitHub Pages。

## 网站定位

- 学术主页：`https://elegantwolf.org/`
- 现有博客：`https://blog.elegantwolf.org/`
- 设计参考：[Adam Distler 的主页](https://adam-distler.github.io/)

采用简洁的单页结构，使用清晰的导航、充足留白、个人照片和少量研究配图。以自己的内容和图片实现页面。

## 第一版内容

1. **About**：姓名、博士生身份、学校与导师、研究方向、简短经历。
2. **Research**：当前或过去的研究项目，介绍研究问题、个人贡献与进展；支持进行中的工作。
3. **Writing**：精选博客文章，链接到现有博客。
4. **CV**：可公开的 PDF 简历；收到文件后添加链接。
5. **Contact**：公开联系邮箱及实际使用的学术账号。

有论文后可以加入 Publications，已有少量论文也可以放在对应研究项目下。

## 当前文件

- `README.md`：定位、页面结构与维护方式。
- `CONTENT.md`：需要一起填写的个人资料和内容清单。

当前是内容筹备阶段，尚未发布网站，也未绑定域名。

## 页面实现后的文件结构（计划）

```text
index.html              # 单页主页
assets/
  css/style.css         # 页面样式
  images/               # 头像和研究配图
  files/cv.pdf          # 可公开简历
README.md
CONTENT.md
.nojekyll               # 采用纯 HTML/CSS 时加入
```

优先使用纯 HTML/CSS，避免引入不需要的构建依赖。只有需要交互时才添加少量 JavaScript。

## 后续步骤

1. 填写 `CONTENT.md` 中的首批资料。
2. 确认页面内容，制作第一版页面。
3. 检查电脑、手机显示和链接。
4. 确认现有博客的托管及 DNS 配置，启用 GitHub Pages 并绑定域名。

域名配置阶段保留博客现有的 `blog` 记录。`www.elegantwolf.org` 计划作为主站的访问别名。
