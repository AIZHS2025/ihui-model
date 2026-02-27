# ihui_public API 项目

这是从 coze_zhs_py 项目中提取的公共 API 接口项目。

## 项目结构

```
ihui_public/
├── api/                    # API 接口层
├── config.py              # 配置文件
├── database.py            # 数据库连接
├── database_utils.py      # 数据库工具
├── main.py              # 主程序入口
├── requirements.txt       # 依赖列表
└── docs/               # 文档目录
```

## API 接口文档

### 通用参数说明

所有接口都需要以下通用参数：

- `user_uuid` (必填): 用户唯一标识符，用于计费和记录
- `chat_id` (可选): 会话ID，用于关联对话记录
- 接口返回格式统一为: `{"code": 0, "data": {...}}` 或错误时 `{"code": xxx, "msg": "error message"}`

---

### WebSocket 接口

#### 1. 豆包流式对话
**路径**: `ws://host/cozeZhsApi/ws/doubao/streamDou?client_id=xxx&user_uuid=xxx`

**功能**: 提供豆包大模型的流式对话服务

**连接参数**:
- `client_id`: 客户端ID（可选，不提供则自动生成）
- `user_uuid`: 用户UUID（可选）

**消息格式**:
```json
{
  "type": "chat",
  "data": {
    "prompt": "你的问题",
    "chat_id": "会话ID"
  }
}
```

**心跳消息**:
```json
{
  "type": "ping"
}
```

---

#### 2. 通义千问流式对话
**路径**: `ws://host/cozeZhsApi/ws/qwen/stream?client_id=xxx&user_uuid=xxx`

**功能**: 提供通义千问大模型的流式对话服务

**消息格式**: 同豆包流式对话

---

#### 3. 通义千问 Omni 流式对话
**路径**: `ws://host/cozeZhsApi/ws/chatomni/stream?client_id=xxx&user_uuid=xxx`

**功能**: 提供通义千问 Omni 多模态大模型的流式对话服务

**消息格式**: 同豆包流式对话

---

#### 4. 智谱流式对话
**路径**: `ws://host/cozeZhsApi/ws/zhipu/stream?client_id=xxx&user_uuid=xxx`

**功能**: 提供智谱大模型的流式对话服务

**消息格式**: 同豆包流式对话

---

#### 5. DeepSeek 流式对话
**路径**: `ws://host/cozeZhsApi/ws/chatdeepseek/stream?client_id=xxx&user_uuid=xxx`

**功能**: 提供DeepSeek大模型的流式对话服务

**消息格式**: 同豆包流式对话

---

### HTTP 接口

#### 1. 豆包视频生成
**路径**: `POST /cozeZhsApi/proxy/video-generation`

**功能**: 豆包图生视频

**请求参数**:
```json
{
  "prompt": "视频生成提示词",
  "images": ["图片URL列表"],
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）",
  "zidingyican": [
    {"name": "参数名", "value": "参数值"}
  ]
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "video_url": "生成的视频URL",
    "task_id": "任务ID"
  }
}
```

---

#### 2. 豆包图片生成
**路径**: `POST /cozeZhsApi/proxy/doubao-seedream-generation`

**功能**: 豆包Seedream图片生成

**请求参数**:
```json
{
  "prompt": "图片生成提示词",
  "images": ["参考图片URL列表（可选）"],
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）",
  "zidingyican": [
    {"name": "参数名", "value": "参数值"}
  ]
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "image_url": "生成的图片URL",
    "task_id": "任务ID"
  }
}
```

---

#### 3. 豆包图片编辑
**路径**: `POST /cozeZhsApi/proxy/doubao-image-edit`

**功能**: 豆包图片编辑

**请求参数**:
```json
{
  "prompt": "编辑提示词",
  "image": "输入图片URL",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "image_url": "编辑后的图片URL"
  }
}
```

---

#### 4. 通义千问图片生成
**路径**: `POST /cozeZhsApi/dashscope/image/generate/qwen-image-plus`

**功能**: 通义千问Plus版图片生成

**请求参数**:
```json
{
  "prompt": "图片生成提示词",
  "model": "qwen-image-plus",
  "size": "1024*1024",
  "n": 1,
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "image_urls": ["图片URL列表"]
  }
}
```

---

#### 5. 通义千问图片生成（标准版）
**路径**: `POST /cozeZhsApi/dashscope/image/generate/qwen-image`

