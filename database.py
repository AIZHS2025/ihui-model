#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ihui_public 数据库连接配置
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config import settings
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 数据库连接配置
DATABASE_URL = settings.DATABASE_URL or "mysql+pymysql://root:password@localhost:3306/ihui_public?charset=utf8mb4"

# 连接池配置
POOL_SIZE = 10
MAX_OVERFLOW = 20
POOL_TIMEOUT = 30
POOL_RECYCLE = 3600

# 定义需要使用数据源2的表名
DATASOURCE_2_TABLES = {
    'users',
    'user_margin',
    'user_auth_info'
}

# 通用引擎配置函数
def create_database_engine(database_url: str, echo: bool = False):
    """创建数据库引擎的通用函数"""
    return create_engine(
        database_url,
        # 连接池配置
        poolclass=QueuePool,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=True,

        # 性能优化配置
        echo=echo,
        echo_pool=False,

        # 连接参数优化
        connect_args={
            "charset": "utf8mb4",
            "connect_timeout": 10,
            "read_timeout": 30,
            "write_timeout": 30,
            "autocommit": False,
        }
    )

# 创建数据库引擎
engine = create_database_engine(DATABASE_URL, settings.DATABASE_ECHO)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_by_table(table_name: str = None):
    """根据表名获取对应的数据库会话"""
    if table_name and table_name in DATASOURCE_2_TABLES:
        # 使用数据源2（中心库）
        db = SessionLocal()
        logger.debug(f"使用数据源2（中心库）访问表: {table_name}")
    else:
        # 使用数据源1（小程序库）
        db = SessionLocal()
        if table_name:
            logger.debug(f"使用数据源1（小程序库）访问表: {table_name}")

    try:
        yield db
    finally:
        db.close()

# 智能数据库会话管理器
class SmartDBSession:
    """智能数据库会话管理器 - 自动根据模型选择数据源"""

    def __init__(self):
        self._sessions = {}

    def get_session_for_model(self, model_class):
        """根据模型类获取对应的数据库会话"""
        table_name = getattr(model_class, '__tablename__', None)
        if not table_name:
            # 如果没有表名，使用默认数据源
            return SessionLocal()

        if table_name in DATASOURCE_2_TABLES:
            return SessionLocal()
        else:
            return SessionLocal()

    def get_db_for_model(self, model_class):
        """获取模型对应的数据库会话生成器（用于FastAPI依赖注入）"""
        table_name = getattr(model_class, '__tablename__', None)

        def _get_db():
            if table_name and table_name in DATASOURCE_2_TABLES:
                db = SessionLocal()
                logger.debug(f"为模型 {model_class.__name__} 使用数据源2（中心库）")
            else:
                db = SessionLocal()
                logger.debug(f"为模型 {model_class.__name__} 使用数据源1（小程序库）")

            try:
                yield db
            finally:
                db.close()

        return _get_db

# 创建全局智能会话管理器实例
smart_db = SmartDBSession()

# 打印数据库连接配置
logger.info("=" * 60)
logger.info("🔗 数据库连接配置详情:")
logger.info(f"   数据库URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}")
logger.info(f"   连接池大小: {POOL_SIZE}")
logger.info(f"   最大溢出连接: {MAX_OVERFLOW}")
logger.info(f"   连接超时时间: {POOL_TIMEOUT}秒")
logger.info(f"   连接回收时间: {POOL_RECYCLE}秒")
logger.info("=" * 60)
