---
layout: archive
title: "个人简历"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

## 教育背景

* [学位] - [学校名称]，[专业]，[年份]
* [学位] - [学校名称]，[专业]，[年份]

## 工作经历

* [职位] - [公司/机构名称]，[时间段]
  * [工作职责描述]

* [职位] - [公司/机构名称]，[时间段]
  * [工作职责描述]

## 专业技能

* [技能类别1]: [具体技能]
* [技能类别2]: [具体技能]
* [技能类别3]: [具体技能]

## 学术成果

<ul>{% for post in site.publications reversed %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>

## 演讲报告

<ul>{% for post in site.talks reversed %}
  {% include archive-single-talk-cv.html %}
{% endfor %}</ul>

## 教学经历

<ul>{% for post in site.teaching reversed %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>
