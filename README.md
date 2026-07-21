# **使用该fork项目前必读：**

该fork仓库的README_template.md（同时影响了README.md）**基本由AI输出**，除**DSM7的使用方法**外都**未经测试**，如果你打算使用README.md（README_template.md）给出的其他方法可能还**需要自行辨认并修改**，在此我表示深深的遗憾，真的真的很不好意思啦。
如果你使用了除DSM7以外的方法，不妨提个issue告诉我该方法是否可行或提出你的建议，当然如果你能一并带上你的修复方法就更好啦。在此我感激不尽

------


# CheckTMDB

每日自动探测并更新 TMDB、IMDB、TVDB、Fanart、Trakt 等影视元数据域名的最快可用 IP，通过 DNS-over-HTTPS（DoH）多源回退 + TCP 延迟测速，自动生成最优 hosts 文件，解决国内 DNS 污染问题。

适用于 tinyMediaManager（TMM 刮削器）、Kodi 刮削器、群晖 Video Station 海报墙、Plex Server 元数据代理、Emby Server 元数据下载器、Infuse、NPlayer 等影视刮削场景。

---

## 一、项目背景

国内用户在使用 NAS 或家庭影院系统时，常常发现电视端无法生成正常的海报墙、刮削器无法获取影片信息。根本原因是 `themoviedb.org`、`tmdb.org`、`imdb.com`、`thetvdb.com`、`fanart.tv`、`trakt.tv` 等影视元数据服务的域名遭到 DNS 污染，无法正确解析到真实 IP。

本项目通过 **DNS-over-HTTPS（DoH）多源查询**（AliDNS → 360DNS → GoogleDNS 自动回退）获取域名的真实 IP，并使用 **TCP 延迟测速**自动筛选出当前网络环境下延迟最低的最快 IP，生成 hosts 文件。

**本项目无需安装任何程序**——您可以直接使用远程 hosts 文件（由 GitHub Actions 每日自动更新），也可以在本地运行脚本获取适合您网络环境的最优 IP。

---

## 二、覆盖域名

脚本覆盖以下 **6 大服务、共 28 个域名**：

| 服务 | 域名 | 用途 |
|------|------|------|
| **TMDB** | `tmdb.org`、`api.tmdb.org`、`files.tmdb.org`、`themoviedb.org`、`api.themoviedb.org`、`www.themoviedb.org`、`auth.themoviedb.org`、`image.tmdb.org`、`images.tmdb.org` | 影视元数据、海报图片 |
| **IMDB** | `imdb.com`、`www.imdb.com`、`secure.imdb.com`、`s.media-imdb.com`、`us.dd.imdb.com`、`www.imdb.to`、`origin-www.imdb.com`、`ia.media-imdb.com`、`imdb-video.media-imdb.com` | 影视评分、元数据、媒体资源 |
| **TVDB** | `thetvdb.com`、`api.thetvdb.com` | 电视剧元数据 |
| **Amazon CDN** | `f.media-amazon.com` | IMDB 媒体资源加速 |
| **Fanart** | `fanart.tv`、`webservice.fanart.tv`、`images.fanart.tv`、`assets.fanart.tv` | 高清海报、背景图、横幅 |
| **Trakt** | `trakt.tv`、`api.trakt.tv`、`api-staging.trakt.tv` | 观看记录同步、评分 |

---

## 三、使用方法

### 3.1 远程 hosts 文件（推荐）

以下文件由 GitHub Actions 每天自动更新两次，可直接订阅使用：

- **IPv4 hosts**：[Tmdb_host_ipv4](https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4)
  ```
  https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
  ```
- **IPv6 hosts**：[Tmdb_host_ipv6](https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv6)
  ```
  https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
  ```

### 3.2 手动复制

#### 3.2.1 IPv4 hosts 内容

