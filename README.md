# 项目简介 / Project Introduction

该项目旨在将Markdown文件的标签表格转换为YAML头部格式。它提供了一种简单的方法来处理Markdown文件，并将其内容转换为结构化的YAML数据格式，方便进一步的数据处理和分析。

This project aims to convert the tag tables in Markdown files into YAML header format. It provides a simple way to process Markdown files and convert their content into structured YAML data format for further data processing and analysis.

## 项目架构 / Project Architecture

项目采用Python编写，主要功能模块包括：
- Markdown解析模块：负责解析Markdown文件的内容。
- YAML生成模块：将解析后的内容转换为YAML格式。

The project is written in Python, with the main functional modules including:
- Markdown Parsing Module: Responsible for parsing the content of Markdown files.
- YAML Generation Module: Converts the parsed content into YAML format.

## 依赖 / Dependencies

项目依赖以下Python库：
- `frontmatter`: 用于处理Markdown文件的元数据。

The project depends on the following Python libraries:
- `frontmatter`: Used for handling metadata in Markdown files.

建议使用Conda创建虚拟环境并安装依赖，以确保环境的隔离性和依赖的可控性。

It is recommended to use Conda to create a virtual environment and install dependencies to ensure environment isolation and dependency control.