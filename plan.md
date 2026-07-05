# CheckTMDB 项目架构分析与代码质量审查修复计划

## Context

CheckTMDB 项目旨在解决国内 DNS 污染导致 TMDB/IMDB/TVDB 等影视元数据网站无法访问的问题，为 NAS/家庭影院用户自动生成最优 hosts 文件。核心脚本 `check_tmdb_github_dnschecked.py` 存在多处资源泄漏、异常处理不完善、逻辑缺陷等问题，需要系统性修复。

---

## Task 1: 项目架构分析报告（只读，输出在回复中）

对以下维度进行完整分析并在回复中输出：
- 项目整体概述与工作原理
- 核心脚本深度剖析（DoH 多源回退、TCP 延迟测试、hosts 生成与写入、命令行参数）
- CI/CD 自动化工作流分析
- 版本演进对比（旧版 vs 新版）

---

## Task 2: 资源泄漏修复（严重）

**文件**: `check_tmdb_github_dnschecked.py`

### 2a. `get_github_hosts()` response 未关闭（第171行）
- `requests.get(url)` 未使用 `with` 语句
- 修复：改为 `with requests.get(url) as response:` 包裹后续逻辑

### 2b. `_query_dns_server()` response 未关闭（第217行）
- `requests.get(...)` 返回的 response 未正确管理
- 修复：改为 `with requests.get(...) as response:` 包裹后续逻辑

---

## Task 3: 异常处理加固（严重/中等）

### 3a. `write_file()` README 解析无异常保护（第94行）
- `split("```bash")[1]` 在 README 格式异常时直接 IndexError 崩溃
- 修复：增加 `try/except IndexError` 保护，异常时跳过增量对比

### 3b. `update_system_hosts` 备份恢复逻辑不完善（第424-436行）
- 第431行裸 `except Exception:` 不记录异常详情
- 第434行 `except OSError` 分支未尝试恢复备份
- 修复：提取 `_restore_backup()` 辅助函数，统一处理恢复逻辑，记录异常详情

---

## Task 4: 逻辑缺陷修复（中等）

### 4a. DOMAINS 列表重复项（第31行、第34行）
- `'ia.media-imdb.com'` 出现两次，浪费约10-15秒运行时间
- 修复：删除第34行的重复项

### 4b. `get_github_hosts()` 返回类型注解错误（第161行）
- 标注为 `-> None` 但实际可能返回 `str`
- 修复：改为 `-> str | None`（Python 3.10+ 语法）

### 4c. `_backup_hosts` 时间戳精度不足（第351行）
- 秒级时间戳在极短时间内可能冲突
- 修复：改为 `%Y%m%d_%H%M%S_%f`（微秒精度）

### 4d. `CHECKTMDB_MARKER_PATTERN` 多标记块问题（第409行）
- `re.sub` 会替换所有匹配块
- 修复：添加 `count=1` 参数仅替换第一个匹配块，多块时打印警告

---

## Task 5: 性能优化（中等/轻微）

### 5a. `validate_ip` 正则预编译（第133-150行）
- 每次调用都使用字符串模式（虽有缓存但不够明确）
- 修复：提取为模块级编译常量 `_IPV4_RE` 和 `_IPV6_RE`

### 5b. `ping_ip` 冗余输出（第279行）
- 每次调用都打印说明文字
- 修复：删除该行（信息已在 README 中说明）

### 5c. DNS 重试无退避（第264行）
- 固定 `sleep(1)` 重试
- 修复：改为 `sleep(1 * attempt)` 指数退避

---

## Task 6: 代码清理（轻微）

### 6a. 删除未使用的 `import random`（第3行）
### 6b. 删除死代码 `is_ci_environment()` 函数（第186-196行）

---

## Task 7: 全面验证

- 使用 `python -m py_compile check_tmdb_github_dnschecked.py` 验证语法正确性
- 使用 `GetProblems` 工具检查代码问题
- 检查是否还有遗漏点（如其他未关闭的资源、未处理的边界条件等）

---

## 修改摘要表（预期）

| 序号 | 问题 | 严重程度 | 位置 | 修复方式 |
|------|------|----------|------|----------|
| 1 | get_github_hosts response 未关闭 | 严重 | L171 | with 语句 |
| 2 | _query_dns_server response 未关闭 | 严重 | L217 | with 语句 |
| 3 | write_file README 解析无保护 | 严重 | L94 | try/except IndexError |
| 4 | 备份恢复逻辑不完善 | 中等 | L424-436 | 提取辅助函数 + 统一恢复 |
| 5 | DOMAINS 重复项 | 中等 | L31,34 | 删除重复 |
| 6 | get_github_hosts 类型注解 | 轻微 | L161 | 改为 str \| None |
| 7 | 备份时间戳精度 | 中等 | L351 | 微秒精度 |
| 8 | 正则多标记块问题 | 中等 | L409 | count=1 |
| 9 | validate_ip 正则预编译 | 轻微 | L133-150 | 模块级编译 |
| 10 | ping_ip 冗余输出 | 轻微 | L279 | 删除 |
| 11 | DNS 重试无退避 | 轻微 | L264 | 指数退避 |
| 12 | 未使用 import random | 轻微 | L3 | 删除 |
| 13 | 死代码 is_ci_environment | 轻微 | L186-196 | 删除 |

## 关键文件

- `check_tmdb_github_dnschecked.py` — 所有代码修改的唯一目标文件
