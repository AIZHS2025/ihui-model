# 剩余接口创建指南

## 📋 已完成的接口（15/28个）

### ✅ WebSocket 接口（5/5个）
1. ✅ `/cozeZhsApi/ws/doubao/streamDou` - 豆包流式对话
2. ✅ `/cozeZhsApi/ws/qwen/stream` - 通义千问流式对话
3. ✅ `/cozeZhsApi/ws/chatomni/stream` - 通义千问 Omni 流式对话
4. ✅ `/cozeZhsApi/ws/zhipu/stream` - 智谱流式对话
5. ✅ `/cozeZhsApi/ws/chatdeepseek/stream` - DeepSeek 流式对话

### ✅ HTTP 接口（10/23个）
1. ✅ `/cozeZhsApi/proxy/video-generation` - 豆包视频生成
2. ✅ `/cozeZhsApi/dashscope/image-to-image` - 通义千问图生图
3. ✅ `/cozeZhsApi/dashscope/image/generate/qwen-image-plus` - 通义千问图片生成
4. ✅ `/cozeZhsApi/dashscope/image/generate/qwen-image` - 通义千问图片生成
5. ✅ `/cozeZhsApi/dashscope/image/generate/wan2.5-t2i-preview` - 通义万相图片生成
6. ✅ `/cozeZhsApi/stock/analyse` - 股票分析
7. ✅ `/cozeZhsApi/luyala/video/create` - Luyala 视频创建
8. ✅ `/cozeZhsApi/luyala/chat/completions` - Luyala 对话补全
9. ✅ `/cozeZhsApi/dashscope/audio/recognize` - 通义千问音频识别
10. ✅ `/cozeZhsApi/proxy/doubao-seedream-generation` - 豆包 Seedream 图片生成

## ❌ 剩余需要创建的接口（13/28个）

### HTTP 接口（13个）
1. ❌ `/suno/generate/music` - Suno 音乐生成
   - 文件：suno_proxy.py
   - 路由前缀：/suno
   - 端点：/generate/music

2. ❌ `/cozeZhsApi/proxy/volcengine/image` - 火山引擎图片代理
   - 文件：volcengine_image_proxy.py
   - 路由前缀：/cozeZhsApi/proxy
   - 端点：/volcengine/image

3. ❌ `/gemini/3/generate` - Gemini 生成
   - 文件：gemini_proxy.py
   - 路由前缀：/gemini/3
   - 端点：/generate

4. ❌ `/cozeZhsApi/dashscope/vision/chat` - 通义千问视觉对话
   - 文件：dashscope_vision.py
   - 路由前缀：/cozeZhsApi/dashscope
   - 端点：/vision/chat

5. ❌ `/ws/tts-websocket` - TTS WebSocket
   - 文件：websocket_tts.py
   - 路由前缀：/ws
   - 端点：/tts-websocket

6. ❌ `/api/v1/dashscope/image/edit/simple` - 通义千问图片编辑
   - 文件：dashscope_image_edit.py
   - 路由前缀：/api/v1/dashscope/image
   - 端点：/edit/simple

7. ❌ `/cozeZhsApi/dashscope/video-synthesis/ws` - 通义千问视频合成
   - 文件：dashscope_video_synthesis.py
   - 路由前缀：/cozeZhsApi/dashscope
   - 端点：/video-synthesis/ws

8. ❌ `/cozeZhsApi/kling/generate/o1` - 可灵视频生成
   - 文件：kling_video_synthesis.py
   - 路由前缀：/cozeZhsApi/kling
   - 端点：/generate/o1

9. ❌ `/cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_tail_v30` - 即梦图片生成
   - 文件：volcengine_jimeng31_proxy.py
   - 路由前缀：/cozeZhsApi/proxy/volcengine/visual/images
   - 端点：/jimeng_i2v_first_tail_v30

10. ❌ `/cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_v30` - 即梦图片生成
    - 文件：volcengine_jimeng31_proxy.py
    - 路由前缀：/cozeZhsApi/proxy/volcengine/visual/images
    - 端点：/jimeng_i2v_first_v30

11. ❌ `/cozeZhsApi/proxy/volcengine/visual/jimeng_t2v_v30_1080p` - 即梦视频生成
    - 文件：volcengine_jimeng31_proxy.py
    - 路由前缀：/cozeZhsApi/proxy/volcengine/visual
    - 端点：/jimeng_t2v_v30_1080p

12. ❌ `/cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_recamera_v30` - 即梦图片生成
    - 文件：volcengine_jimeng31_proxy.py
    - 路由前缀：/cozeZhsApi/proxy/volcengine/visual/images
    - 端点：/jimeng_i2v_recamera_v30

## 📊 完成统计

- **已完成**：15/28 个接口（53.6%）
- **未完成**：13/28 个接口（46.4%）

## 🎯 需要创建的文件清单

1. suno_proxy.py
2. volcengine_image_proxy.py
3. gemini_proxy.py
4. dashscope_vision.py
5. websocket_tts.py
6. dashscope_image_edit.py
7. dashscope_video_synthesis.py
8. kling_video_synthesis.py
9. volcengine_jimeng31_proxy.py

## 💡 创建建议

由于这些文件结构相似，可以基于已创建的文件（如 dashscope_image.py）作为模板，快速创建剩余的文件。每个文件需要：

1. 定义 Pydantic 模型（Request 和 Response）
2. 创建 APIRouter 和路由
3. 实现接口处理函数
4. 添加 Token 验证和扣减逻辑
5. 添加消息发送和对话记录保存

## ⚠️ 注意事项

1. **路由前缀**：确保每个文件的路由前缀正确
2. **端点路径**：确保端点路径与要求的接口路径匹配
3. **模型名称**：使用正确的模型名称用于日志和计费
4. **费用计算**：根据实际API定价计算费用
5. **错误处理**：添加适当的错误处理和日志记录
