# ihui_public 项目结构说明

## 项目概述

ihui_public 是从 coze_zhs_py 项目中提取的公共 API 接口项目，包含以下主要功能模块：

1. **豆包相关接口**
   - 豆包流式对话 (WebSocket)
   - 豆包图片生成 (HTTP)
   - 豆包视频生成 (HTTP)

2. **通义千问相关接口**
   - 图片生成 (HTTP)
   - 图生图 (HTTP)
   - 图片编辑 (HTTP)
   - 音频识别 (HTTP)
   - 视觉对话 (HTTP)
   - 视频合成 (HTTP)
   - 流式对话 (WebSocket)
   - Omni流式对话 (WebSocket)

3. **智谱相关接口**
   - 流式对话 (WebSocket)

4. **火山引擎相关接口**
   - 图片生成代理 (HTTP)
   - 视觉图片生成 (HTTP)
   - 即梦图片生成 (HTTP)

5. **可灵相关接口**
   - 视频生成 (HTTP)

6. **DeepSeek相关接口**
   - 流式对话 (WebSocket)

7. **Luyala相关接口**
   - 视频创建 (HTTP)
   - 对话补全 (HTTP)

8. **股票分析接口**
   - 股票分析 (HTTP + WebSocket)

## 目录结构

```
ihui_public/
├── api/                          # API 接口层
│   ├── __init__.py             # API 模块初始化
│   ├── token_utils.py          # Token 工具
│   ├── public_socket.py        # 公共 Socket 模块
│   ├── doubao_image_proxy.py  # 豆包图片生成
│   ├── stock_analyse.py        # 股票分析
│   └── ...                    # 其他 API 文件
├── config.py                   # 配置文件
├── database.py                 # 数据库连接
├── database_utils.py           # 数据库工具
├── main.py                    # 主程序入口
├── requirements.txt            # 依赖列表
└── docs/                      # 文档目录
    └── PROJECT_STRUCTURE.md     # 本文件
```

## 核心功能说明

### 1. Token 管理
- 用户余额验证
- Token 扣减
- 费用计算
- 对话历史保存

### 2. 公共 Socket
- WebSocket 连接管理
- 消息推送
- 连接状态监控

### 3. 多模型支持
- 支持多种 AI 模型接口
- 统一的请求/响应格式
- 流式和非流式接口

## 配置说明

主要配置项：
- API 服务配置（端口、调试模式等）
- 数据库连接配置
- 各 API 密钥配置
- Token 计算配置
- 文件上传配置

## 启动方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

## 注意事项

1. **API 密钥配置**：所有 API 密钥需要在 config.py 中配置
2. **数据库配置**：需要配置数据库连接信息
3. **依赖安装**：确保所有依赖都已安装
4. **端口配置**：默认使用 8000 端口，可在 config.py 中修改

## 接口清单

### WebSocket 接口
- /cozeZhsApi/ws/doubao/streamDou
- /cozeZhsApi/ws/qwen/stream
- /cozeZhsApi/ws/chatomni/stream
- /cozeZhsApi/ws/zhipu/stream
- /cozeZhsApi/ws/chatdeepseek/stream
- /cozeZhsApi/stock/ws/analyse

### HTTP 接口
- /cozeZhsApi/proxy/video-generation
- /cozeZhsApi/proxy/doubao-seedream-generation
- /cozeZhsApi/dashscope/image-to-image
- /cozeZhsApi/dashscope/image/generate/qwen-image-plus
- /cozeZhsApi/dashscope/image/generate/qwen-image
- /cozeZhsApi/dashscope/image/generate/wan2.5-t2i-preview
- /cozeZhsApi/stock/analyse
- /cozeZhsApi/luyala/video/create
- /cozeZhsApi/luyala/chat/completions
- /cozeZhsApi/dashscope/audio/recognize
- /cozeZhsApi/proxy/volcengine/image
- /cozeZhsApi/dashscope/vision/chat
- /api/v1/dashscope/image/edit/simple
- /cozeZhsApi/dashscope/video-synthesis/ws
- /cozeZhsApi/kling/generate/o1
- /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_tail_v30
- /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_v30
- /cozeZhsApi/proxy/volcengine/visual/jimeng_t2v_v30_1080p
- /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_recamera_v30
- /cozeZhsApi/ws/chatdeepseek/stream
