#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库工具模块
"""

import logging
from functools import wraps
from typing import Type, Any, Callable
from sqlalchemy.orm import Session
from fastapi import Depends

from .database import (
    get_db,
    get_db_by_table,
    smart_db,
    DATASOURCE_2_TABLES,
    SessionLocal
)

logger = logging.getLogger(__name__)

def get_smart_db_session(model_class: Type[Any] = None, table_name: str = None):
    """
    智能获取数据库会话的依赖注入函数

    Args:
        model_class: 模型类，用于自动检测表名
        table_name: 直接指定表名

    Returns:
        数据库会话生成器
    """
    # 确定表名
    if table_name:
        target_table = table_name
    elif model_class and hasattr(model_class, '__tablename__'):
        target_table = model_class.__tablename__
    else:
        target_table = None

    # 根据表名选择数据源
    if target_table and target_table in DATASOURCE_2_TABLES:
        logger.debug(f"使用数据源2（中心库）访问表: {target_table}")
        return get_db_by_table(table_name)
    else:
        logger.debug(f"使用数据源1（小程序库）访问表: {target_table}")
        return get_db()

def smart_db_dependency(model_class: Type[Any] = None, table_name: str = None):
    """
    创建智能数据库依赖注入装饰器

    Args:
        model_class: 模型类
        table_name: 表名

    Returns:
        FastAPI依赖注入函数
    """
    def dependency():
        return get_smart_db_session(model_class, table_name)

    return dependency

class SmartDBManager:
    """智能数据库管理器"""

    @staticmethod
    def get_session_for_model(model_class: Type[Any]) -> Session:
        """根据模型类获取对应的数据库会话"""
        table_name = getattr(model_class, '__tablename__', None)

        if table_name and table_name in DATASOURCE_2_TABLES:
            session = SessionLocal()
            logger.debug(f"为模型 {model_class.__name__} 使用数据源2（中心库）")
        else:
            session = SessionLocal()
            logger.debug(f"为模型 {model_class.__name__} 使用数据源1（小程序库）")

        return session

    @staticmethod
    def get_session_for_table(table_name: str) -> Session:
        """根据表名获取对应的数据库会话"""
        if table_name in DATASOURCE_2_TABLES:
            session = SessionLocal()
            logger.debug(f"为表 {table_name} 使用数据源2（中心库）")
        else:
            session = SessionLocal()
            logger.debug(f"为表 {table_name} 使用数据源1（小程序库）")

        return session

    @staticmethod
    def execute_with_smart_session(model_class: Type[Any], operation: Callable):
        """使用智能会话执行操作"""
        session = SmartDBManager.get_session_for_model(model_class)
        try:
            return operation(session)
        finally:
            session.close()

# 创建全局智能数据库管理器实例
smart_db_manager = SmartDBManager()

# 装饰器：自动选择数据源
def auto_datasource(func):
    """
    自动选择数据源的装饰器
    根据函数中使用的模型自动选择合适的数据源
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# 数据源路由表
DATASOURCE_ROUTING = {
    'users': 'datasource_2',
    'user_margin': 'datasource_2',
    'user_auth_info': 'datasource_2',
    # 其他表默认使用 datasource_1
}

def get_datasource_info():
    """获取数据源配置信息"""
    return {
        'datasource_1': {
            'name': '主数据库 (ihui_public)',
            'tables': []
        },
        'datasource_2': {
            'name': '中心库 (zhs_center_project)',
            'tables': list(DATASOURCE_2_TABLES)
        },
        'routing': DATASOURCE_ROUTING
    }

# 日志记录
logger.info("🔧 数据库工具模块已加载")
logger.info(f"   数据源2专用表: {', '.join(DATASOURCE_2_TABLES)}")
