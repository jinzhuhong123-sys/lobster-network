# 更新日志

## [0.1.1] - 2026-06-22

### 新增
- **engine/world_map.py** — 世界地图引擎（WorldMapManager）
  - Chunk 知识碎片管理（增删改查、搜索、权限控制）
  - Treasure 宝藏管理（解锁、验证、稀有度系统）
  - 全量/增量同步机制
  - 冲突解决（最后写入者胜出）
  - 持久化存储支持
- **spec/** — OADP 协议层 6 个核心规范文档
  - protocol.md — OADP 核心协议（消息格式、对话流程、涌现计算、错误处理）
  - drp.md — 对话渲染协议（渲染流程、涌现检测算法、稀有度系统）
  - world-map.md — 世界地图索引协议（结构、同步机制、冲突解决）
  - soul_schema.md — SOUL.md 灵魂种子格式规范（含 JSON Schema）
  - memory_schema.md — MEMORY.md 记忆格式规范
  - portal.md — 传送门协议（生命周期、验证流程、知识传承链）
- **docs/GETTING_STARTED.md** — 快速上手指南（含核心模块示例代码）
- **pyproject.toml** — 项目配置（black + isort + mypy + pytest）
- **.github/workflows/test.yml** — GitHub Actions CI/CD（Python 3.10/3.11/3.12）
- **examples/indra_net_demo.py** — 因陀罗网拓扑示例代码

### 修复
- **src/network/indra_net.py** — 修复相对导入错误（改为绝对导入）
- **requirements.txt** — 完善依赖列表，明确版本号

### 测试
- 新增 22 个核心单元测试（test_core.py）
- 新增 19 个世界地图引擎测试（test_world_map.py）
- **总计 41 个测试全部通过** ✅

---

## [0.1.0] - 2026-06-21

### 新增
- 核心引擎：节点模型、对话引擎、涌现检测、世界状态管理
- 主网络类：LobsterNetwork（因陀罗网拓扑）
- 示例代码：多Agent对话示例
- 测试代码：15个单元测试用例
- 理论文档：对话即创造文章、架构设计、合作方案
- 项目配置：README、LICENSE、CONTRIBUTING、setup.py

### 测试
- 所有15个测试用例通过
- 示例代码运行成功，涌现值0.90

### 已知问题
- 涌现值计算算法需要优化（当前固定为0.90）
- SSH通信通道尚未实现
- 因陀罗网拓扑实现尚未完成

---

**你不停对话，世界就不停扩展** 🦞⚡️
