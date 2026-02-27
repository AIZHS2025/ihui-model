#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎即梦图片/视频生成接口
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
router = APIRouter(prefix="/cozeZhsApi/proxy/volcengine", tags=["火山引擎即梦"])

# --- Pydantic模型定义 ---
class JimengImageRequest(BaseModel):
    prompt: str = Field(..., description="生成提示词")
    model: str = Field(..., description="模型名称")
    image_url: Optional[str] = Field(None, description="输入图片URL（图生图）")
    size: str = Field(default="1024*1024", description="图片尺寸")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class JimengVideoRequest(BaseModel):
    prompt: str = Field(..., description="生成提示词")
    model: str = Field(..., description="模型名称")
    duration: int = Field(default=5, description="视频时长（秒）")
    resolution: str = Field(default="1080p", description="视频分辨率")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class JimengResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    result_url: Optional[str] = Field(None, description="生成的图片/视频URL")

# --- API接口 ---
@router.post("/visual/images/jimeng_i2v_first_tail_v30")
async def jimeng_i2v_first_tail_v30(request: JimengImageRequest):
    """
    即梦图生图接口（尾部增强）
    /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_tail_v30
    """
    logger.info(f"🎨 (即梦图生图-尾部增强) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="jimeng-i2v-tail",
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
        # 在实际项目中，这里会调用即梦API进行图生图
        result_url = f"https://example.com/jimeng_tail_{uuid.uuid4().hex[:8]}.jpg"

        # 计算费用
        cost = 0.15

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="即梦图生图-尾部增强"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="jimeng-i2v-tail",
            problem=request.prompt,
            answer=result_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="jimeng-i2v-tail",
            message={
                "event": "image_generation_completed",
                "result_url": result_url
            },
            chat_id=request.chat_id,
            event_name="image_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "result_url": result_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")

@router.post("/visual/images/jimeng_i2v_first_v30")
async def jimeng_i2v_first_v30(request: JimengImageRequest):
    """
    即梦图生图接口
    /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_first_v30
    """
    logger.info(f"🎨 (即梦图生图) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="jimeng-i2v",
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
        # 在实际项目中，这里会调用即梦API进行图生图
        result_url = f"https://example.com/jimeng_i2v_{uuid.uuid4().hex[:8]}.jpg"

        # 计算费用
        cost = 0.15

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="即梦图生图"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="jimeng-i2v",
            problem=request.prompt,
            answer=result_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="jimeng-i2v",
            message={
                "event": "image_generation_completed",
                "result_url": result_url
            },
            chat_id=request.chat_id,
            event_name="image_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "result_url": result_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")

@router.post("/visual/jimeng_t2v_v30_1080p")
async def jimeng_t2v_v30_1080p(request: JimengVideoRequest):
    """
    即梦文生视频接口（1080p）
    /cozeZhsApi/proxy/volcengine/visual/jimeng_t2v_v30_1080p
    """
    logger.info(f"🎬 (即梦文生视频) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="jimeng-t2v-1080p",
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
        # 在实际项目中，这里会调用即梦API进行文生视频
        result_url = f"https://example.com/jimeng_t2v_{uuid.uuid4().hex[:8]}.mp4"

        # 计算费用
        cost = 0.5 * request.duration

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="即梦文生视频"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="jimeng-t2v-1080p",
            problem=request.prompt,
            answer=result_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="jimeng-t2v-1080p",
            message={
                "event": "video_generation_completed",
                "result_url": result_url
            },
            chat_id=request.chat_id,
            event_name="video_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "result_url": result_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 文生视频失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文生视频失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 文生视频失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文生视频失败: {str(e)}")

@router.post("/visual/images/jimeng_i2v_recamera_v30")
async def jimeng_i2v_recamera_v30(request: JimengImageRequest):
    """
    即梦图生图接口（重相机）
    /cozeZhsApi/proxy/volcengine/visual/images/jimeng_i2v_recamera_v30
    """
    logger.info(f"🎨 (即梦图生图-重相机) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="jimeng-i2v-recamera",
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
        # 在实际项目中，这里会调用即梦API进行图生图
        result_url = f"https://example.com/jimeng_recamera_{uuid.uuid4().hex[:8]}.jpg"

        # 计算费用
        cost = 0.15

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="即梦图生图-重相机"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="jimeng-i2v-recamera",
            problem=request.prompt,
            answer=result_url,
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="jimeng-i2v-recamera",
            message={
                "event": "image_generation_completed",
                "result_url": result_url
            },
            chat_id=request.chat_id,
            event_name="image_generation",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "result_url": result_url
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 图生图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图生图失败: {str(e)}")
