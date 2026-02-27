#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ihui_public API 模块
从 coze_zhs_py 项目提取的公共 API 接口
"""

from api.websocket_doubao_stream_simplified import router as doubao_router
from api.doubao_video_proxy import router as doubao_video_router
from api.dashscope_image_to_image import router as dashscope_image_to_image_router
from api.dashscope_image import router as dashscope_image_router
from api.stock_analyse import router as stock_analyse_router
from api.luyala_proxy import router as luyala_router
from api.dashscope_audio import router as dashscope_audio_router
from api.websocket_qwen_stream import router as qwen_stream_router
from api.websocket_qwen_stream_omni import router as qwen_omni_router
from api.volcengine_image_proxy import router as volcengine_image_router
from api.volcengine_jimeng31_proxy import router as volcengine_visual_router
from api.dashscope_vision import router as dashscope_vision_router
from api.websocket_zhipu_stream import router as zhipu_router
from api.doubao_image_proxy import router as doubao_image_router
from api.doubao_image_edit_proxy import router as doubao_image_edit_router
from api.dashscope_image_edit import router as dashscope_image_edit_router
from api.dashscope_video_synthesis import router as dashscope_video_router
from api.kling_video_synthesis import router as kling_router
from api.websocket_deepseek_stream import router as deepseek_router
from api.volcengine_jimeng31_proxy import router as jimeng_router
from api.suno_proxy import router as suno_router
from api.websocket_tts import router as tts_router

__all__ = [
    'doubao_router',
    'doubao_video_router',
    'dashscope_image_to_image_router',
    'dashscope_image_router',
    'stock_analyse_router',
    'luyala_router',
    'dashscope_audio_router',
    'qwen_stream_router',
    'qwen_omni_router',
    'volcengine_image_router',
    'volcengine_visual_router',
    'dashscope_vision_router',
    'zhipu_router',
    'doubao_image_router',
    'doubao_image_edit_router',
    'dashscope_image_edit_router',
    'dashscope_video_router',
    'kling_router',
    'deepseek_router',
    'jimeng_router',
    'suno_router',
    'tts_router',
]
