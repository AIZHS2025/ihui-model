#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公共Socket接口
从 coze_zhs_py 项目提取的公共 API 接口 Socket 模块
简化版本，移除了Redis依赖
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from config import settings

logger = logging.getLogger("public-socket")

# 创建API路由
router = APIRouter(prefix="/cozeZhsApi/public-socket", tags=["公共Socket接口"])

class PublicSocketManager:
    """公共Socket管理器 - 支持user_uuid+model_id作为唯一标识"""

    def __init__(self):
        # 连接管理 - 使用复合键 user_uuid:model_id 作为唯一标识
        self.connections: Dict[str, WebSocket] = {}
        self.websocket_to_user_model: Dict[WebSocket, str] = {}

    def _generate_key(self, user_uuid: str, model_id: str, chat_id: str = None) -> str:
        """生成复合键"""
        if chat_id:
            return f"{user_uuid}:{model_id}:{chat_id}"
        return f"{user_uuid}:{model_id}"

    def _parse_key(self, key: str) -> tuple:
        """解析复合键"""
        parts = key.split(':', 2)
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            return parts[0], parts[1], None
        return None, None, None

    async def add_connection(self, websocket: WebSocket, user_uuid: str, model_id: str, chat_id: str = None):
        """添加连接"""
        key = self._generate_key(user_uuid, model_id, chat_id)

        # 如果已存在连接，先断开旧连接
        if key in self.connections:
            old_websocket = self.connections[key]
            try:
                await old_websocket.close()
                logger.info(f"🔄 断开旧连接: {key}")
            except:
                pass

        # 建立新连接
        self.connections[key] = websocket
        self.websocket_to_user_model[websocket] = key

        logger.info(f"✅ 公共Socket连接建立: {key}, 当前连接数: {len(self.connections)}")

        # 发送连接成功消息
        connection_data = {
            "user_uuid": user_uuid,
            "model_id": model_id,
            "connection_time": time.time()
        }

        if chat_id:
            connection_data["chat_id"] = chat_id

        await websocket.send_text(json.dumps({
            "event": "connected",
            "code": 200,
            "msg": "success",
            "data": connection_data
        }))

        return True

    async def remove_connection(self, websocket: WebSocket):
        """移除连接"""
        key = self.websocket_to_user_model.get(websocket)

        if key:
            if key in self.connections:
                del self.connections[key]

            if websocket in self.websocket_to_user_model:
                del self.websocket_to_user_model[websocket]

            logger.info(f"🔌 公共Socket连接断开: {key}, 剩余连接数: {len(self.connections)}")

    async def send_message(self, user_uuid: str, model_id: str, message: Any, event_name: str = "message", chat_id: str = None):
        """
        向指定用户和模型发送消息

        Args:
            user_uuid: 用户UUID
            model_id: 模型ID
            message: 要发送的消息内容
            event_name: 事件名称，默认为"message"
            chat_id: 会话ID，可选

        Returns:
            bool: 是否发送成功
        """
        key = self._generate_key(user_uuid, model_id, chat_id)
        websocket = self.connections.get(key)

        # 提取消息内容、状态和token数
        content = message
        status = "run"  # 默认状态
        total_tokens = None  # 默认为None

        if isinstance(message, dict) and "content" in message:
            content = message["content"]
            status = message.get("status", "run")
            total_tokens = message.get("total_tokens")

        logger.info(f"📤 发送消息: {key}, 内容: {content}, 状态: {status}")

        try:
            # 发送消息
            message_data = {
                "event": event_name,
                "user_uuid": user_uuid,
                "model_id": model_id,
                "timestamp": time.time(),
                "message": content,
                "status": status
            }

            if total_tokens is not None:
                message_data["total_tokens"] = total_tokens

            if chat_id:
                message_data["chat_id"] = chat_id

            await websocket.send_text(json.dumps(message_data))

            logger.debug(f"✅ 消息已发送: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ 发送消息失败 {key}: {e}")
            return False

    def is_connected(self, user_uuid: str, model_id: str, chat_id: str = None) -> bool:
        """检查指定用户、模型和会话是否已连接"""
        key = self._generate_key(user_uuid, model_id, chat_id)
        return key in self.connections

# 创建全局Socket管理器实例
public_socket_manager = PublicSocketManager()

