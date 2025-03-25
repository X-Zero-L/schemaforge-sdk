# SchemaForge Python SDK

<div align="center">
  <p>
    <strong>以AI为动力的数据结构化工具</strong>
  </p>
  <p>
    <a href="https://github.com/X-Zero-L/schemaforge-ai"><strong>GitHub</strong></a> ·
    <a href="https://github.com/X-Zero-L/schemaforge-sdk/docs"><strong>文档</strong></a> ·
    <a href="https://github.com/X-Zero-L/schemaforge-sdk"><strong>官网</strong></a>
  </p>
</div>

[English](./README.md) | 中文

## 关于

这是 [SchemaForge AI](https://github.com/X-Zero-L/schemaforge-ai) 的官方Python SDK。SchemaForge AI 是一个统一的AI结构化数据处理服务，使用Pydantic模型定义输出格式，支持多个AI大语言模型。

## 安装

```bash
pip install schemaforge
```

## 快速开始

```python
from pydantic import BaseModel
from schemaforge import SchemaForge

# 初始化客户端
client = SchemaForge(api_key="your_secure_api_key_here")

# 定义Pydantic模型
class Person(BaseModel):
    name: str
    age: int
    occupation: str
    email: str

# 使用模型结构化文本
person = client.structure(
    content="张三是一位30岁的软件工程师，邮箱是zhangsan@example.com",
    model_class=Person
)
print(person.model_dump())
# {'name': '张三', 'age': 30, 'occupation': '软件工程师', 'email': 'zhangsan@example.com'}
```

## 功能特性

- **结构化非结构化文本** 转换为Pydantic模型
- **从自然语言描述生成Pydantic模型**
- **自动处理复杂模型依赖**
- **支持异步操作**

## 文档

查看[完整文档](https://github.com/X-Zero-L/schemaforge-sdk/tree/master/docs)了解详细示例和API参考。 