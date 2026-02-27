# 批量复制剩余 API 文件指南

## 📋 剩余需要复制的文件清单

根据原项目分析，还有以下 **13 个 API 文件**需要复制到 ihui_public 项目：

### WebSocket 接口（1个）
- ✅ websocket_doubao_stream_simplified.py

### HTTP 接口（12个）
- ✅ doubao_video_proxy.py
- ✅ doubao_image_proxy.py
- ✅ dashscope_image_to_image.py
- ✅ dashscope_image.py
- ✅ stock_analyse.py
- ✅ luyala_proxy.py
- ✅ dashscope_audio.py
- ✅ websocket_qwen_stream.py
- ✅ websocket_qwen_stream_omni.py
- ✅ volcengine_image_proxy.py
- ✅ volcengine_visual_proxy.py
- ✅ dashscope_vision.py
- ✅ websocket_zhipu_stream.py
- ✅ dashscope_image_edit.py
- ✅ dashscope_video_synthesis.py
- ✅ kling_video_synthesis.py
- ✅ websocket_deepseek_stream.py
- ✅ volcengine_jimeng31_proxy.py

## 📝 复制顺序建议

由于这些文件之间存在依赖关系，建议按照以下顺序复制：

### 第一批：核心工具和配置（已完成）
1. ✅ config.py
2. ✅ database.py
3. ✅ database_utils.py
4. ✅ api/token_utils.py
5. ✅ api/public_socket.py

### 第二批：主要 API 文件（已完成）
6. ✅ api/doubao_image_proxy.py
7. ✅ api/stock_analyse.py
8. ✅ api/dashscope_image_to_image.py
9. ✅ api/luyala_proxy.py
10. ✅ api/dashscope_audio.py
11. ✅ api/websocket_qwen_stream.py
12. ✅ api/websocket_qwen_stream_omni.py
13. ✅ api/volcengine_image_proxy.py
14. ✅ api/volcengine_visual_proxy.py
15. ✅ api/dashscope_vision.py
16. ✅ api/websocket_zhipu_stream.py
17. ✅ api/dashscope_image_edit.py
18. ✅ api/dashscope_video_synthesis.py
19. ✅ api/kling_video_synthesis.py
20. ✅ api/websocket_deepseek_stream.py
21. ✅ api/volcengine_jimeng31_proxy.py

### 第三批：WebSocket 和其他接口（待复制）
22. websocket_doubao_stream_simplified.py
23. dashscope_image.py
24. luyala_proxy.py
25. dashscope_audio.py
26. websocket_qwen_stream.py
27. websocket_qwen_stream_omni.py
28. volcengine_image_proxy.py
29. volcengine_visual_proxy.py
30. dashscope_vision.py
31. websocket_zhipu_stream.py
32. dashscope_image_edit.py
33. dashscope_video_synthesis.py
34. kling_video_synthesis.py
35. websocket_deepseek_stream.py
36. volcengine_jimeng31_proxy.py
37. doubao_socket_handler.py
38. doubao_image_edit_proxy.py
39. dashscope_image.py
40. luyala_proxy.py
41. dashscope_audio.py
42. websocket_qwen_stream.py
43. websocket_qwen_stream_omni.py
44. volcengine_image_proxy.py
45. volcengine_visual_proxy.py
46. dashscope_vision.py
47. websocket_zhipu_stream.py
48. dashscope_image_edit.py
49. dashscope_video_synthesis.py
50. kling_video_synthesis.py
51. websocket_deepseek_stream.py
52. volcengine_jimeng31_proxy.py

## 🔍 注意事项

1. **依赖检查**：复制每个文件前，先检查原项目中的依赖文件是否都已复制
2. **导入路径**：新项目中使用相对导入（`from ..config`），确保路径正确
3. **配置要求**：复制完成后，需要在 `config.py` 中配置相应的 API 密钥
4. **文件大小**：部分文件较大（如 stock_analyse.py 超过 900 行），复制时可能需要等待
5. **测试建议**：建议逐个测试接口，而不是批量测试所有接口

## 📌 复制进度

当前已完成：**21 个文件** / 总计 **34 个文件**

还需要复制：**13 个文件**

请告诉我是否继续复制剩余的文件？
