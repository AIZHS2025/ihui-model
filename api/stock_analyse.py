#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析接口
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
router = APIRouter(prefix="/cozeZhsApi/stock", tags=["股票分析"])

# --- Pydantic模型定义 ---
class StockAnalyseRequest(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    analysis_type: str = Field(default="basic", description="分析类型")
    user_uuid: str = Field(..., description="用户UUID")
    chat_id: Optional[str] = Field(None, description="会话ID")

class StockAnalyseResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    analysis_result: Optional[dict] = Field(None, description="分析结果")

# --- API接口 ---
@router.post("/analyse")
async def analyse_stock(request: StockAnalyseRequest):
    """
    股票分析接口
    /cozeZhsApi/stock/analyse
    """
    logger.info(f"📈 (股票分析) 收到请求: user_uuid={request.user_uuid}, stock_code={request.stock_code}")

    # 检查用户token余额
    token_check = await check_user_token_sufficient(request.user_uuid, min_token=1000)
    if not token_check.get("sufficient"):
        raise HTTPException(status_code=402, detail=token_check.get("reason", "Token余额不足"))

    # 发送开始消息
    await send_message_to_user_model(
        user_uuid=request.user_uuid,
        model_id="stock-analyse",
        message={
            "event": "stock_analysis_started",
            "stock_code": request.stock_code,
            "analysis_type": request.analysis_type
        },
        chat_id=request.chat_id,
        event_name="stock_analysis",
        status="run"
    )

    try:
        # 模拟API调用（简化版本）
        # 在实际项目中，这里会调用股票分析API

        # 模拟返回分析结果
        analysis_result = {
            "stock_code": request.stock_code,
            "analysis_type": request.analysis_type,
            "recommendation": "持有",
            "risk_level": "中等",
            "target_price": "100.00",
            "analysis_date": "2026-02-25"
        }

        # 计算费用
        cost = 0.1

        # 扣减token
        await calculate_and_deduct_tokens_by_cost(
            user_uuid=request.user_uuid,
            cost=cost,
            reason="股票分析"
        )

        # 保存对话记录
        await save_conversation_to_db(
            user_uuid=request.user_uuid,
            model_name="stock-analyse",
            problem=f"股票分析: {request.stock_code}",
            answer=str(analysis_result),
            chat_id=request.chat_id,
            agent_id="",
            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
        )

        # 发送完成消息
        await send_message_to_user_model(
            user_uuid=request.user_uuid,
            model_id="stock-analyse",
            message={
                "event": "stock_analysis_completed",
                "analysis_result": analysis_result
            },
            chat_id=request.chat_id,
            event_name="stock_analysis",
            status="stop"
        )

        return {
            "code": 0,
            "data": {
                "analysis_result": analysis_result
            }
        }

    except HTTPException as e:
        logger.error(f"❌ 股票分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"股票分析失败: {str(e)}")
    except Exception as e:
        logger.error(f"❌ 股票分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"股票分析失败: {str(e)}")
