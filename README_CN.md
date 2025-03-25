# SchemaForge Python SDK

<div align="center">
  <p>
    <strong>以AI为动力的数据结构化工具</strong>
  </p>
  <p>
    <a href="https://github.com/X-Zero-L/schemaforge-ai"><strong>GitHub</strong></a> ·
    <a href="https://schemaforge.ai/docs"><strong>文档</strong></a> ·
    <a href="https://schemaforge.ai"><strong>官网</strong></a>
  </p>
</div>

[English](./README.md) | 中文

## 关于

这是 [SchemaForge AI](https://github.com/X-Zero-L/schemaforge-ai) 的官方Python SDK。SchemaForge AI 是一个统一的AI结构化数据处理服务，使用Pydantic模型定义输出格式，支持多个AI大语言模型。

## 简介

SchemaForge是一个强大的Python SDK，用于快速将非结构化数据转换为结构化格式，以及从样本数据生成Pydantic模型。它提供了直观的API，可用于:

- **结构化文本数据**：将非结构化文本转换为结构化Pydantic模型
- **从样本数据生成模型**：基于样本数据生成Pydantic模型
- **异步支持**：所有操作都支持同步和异步调用

## 安装

```bash
pip install schemaforge
```

## 快速开始

### 初始化客户端

```python
from schemaforge import SchemaForge

# 使用API密钥初始化客户端
client = SchemaForge(api_key="your_secure_api_key_here")

# 或者从环境变量获取API密钥
# export SCHEMAFORGE_API_KEY=your_secure_api_key_here
client = SchemaForge()
```

### 结构化文本数据

```python
from pydantic import BaseModel

# 定义Pydantic模型
class Person(BaseModel):
    name: str
    age: int
    occupation: str

# 使用模型结构化文本
person = client.structure(
    content="张三是一位30岁的软件工程师",
    model_class=Person
)
print(person)
```

### 从样本数据生成模型

```python
# 样例JSON数据
json_sample = '''
{
    "product_id": "P12345",
    "name": "智能手表",
    "price": 1999.99,
    "in_stock": true,
    "specifications": {
        "screen_size": "6.5英寸",
        "processor": "SnapDragon 8",
        "storage": "128GB",
        "camera": "48MP"
    },
    "colors": ["黑色", "银色", "金色"],
    "release_date": "2024-01-15"
}
'''

# 从样本数据生成模型
result = client.generate_model(
    sample_data=json_sample,
    model_name="Product",
    description="产品信息模型，包含规格信息"
)

if result.get("success"):
    # 加载生成的模型
    Product = client.load_model(result["model_code"])
    print(Product)
```

### 异步支持

```python
import asyncio
from schemaforge import SchemaForge

async def main():
    client = SchemaForge(api_key="your_secure_api_key_here")
    
    # 异步结构化文本
    person = await client.astructure(
        content="李四是一位25岁的数据科学家",
        model_class=Person
    )
    print(person)
    
    # 异步生成模型
    result = await client.agenerate_model(
        sample_data='{"name": "笔记本电脑", "price": 5999.99}',
        model_name="Laptop",
        description="笔记本电脑信息模型"
    )
    
    if result.get("success"):
        Laptop = client.load_model(result["model_code"])
        print(Laptop)

asyncio.run(main())
```

## 高级用法

### 自定义配置

```python
from schemaforge import SchemaForge

# 使用自定义配置创建客户端
client = SchemaForge(
    api_key="your_secure_api_key_here",
    api_base="https://custom-endpoint.schemaforge.ai",
    default_model="gpt-4",
    timeout=60.0,
    max_retries=3,
    retry_delay=1.0,
    retry_jitter=True,
    verbose=True
)
```

### 错误处理

```python
from schemaforge import SchemaForge
from schemaforge.exceptions.api_error import SchemaForgeError

client = SchemaForge(api_key="your_secure_api_key_here")

try:
    person = client.structure(
        content="无效文本",
        model_class=Person
    )
except SchemaForgeError as e:
    print(f"错误: {e}")
```

## 进一步阅读

有关完整的API文档和更多示例，请访问[SchemaForge文档](https://schemaforge.ai/docs)。 