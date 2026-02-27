#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问视觉对话接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
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
router = APIRouter(prefix="/cozeZhsApi/dashscope", tags=["通义千问视觉对话"])

# --- Pydantic模型定义 ---
class VisionRequest(BaseModel):
    prompt: str = Field(..., description="对话提示词")
    image_urls: List[str] = Field(..., description="图片URL列表")
    model: str = Field(default="qwen-vl-max", description="模型名称")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class VisionResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    content: Optional[str] = Field(None, description="对话内容")

# --- API接口 ---
@router.post("/vision/chat")
async def vision_chat(request: VisionRequest):
    """
    通义千问视觉对话接口
    /cozeZhsApi/dashscope/vision/chat
    """
    logger.info(f"👁️ (通义千问视觉对话) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="qwen-vl-max",
        message={
            "event": "vision_chat_started",
            "prompt": request.prompt,
            "image_count": len(request.image_urls)
        },
        chat_id=request.chat_id,
        event_name="vision_chat",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用通义千问视觉API进行对话

        # 模拟返回内容
        content = f"这是对 '{request.prompt}' 的视觉对话回复，基于 {len(request.image_urls)} 张图片。"

        # 计算费用
        cost = 0.08 * len(request.image_urls)

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="通义千问视觉对话"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="qwen-vl-max",
            problem=request.prompt,
            answer=content,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="qwen-vl-max",
            message={
                "event": "vision_chat_completed",
                "content": content
            },
            chat_id=request.chat_id,
            event_name="vision_chat",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "content": content
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 视觉对话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视觉对话失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 视觉对话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"视觉对话失败: {str(e)}")