**功能**: 通义千问标准版图片生成

**请求参数**: 同Plus版

---

#### 6. 通义万相图片生成
**路径**: `POST /cozeZhsApi/dashscope/image/generate/wan2.5-t2i-preview`

**功能**: 通义万相图片生成

**请求参数**: 同通义千问图片生成

---

#### 7. 通义千问图生图
**路径**: `POST /cozeZhsApi/dashscope/image-to-image`

**功能**: 根据输入图片和文本提示生成新图像

**请求参数**:
```json
{
  "images": [
    {
      "imgUrl": "图片URL",
      "originalUrl": "原始图片URL",
      "id": "图片ID",
      "width": 1024,
      "height": 1024
    }
  ],
  "prompt": "图像合成的文本提示",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）",
  "zidingyican": [
    {"name": "参数名", "desc": "参数描述", "value": "参数值"}
  ]
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "image_urls": ["生成的图片URL列表"],
    "lists": [
      {"text": "文本", "images": ["图片URL"]}
    ]
  }
}
```

---

#### 8. 通义千问图片编辑
**路径**: `POST /api/v1/dashscope/image/edit/simple`

**功能**: 通义千问图片编辑

**请求参数**:
```json
{
  "prompt": "编辑提示词",
  "image_url": "原始图片URL",
  "model": "qwen-image-edit",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "edited_image_url": "编辑后的图片URL"
  }
}
```

---

#### 9. 通义千问视觉对话
**路径**: `POST /cozeZhsApi/dashscope/vision/chat`

**功能**: 通义千问视觉对话，支持图片理解

**请求参数**:
```json
{
  "prompt": "对话提示词",
  "image_urls": ["图片URL列表"],
  "model": "qwen-vl-max",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "content": "对话内容"
  }
}
```

---

#### 10. 通义千问音频识别
**路径**: `POST /cozeZhsApi/dashscope/audio/recognize`

**功能**: 通义千问语音识别

**请求参数**:
```json
{
  "audio_url": "音频文件的URL地址",
  "model": "qwen3-asr-flash",
  "language": "zh",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）",
  "system_prompt": "系统提示词（可选）"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "识别完成",
  "transcription": "识别结果文本",
  "language_detected": "检测到的语言",
  "total_tokens": 100
}
```

---

#### 11. 通义千问视频合成
**路径**: `ws://host/cozeZhsApi/dashscope/video-synthesis/ws?client_id=xxx&user_uuid=xxx`

**功能**: 通义千问视频合成（WebSocket）

**消息格式**:
```json
{
  "type": "video_synthesis",
  "data": {
    "prompt": "视频合成提示词",
    "chat_id": "会话ID"
  }
}
```

---

#### 12. 股票分析
**路径**: `POST /cozeZhsApi/stock/analyse`

**功能**: 股票分析

**请求参数**:
```json
{
  "stock_code": "股票代码",
  "analysis_type": "basic",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "analysis_result": {
      "stock_code": "股票代码",
      "analysis_type": "分析类型",
      "recommendation": "持有",
      "risk_level": "中等",
      "target_price": "100.00",
      "analysis_date": "2026-02-25"
    }
  }
}
```

---

#### 13. Luyala视频创建
**路径**: `POST /cozeZhsApi/luyala/video/create`

**功能**: Luyala视频生成

**请求参数**:
```json
{
  "prompt": "视频生成提示词",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "video_url": "生成的视频URL"
  }
}
```

---

#### 14. Luyala对话补全
**路径**: `POST /cozeZhsApi/luyala/chat/completions`

**功能**: Luyala对话补全

**请求参数**:
```json
{
  "prompt": "对话补全提示词",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "completion": "补全结果"
  }
}
```

---

#### 15. 火山引擎图片生成
**路径**: `POST /cozeZhsApi/proxy/volcengine/image`

**功能**: 火山引擎图片生成

**请求参数**:
```json
{
  "prompt": "图片生成提示词",
  "model": "volcengine-image",
  "size": "1024*1024",
  "n": 1,
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "image_urls": ["图片URL列表"]
  }
}
```

---

#### 16. 即梦图片生成（尾部增强）
**路径**: `POST /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_tail_v30`

**功能**: 即梦图生图（尾部增强）

**请求参数**:
```json
{
  "prompt": "生成提示词",
  "model": "jimeng-i2v-tail",
  "image_url": "输入图片URL（可选）",
  "size": "1024*1024",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "result_url": "生成的图片URL"
  }
}
```

