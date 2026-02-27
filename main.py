#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ihui_public 主程序入口
从 coze_zhs_py 项目提取的公共 API 接口服务
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api import (
    doubao_router,
    doubao_video_router,
    dashscope_image_to_image_router,
    dashscope_image_router,
    stock_analyse_router,
    luyala_router,
    dashscope_audio_router,
    qwen_stream_router,
    qwen_omni_router,
    volcengine_image_router,
    volcengine_visual_router,
    dashscope_vision_router,
    zhipu_router,
    doubao_image_router,
    doubao_image_edit_router,
    dashscope_image_edit_router,
    dashscope_video_router,
    kling_router,
    deepseek_router,
    jimeng_router,
    suno_router,
    tts_router,
)

# 创建FastAPI应用
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.API_DEBUG,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 注册所有路由
app.include_router(doubao_router)
app.include_router(doubao_video_router)
app.include_router(dashscope_image_to_image_router)
app.include_router(dashscope_image_router)
app.include_router(stock_analyse_router)
app.include_router(luyala_router)
app.include_router(dashscope_audio_router)
app.include_router(qwen_stream_router)
app.include_router(qwen_omni_router)
app.include_router(volcengine_image_router)
app.include_router(volcengine_visual_router)
app.include_router(dashscope_vision_router)
app.include_router(zhipu_router)
app.include_router(doubao_image_router)
app.include_router(doubao_image_edit_router)
app.include_router(dashscope_image_edit_router)
app.include_router(dashscope_video_router)
app.include_router(kling_router)
app.include_router(deepseek_router)
app.include_router(jimeng_router)
app.include_router(suno_router)
app.include_router(tts_router)

# 根路径
@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "message": "ihui_public API服务已启动"
    }

if __name__ == "__main__":
    # 启动服务
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=settings.API_WORKERS,
    )