# WebSocket路由
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点"""
    await websocket.accept()
    logger.info(f"🔌 客户端尝试连接: {websocket.client}")

    # 初始化变量
    user_uuid = None
    model_id = None
    chat_id = None
    registered = False

    try:
        # 接收消息循环
        while True:
            try:
                # 接收客户端消息
                data = await websocket.receive_text()
                message = json.loads(data)

                # 处理注册消息
                if message.get("event") == "register":
                    user_uuid = message.get("user_uuid")
                    model_id = message.get("model_id")
                    chat_id = message.get("chat_id")  # 可选参数

                    if not user_uuid or not model_id:
                        await websocket.send_text(json.dumps({
                            "event": "error",
                            "code": "MISSING_PARAMS",
                            "message": "缺少必要参数: user_uuid和model_id"
                        }))
                        continue

                    # 添加连接
                    await public_socket_manager.add_connection(
                        websocket=websocket,
                        user_uuid=user_uuid,
                        model_id=model_id,
                        chat_id=chat_id
                    )
                    registered = True

                # 处理其他消息
                elif registered:
                    # 这里可以添加其他消息处理逻辑
                    pass

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "event": "error",
                    "code": "INVALID_JSON",
                    "message": "无效的JSON格式"
                }))
            except Exception as e:
                logger.error(f"❌ 处理WebSocket消息失败: {e}")
                await websocket.send_text(json.dumps({
                    "event": "error",
                    "code": "PROCESSING_ERROR",
                    "message": f"处理消息失败: {str(e)}"
                }))

    except WebSocketDisconnect:
        pass
    finally:
        # 断开连接时清理
        if registered:
            await public_socket_manager.remove_connection(websocket)
            logger.info(f"🔌 客户端断开连接: {websocket.client}")

# API路由
@router.post("/send-message/{user_uuid}/{model_id}")
async def send_message_to_connection(user_uuid: str, model_id: str, request: dict):
    """向指定用户和模型发送消息"""
    message = request.get("message")
    event_name = request.get("event_name", "message")
    status = request.get("status", "run")  # 默认为"run"
    chat_id = request.get("chat_id")  # 可选参数
    total_tokens = request.get("total_tokens")  # 可选参数，用于记录token使用量

    if not message:
        raise HTTPException(status_code=400, detail="消息内容不能为空")

    # 创建包含状态的消息
    message_with_status = {
        "content": message,
        "status": status
    }

    # 如果提供了total_tokens，添加到消息中
    if total_tokens is not None:
        message_with_status["total_tokens"] = total_tokens

    success = await public_socket_manager.send_message(user_uuid, model_id, message_with_status, event_name, chat_id)

    response_data = {
        "user_uuid": user_uuid,
        "model_id": model_id,
        "event_name": event_name,
        "status": status,
        "sent": success
    }

    if chat_id:
        response_data["chat_id"] = chat_id

    if total_tokens is not None:
        response_data["total_tokens"] = total_tokens

    return {
        "code": 200 if success else 404,
        "msg": "success" if success else "未找到连接",
        "data": response_data
    }

# 创建一个公共函数，供其他模块调用
async def send_message_to_user_model(
    user_uuid: str,
    model_id: str,
    message: Any,
    chat_id: str = None,
    event_name: str = "message",
    status: str = "run",
    total_tokens: Optional[int] = None
) -> bool:
    """
    向指定用户和模型发送消息的公共函数

    Args:
        user_uuid: 用户UUID
        model_id: 模型ID
        message: 要发送的消息内容，可以是字符串或包含content和status的字典
        chat_id: 会话ID，可选
        event_name: 事件名称，默认为"message"
        status: 消息状态，默认为"run"
        total_tokens: token总数，可选

    Returns:
        bool: 是否发送成功
    """
    # 打印所有入参
    logger.info(f"send_message_to_user_model 入参: "
               f"user_uuid={user_uuid}, "
               f"model_id={model_id}, "
               f"message={message}, "
               f"chat_id={chat_id}, "
               f"event_name={event_name}, "
               f"status={status}, "
               f"total_tokens={total_tokens}")

    # 对于列表格式的消息，需要包装以包含状态信息
    if isinstance(message, list):
        message_with_status = {
            "content": message,
            "status": status
        }
    else:
        # 其他情况，使用原有逻辑
        message_with_status = {
            "content": message,
            "status": status
        }

    # 如果提供了total_tokens，添加到消息中
    if total_tokens is not None:
        message_with_status["total_tokens"] = total_tokens

    # 发送消息
    success = await public_socket_manager.send_message(user_uuid, model_id, message_with_status, event_name, chat_id)

    return success
