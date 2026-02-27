#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可灵视频生成接口
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
router = APIRouter(prefix="/cozeZhsApi/kling", tags=["可灵视频生成"])

# --- Pydantic模型定义 ---
class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., description="视频生成提示词")
    model: str = Field(default="kling-o1", description="模型名称")
    duration: int = Field(default=5, description="视频时长（秒）")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class VideoGenerationResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    video_url: Optional[str] = Field(None, description="生成的视频URL")

# --- API接口 ---
@router.post("/generate/o1")
async def generate_video_o1(request: VideoGenerationRequest):
    """
    可灵视频生成接口
    /cozeZhsApi/kling/generate/o1
    """
    logger.info(f"🎬 (可灵视频生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="kling-o1",
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
        # 在实际项目中，这里会调用可灵API进行视频生成

        # 模拟返回视频URL
        video_url = f"https://example.com/kling_video_{uuid.uuid4().hex[:8]}.mp4"

        # 计算费用
        cost = 0.5 * request.duration

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="可灵视频生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="kling-o1",
            problem=request.prompt,
            answer=video_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="kling-o1",
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
        logger.error(f"❌ 视频生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 视频生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")
