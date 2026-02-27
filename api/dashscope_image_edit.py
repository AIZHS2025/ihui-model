#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问图片编辑接口
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
router = APIRouter(prefix="/api/v1/dashscope/image", tags=["通义千问图片编辑"])

# --- Pydantic模型定义 ---
class ImageEditRequest(BaseModel):
    prompt: str = Field(..., description="编辑提示词")
    image_url: str = Field(..., description="原始图片URL")
    model: str = Field(default="qwen-image-edit", description="模型名称")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class ImageEditResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    edited_image_url: Optional[str] = Field(None, description="编辑后的图片URL")

# --- API接口 ---
@router.post("/edit/simple")
async def edit_image_simple(request: ImageEditRequest):
    """
    通义千问图片编辑接口（简单版）
    /api/v1/dashscope/image/edit/simple
    """
    logger.info(f"🎨 (通义千问图片编辑) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="qwen-image-edit",
        message={
            "event": "image_edit_started",
            "prompt": request.prompt,
            "original_image": request.image_url
        },
        chat_id=request.chat_id,
        event_name="image_edit",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用通义千问API进行图片编辑

        # 模拟返回编辑后的图片URL
        edited_image_url = f"https://example.com/qwen_edited_{uuid.uuid4().hex[:8]}.jpg"

        # 计算费用
        cost = 0.15

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义千问图片编辑"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="qwen-image-edit",
            problem=request.prompt,
            answer=edited_image_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="qwen-image-edit",
            message={
                "event": "image_edit_completed",
                "edited_image_url": edited_image_url
            },
            chat_id=request.chat_id,
            event_name="image_edit",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "edited_image_url": edited_image_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图片编辑失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片编辑失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图片编辑失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片编辑失败: {str(e)}")
