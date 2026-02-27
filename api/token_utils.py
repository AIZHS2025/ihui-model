#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 工具模块
从 coze_zhs_py 项目提取的公共 API 接口 Token 工具
"""

import asyncio
import logging
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from config import settings
from database import get_db

logger = logging.getLogger(__name__)

async def check_user_token_sufficient(user_uuid: str, min_token: int = 1000) -> Dict[str, Any]:
    """
    验证用户token余额是否充足

    Args:
        user_uuid: 用户唯一标识
        min_token: 最低要求token数量，默认为1000

    Returns:
        Dict[str, Any]: 包含验证结果的字典
    """
    if not user_uuid:
        logger.warning("⚠️ 无法验证token余额: 用户UUID为空")
        return {
            "sufficient": False,
            "reason": "用户UUID为空",
            "user_uuid": None,
            "current_balance": 0,
            "min_token": min_token
        }

    logger.info(f"🔍 验证用户token余额: user_uuid={user_uuid}, 最低要求={min_token}")

    # 这里简化处理，实际项目中需要连接数据库验证
    # 暂时返回成功，后续可以根据需要添加数据库验证
    return {
        "sufficient": True,
        "reason": "token余额充足",
        "user_uuid": user_uuid,
        "current_balance": 0,
        "min_token": min_token
    }

async def deduct_user_tokens(user_uuid: str, tokens_to_deduct: int, reason: str = None) -> Dict[str, Any]:
    """
    从用户余额中扣减tokens的通用方法

    Args:
        user_uuid: 用户唯一标识
        tokens_to_deduct: 需要扣减的tokens数量
        reason: 扣减原因（可选）

    Returns:
        Dict[str, Any]: 包含操作结果的字典
    """
    if not user_uuid:
        logger.warning("⚠️ 无法扣减tokens: 用户UUID为空")
        return {
            "success": False,
            "reason": "用户UUID为空",
            "tokens_deducted": 0
        }

    logger.info(f"💰 扣减用户tokens: user_uuid={user_uuid}, 数量={tokens_to_deduct}, 原因={reason}")

    # 这里简化处理，实际项目中需要连接数据库扣减
    # 暂时返回成功，后续可以根据需要添加数据库扣减
    return {
        "success": True,
        "reason": "扣减成功",
        "tokens_deducted": tokens_to_deduct
    }

async def calculate_and_deduct_tokens_by_cost(
    user_uuid: str,
    cost: float,
    reason: str = None
) -> Dict[str, Any]:
    """
    根据费用计算并扣减tokens

    Args:
        user_uuid: 用户唯一标识
        cost: 费用（元）
        reason: 扣减原因（可选）

    Returns:
        Dict[str, Any]: 包含操作结果的字典
    """
    if not user_uuid:
        logger.warning("⚠️ 无法计算并扣减tokens: 用户UUID为空")
        return {
            "success": False,
            "reason": "用户UUID为空",
            "tokens_deducted": 0
        }

    # 计算tokens数量（费用 * 基础倍率）
    tokens_to_deduct = int(cost * settings.TOKEN_BASE_MULTIPLIER)

    logger.info(f"💰 计算并扣减tokens: user_uuid={user_uuid}, 费用={cost}元, tokens={tokens_to_deduct}")

    # 执行扣减
    result = await deduct_user_tokens(user_uuid, tokens_to_deduct, reason)

    return result

async def download_file_from_url(url: str, timeout: int = 30) -> Optional[bytes]:
    """
    从URL下载文件

    Args:
        url: 文件URL
        timeout: 超时时间（秒）

    Returns:
        bytes: 文件内容，失败返回None
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
    except Exception as e:
        logger.error(f"❌ 下载文件失败: {url}, 错误: {e}")
        return None

async def upload_file_to_server(
    file_content: bytes,
    filename: str,
    logger_obj: logging.Logger = None
) -> Optional[str]:
    """
    上传文件到服务器

    Args:
        file_content: 文件内容（bytes）
        filename: 文件名
        logger_obj: 日志对象

    Returns:
        str: 上传后的文件URL，失败返回None
    """
    try:
        upload_url = f"{settings.FILE_UPLOAD_BASE_URL}{settings.FILE_UPLOAD_BASE64_ENDPOINT}"

        async with httpx.AsyncClient(timeout=settings.FILE_UPLOAD_TIMEOUT) as client:
            files = {
                'file': (filename, file_content)
            }
            response = await client.post(upload_url, files=files)
            response.raise_for_status()

            result = response.json()
            file_url = result.get('data', {}).get('url', '')

            if logger_obj:
                logger_obj.info(f"✅ 文件上传成功: {filename}, URL: {file_url}")
            else:
                logger.info(f"✅ 文件上传成功: {filename}, URL: {file_url}")

            return file_url
    except Exception as e:
        if logger_obj:
            logger_obj.error(f"❌ 文件上传失败: {filename}, 错误: {e}")
        else:
            logger.error(f"❌ 文件上传失败: {filename}, 错误: {e}")
        return None

async def save_conversation_to_db(
    user_uuid: str,
    model_name: str,
    problem: str,
    answer: str,
    chat_id: str = "",
    agent_id: str = "",
    summary: str = None,
    field1: str = None,
    agent_url: str = None
) -> bool:
    """
    保存对话记录到数据库

    Args:
        user_uuid: 用户唯一标识
        model_name: 模型名称
        problem: 用户问题
        answer: 模型回答
        chat_id: 聊天ID
        agent_id: 智能体ID
        summary: 思考过程
        field1: 自定义字段1
        agent_url: 文件URL

    Returns:
        bool: 保存是否成功
    """
    try:
        db = next(get_db())

        # 构建SQL语句
        insert_sql = text("""
            INSERT INTO zhs_conversation_history 
            (user_uuid, model_name, problem, answer, chat_id, agent_id, summary, field1, agent_url, created_at)
            VALUES 
            (:user_uuid, :model_name, :problem, :answer, :chat_id, :agent_id, :summary, :field1, :agent_url, NOW())
        """)

        params = {
            'user_uuid': user_uuid,
            'model_name': model_name,
            'problem': problem,
            'answer': answer,
            'chat_id': chat_id,
            'agent_id': agent_id,
            'summary': summary,
            'field1': field1,
            'agent_url': agent_url
        }

        db.execute(insert_sql, params)
        db.commit()

        logger.info(f"✅ 对话记录保存成功: user_uuid={user_uuid}, chat_id={chat_id}")
        return True
    except Exception as e:
        logger.error(f"❌ 保存对话记录失败: {str(e)}")
        return False
