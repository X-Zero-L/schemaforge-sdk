"""
SchemaForge SDK 使用示例
本文件展示了如何使用 SchemaForge SDK 进行数据结构化和模型生成。
"""

import asyncio
from typing import Dict, Type
from pydantic import BaseModel
from schemaforge import SchemaForge


def main():
    # 初始化 SDK
    client = SchemaForge(
        api_key="your_secure_api_key_here",
        api_base="http://localhost:8000",
        default_model="openai:gpt-4o",
    )

    # 示例 1: 使用预定义模型结构化文本
    print("\n=== 示例 1: 文本结构化 ===")

    class Person(BaseModel):
        name: str
        age: int
        occupation: str
        email: str

    # 同步调用
    person = client.structure(
        content="张三是一名30岁的软件工程师，邮箱是zhangsan@example.com",
        model_class=Person,
    )
    print(f"结构化结果: {person.model_dump()}")

    # 示例 2: 从样本数据生成模型
    print("\n=== 示例 2: 模型生成 ===")

    # 使用自然语言描述的数据
    sample_data = """
    这是一款智能手表产品，型号是P12345，售价199.99元，目前有货。
    手表配备了6.5英寸的显示屏，使用SnapDragon 8处理器，存储容量128GB，摄像头像素4800万。
    产品有黑色、银色和金色三种颜色可选，于2024年1月15日正式发布。
    """

    # 生成模型
    response = client.generate_model(
        sample_data=sample_data,
        model_name="Product",
        description="产品信息模型，包含基本信息、规格和颜色选项",
    )

    if response.success:
        print("✅ 模型生成成功！")
        print(f"模型名称: {response.model_name}")

        # 获取所有生成的模型（包括子模型）
        models: Dict[str, Type[BaseModel]] = client.load_generated_model(response)
        print("\n生成的模型:")
        for name, model in models.items():
            print(f"\n{name}:")
            print(model.model_json_schema())

        # 只获取主模型
        main_model = client.get_main_model(response)
        print("\n主模型:")
        print(main_model.model_json_schema())

        # 获取完整代码
        complete_code = client.get_model_code(response)
        print("\n完整代码:")
        print(complete_code)
    else:
        print(f"❌ 模型生成失败: {response.error}")


async def async_examples():
    print("\n=== 示例 3: 异步调用 ===")

    client = SchemaForge(api_key="your_secure_api_key_here")

    # 异步文本结构化
    class Person(BaseModel):
        name: str
        age: int
        occupation: str

    person = await client.astructure(
        content="李四是一名25岁的数据科学家", model_class=Person
    )
    print(f"异步结构化结果: {person.model_dump()}")

    # 异步模型生成
    sample_data = """
    这是一台高性能笔记本电脑，售价999.99元，目前有货。
    电脑配备了Intel i7处理器，16GB内存，512GB SSD固态硬盘。
    整机采用铝合金材质，重量约1.5kg，续航时间可达8小时。
    """

    response = await client.agenerate_model(
        sample_data=sample_data,
        model_name="Laptop",
        description="笔记本电脑信息模型，包含规格信息",
    )

    if response.success:
        print("✅ 异步模型生成成功！")
        models = client.load_generated_model(response)
        print("\n生成的模型:")
        for name, model in models.items():
            print(f"\n{name}:")
            print(model.model_json_schema())
    else:
        print(f"❌ 异步模型生成失败: {response.error}")


if __name__ == "__main__":
    # 运行同步示例
    main()

    # 运行异步示例
    asyncio.run(async_examples())
