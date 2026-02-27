#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问 Omni 流式对话接口
从 coze_zhs_py 项目提取
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict, Optional
import json
import asyncio
import logging
import uuid
from datetime import datetime

from config import settings
from .token_utils import (
    check_user_token_sufficient,
    calculate_and_deduct_tokens_by_cost,
    save_conversation_to_db,
)
from .public_socket import send_message_to_user_model

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cozeZhsApi/ws", tags=["WebSocket通义千问Omni流式"])

# --- 连接管理器 ---
class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_info: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """建立WebSocket连接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_info[client_id] = {
            "connected_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": 0
        }
        logger.info(f"WebSocket连接已建立: {client_id}")

    def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.connection_info:
            del self.connection_info[client_id]
        logger.info(f"WebSocket连接已断开: {client_id}")

    async def send_message(self, client_id: str, message: dict):
        """发送消息到指定客户端"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(json.dumps(message, ensure_ascii=False))

                # 更新连接信息
                if client_id in self.connection_info:
                    self.connection_info[client_id]["last_activity"] = datetime.now().isoformat()
                    self.connection_info[client_id]["message_count"] += 1

                # 确保消息立即发送到客户端
                await asyncio.sleep(0)

                return True
            except Exception as e:
                logger.error(f"发送消息失败 {client_id}: {e}")
                self.disconnect(client_id)
                return False
        return False

# 全局连接管理器
manager = ConnectionManager()

# --- WebSocket接口 ---
@router.websocket("/chatomni/stream")
async def websocket_qwen_omni_stream(
    websocket: WebSocket,
    client_id: Optional[str] = Query(None, description="客户端ID"),
    user_uuid: Optional[str] = Query(None, description="用户UUID")
):
    """
    通义千问 Omni 流式对话接口
    /cozeZhsApi/ws/chatomni/stream
    """
    # 生成客户端ID（如果未提供）
    if not client_id:
        client_id = f"qwen_omni_{uuid.uuid4().hex[:8]}"

    logger.info(f"收到通义千问Omni WebSocket流式连接请求: {client_id}")

    try:
        # 接受连接
        await manager.connect(websocket, client_id)

        # 发送连接成功消息
        await manager.send_message(client_id, {
            "code": 200,
            "msg": "success",
            "data": {
                "id": client_id,
                "conversation_id": "",
                "bot_id": "qwen-omni",
                "role": "system",
                "type": "connected",
                "content": "WebSocket连接已建立",
                "content_type": "text",
                "chat_id": "",
                "created_at": datetime.now().isoformat()
            },
            "event": "system.connected"
        })

        # 消息处理循环
        timeout = 300  # 5分钟超时
        while True:
            try:
                # 接收消息，带超时
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=timeout
                )

                # 解析消息
                try:
                    message = json.loads(data)
                except json.JSONDecodeError as e:
                    error_message = {
                        "code": 400,
                        "msg": "error",
                        "data": {
                            "type": "error",
                            "content": f"JSON格式错误: {str(e)}"
                        },
                        "event": "system.error"
                    }
                    await manager.send_message(client_id, error_message)
                    continue

                # 处理不同类型的消息
                message_type = message.get("type", "")

                # 聊天请求
                if message_type == "chat":
                    chat_data = message.get("data", {})
                    prompt = chat_data.get("prompt", "")
                    chat_id = chat_data.get("chat_id", "")

                    # 验证用户token余额
                    if user_uuid:
                        token_check = await check_user_token_sufficient(user_uuid)
                        if not token_check.get("sufficient"):
                            error_message = {
                                "code": 402,
                                "msg": "error",
                                "data": {
                                    "type": "error",
                                    "content": token_check.get("reason", "Token余额不足")
                                },
                                "event": "system.error"
                            }
                            await manager.send_message(client_id, error_message)
                            continue

                    # 发送开始生成消息
                    await manager.send_message(client_id, {
                        "code": 200,
                        "msg": "success",
                        "data": {
                            "type": "stream_start",
                            "content": "开始生成",
                            "chat_id": chat_id
                        },
                        "event": "conversation.chat.created"
                    })

                    # 模拟流式响应（简化版本）
                    # 在实际项目中，这里会调用通义千问Omni API
                    response_text = f"这是对 '{prompt}' 的通义千问Omni流式响应。"

                    # 发送流式内容
                    await manager.send_message(client_id, {
                        "code": 200,
                        "msg": "success",
                        "data": {
                            "type": "content",
                            "content": response_text,
                            "chat_id": chat_id
                        },
                        "event": "conversation.message.delta"
                    })

                    # 发送完成消息
                    await manager.send_message(client_id, {
                        "code": 200,
                        "msg": "success",
                        "data": {
                            "type": "completed",
                            "content": "生成完成",
                            "chat_id": chat_id
                        },
                        "event": "conversation.chat.completed"
                    })

                    # 计算费用并扣减token
                    if user_uuid:
                        cost = 0.05
                        await calculate_and_deduct_tokens_by_cost(
                            user_uuid=user_uuid,
                            cost=cost,
                            reason="通义千问Omni流式对话"
                        )

                        # 保存对话记录
                        await save_conversation_to_db(
                            user_uuid=user_uuid,
                            model_name="qwen-omni",
                            problem=prompt,
                            answer=response_text,
                            chat_id=chat_id,
                            agent_id="",
                            field1=str(int(cost * settings.TOKEN_BASE_MULTIPLIER))
                        )

                # 心跳请求
                elif message_type == "ping":
                    pong_message = {
                        "code": 200,
                        "msg": "heartbeat",
                        "data": {
                            "type": "pong",
                            "content": "pong"
                        },
                        "event": "connection.heartbeat"
                    }
                    await manager.send_message(client_id, pong_message)

                # 未知请求类型
                else:
                    error_message = {
                        "code": 400,
                        "msg": "error",
                        "data": {
                            "type": "error",
                            "content": f"未知的消息类型: {message_type}"
                        },
                        "event": "system.error"
                    }
                    await manager.send_message(client_id, error_message)

            except asyncio.TimeoutError:
                # 连接超时
                timeout_message = {
                    "code": 408,
                    "msg": "timeout",
                    "data": {
                        "type": "timeout",
                        "content": f"连接超时: {timeout}秒无活动"
                    },
                    "event": "connection.timeout"
                }
                await manager.send_message(client_id, timeout_message)
                break

            except WebSocketDisconnect:
                logger.info(f"WebSocket连接断开: {client_id}")
                break

            except Exception as e:
                logger.error(f"处理消息时发生错误: {e}")
                error_message = {
                    "code": 500,
                    "msg": "error",
                    "data": {
                        "type": "error",
                        "content": f"处理错误: {str(e)}"
                    },
                    "event": "system.error"
                }
                await manager.send_message(client_id, error_message)

    except Exception as e:
        logger.error(f"WebSocket连接错误: {e}")
    finally:
        # 断开连接
        manager.disconnect(client_id)
