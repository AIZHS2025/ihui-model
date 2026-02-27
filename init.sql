CREATE TABLE `zhs_ai_model_info` (
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT (uuid()),
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '模型名称',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '来源厂商',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '图片地址',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注',
  `type` tinyint DEFAULT '0' COMMENT '模型类别 0其他 | 1文本 | 2图片 | 3视频 | 4音频',
  `sort` int NOT NULL AUTO_INCREMENT,
  `is_del` tinyint DEFAULT '0' COMMENT '是否删除',
  `creator` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updator` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '修改人',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `quest_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '请求类型',
  `variables` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '存储模型相关变量信息',
  `is_new` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '是否新增',
  `is_top` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '排序',
  `manufacturer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '厂商',
  `grass_roots` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'python' COMMENT '底层来源',
  `is_gratis` tinyint DEFAULT '1' COMMENT '是否免费 0免费 | 1收费',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_sort` (`sort`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='大模型信息表';

CREATE TABLE `zhs_user_agent_context` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键',
  `agent_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'agent_id',
  `user_uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户唯一主键',
  `problem` text,
  `answer` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '智能体回答',
  `user_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '用户上传文件路径 分割：,',
  `agent_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '智能体回答文件 分割：,',
  `send_time` bigint NOT NULL COMMENT '消息发送时间：秒值',
  `field1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '备用字段',
  `chat_id` varchar(225) DEFAULT NULL,
  `model_name` varchar(225) DEFAULT NULL,
  `video_ratio` varchar(10) DEFAULT NULL,
  `summary` text COMMENT '智能体深度思考内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='用户关于智能体上下文';

CREATE TABLE `users` (
  `uuid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT (uuid()) COMMENT '用户唯一标识',
  `password_hash` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '密码哈希值',
  `password_salt` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码盐值',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '头像URL',
  `gender` tinyint DEFAULT '0' COMMENT '性别(0-沃尔玛购物袋,1-男,2-女)',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `status` tinyint DEFAULT '1' COMMENT '状态(0-禁用,1-正常,2-锁定, 3-注销)',
  `invite_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '分销邀请码（唯一）',
  `parent_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '上级推荐人ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_vip` tinyint DEFAULT '0' COMMENT '是否是vip 0不是 | 1是vip | 2操盘手',
  PRIMARY KEY (`uuid`) USING BTREE,
  UNIQUE KEY `invite_code` (`invite_code`) USING BTREE,
  KEY `idx_users_uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='用户主表';


CREATE TABLE `user_margin` (
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_uuid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户唯一id',
  `token_quantity` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '用户token数量',
  `token_free` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '每日免费数量',
  `aument` bigint DEFAULT NULL COMMENT '用户当前金额 单位分',
  `field1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '预留字段',
  `field2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '预留字段2',
  `field3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '预留字段3',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id_user_uuid` (`user_uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='用户余量表';


CREATE TABLE `user_auth_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_uuid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户UUID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '手机号',
  `certificate` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '身份证号',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '邮箱',
  `country` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '国',
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `cancel_phone` varchar(50) DEFAULT NULL COMMENT '弃用的手机号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `idx_user_uuid` (`user_uuid`) USING BTREE,
  UNIQUE KEY `idx_mobile` (`phone`) USING BTREE,
  KEY `idx_certificate` (`certificate`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=531 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='用户认证身份信息表';