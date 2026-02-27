#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ihui_public 配置文件
从 coze_zhs_py 项目提取的公共 API 接口配置
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    """
    应用程序配置类
    统一管理环境变量配置、API配置、密钥配置和启动端口路径等
    """

    # API服务配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True
    API_RELOAD: bool = True
    API_WORKERS: int = 1
    API_TITLE: str = "Ihui Public API服务"
    API_DESCRIPTION: str = "公共API接口服务"
    API_VERSION: str = "1.0.0"

    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # 数据库配置
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False

    # 数据库连接池配置
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = True

    # 超时配置（秒）
    REQUEST_TIMEOUT: float = 600.0
    CONNECT_TIMEOUT: float = 5.0
    MAX_CONNECTIONS: int = 1000
    MAX_KEEPALIVE_CONNECTIONS: int = 100
    WEBSOCKET_TIMEOUT: int = 900

    # 会话存储配置
    SESSION_SECRET_KEY: str = "ihui_public_secret_key"
    SESSION_EXPIRE_MINUTES: int = 60

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024

    # API密钥配置 - 请根据实际环境修改

    # 豆包API配置
    DOUBAO_API_KEY: Optional[str] = None
    DOUBAO_MODEL_URL: str = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    DOUBAO_IMAGE_API_URL: str = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

    # 即梦API配置
    DOUBAO_JM_API_KEY: Optional[str] = None
    DOUBAO_JM_SECRET_KEY: Optional[str] = None

    # 通义千问API配置
    DASHSCOPE_API_KEY: Optional[str] = None
    DASHSCOPE_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
    DASHSCOPE_TIMEOUT: int = 30
    DASHSCOPE_MAX_RETRIES: int = 3

    # 智谱API配置
    GLM_API_KEY: Optional[str] = None

    # DeepSeek API配置
    DEEPSEEK_API_KEY: Optional[str] = None

    # Gemini API配置
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v3beta/models/gemini-3:generateContent"

    # Suno API配置
    SUNO_API_KEY: Optional[str] = None
    SUNO_API_URL: str = "https://api.suno.ai/v1/generate/music"

    # Kling API配置（可灵视频生成）
    KLING_ACCESS_KEY: Optional[str] = None
    KLING_SECRET_KEY: Optional[str] = None
    KLING_MODEL_DOMAIN: str = "https://api-beijing.klingai.com"

    # Luyala API配置
    LUYALA_API_KEY: Optional[str] = None

    # 火山引擎API配置
    VOLC_APP_ID: Optional[str] = None
    VOLC_ACCESS_KEY: Optional[str] = None
    VOLC_RESOURCE_ID: str = "volc.speech.dialog"
    VOLC_APP_KEY: Optional[str] = None

    # 腾讯云API配置
    TENCENT_SECRET_ID: Optional[str] = None
    TENCENT_SECRET_KEY: Optional[str] = None

    # 豆包流式响应事件名称配置
    DOUBAO_STREAM_EVENT_THINKING: str = "conversation.message.delta"
    DOUBAO_STREAM_EVENT_COMPLETED: str = "conversation.chat.completed"

    # 统一错误事件名称
    COMMON_STREAM_EVENT_ERROR: str = "system.error"

    # Token计算配置
    TOKEN_BASE_MULTIPLIER: float = 2.0

    # WebSocket超时配置
    WEBSOCKET_TIMEOUT: int = 900

    # 文件上传配置
    FILE_UPLOAD_BASE_URL: str = "https://bsm.aizhs.top/prod-api"
    FILE_UPLOAD_BASE64_ENDPOINT: str = "/file/uploadByBase64"
    FILE_UPLOAD_TIMEOUT: int = 60
    FILE_UPLOAD_MAX_SIZE: int = 10 * 1024 * 1024

settings = Settings()
