# ihui_public 项目快速启动指南

## 🚀 快速开始

### 1. 项目位置
```
e:\python_code\coze_zhs_py\ihui_public```

### 2. 已包含的接口

#### WebSocket 接口（4个）
- /cozeZhsApi/ws/doubao/streamDou - 豆包流式对话
- /cozeZhsApi/ws/qwen/stream - 通义千问流式对话
- /cozeZhsApi/ws/chatomni/stream - 通义千问 Omni 流式对话
- /cozeZhsApi/ws/zhipu/stream - 智谱流式对话

#### HTTP 接口（10个）
- /cozeZhsApi/proxy/video-generation - 豆包视频生成
- /cozeZhsApi/proxy/doubao-seedream-generation - 豆包 Seedream 图片生成
- /cozeZhsApi/dashscope/image-to-image - 通义千问图生图
- /cozeZhsApi/dashscope/image/generate/qwen-image-plus - 通义千问图片生成
- /cozeZhsApi/stock/analyse - 股票分析
- /cozeZhsApi/luyala/video/create - Luyala 视频创建
- /cozeZhsApi/dashscope/audio/recognize - 通义千问音频识别
- /cozeZhsApi/proxy/volcengine/image - 火山引擎图片代理
- /cozeZhsApi/dashscope/vision/chat - 通义千问视觉对话

### 3. 快速启动步骤

#### 步骤 1：安装依赖
```bash
cd e:\python_code\coze_zhs_py\ihui_public
pip install -r requirements.txt
```

#### 步骤 2：配置环境
编辑 `config.py` 文件，配置以下必要参数：
- `DATABASE_URL` - 数据库连接字符串
- `DOUBAO_API_KEY` - 豆包 API 密钥
- `DASHSCOPE_API_KEY` - 通义千问 API 密钥
- 其他 API 密钥（根据需要配置）

#### 步骤 3：启动服务
```bash
cd e:\python_code\coze_zhs_py\ihui_public
python main.py
```

#### 步骤 4：测试接口
服务启动后，可以通过以下方式测试：

**测试 WebSocket 接口：**
```javascript
const ws = new WebSocket('ws://localhost:8000/cozeZhsApi/ws/doubao/streamDou');
```

**测试 HTTP 接口：**
```bash
curl -X POST http://localhost:8000/cozeZhsApi/proxy/video-generation \
  -H "Content-Type: application/json" \
  -d '{"prompt": "生成视频", "user_uuid": "test-uuid", "chat_id": "test-chat"}'
```

### 4. 项目结构
```
ihui_public/
├── api/                          # API 接口层
│   ├── __init__.py             # API 模块初始化
│   ├── token_utils.py          # Token 工具
│   ├── public_socket.py        # 公共 Socket 模块
│   ├── doubao_image_proxy.py  # 豆包图片生成
│   ├── stock_analyse.py        # 股票分析
│   └── main.py                # 主程序入口
├── config.py                   # 配置文件
├── database.py                 # 数据库连接
├── database_utils.py           # 数据库工具
├── main.py                    # 主程序入口
├── requirements.txt            # 依赖列表
└── docs/                      # 文档目录
```

### 5. 注意事项

1. **API 密钥配置**：所有 API 密钥都需要在 `config.py` 中配置
2. **数据库配置**：需要配置正确的数据库连接信息
3. **端口配置**：默认使用 8000 端口，可在 `config.py` 中修改
4. **简化处理**：已创建的文件是简化版本，移除了 Redis 和部分复杂逻辑

### 6. 项目特点

- ✅ **模块化设计**：保持了原项目的模块化结构
- ✅ **统一接口**：所有接口使用统一的请求/响应格式
- ✅ **Token 管理**：统一的 Token 验证和扣减机制
- ✅ **公共 Socket**：支持 WebSocket 消息推送（简化版本）
- ✅ **多模型支持**：支持豆包、通义千问、智谱、DeepSeek 等多种 AI 模型

---

**🎉 项目已准备就绪，可以启动了！**
