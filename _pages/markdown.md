---
permalink: /markdown/
title: "MarkdownGuide"
author_profile: true
redirect_from: 
  - /md/
  - /markdown.html
---

## Basic Markdown Syntax

### Headers

```markdown
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6
```

### Paragraphs and Line Breaks

- Regular paragraph: Direct text input
- Line break: Add two spaces at end of line or empty line

### Lists

#### Unordered List
```markdown
- Item 1
- Item 2
  - Subitem 1
  - Subitem 2
```

#### Ordered List
```markdown
1. First item
2. Second item
   1. Subitem 1
   2. Subitem 2
```

### Emphasis

```markdown
*Italic text*
**Bold text**
***Bold italic text***
```

### Links and Images

```markdown
[Link text](https://example.com)
![Image description](image-path)
```

### Code

Inline code: `code`

Code block:
```python
print("Hello World!")
```

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Content 1 | Content 2 | Content 3 |
| Content 4 | Content 5 | Content 6 |
```

### Blockquotes

```markdown
> Blockquote text
> Multi-line blockquote
```

## Extended Features Supported on This Site

### Mathematical Formulas

Supports MathJax for LaTeX formula rendering:

Inline formula: \(E = mc^2\)

Block formula:
$$
\nabla \cdot E = \frac{\rho}{\epsilon_0}
$$

### Diagrams

Supports Mermaid diagrams:

```mermaid
graph LR
A-->B
```

### Advanced Features

- Footnote support
- HTML tag embedding
- Custom style classes

*For more detailed syntax reference, please see [Markdown Official Documentation](https://www.markdownguide.org/)*
