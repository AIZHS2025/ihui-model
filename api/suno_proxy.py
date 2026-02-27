#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suno 音乐生成接口
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
router = APIRouter(prefix="/suno", tags=["Suno音乐生成"])

# --- Pydantic模型定义 ---
class MusicGenerationRequest(BaseModel):
    prompt: str = Field(..., description="音乐生成提示词")
    model: str = Field(default="suno-v3", description="模型名称")
    duration: int = Field(default=30, description="音乐时长（秒）")
    style: Optional[str] = Field(None, description="音乐风格")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class MusicGenerationResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    music_url: Optional[str] = Field(None, description="生成的音乐URL")

# --- API接口 ---
@router.post("/generate/music")
async def generate_music(request: MusicGenerationRequest):
    """
    Suno 音乐生成接口
    /suno/generate/music
    """
    logger.info(f"🎵 (Suno音乐生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="suno-v3",
        message={
            "event": "music_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="music_generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用Suno API进行音乐生成

        # 模拟返回音乐URL
        music_url = f"https://example.com/suno_music_{uuid.uuid4().hex[:8]}.mp3"

        # 计算费用
        cost = 0.3 * (request.duration / 30)

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="Suno音乐生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="suno-v3",
            problem=request.prompt,
            answer=music_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="suno-v3",
            message={
                "event": "music_generation_completed",
                "music_url": music_url
            },
            chat_id=request.chat_id,
            event_name="music_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "music_url": music_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 音乐生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音乐生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 音乐生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音乐生成失败: {str(e)}")