```bash
# Tmdb Hosts Start
18.238.96.86                tmdb.org
18.155.173.89               api.tmdb.org
18.238.109.48               files.tmdb.org
18.155.173.111              themoviedb.org
65.8.20.119                 api.themoviedb.org
18.155.173.2                www.themoviedb.org
18.238.96.82                auth.themoviedb.org
138.199.9.104               image.tmdb.org
169.150.249.162             images.tmdb.org
98.82.158.179               imdb.com
18.155.175.50               www.imdb.com
18.155.175.50               secure.imdb.com
18.155.175.50               s.media-imdb.com
98.82.155.134               us.dd.imdb.com
18.155.175.50               www.imdb.to
98.82.155.134               origin-www.imdb.com
18.238.91.118               ia.media-imdb.com
65.8.197.76                 thetvdb.com
65.8.197.76                 api.thetvdb.com
146.75.121.16               f.media-amazon.com
65.8.20.32                  imdb-video.media-imdb.com
148.113.196.166             webservice.fanart.tv
104.26.12.126               images.fanart.tv
158.69.210.98               assets.fanart.tv
172.67.74.146               fanart.tv
104.20.13.80                api.trakt.tv
104.20.13.80                trakt.tv
# Update time: 2026-07-22T06:53:59+08:00
# IPv4 Update url: https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新，数据更新时间：2026-07-22T06:53:59+08:00

#### 3.2.2 IPv6 hosts 内容

```bash
# Tmdb Hosts Start
2600:9000:2776:da00:10:db24:6940:93a1              tmdb.org
2600:9000:246b:da00:10:fb02:4000:93a1              api.tmdb.org
2600:9000:2778:6e00:5:da10:7440:93a1               files.tmdb.org
2600:9000:246b:6a00:e:5373:440:93a1                themoviedb.org
2600:9000:2105:b000:c:174a:c400:93a1               api.themoviedb.org
2600:9000:246b:8e00:e:5373:440:93a1                www.themoviedb.org
2600:9000:2776:a800:16:e4a1:eb00:93a1              auth.themoviedb.org
2400:52e0:1a01::994:1                              image.tmdb.org
2400:52e0:1a01::912:1                              images.tmdb.org
2a04:4e42:8d::272                                  ia.media-imdb.com
2a04:4e42:8d::272                                  f.media-amazon.com
2606:4700:20::681a:c7e                             images.fanart.tv
2606:4700:20::681a:c7e                             fanart.tv
2606:4700:10::6814:e50                             api.trakt.tv
2606:4700:10::6814:e50                             trakt.tv
# Update time: 2026-07-22T06:53:59+08:00
# IPv4 Update url: https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新，数据更新时间：2026-07-22T06:53:59+08:00

> [!NOTE]
> 延迟数据获取于 GitHub Actions 虚拟主机网络环境（美国机房），与您本地网络的最优 IP 可能存在差异。建议在本地网络环境运行脚本以获得最佳效果。

### 3.3 修改 hosts 文件

hosts 文件在各操作系统中的位置如下：

| 操作系统 | hosts 文件路径 |
|----------|---------------|
| Windows | `C:\Windows\System32\drivers\etc\hosts` |
| Linux | `/etc/hosts` |
| macOS | `/etc/hosts` |
| Android（需 root） | `/system/etc/hosts` |
| iOS（需越狱） | `/etc/hosts` |

修改方法——将上方 hosts 内容追加到文件末尾：

1. **Windows**：以管理员身份运行记事本，打开 hosts 文件进行编辑
2. **Linux / macOS**：使用 `sudo` 权限编辑：`sudo nano /etc/hosts`
3. **Android / iOS**：需要 root 或越狱后使用文件管理器编辑

### 3.4 激活生效

大部分情况下修改后立即生效。如未生效，可尝试刷新 DNS 缓存：

| 操作系统 | 刷新命令 |
|----------|----------|
| Windows | `ipconfig /flushdns` |
| Linux | `sudo nscd restart`（如报错需安装：`sudo apt install nscd`） |
| macOS | `sudo killall -HUP mDNSResponder` |

> **提示**：上述方法无效时，可尝试重启设备。

---

## 四、自动化定时更新配置

为保持 hosts 记录始终最新，建议在您的设备上配置定时任务自动更新。以下提供多种环境的配置方案。

### 4.1 SwitchHosts（跨平台 GUI，推荐普通用户使用）

