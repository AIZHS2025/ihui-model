#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包 Seedream 图片生成代理接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging
import httpx
import asyncio
from datetime import datetime
import uuid

from config import settings
from .token_utils import (
    calculate_and_deduct_tokens_by_cost,
    check_user_token_sufficient,
    upload_file_to_server,
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cozeZhsApi/proxy", tags=["Doubao Proxy"])

# --- Pydantic模型定义 ---
class ImageRequest(BaseModel):
    prompt: str = Field(..., description="图片生成提示词")
    images: Optional[list] = None  # 图片列表
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = None
    # 自定义参数
    zidingyican: Optional[list] = None

# --- 辅助函数 ---
async def poll_task_status(task_id: str, headers: dict) -> dict:
    """轮询任务状态"""
    status_url = f"https://ark.cn-beijing.volces.com/api/v3/images/generations/tasks/{task_id}"
    timeout = 300  # 5分钟超时
    start_time = asyncio.get_event_loop().time()

    async with httpx.AsyncClient(timeout=60.0) as client:
        while asyncio.get_event_loop().time() - start_time < timeout:
            try:
                response = await client.get(status_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                status = data.get("status")

                if status == "succeeded":
                    logger.info(f"任务 {task_id} 已成功。")
                    return data
                elif status in ["failed", "cancelled"]:
                    logger.error(f"任务 {task_id} 失败，状态: {status}")
                    raise HTTPException(status_code=500, detail=f"图片生成失败，状态: {status}")

                logger.info(f"任务 {task_id} 状态: {status}。3秒后再次轮询...")
                await asyncio.sleep(3)

            except httpx.HTTPStatusError as e:
                logger.error(f"轮询任务 {task_id} 时发生HTTP错误: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail="轮询任务状态失败。")

    raise HTTPException(status_code=408, detail="轮询图片生成结果超时。")

# --- API接口 ---
@router.post("/doubao-seedream-generation")
async def doubao_seedream_generation(request: ImageRequest):
    """
    处理豆包Seedream图片生成任务（带轮询）
    /cozeZhsApi/proxy/doubao-seedream-generation
    """
    start_time = asyncio.get_event_loop().time()

    logger.info(f"📥 (豆包图片生成) 收到请求: user_uuid={request.user_uuid}, prompt={request.prompt[:50]}...")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 构建请求体
    request_body = {
        "prompt": request.prompt,
        "size": "1024*1024"
    }

    # 处理自定义参数
    if request.zidingyican:
        for param in request.zidingyican:
            if "name" in param and "value" in param:
                param_value = param["value"]
                if param_value == "" or param_value == []:
                    continue
                request_body[param["name"]] = param_value

    # 发送消息到公共socket
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="doubao-seedream",
        message={
            "event": "image_generation_started",
            "prompt": request.prompt
        },
        chat_id=request.chat_id,
        event_name="image_generation",
        status="run"
    )

    try:
        # 发起请求
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://ark.cn-beijing.volces.com/api/v3/images/generations",
                json=request_body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DOUBAO_API_KEY}"
                }
            )
            response.raise_for_status()
            result = response.json()

            task_id = result.get("output", {}).get("task_id")

            if not task_id:
                raise HTTPException(status_code=500, detail="未获取到任务ID")

            logger.info(f"✅ 图片生成任务已创建: task_id={task_id}")

            # 轮询任务状态
            final_result = await poll_task_status(task_id, {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.DOUBAO_API_KEY}"
            })

            # 提取图片URL
            image_url = final_result.get("output", {}).get("results", [{}])[0].get("url", "")

            if not image_url:
                raise HTTPException(status_code=500, detail="未获取到图片URL")

            logger.info(f"✅ 图片生成完成: {image_url}")

            # 计算费用并扣减token
            cost = 0.5  # 图片生成费用
            await calculate_and_deduct_tokens_by_cost(
                user_uuid=request.user_uuid,
                cost=cost,
                reason="豆包Seedream图片生成"
            )

            # 保存对话记录
            await save_conversation_to_db(
                user_uuid=request.user_uuid,
                model_name="doubao-seedream",
                problem=request.prompt,
                answer=image_url,
                chat_id=request.chat_id,
                agent_id="",
                field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
            )

            # 发送完成消息到公共socket
            await send_message_to_user_model(
                user_uuid=request.user_uuid,
                model_id="doubao-seedream",
                message={
                    "event": "image_generation_completed",
                    "image_url": image_url
                },
                chat_id=request.chat_id,
                event_name="image_generation",
                status="stop",
                total_tokens=int(cost * settings.TOKEN_BASE_MULTIPLIER)
            )

            return {
                "code": 0,
                "data": {
                    "image_url": image_url,
                    "task_id": task_id
                }
            }

    except httpx.HTTPStatusError as e:
        logger.error(f"❌ HTTP错误: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"请求失败: {e.response.text}")
    except Exception as e:
        logger.error(f"❌ 图片生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图片生成失败: {str(e)}")
