#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 生成接口
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
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gemini/3", tags=["Gemini生成"])

# --- Pydantic模型定义 ---
class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="生成提示词")
    model: str = Field(default="gemini-3", description="模型名称")
    temperature: float = Field(default=0.7, description="温度参数")
    max_tokens: int = Field(default=1000, description="最大token数")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class GenerationResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    content: Optional[str] = Field(None, description="生成内容")

# --- API接口 ---
@router.post("/generate")
async def generate_content(request: GenerationRequest):
    """
    Gemini 生成接口
    /gemini/3/generate
    """
    logger.info(f"🤖 (Gemini生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="gemini-3",
        message={
            "event": "generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="generation",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用Gemini API进行内容生成

        # 模拟返回内容
        content = f"这是对 '{request.prompt}' 的Gemini生成内容。"

        # 计算费用
        cost = 0.05

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="Gemini生成"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="gemini-3",
            problem=request.prompt,
            answer=content,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="gemini-3",
            message={
                "event": "generation_completed",
                "content": content
            },
            chat_id=request.chat_id,
            event_name="generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "content": content
            }
        }

    except HTTPException as e:
        logger.error(f"❌ Gemini生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Gemini生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")