---

#### 17. 即梦图片生成
**路径**: `POST /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_v30`

**功能**: 即梦图生图

**请求参数**: 同即梦图片生成（尾部增强）

---

#### 18. 即梦图片生成（重相机）
**路径**: `POST /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_recamera_v30`

**功能**: 即梦图生图（重相机）

**请求参数**: 同即梦图片生成（尾部增强）

---

#### 19. 即梦视频生成
**路径**: `POST /cozeZhsApi/proxy/volcengine/visual/jimeng_t2v_v30_1080p`

**功能**: 即梦文生视频

**请求参数**:
```json
{
  "prompt": "视频生成提示词",
  "model": "jimeng-t2v-1080p",
  "duration": 5,
  "resolution": "1080p",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "result_url": "生成的视频URL"
  }
}
```

---

#### 20. 可灵视频生成
**路径**: `POST /cozeZhsApi/kling/generate/o1`

**功能**: 可灵视频生成

**请求参数**:
```json
{
  "prompt": "视频生成提示词",
  "model": "kling-o1",
  "duration": 5,
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "video_url": "生成的视频URL"
  }
}
```

---

#### 21. Suno音乐生成
**路径**: `POST /suno/generate/music`

**功能**: Suno音乐生成

**请求参数**:
```json
{
  "prompt": "音乐生成提示词",
  "model": "suno-v3",
  "duration": 30,
  "style": "音乐风格（可选）",
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "music_url": "生成的音乐URL"
  }
}
```

---

#### 22. Gemini生成
**路径**: `POST /gemini/3/generate`

**功能**: Gemini内容生成

**请求参数**:
```json
{
  "prompt": "生成提示词",
  "model": "gemini-3",
  "temperature": 0.7,
  "max_tokens": 1000,
  "user_uuid": "用户UUID",
  "chat_id": "会话ID（可选）"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "content": "生成的内容"
  }
}
```

---

### 公共Socket接口

#### WebSocket连接
**路径**: `ws://host/cozeZhsApi/public-socket/ws`

**功能**: 公共Socket连接，用于接收实时消息

**连接流程**:
1. 建立WebSocket连接
2. 发送注册消息:
```json
{
  "event": "register",
  "user_uuid": "用户UUID",
  "model_id": "模型ID",
  "chat_id": "会话ID（可选）"
}
```
3. 接收实时消息

---

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 配置

### 配置方式

项目支持两种配置方式：

1. **直接修改 config.py**：直接在配置文件中修改各项配置
2. **使用环境变量**：在项目根目录创建 `.env` 文件，配置环境变量

### API 密钥配置

项目需要配置多个第三方服务的 API 密钥，以下是详细说明：

#### 1. 豆包 API（豆包对话、图片生成、视频生成）

```env
# 豆包对话和图片生成
DOUBAO_API_KEY=your_doubao_api_key_here

# 豆包图片生成专用
DOUBAO_IMAGE_API_URL=https://ark.cn-beijing.volces.com/api/v3/images/generations
```