[SwitchHosts](https://github.com/oldj/SwitchHosts) 是一款跨平台的 hosts 管理工具，支持远程 hosts 自动订阅。

**安装**：前往 [GitHub Releases](https://github.com/oldj/SwitchHosts/releases/latest) 下载对应系统版本。

**配置步骤**：

1. 打开 SwitchHosts，点击左上角 **"+"** 添加新规则
2. 进行以下配置：
   - **Hosts 类型**：选择 `远程`
   - **Hosts 标题**：填写任意名称（如 `CheckTMDB IPv4`）
   - **URL**：
     - IPv4：`https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4`
     - IPv6：`https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv6`
   - **自动刷新**：选择 `1 小时`
3. 在左侧边栏**启用**该 hosts 规则，软件会自动获取内容

> **提示**：如果无法连接 GitHub，可以尝试用同样方法添加 [GitHub520](https://github.com/521xueweihan/GitHub520) hosts 以加速 GitHub 访问。

### 4.2 群晖 NAS — DSM 7 定时任务

适用于群晖 DSM 7.x 系统，通过"任务计划"定时拉取远程 hosts 并写入系统 hosts 文件。

#### 方案一：本地运行 Python 脚本（适合高级用户，该方法涉及到了IPv6 hosts的写入）

前提：已通过群晖「套件中心」安装 **Python 3** 套件。

1. 通过 SSH 或 File Station 将脚本文件上传到群晖，例如 `/volume1/homes/你的用户名/CheckTMDB/`
2. 在 **「任务计划」** → **「新增」** → **「计划的任务」** → **「用户定义的脚本」** 中配置：
   - **任务名称**：`CheckTMDB Python`
   - **用户**：`root`
   - **计划**：每天，时间选择 08:00（可自定义）
3. 脚本内容：

```shell
#!/bin/sh
SCRIPT_DIR="/volume1/homes/你的用户名/CheckTMDB"
cd "$SCRIPT_DIR"
# 安装依赖（首次运行需要）
/usr/local/bin/pip3 install requests -q 2>/dev/null
# 执行脚本并自动写入系统 hosts
/usr/local/bin/python3 check_tmdb_github_dnschecked.py -H >> /var/log/checktmdb.log 2>&1
```

> **注意**：请将 `/volume1/homes/你的用户名/CheckTMDB` 替换为实际路径，Python 路径可能因套件版本不同而有所差异，可通过 `which python3` 命令确认。

#### 方案二：定时拉取远程 hosts（无需安装 Python，该方法没有涉及到IPv6 hosts的写入，若有需要可以自己完善一下。并且没有验证是否有效）

1. 登录 DSM 管理界面，打开 **「控制面板」** → **「任务计划」**
2. 点击 **「新增」** → **「触发的任务」** → **「用户定义的脚本」**
3. **常规**选项卡：
   - **任务名称**：`Update TMDB Hosts`
   - **事件**：选择 `开机`（开机时自动执行一次）
   - **用户**：`root`
4. **任务设置**选项卡，在"脚本内容"中粘贴以下内容：

```shell
#!/bin/sh
# 拉取远程 hosts 并合并到系统 hosts（保留自定义内容）
MARKER_START="# CheckTMDB START"
MARKER_END="# CheckTMDB END"
HOSTS_FILE="/etc/hosts"
TEMP_FILE="/tmp/checktmdb_hosts.tmp"

# 下载最新 IPv4 hosts
curl -fsSL "https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4" > "$TEMP_FILE" 2>/dev/null

if [ $? -eq 0 ] && [ -s "$TEMP_FILE" ]; then
    # 移除旧的 CheckTMDB 区块
    sed -i "/$MARKER_START/,/$MARKER_END/d" "$HOSTS_FILE"
    # 追加新内容
    echo "" >> "$HOSTS_FILE"
    echo "$MARKER_START" >> "$HOSTS_FILE"
    cat "$TEMP_FILE" >> "$HOSTS_FILE"
    echo "$MARKER_END" >> "$HOSTS_FILE"
    echo "$(date): CheckTMDB hosts 更新成功" >> /var/log/checktmdb.log
else
    echo "$(date): CheckTMDB hosts 下载失败，保留旧记录" >> /var/log/checktmdb.log
fi

rm -f "$TEMP_FILE"
```

5. 点击 **「确定」** 保存

如需**定时执行**（如每天两次），在上述步骤 2 中选择 **「计划的任务」** → **「用户定义的脚本」**，然后在"计划"选项卡中设置执行频率（如每天 8:00 和 20:00）。

### 4.3 群晖 NAS — DSM 6 定时任务

DSM 6 的任务计划配置与 DSM 7 基本一致，主要差异如下：

1. **Python 3 安装**：在「套件中心」搜索 **Python3** 套件并安装（DSM 6 的套件版本可能较旧）
2. **Python 路径**：DSM 6 中 Python 3 的默认路径通常为 `/usr/local/bin/python3` 或 `/var/packages/py3k/target/usr/local/bin/python3`，可通过 SSH 执行 `which python3` 确认
3. **任务计划入口**：「控制面板」→「任务计划」→「新增」，后续步骤与 DSM 7 相同，参照上方 4.2 节配置即可

> **提示**：DSM 6 已于 2025 年 6 月停止安全更新支持，建议有条件时升级到 DSM 7。

### 4.4 Windows 任务计划程序

通过 Windows 内置的"任务计划程序"定时运行脚本或拉取远程 hosts。

#### 方式一：定时拉取远程 hosts（无需 Python）

1. 以管理员身份打开 **PowerShell**，创建更新脚本：

```shell
# 将以下内容保存为 C:\Scripts\Update-CheckTMDB.ps1
$hostsFile = "$env:SystemRoot\System32\drivers\etc\hosts"
$url = "https://raw.githubusercontent.com/tangyuanpro/CheckTMDB/refs/heads/main/Tmdb_host_ipv4"
$marker = "# CheckTMDB"

# 下载最新 hosts
try {
    $newHosts = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
    $content = Get-Content $hostsFile -Raw -ErrorAction SilentlyContinue
    # 移除旧的 CheckTMDB 区块
    $content = $content -replace '(?ms)^# CheckTMDB START.*?^# CheckTMDB END\s*', ''
    # 追加新内容
    $content += "`n# CheckTMDB START`n$($newHosts.Content)`n# CheckTMDB END`n"
    Set-Content $hostsFile -Value $content -Encoding UTF8
    Write-Output "$(Get-Date): CheckTMDB hosts updated successfully"
} catch {
    Write-Output "$(Get-Date): Failed to update hosts - $($_.Exception.Message)"
}
```

2. 打开 **任务计划程序**（`Win + R` 输入 `taskschd.msc`）
3. 点击右侧 **「创建基本任务」**：
   - **名称**：`CheckTMDB Hosts Update`
   - **触发器**：选择 `每天`，设置时间（如 08:00）
   - **操作**：选择 `启动程序`
   - **程序或脚本**：`powershell.exe`
   - **添加参数**：`-ExecutionPolicy Bypass -File "C:\Scripts\Update-CheckTMDB.ps1"`
4. 双击创建的任务，勾选 **「使用最高权限运行」**（写入 hosts 需要管理员权限）

#### 方式二：定时运行 Python 脚本

1. 确保已安装 Python 并配置好环境变量
2. 在任务计划程序中创建基本任务：
   - **程序或脚本**：`python`（或 Python 完整路径）
   - **添加参数**：`check_tmdb_github_dnschecked.py -H`
   - **起始于**：脚本所在目录（如 `C:\CheckTMDB`）
3. 勾选 **「使用最高权限运行」**

### 4.5 Linux / macOS — cron 定时任务

#### 基本配置

1. 克隆仓库并安装依赖：

```shell
git clone https://github.com/tangyuanpro/CheckTMDB.git /opt/CheckTMDB
cd /opt/CheckTMDB
pip3 install -r requirements.txt
```

2. 编辑 crontab（需要 root 权限写入 `/etc/hosts`）：

```shell
sudo crontab -e
```

3. 添加以下行（每天 8:00 和 20:00 执行）：

```shell
0 8,20 * * * cd /opt/CheckTMDB && /usr/bin/python3 check_tmdb_github_dnschecked.py -H >> /var/log/checktmdb.log 2>&1
```

#### macOS sudo 免密配置

macOS 上 cron 以当前用户身份运行，写入 `/etc/hosts` 需要 sudo 权限：

1. 执行 `sudo visudo`，添加以下行（将 `你的用户名` 替换为实际用户名）：

```shell
你的用户名 ALL=(ALL) NOPASSWD: /usr/bin/python3 /opt/CheckTMDB/check_tmdb_github_dnschecked.py
```

2. crontab 中改用：

```shell
0 8,20 * * * cd /opt/CheckTMDB && sudo /usr/bin/python3 check_tmdb_github_dnschecked.py -H >> /var/log/checktmdb.log 2>&1
```

### 4.6 macOS — launchd（推荐方式）

macOS 官方推荐使用 `launchd` 代替 cron。创建 plist 配置文件：

1. 创建文件 `~/Library/LaunchAgents/com.checktmdb.update.plist`：

```shell
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.checktmdb.update</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/opt/CheckTMDB/check_tmdb_github_dnschecked.py</string>
        <string>-H</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/opt/CheckTMDB</string>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>20</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>/tmp/checktmdb.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/checktmdb_error.log</string>
</dict>
</plist>
```

2. 加载并启用任务：

```shell
launchctl load ~/Library/LaunchAgents/com.checktmdb.update.plist
```

> **注意**：launchd 以当前用户身份运行，写入 `/etc/hosts` 仍需配合 4.5 节的 sudo 免密配置。

### 4.7 OpenWrt 路由器

在路由器上直接运行脚本，hosts 生效后局域网内所有设备自动受益。

1. SSH 登录路由器，安装 Python 3 和依赖：

```shell
opkg update
opkg install python3 python3-pip git git-http
pip3 install requests
```

2. 克隆仓库：

```shell
cd /root
git clone https://github.com/tangyuanpro/CheckTMDB.git
```

3. 添加 cron 定时任务（每天 8:00 和 20:00 执行）：

```shell
echo "0 8,20 * * * cd /root/CheckTMDB && python3 check_tmdb_github_dnschecked.py -H >> /var/log/checktmdb.log 2>&1" >> /etc/crontabs/root
/etc/init.d/cron restart
```

> **提示**：OpenWrt 的 `/etc/hosts` 由 dnsmasq 管理，脚本写入后局域网内所有设备的 DNS 查询将自动使用新的 IP 映射。部分 OpenWrt 固件可能需要确认 dnsmasq 配置中 `addn-hosts` 或 `no-hosts` 选项未屏蔽自定义 hosts。

### 4.8 Docker 环境

适合已有 Docker 环境的 NAS 或服务器用户。

1. 创建 `docker-compose.yml`：

```shell
version: "3"
services:
  checktmdb:
    image: python:3.10-slim
    container_name: checktmdb
    restart: unless-stopped
    volumes:
      - ./scripts:/app
      - /etc/hosts:/etc/hosts
    working_dir: /app
    command: >
      sh -c "pip install requests -q &&
             while true; do
               python3 check_tmdb_github_dnschecked.py -H;
               sleep 43200;
             done"
```

2. 将 `check_tmdb_github_dnschecked.py` 放入 `./scripts/` 目录，启动容器：

```shell
docker compose up -d
```

> **说明**：容器每 12 小时（43200 秒）执行一次脚本，通过挂载 `/etc/hosts` 直接更新宿主机 hosts 文件。如需调整频率，修改 `sleep` 参数即可。

---

## 五、本地运行脚本

### 5.1 环境准备

- **Python** >= 3.10
- 安装依赖（仅需 `requests` 库）：

```shell
pip install -r requirements.txt
```

### 5.2 参数说明

| 参数 | 长参数 | 说明 |
|------|--------|------|
| （无参数） | — | 查询所有域名的最快 IPv4/IPv6 地址，生成 `Tmdb_host_ipv4` 和 `Tmdb_host_ipv6` 文件 |
| `-G` | `--github` | 在输出文件中追加 GitHub 相关域名的最快 IP |
| `-H` | `--hosts` | 将探测结果自动写入系统 hosts 文件（需要 root/管理员权限），IPv4 hosts与IPv6 hosts将会一并写入 |
| — | `--hosts-path PATH` | 自定义 hosts 文件路径（默认自动检测系统路径） |

### 5.3 使用示例

```shell
# 仅生成 hosts 文件（CI 默认行为）
python check_tmdb_github_dnschecked.py

# 生成 hosts 文件并追加 GitHub IP
python check_tmdb_github_dnschecked.py -G

# 生成 hosts 文件并自动更新系统 hosts（需要 root 权限），IPv4 hosts与IPv6 hosts将会一并写入
sudo python check_tmdb_github_dnschecked.py -H

# 同时追加 GitHub IP 并更新系统 hosts（需要 root 权限），IPv4 hosts与IPv6 hosts将会一并写入
sudo python check_tmdb_github_dnschecked.py -G -H

# 指定自定义 hosts 路径（测试用），IPv4 hosts与IPv6 hosts将会一并写入
python check_tmdb_github_dnschecked.py -H --hosts-path /tmp/test_hosts
```

> **注意**：使用 `-H` 参数时，脚本会在 hosts 文件中用 `# CheckTMDB START` / `# CheckTMDB END` 标记写入区域，支持增量更新，不会影响文件中的其他内容。每次写入前会自动备份原文件。

### 5.4 DNS 查询策略

脚本使用 **DNS-over-HTTPS（DoH）** JSON API 进行域名解析，内置多源自动回退机制，按优先级依次尝试：

| 优先级 | DNS 服务 | 接口地址 | 超时时间 | 适用场景 |
|--------|----------|----------|----------|----------|
| 1 | **AliDNS**（阿里公共 DNS） | `https://dns.alidns.com/resolve` | 10s | 境内首选 |
| 2 | **360DNS** | `https://doh.360.cn/resolve` | 10s | 境内备选 |
| 3 | **GoogleDNS** | `https://dns.google/resolve` | 15s | 境外 / CI 环境备用 |

- 每个 DNS 源最多重试 **2 次**，采用线性退避策略
- 任一 DNS 源可用即返回结果，无需手动配置
- 返回的 IP 会经过合法性验证（IPv4/IPv6 正则校验）并自动去重

### 5.5 系统 hosts 写入机制

使用 `-H` 参数时，脚本会将探测结果写入系统 hosts 文件，具备以下安全特性：

- **标记块管理**：用 `# CheckTMDB START` / `# CheckTMDB END` 标记写入区域
- **增量更新**：通过正则匹配替换已有标记块，不影响 hosts 文件中的其他内容
- **自动备份**：每次写入前自动备份原文件（带时间戳文件名）
- **失败恢复**：写入失败时自动从备份恢复原始 hosts 文件
- **跨平台路径检测**：自动识别 Windows / Linux / macOS 的默认 hosts 路径，也可通过 `--hosts-path` 自定义

---

## 六、GitHub Actions 自动执行

本项目已配置 GitHub Actions 自动运行，配置文件位于 `.github/workflows/main.yml`：

- **执行频率**：每天 UTC 10:00 和 22:00（北京时间 18:00 和次日 06:00），每日两次自动更新
- **手动触发**：在仓库的 **Actions** 页面，点击 `Check TMDB IP` → `Run workflow` 可手动执行
- **自动提交**：执行完成后自动将 `README.md`、`Tmdb_host_ipv4`、`Tmdb_host_ipv6` 提交到 `main` 分支
- **运行环境**：Ubuntu latest + Python 3.10

---

## 七、致谢与其他

- 本项目 README 及部分代码参考 [GitHub520](https://github.com/521xueweihan/GitHub520)
- DNS 解析服务由 [AliDNS](https://alidns.com/)、[360 DNS](https://doh.360.cn/)、[Google Public DNS](https://dns.google/) 提供
- 如有问题或建议，欢迎提交 [Issues](https://github.com/tangyuanpro/CheckTMDB/issues/new)

> **免责声明**：本项目仅在作者本机测试通过，不同网络环境下 IP 可用性可能存在差异。生成的 hosts 内容仅供参考，请自行测试可用性后使用。
