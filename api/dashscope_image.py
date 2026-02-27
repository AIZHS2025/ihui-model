#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问图片生成接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging
import uuid

from config import settings
from .token_utils import (
    check_user_token_sufficient,
    calculate_and_deduct_tokens_by_cost,
    upload_file_to_server,
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cozeZhsApi/dashscope/image", tags=["通义千问图片生成"])

# --- Pydantic模型定义 ---
class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="图片生成提示词")
    model: str = Field(default="qwen-image-plus", description="模型名称")
    size: str = Field(default="1024*1024", description="图片尺寸")
    n: int = Field(default=1, description="生成图片数量")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class ImageGenerationResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    image_urls: Optional[list] = Field(None, description="生成的图片URL列表")

# --- API接口 ---
@router.post("/generate/qwen-image-plus")
async def generate_qwen_image_plus(request: ImageGenerationRequest):
    """
    通义千问图片生成接口（Plus版本）
    /cozeZhsApi/dashscope/image/generate/qwen-image-plus
    """
    logger.info(f"🎨 (通义千问图片生成Plus) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="qwen-image-plus",
        message={
            "event": "image_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="image_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用通义千问API进行图片生成

        # 模拟返回图片URL
        image_urls = [
            f"https://example.com/qwen_image_{uuid.uuid4().hex[:8]}.jpg"
            for _ in range(request.n)
        ]

        # 计算费用
        cost = 0.2 * request.n

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义千问图片生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="qwen-image-plus",
            problem=request.prompt,
            answer=",".join(image_urls),
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="qwen-image-plus",
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
                "image_urls": image_urls
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")

@router.post("/generate/qwen-image")
async def generate_qwen_image(request: ImageGenerationRequest):
    """
    通义千问图片生成接口（标准版）
    /cozeZhsApi/dashscope/image/generate/qwen-image
    """
    logger.info(f"🎨 (通义千问图片生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="qwen-image",
        message={
            "event": "image_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="image_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用通义千问API进行图片生成

        # 模拟返回图片URL
        image_urls = [
            f"https://example.com/qwen_image_{uuid.uuid4().hex[:8]}.jpg"
            for _ in range(request.n)
        ]

        # 计算费用
        cost = 0.15 * request.n

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义千问图片生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="qwen-image",
            problem=request.prompt,
            answer=",".join(image_urls),
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="qwen-image",
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
                "image_urls": image_urls
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")

@router.post("/generate/wan2.5-t2i-preview")
async def generate_wan_image(request: ImageGenerationRequest):
    """
    通义万相图片生成接口
    /cozeZhsApi/dashscope/image/generate/wan2.5-t2i-preview
    """
    logger.info(f"🎨 (通义万相图片生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="wan2.5-t2i-preview",
        message={
            "event": "image_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="image_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用通义万相API进行图片生成

        # 模拟返回图片URL
        image_urls = [
            f"https://example.com/wan_image_{uuid.uuid4().hex[:8]}.jpg"
            for _ in range(request.n)
        ]

        # 计算费用
        cost = 0.18 * request.n

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义万相图片生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="wan2.5-t2i-preview",
            problem=request.prompt,
            answer=",".join(image_urls),
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="wan2.5-t2i-preview",
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
                "image_urls": image_urls
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")
