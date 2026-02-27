#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问图生图API接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict
import logging
import asyncio
import uuid
from datetime import datetime

from config import settings
from .token_utils import (
    check_user_token_sufficient,
    calculate_and_deduct_tokens_by_cost,
    upload_file_to_server,
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cozeZhsApi/dashscope", tags=["通义千问图生图"])

# --- Pydantic模型定义 ---
class CustomParameter(BaseModel):
    """自定义参数模型"""
    name: str = Field(..., description="参数名称")
    desc: str = Field(..., description="参数描述")
    value: Any = Field(..., description="参数值")

class ImageInfo(BaseModel):
    """图片信息模型"""
    imgUrl: str = Field(..., description="图片URL")
    originalUrl: Optional[str] = Field(None, description="原始图片URL")
    id: Optional[str] = Field(None, description="图片ID")
    width: Optional[int] = Field(None, description="图片宽度")
    height: Optional[int] = Field(None, description="图片高度")

class ImageToImageRequest(BaseModel):
    """图生图请求模型"""
    images: list = Field(..., description="作为参考的图片信息列表")
    prompt: str = Field(..., description="图像合成的文本提示")
    user_uuid: str = Field(..., description="用户唯一标识")
    chat_id: Optional[str] = Field(None, description="对话ID")
    zidingyican: Optional[list] = Field(default_factory=list, description="自定义参数列表")

class ImageToImageResponse(BaseModel):
    """图生图响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    image_urls: Optional[List[str]] = None
    total_tokens: Optional[int] = None
    lists: Optional[List[Dict[str, Any]]] = Field(default=None, description="顺序展示的文本和图片列表")

# --- API接口 ---
@router.post("/image-to-image", response_model=ImageToImageResponse)
async def generate_image_from_image(request: ImageToImageRequest):
    """
    根据输入图片和文本提示生成新图像
    请求路径 /cozeZhsApi/dashscope/image-to-image
    """
    logger.info(f"🎨 (图生图) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 验证用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 构建请求体
    content = [{"text": request.prompt}]

    # 处理自定义参数
    params = {}
    if request.zidingyican:
        for param in request.zidingyican:
            params[param.name] = param.value

    # 发送消息到公共socket
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="dashscope-image-to-image",
        message={
            "event": "image_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="image_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本，不实际调用DashScope API）
        # 在实际项目中，这里会调用DashScope API并轮询任务状态

        # 模拟返回结果
        image_urls = []

        # 发送完成消息到公共socket
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="dashscope-image-to-image",
            message={
                "event": "image_generation_completed",
                "image_urls": image_urls
            },
            chat_id=request.chat_id,
            event_name="image_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "image_urls": image_urls,
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
