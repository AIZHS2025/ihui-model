# 批量复制剩余 API 文件指南

## 📋 剩余需要复制的文件清单

根据原项目分析，还有以下 **13 个 API 文件**需要复制到 ihui_public 项目：

### WebSocket 接口（1个）
- websocket_doubao_stream_simplified.py

### HTTP 接口（12个）
- doubao_video_proxy.py
- doubao_image_proxy.py
- dashscope_image_to_image.py
- dashscope_image.py
- stock_analyse.py
- luyala_proxy.py
- dashscope_audio.py
- websocket_qwen_stream.py
- websocket_qwen_stream_omni.py
- volcengine_image_proxy.py
- volcengine_visual_proxy.py
- dashscope_vision.py
- websocket_zhipu_stream.py
- dashscope_image_edit.py
- dashscope_video_synthesis.py
- kling_video_synthesis.py
- websocket_deepseek_stream.py
- volcengine_jimeng31_proxy.py

## 🔍 复制方法

### 方法 1：手动复制（推荐）
1. 打开原项目文件：`e:\python_code\coze_zhs_pypi\[文件名]`
2. 复制全部内容
3. 在新项目中创建文件：`e:\python_code\coze_zhs_py\ihui_publicpi\[文件名]`
4. 粘贴内容并保存

### 方法 2：使用脚本（高级）
可以创建一个 Python 脚本来自动复制文件：

```python
import os
import shutil

# 原项目目录
source_dir = r'e:\python_code\coze_zhs_pypi'
# 目标目录
target_dir = r'e:\python_code\coze_zhs_py\ihui_publicpi'

# 需要复制的文件列表
files_to_copy = [
    'websocket_doubao_stream_simplified.py',
    'doubao_video_proxy.py',
    'doubao_image_proxy.py',
    'dashscope_image_to_image.py',
    'dashscope_image.py',
    'stock_analyse.py',
    'luyala_proxy.py',
    'dashscope_audio.py',
    'websocket_qwen_stream.py',
    'websocket_qwen_stream_omni.py',
    'volcengine_image_proxy.py',
    'volcengine_visual_proxy.py',
    'dashscope_vision.py',
    'websocket_zhipu_stream.py',
    'dashscope_image_edit.py',
    'dashscope_video_synthesis.py',
    'kling_video_synthesis.py',
    'websocket_deepseek_stream.py',
    'volcengine_jimeng31_proxy.py'
]

# 复制文件
for file_name in files_to_copy:
    source_path = os.path.join(source_dir, file_name)
    target_path = os.path.join(target_dir, file_name)

    if os.path.exists(source_path):
        shutil.copy2(source_path, target_path)
        print(f'✅ 已复制: {file_name}')
    else:
        print(f'❌ 文件不存在: {file_name}')

print('\n🎉 复制完成！')
```

## 📝 注意事项

1. **依赖检查**：复制每个文件前，先检查原项目中的依赖文件是否都已复制
2. **导入路径**：新项目中使用相对导入（`from ..config`），确保路径正确
3. **配置要求**：复制完成后，需要在 `config.py` 中配置相应的 API 密钥
4. **文件大小**：部分文件较大（如 stock_analyse.py 超过 900 行），复制时可能需要等待
5. **测试建议**：建议逐个测试接口，而不是批量测试所有接口

## 📌 复制进度

当前已完成：**17 个文件** / 总计 **34 个文件**

还需要复制：**17 个文件**

请告诉我是否继续复制剩余的文件？
