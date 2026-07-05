# CheckTMDB

每日自动更新TMDB，themoviedb、thetvdb 国内可正常连接IP，解决DNS污染，供tinyMediaManager(TMM削刮器)、Kodi的刮削器、群晖VideoStation的海报墙、Plex Server的元数据代理、Emby Server元数据下载器、Infuse、Nplayer等正常削刮影片信息。

## 一、前景

自从我早两年使用了黑群NAS以后，下了好多的电影电视剧，发现电视端无法生成正常的海报墙。查找资料得知应该是 themoviedb.org、tmdb.org 无法正常访问，因为DNS受到了污染无法正确解析到TMDB的IP，故依葫芦画瓢写了一个python脚本，每日定时通过[dnschecker](https://dnschecker.org/)查询出最佳IP，并自动同步到路由器外挂hosts，可正常削刮。

**本项目无需安装任何程序**

通过修改本地、路由器 hosts 文件，即可正常削刮影片信息。

## 文件地址

- TMDB IPv4 hosts：`https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4` ，[链接](https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4)
- TMDB IPv6 hosts：`https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6` ，[链接](https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6)

## 二、使用方法

### 2.1 手动方式

#### 2.1.1 IPv4地址复制下面的内容

```bash
# Tmdb Hosts Start
18.155.192.38               tmdb.org
52.85.151.110               api.tmdb.org
65.8.54.86                  files.tmdb.org
65.8.54.76                  themoviedb.org
202.160.128.40              api.themoviedb.org
65.8.54.74                  www.themoviedb.org
13.249.74.105               auth.themoviedb.org
143.244.50.210              image.tmdb.org
143.244.50.210              images.tmdb.org
98.82.158.179               imdb.com
18.155.187.37               www.imdb.com
18.155.187.37               secure.imdb.com
18.155.187.37               s.media-imdb.com
98.82.158.179               us.dd.imdb.com
18.155.187.37               www.imdb.to
98.82.155.134               origin-www.imdb.com
199.232.161.16              ia.media-imdb.com
199.59.149.210              thetvdb.com
202.160.128.238             api.thetvdb.com
199.232.161.16              ia.media-imdb.com
146.75.113.16               f.media-amazon.com
18.238.192.108              imdb-video.media-imdb.com
148.113.196.166             webservice.fanart.tv
104.26.13.126               images.fanart.tv
158.69.209.125              assets.fanart.tv
172.67.74.146               fanart.tv
104.20.13.80                api.trakt.tv
104.20.13.80                trakt.tv
# Update time: 2026-07-04T22:13:12+08:00
# IPv4 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新， 数据更新时间：2026-07-04T22:13:12+08:00

#### 2.1.2 IPv6地址复制下面的内容

```bash
# Tmdb Hosts Start
2600:9000:24bb:9200:10:db24:6940:93a1              tmdb.org
2600:9000:201e:d600:10:fb02:4000:93a1              api.tmdb.org
2600:9000:204d:d200:5:da10:7440:93a1               files.tmdb.org
2600:9000:204d:1e00:e:5373:440:93a1                themoviedb.org
2a03:2880:f11a:83:face:b00c:0:25de                 api.themoviedb.org
2600:9000:204d:c400:e:5373:440:93a1                www.themoviedb.org
2600:9000:211f:9400:16:e4a1:eb00:93a1              auth.themoviedb.org
2400:52e0:1a01::992:1                              image.tmdb.org
2400:52e0:1a01::992:1                              images.tmdb.org
2600:9000:25f1:4a00:1d:d7f6:39d6:4401              ia.media-imdb.com
2a03:2880:f11c:8183:face:b00c:0:25de               thetvdb.com
2a03:2880:f12d:83:face:b00c:0:25de                 api.thetvdb.com
2a04:4e42:8c::272                                  ia.media-imdb.com
2a04:4e42:8c::272                                  f.media-amazon.com
2606:4700:20::681a:d7e                             images.fanart.tv
2606:4700:20::681a:d7e                             fanart.tv
2606:4700:10::6814:e50                             api.trakt.tv
2606:4700:10::6814:e50                             trakt.tv
# Update time: 2026-07-04T22:13:12+08:00
# IPv4 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新， 数据更新时间：2026-07-04T22:13:12+08:00

> [!NOTE]
> 由于项目搭建在Github Aciton，延时数据获取于Github Action 虚拟主机网络环境，请自行测试可用性，建议使用本地网络环境自动设置。

#### 2.1.3 修改 hosts 文件

hosts 文件在每个系统的位置不一，详情如下：

- Windows 系统：`C:\Windows\System32\drivers\etc\hosts`
- Linux 系统：`/etc/hosts`
- Mac（苹果电脑）系统：`/etc/hosts`
- Android（安卓）系统：`/system/etc/hosts`
- iPhone（iOS）系统：`/etc/hosts`

修改方法，把第一步的内容复制到文本末尾：

1. Windows 使用记事本。
2. Linux、Mac 使用 Root 权限：`sudo vi /etc/hosts`。
3. iPhone、iPad 须越狱、Android 必须要 root。

#### 2.1.4 激活生效

大部分情况下是直接生效，如未生效可尝试下面的办法，刷新 DNS：

1. Windows：在 CMD 窗口输入：`ipconfig /flushdns`

2. Linux 命令：`sudo nscd restart`，如报错则须安装：`sudo apt install nscd` 或 `sudo /etc/init.d/nscd restart`

3. Mac 命令：`sudo killall -HUP mDNSResponder`

**Tips：** 上述方法无效可以尝试重启机器。

### 2.2 自动方式

#### 2.2.1 安装 SwitchHosts

GitHub 发行版：https://github.com/oldj/SwitchHosts/releases/latest

#### 2.2.2 添加 hosts

点击左上角“+”，并进行以下配置：

- Hosts 类型：`远程`
- Hosts 标题：任意
- URL
    - IPv4：`https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4`
    - IPv6：`https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6`
- 自动刷新：`1 小时`

#### 2.2.3 启用 hosts

在左侧边栏启用 hosts，首次使用时软件会自动获取内容。如果无法连接到 GitHub，可以尝试用同样的方法添加 [GitHub520](https://github.com/521xueweihan/GitHub520) hosts。

## 三、本地运行脚本

### 3.1 环境准备

```bash
pip install -r requirements.txt
```

### 3.2 参数说明

| 参数 | 说明 |
|------|------|
| （无参数） | 查询所有域名的最快 IPv4/IPv6 地址，生成 `Tmdb_host_ipv4` 和 `Tmdb_host_ipv6` 文件 |
| `-G` | 在输出文件中追加 GitHub 相关域名的最快 IP |
| `-H` | 将探测结果自动写入系统 `/etc/hosts` 文件（需要 sudo/root 权限） |
| `--hosts-path PATH` | 自定义 hosts 文件路径（默认自动检测系统路径） |

### 3.3 使用示例

```bash
# 仅生成 hosts 文件（CI 默认行为）
python check_tmdb_github_dnschecked.py

# 生成 hosts 文件并追加 GitHub IP
python check_tmdb_github_dnschecked.py -G

# 生成 hosts 文件并自动更新系统 /etc/hosts（需要 root 权限）
sudo python check_tmdb_github_dnschecked.py -H

# 同时追加 GitHub IP 并更新系统 hosts
sudo python check_tmdb_github_dnschecked.py -G -H

# 指定自定义 hosts 路径（测试用）
python check_tmdb_github_dnschecked.py -H --hosts-path /tmp/test_hosts
```

> **注意**：使用 `-H` 参数时，脚本会在 `/etc/hosts` 中用 `# CheckTMDB START` / `# CheckTMDB END` 标记写入区域，支持增量更新，不会影响文件中的其他内容。每次写入前会自动备份原文件。

### 3.4 DNS 查询策略

脚本内置多 DNS 源自动回退机制，按优先级依次尝试：
1. **AliDNS**（阿里公共 DNS）— 境内首选
2. **360DNS** — 境内备选
3. **GoogleDNS** — 境外/CI 环境备用

任一 DNS 源可用即返回结果，无需手动配置。

## 其他

- [x] README.md 及 部分代码 参考[GitHub520](https://github.com/521xueweihan/GitHub520)
- [x] * 本项目仅在本机测试通过，如有问题欢迎提 [issues](https://github.com/cnwikee/CheckTMDB/issues/new)
