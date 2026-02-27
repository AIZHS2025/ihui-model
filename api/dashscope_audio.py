#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问音频识别API接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging
import uuid
import httpx

from config import settings
from .token_utils import (
    check_user_token_sufficient,
    calculate_and_deduct_tokens_by_cost,
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cozeZhsApi/dashscope", tags=["通义千问音频识别"])

# --- Pydantic模型定义 ---
class AudioRecognitionRequest(BaseModel):
    """音频识别请求模型"""
    audio_url: str = Field(..., description="音频文件的URL地址")
    model: str = Field(default="qwen3-asr-flash", description="语音识别模型名称")
    language: Optional[str] = Field(None, description="指定音频语言")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="对话ID")
    system_prompt: Optional[str] = Field("", description="系统提示词")

class AudioRecognitionResponse(BaseModel):
    """音频识别响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    transcription: Optional[str] = Field(None, description="识别结果")
    language_detected: Optional[str] = Field(None, description="检测到的语言")
    total_tokens: Optional[int] = Field(None, description="消耗的token")

# --- API接口 ---
@router.post("/audio/recognize", response_model=AudioRecognitionResponse)
async def recognize_audio(request: AudioRecognitionRequest):
    """
    音频识别接口
    /cozeZhsApi/dashscope/audio/recognize

    使用通义千问的语音识别模型识别音频内容
    """
    logger.info(f"🎵 (音频识别) 收到请求: user_uuid={request.user_uuid}, audio_url={request.audio_url[:50]}...")

    # 验证用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        return AudioRecognitionResponse(
            success=False,
            message=token_check.get("reason", "Token余额不足")
        )

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="dashscope-audio",
        message={
            "event": "audio_recognition_started",
            "audio_url": request.audio_url
        },
        chat_id=request.chat_id,
        event_name="audio_recognition",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用DashScope API进行音频识别

        # 模拟识别结果
        transcription = f"这是对音频 '{request.audio_url}' 的识别结果。"
        language_detected = request.language or "zh"

        # 计算费用（根据音频时长）
        cost = 0.05

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义千问音频识别"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="dashscope-audio",
            problem=f"音频识别: {request.audio_url}",
            answer=transcription,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="dashscope-audio",
            message={
                "event": "audio_recognition_completed",
                "transcription": transcription
            },
            chat_id=request.chat_id,
            event_name="audio_recognition",
            status="stop"
        )

        return AudioRecognitionResponse(
            success=True,
            message="识别完成",
            transcription=transcription,
            language_detected=language_detected,
            total_tokens=int(cost * settings.TOKEN_BASE_MULTIPLIER)
        )

    except HTTPException as e:
        logger.error(f"❌ 音频识别失败: {str(e)}")
        return AudioRecognitionResponse(
            success=False,
            message=f"音频识别失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"❌ 音频识别失败: {str(e)}")
        return AudioRecognitionResponse(
            success=False,
            message=f"音频识别失败: {str(e)}"
        )