**获取方式**：
- 访问 [火山引擎控制台](https://console.volcengine.com/)
- 创建应用后获取 API Key

---

#### 2. 即梦 API（火山引擎）

```env
# 即梦 API 密钥
DOUBAO_JM_API_KEY=your_jimeng_api_key_here
DOUBAO_JM_SECRET_KEY=your_jimeng_secret_key_here
```

**获取方式**：
- 访问 [火山引擎控制台](https://console.volcengine.com/)
- 开通即梦服务后获取密钥

---

#### 3. 通义千问 API（图片生成、视觉对话、音频识别、视频合成）

```env
# 通义千问 API 密钥
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**获取方式**：
- 访问 [阿里云控制台](https://dashscope.console.aliyun.com/)
- 开通 DashScope 服务后获取 API Key

---

#### 4. 智谱 API（智谱对话）

```env
# 智谱 API 密钥
GLM_API_KEY=your_glm_api_key_here
```

**获取方式**：
- 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
- 注册后获取 API Key

---

#### 5. DeepSeek API（DeepSeek 对话）

```env
# DeepSeek API 密钥
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**获取方式**：
- 访问 [DeepSeek 官网](https://platform.deepseek.com/)
- 注册后获取 API Key

---

#### 6. Gemini API（Gemini 生成）

```env
# Gemini API 密钥
GEMINI_API_KEY=your_gemini_api_key_here
```

**获取方式**：
- 访问 [Google AI Studio](https://aistudio.google.com/)
- 创建项目后获取 API Key

---

#### 7. Suno API（音乐生成）

```env
# Suno API 密钥
SUNO_API_KEY=your_suno_api_key_here
```

**获取方式**：
- 访问 [Suno 官网](https://suno.com/)
- 注册后获取 API Key

---

#### 8. Kling API（可灵视频生成）

```env
# Kling API 密钥
KLING_ACCESS_KEY=your_kling_access_key_here
KLING_SECRET_KEY=your_kling_secret_key_here
```

**获取方式**：
- 访问 [可灵 AI 官网](https://klingai.com/)
- 注册后获取 Access Key 和 Secret Key

---

#### 9. Luyala API（视频创建、对话补全）

```env
# Luyala API 密钥
LUYALA_API_KEY=your_luyala_api_key_here
```

**获取方式**：
- 联系 Luyala 服务提供商获取 API Key

---

#### 10. 火山引擎 API（语音、图片等）

```env
# 火山引擎 API 配置
VOLC_APP_ID=your_volc_app_id_here
VOLC_ACCESS_KEY=your_volc_access_key_here
VOLC_RESOURCE_ID=volc.speech.dialog
VOLC_APP_KEY=your_volc_app_key_here
```

**获取方式**：
- 访问 [火山引擎控制台](https://console.volcengine.com/)
- 创建语音或视觉服务后获取相关密钥

---

#### 11. 腾讯云 API（可选）

```env
# 腾讯云 API 密钥
TENCENT_SECRET_ID=your_tencent_secret_id_here
TENCENT_SECRET_KEY=your_tencent_secret_key_here
```

**获取方式**：
- 访问 [腾讯云控制台](https://console.cloud.tencent.com/)
- 开通相关服务后获取密钥

---

### 数据库配置

```env
# 数据库连接配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ihui_public

# 或使用完整的数据库 URL
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ihui_public?charset=utf8mb4
```

---

### 服务配置

```env
# API 服务配置
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
API_RELOAD=True
API_WORKERS=1

# CORS 配置
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=True
```

---

### Token 计费配置

```env
# Token 计费基础倍率
TOKEN_BASE_MULTIPLIER=2.0
```

**说明**：
- 所有接口的计费都会基于此倍率计算
- 实际扣减的 Token 数 = 费用 × TOKEN_BASE_MULTIPLIER

---

### 配置优先级

1. 环境变量（.env 文件）优先级最高
2. config.py 中的默认值优先级最低

**建议**：
- 敏感信息（如 API 密钥）使用环境变量配置
- 非敏感配置（如端口、超时时间）可直接在 config.py 中修改

---

### 配置检查清单

在启动项目前，请确保以下配置项已正确设置：

- [ ] 豆包 API 密钥（DOUBAO_API_KEY）
- [ ] 即梦 API 密钥（DOUBAO_JM_API_KEY, DOUBAO_JM_SECRET_KEY）
- [ ] 通义千问 API 密钥（DASHSCOPE_API_KEY）
- [ ] 智谱 API 密钥（GLM_API_KEY）
- [ ] DeepSeek API 密钥（DEEPSEEK_API_KEY）
- [ ] Gemini API 密钥（GEMINI_API_KEY）
- [ ] Suno API 密钥（SUNO_API_KEY）
- [ ] Kling API 密钥（KLING_ACCESS_KEY, KLING_SECRET_KEY）
- [ ] Luyala API 密钥（LUYALA_API_KEY）
- [ ] 火山引擎 API 配置（VOLC_APP_ID, VOLC_ACCESS_KEY, VOLC_APP_KEY）
- [ ] 数据库连接配置
- [ ] Token 计费倍率（TOKEN_BASE_MULTIPLIER）

## 错误码说明

- `0`: 成功
- `400`: 请求参数错误
- `402`: Token余额不足
- `408`: 请求超时
- `500`: 服务器内部错误

## 注意事项

1. 所有接口都需要有效的 `user_uuid` 参数用于计费
2. WebSocket接口支持心跳保持连接
3. 大部分接口会自动扣减用户Token
4. 所有操作都会记录到数据库
5. 支持通过公共Socket接收实时进度消息
