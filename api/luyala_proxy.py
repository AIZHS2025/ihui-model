#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luyala 视频创建/对话补全接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
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
router = APIRouter(prefix="/cozeZhsApi/luyala", tags=["Luyala"])

# --- Pydantic模型定义 ---
class VideoRequest(BaseModel):
    prompt: str = Field(..., description="视频生成提示词")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class VideoCompletionRequest(BaseModel):
    prompt: str = Field(..., description="对话补全提示词")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

# --- API接口 ---
@router.post("/video/create")
async def luyala_video_create(request: VideoRequest):
    """
    Luyala 视频创建接口
    /cozeZhsApi/luyala/video/create
    """
    logger.info(f"📥 (Luyala视频创建) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="luyala-video",
        message={
            "event": "video_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="video_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用Luyala API进行视频生成

        # 模拟返回视频URL
        video_url = f"https://example.com/luyala_video_{uuid.uuid4().hex[:8]}.mp4"

        # 计算费用
        cost = 1.0

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="Luyala视频生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="luyala-video",
            problem=request.prompt,
            answer=video_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="luyala-video",
            message={
                "event": "video_generation_completed",
                "video_url": video_url
            },
            chat_id=request.chat_id,
            event_name="video_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "video_url": video_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ Luyala视频生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Luyala视频生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")

@router.post("/chat/completions")
async def luyala_chat_completions(request: VideoCompletionRequest):
    """
    Luyala 对话补全接口
    /cozeZhsApi/luyala/chat/completions
    """
    logger.info(f"💬 (Luyala对话补全) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="luyala-chat",
        message={
            "event": "chat_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="chat",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用Luyala API进行对话补全

        # 模拟返回结果
        completion_text = f"这是对 '{request.prompt}' 的对话补全结果。"

        # 计算费用
        cost = 0.05

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="Luyala对话补全"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="luyala-chat",
            problem=request.prompt,
            answer=completion_text,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="luyala-chat",
            message={
                "event": "chat_completed",
                "completion": completion_text
            },
            chat_id=request.chat_id,
            event_name="chat",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "completion": completion_text
            }
        }

    except HTTPException as e:
        logger.error(f"❌ Luyala对话补全失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对话补全失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Luyala对话补全失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对话补全失败: {str(e)}")
