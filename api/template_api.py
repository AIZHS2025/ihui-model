#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 API 接口模板
用于快速创建新的 API 接口文件
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

# --- Pydantic模型定义 ---
class APIRequest(BaseModel):
    """通用API请求模型"""
    prompt: str = Field(..., description="提示词")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")
    zidingyican: Optional[list] = None

class APIResponse(BaseModel):
    """通用API响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[dict] = None

# --- 通用API路由模板 ---
def create_api_router(
    prefix: str,
    tag: str,
    endpoint_path: str,
    model_name: str,
    description: str
):
    """
    创建通用API路由的函数

    Args:
        prefix: 路由前缀
        tag: 路由标签
        endpoint_path: 端点路径
        model_name: 模型名称（用于日志）
        description: 接口描述

    Returns:
        APIRouter: 配置好的路由器
    """
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.post(endpoint_path)
    async def api_endpoint(request: APIRequest):
        """
        通用API端点处理函数

        Args:
            request: API请求

        Returns:
            APIResponse: 响应结果
        """
        logger.info(f"📥 ({model_name}) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

        # 检查用户token余额
        token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
        if not token_check.get("sufficient"):
            return APIResponse(success=False, message=token_check.get("reason", "Token余额不足"))

        # 发送开始消息到公共socket
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id=model_name,
            message={
                "event": "api_started",
                "prompt": request.prompt
            },
            chat_id=request.chat_id,
            event_name="api_started",
            status="run"
        )

        try:
            # 模拟API处理（实际项目中会调用真实API）
            # 这里只是示例，实际使用时需要根据具体接口实现

            # 模拟处理延迟
            await asyncio.sleep(0.5)

            # 发送完成消息
            await send_message_to_user_model(
                user_uuid=request.user_uuid,
                model_id=model_name,
                message={
                    "event": "api_completed",
                    "result": "处理完成（示例）"
                },
                chat_id=request.chat_id,
                event_name="api_completed",
                status="stop"
            )

            return APIResponse(success=True, message="处理完成（示例）", data={"result": "示例"})

        except HTTPException as e:
            logger.error(f"❌ ({model_name}) 处理失败: {str(e)}")
            return APIResponse(success=False, message=str(e))
        except Exception as e:
            logger.error(f"❌ ({model_name}) 处理异常: {str(e)}")
            return APIResponse(success=False, message=f"处理异常: {str(e)}")
