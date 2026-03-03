---
permalink: /markdown/
title: "Markdown语法指南"
author_profile: true
redirect_from: 
  - /md/
  - /markdown.html
---

## 基本Markdown语法

### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

### 段落和换行

- 普通段落：直接输入文本
- 换行：行末添加两个空格或空行

### 列表

#### 无序列表
```markdown
- 项目1
- 项目2
  - 子项目1
  - 子项目2
```

#### 有序列表
```markdown
1. 第一项
2. 第二项
   1. 子项1
   2. 子项2
```

### 强调

```markdown
*斜体文本*
**粗体文本**
***粗斜体文本***
```

### 链接和图片

```markdown
[链接文本](https://example.com)
![图片描述](图片路径)
```

### 代码

行内代码：`code`

代码块：
```python
print("Hello World!")
```

### 表格

```markdown
| 标题1 | 标题2 | 标题3 |
|-------|-------|-------|
| 内容1 | 内容2 | 内容3 |
| 内容4 | 内容5 | 内容6 |
```

### 引用

```markdown
> 引用文本
> 多行引用
```

## 本网站支持的扩展功能

### 数学公式

支持MathJax渲染LaTeX公式：

行内公式：\(E = mc^2\)

块级公式：
$$
\nabla \cdot E = \frac{\rho}{\epsilon_0}
$$

### 图表

支持Mermaid图表：

```mermaid
graph LR
A-->B
```

### 高级功能

- 脚注支持
- HTML标签嵌入
- 自定义样式类

*如需更详细的语法说明，请参考[Markdown官方文档](https://www.markdownguide.org/)*
