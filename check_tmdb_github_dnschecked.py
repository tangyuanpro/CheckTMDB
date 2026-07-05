import requests
from time import sleep
import time
import os
import sys
import re  # 导入正则模块用于IP验证
from datetime import datetime, timezone, timedelta
import socket
import argparse
import shutil
import platform

DOMAINS = [
    'tmdb.org',
    'api.tmdb.org',
    'files.tmdb.org',
    'themoviedb.org',
    'api.themoviedb.org',
    'www.themoviedb.org',
    'auth.themoviedb.org',
    'image.tmdb.org',
    'images.tmdb.org',
    'imdb.com',
    'www.imdb.com',
    'secure.imdb.com',
    's.media-imdb.com',
    'us.dd.imdb.com',
    'www.imdb.to',
    'origin-www.imdb.com',
    'ia.media-imdb.com',
    'thetvdb.com',
    'api.thetvdb.com',
    'f.media-amazon.com',
    'imdb-video.media-imdb.com',
    'webservice.fanart.tv',
    'images.fanart.tv',
    'assets.fanart.tv',
    'fanart.tv',
    'api.trakt.tv',
    'api-staging.trakt.tv',
    'trakt.tv'
]

Tmdb_Host_TEMPLATE = """# Tmdb Hosts Start
{content}
# Update time: {update_time}
# IPv4 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End\n"""

# 境内可用 DNS-over-HTTPS 服务器列表（按优先级排序，列表顺序即尝试顺序）
DNS_SERVERS = [
    {
        "name": "AliDNS",
        "url": "https://dns.alidns.com/resolve",
        "timeout": 10,
    },
    {
        "name": "360DNS",
        "url": "https://doh.360.cn/resolve",
        "timeout": 10,
    },
    {
        "name": "GoogleDNS",
        "url": "https://dns.google/resolve",
        "timeout": 15,
    },
]

# /etc/hosts 写入内容模板
SYSTEM_HOSTS_TEMPLATE = """# CheckTMDB START
# Updated: {update_time}
# Source: https://github.com/cnwikee/CheckTMDB
{content}
# CheckTMDB END"""

# 标记块检测正则（匹配 # CheckTMDB START 到 # CheckTMDB END 之间的全部内容）
CHECKTMDB_MARKER_PATTERN = re.compile(
    r'^#\s*CheckTMDB\s+START\s*$(.*?)^#\s*CheckTMDB\s+END\s*$',
    re.MULTILINE | re.DOTALL
)

# IPv4/IPv6 预编译正则（避免每次调用 validate_ip 时重复编译）
_IPV4_RE = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
)
_IPV6_RE = re.compile(
    r'^(?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$',
    re.IGNORECASE
)

def write_file(ipv4_hosts_content: str, ipv6_hosts_content: str, update_time: str, append_github: bool = False) -> bool:
    output_doc_file_path = os.path.join(os.path.dirname(__file__), "README.md")
    template_path = os.path.join(os.path.dirname(__file__), "README_template.md")
    
    if os.path.exists(output_doc_file_path):
        with open(output_doc_file_path, "r", encoding='utf-8') as old_readme_md:
            old_readme_md_content = old_readme_md.read()            
            if old_readme_md_content:
                try:
                    old_ipv4_block = old_readme_md_content.split("```bash")[1].split("```")[0].strip()
                    old_ipv4_hosts = old_ipv4_block.split("# Update time:")[0].strip()

                    old_ipv6_block = old_readme_md_content.split("```bash")[2].split("```")[0].strip()
                    old_ipv6_hosts = old_ipv6_block.split("# Update time:")[0].strip()
                except IndexError:
                    print("README.md 格式异常，无法解析旧内容，将直接覆盖写入")
                    old_ipv4_hosts = old_ipv6_hosts = None
                    old_ipv4_block = old_ipv6_block = ""
                
                if ipv4_hosts_content != "":
                    if old_ipv4_hosts is not None:
                        new_ipv4_hosts = ipv4_hosts_content.split("# Update time:")[0].strip()
                        if old_ipv4_hosts == new_ipv4_hosts:
                            print("ipv4 host not change")
                            w_ipv4_block = old_ipv4_block
                        else:
                            w_ipv4_block = ipv4_hosts_content
                            write_host_file(ipv4_hosts_content, 'ipv4', append_github)
                    else:
                        w_ipv4_block = ipv4_hosts_content
                        write_host_file(ipv4_hosts_content, 'ipv4', append_github)
                else:
                    print("ipv4_hosts_content is null")
                    w_ipv4_block = old_ipv4_block

                if ipv6_hosts_content != "":
                    if old_ipv6_hosts is not None:
                        new_ipv6_hosts = ipv6_hosts_content.split("# Update time:")[0].strip()
                        if old_ipv6_hosts == new_ipv6_hosts:
                            print("ipv6 host not change")
                            w_ipv6_block = old_ipv6_block
                        else:
                            w_ipv6_block = ipv6_hosts_content
                            write_host_file(ipv6_hosts_content, 'ipv6', append_github)
                    else:
                        w_ipv6_block = ipv6_hosts_content
                        write_host_file(ipv6_hosts_content, 'ipv6', append_github)
                else:
                    print("ipv6_hosts_content is null")
                    w_ipv6_block = old_ipv6_block
                
                with open(template_path, "r", encoding='utf-8') as temp_fb:
                    template_str = temp_fb.read()
                    hosts_content = template_str.format(ipv4_hosts_str=w_ipv4_block, ipv6_hosts_str=w_ipv6_block, update_time=update_time)

                    with open(output_doc_file_path, "w", encoding='utf-8') as output_fb:
                        output_fb.write(hosts_content)
                return True
        return False
               
def validate_ip(ip):
    """
    验证IP是否为合法的IPv4或IPv6地址
    :param ip: 待验证的IP字符串
    :return: True（合法）/False（非法）
    """
    # 优先验证IPv4，再验证IPv6（均使用模块级预编译正则）
    if _IPV4_RE.match(ip):
        return True
    elif _IPV6_RE.match(ip):
        return True
    else:
        return False

def write_host_file(hosts_content: str, filename: str, append_github: bool = False) -> None:
    output_file_path = os.path.join(os.path.dirname(__file__), "Tmdb_host_" + filename)
    if append_github:
        print("\n~追加Github ip~")
        hosts_content = hosts_content + "\n" + (get_github_hosts() or "")
    with open(output_file_path, "w", encoding='utf-8') as output_fb:
        output_fb.write(hosts_content)
        print("\n~最新TMDB" + filename + "地址已更新~")

def get_github_hosts() -> str | None:
    github_hosts_urls = [
        "https://hosts.gitcdn.top/hosts.txt",
        "https://raw.githubusercontent.com/521xueweihan/GitHub520/refs/heads/main/hosts",
        "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts",
        "https://raw.githubusercontent.com/ittuann/GitHub-IP-hosts/refs/heads/main/hosts_single"
    ]
    all_failed = True
    for url in github_hosts_urls:
        try:
            with requests.get(url) as response:
                if response.status_code == 200:
                    github_hosts = response.text
                    all_failed = False
                    break
                else:
                    print(f"\n从 {url} 获取GitHub hosts失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"\n从 {url} 获取GitHub hosts时发生错误: {str(e)}")
    if all_failed:
        print("\n获取GitHub hosts失败: 所有Url项目失败！")
        return None
    else:
        return github_hosts
    
def _query_dns_server(server_config, domain, record_type):
    """
    向单个 DNS 服务器发起 JSON API 查询
    :param server_config: DNS_SERVERS 中的单个配置字典
    :param domain: 目标域名
    :param record_type: A 或 AAAA
    :return: IP 列表（成功），空列表（无记录），None（请求失败，触发 fallback）
    """
    url = server_config["url"]
    server_name = server_config["name"]
    timeout = server_config.get("timeout", 10)

    params = {"name": domain, "type": record_type}
    headers = {
        "accept": "application/dns-json",
        "user-agent": "CheckTMDB/1.0"
    }

    try:
        with requests.get(url, headers=headers, params=params, timeout=timeout) as response:
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                print(f"  [{server_name}] 返回数据格式异常")
                return None

            answer_list = data.get("Answer", [])
            if not answer_list:
                print(f"  [{server_name}] 未找到 {domain} 的{record_type}记录")
                return []

            ips = []
            for answer in answer_list:
                ip = answer.get("data")
                if ip and validate_ip(ip):
                    ips.append(ip)
                    print(f"  [{server_name}] 提取到合法IP：{ip}")
                elif ip:
                    print(f"  [{server_name}] 跳过非法IP格式：{ip}")
            return ips

    except requests.exceptions.RequestException as e:
        print(f"  [{server_name}] 请求失败：{e}")
        return None
    except ValueError:
        print(f"  [{server_name}] 响应不是有效JSON")
        return None


def get_domain_ips(domain, record_type):
    """
    从多个 DoH 服务器获取域名的 A/AAAA 记录，支持自动 fallback
    :param domain: 目标域名（如 tmdb.org）
    :param record_type: 记录类型（A/AAAA）
    :return: 去重后的 IP 列表
    """
    max_retries_per_server = 2

    for server_config in DNS_SERVERS:
        server_name = server_config["name"]
        print(f"正在从 {server_name} 获取 {domain} 的{record_type}记录...")

        for attempt in range(1, max_retries_per_server + 1):
            if attempt > 1:
                print(f"  [{server_name}] 第{attempt}次重试...")
                sleep(1 * attempt)  # 指数退避：第1次等1秒，第2次等2秒

            result = _query_dns_server(server_config, domain, record_type)

            if result is not None:
                # 成功（含空列表——服务器正常但无记录，不触发 fallback）
                unique_ips = list(set(result))
                print(f"  [{server_name}] 最终获取到（去重后）：{unique_ips}")
                return unique_ips
            # result is None → 请求失败，继续重试或切换到下一个服务器

    print(f"所有 DNS 服务器均无法获取 {domain} 的{record_type}记录")
    return []

def ping_ip(ip, port=80):
    try:
        print(f"\n开始 ping {ip}...")
        start_time = time.time()
        with socket.create_connection((ip, port), timeout=2) as sock:
            latency = (time.time() - start_time) * 1000  # 转换为毫秒
            print(f"IP: {ip} 的平均延迟: {latency}ms")
            return latency
    except Exception as e:
        print(f"Ping {ip} 时发生错误: {str(e)}")
        return float('inf')
    
def find_fastest_ip(ips):
    """找出延迟最低的IP地址"""
    if not ips:
        return None
    
    fastest_ip = None
    min_latency = float('inf')
    ip_latencies = []  # 存储所有IP及其延迟
    
    for ip in ips:
        ip = ip.strip()
        if not ip:
            continue
            
        print(f"正在测试 IP: {ip}")
        latency = ping_ip(ip)
        ip_latencies.append((ip, latency))
        print(f"IP: {ip} 延迟: {latency}ms")
        
        if latency < min_latency:
            min_latency = latency
            fastest_ip = ip
            
        sleep(0.5) 
    
    print("\n所有IP延迟情况:")
    for ip, latency in ip_latencies:
        print(f"IP: {ip} - 延迟: {latency}ms")
    
    if fastest_ip:
        print(f"\n最快的IP是: {fastest_ip}，延迟: {min_latency}ms")
    
    return fastest_ip

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="CheckTMDB - 自动探测 TMDB/IMDB/TVDB 域名最快 IP 并生成 hosts 文件"
    )
    parser.add_argument("-G", "--github", action="store_true", default=False,
                        help="在输出文件中追加 GitHub 相关域名的最快 IP")
    parser.add_argument("-H", "--hosts", action="store_true", default=False,
                        help="将结果写入系统 /etc/hosts 文件（需要 sudo/root 权限）")
    parser.add_argument("--hosts-path", type=str, default=None,
                        help="自定义 hosts 文件路径（默认自动检测系统路径）")
    return parser.parse_args()


def _get_default_hosts_path():
    """获取当前操作系统的默认 hosts 文件路径"""
    if platform.system() == "Windows":
        return os.path.join(
            os.environ.get("SystemRoot", r"C:\Windows"),
            "System32", "drivers", "etc", "hosts"
        )
    return "/etc/hosts"


def _backup_hosts(hosts_path):
    """备份 hosts 文件（带时间戳），返回备份路径，失败返回 None"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = f"{hosts_path}.checktmdb_backup_{timestamp}"
    try:
        shutil.copy2(hosts_path, backup_path)
        print(f"已备份 hosts 文件至: {backup_path}")
        return backup_path
    except (OSError, PermissionError) as e:
        print(f"备份 hosts 文件失败: {e}")
        return None


def _restore_backup(backup_path, hosts_path):
    """从备份恢复 hosts 文件，失败时打印详细错误"""
    if backup_path and os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, hosts_path)
            print("已从备份恢复原始 hosts 文件")
        except Exception as e:
            print(f"警告：恢复备份也失败: {e}，请手动检查 hosts 文件")


def update_system_hosts(ipv4_results, ipv6_results, update_time, hosts_path=None):
    """
    将探测结果写入系统 /etc/hosts 文件，支持备份 + 增量更新
    :param ipv4_results: [[ip, domain], ...]
    :param ipv6_results: [[ip, domain], ...]
    :param update_time:  更新时间字符串
    :param hosts_path:   hosts 路径（None 则使用系统默认路径）
    :return: True 成功 / False 失败
    """
    if hosts_path is None:
        hosts_path = _get_default_hosts_path()

    if not os.path.exists(hosts_path):
        print(f"hosts 文件不存在: {hosts_path}")
        return False

    # 构建写入内容
    entries = []
    for ip, domain in ipv4_results:
        entries.append(f"{ip:<27} {domain}")
    for ip, domain in ipv6_results:
        entries.append(f"{ip:<50} {domain}")

    new_block = SYSTEM_HOSTS_TEMPLATE.format(
        update_time=update_time,
        content="\n".join(entries)
    )

    # 读取现有内容
    try:
        with open(hosts_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
    except PermissionError:
        print(f"权限不足：无法读取 {hosts_path}，请使用 sudo/root 权限运行")
        return False
    except OSError as e:
        print(f"读取 hosts 文件失败: {e}")
        return False

    # 备份
    backup_path = _backup_hosts(hosts_path)
    if backup_path is None:
        print("备份失败，中止写入以保护系统安全")
        return False

    # 增量更新逻辑
    matches = CHECKTMDB_MARKER_PATTERN.findall(existing_content)
    if matches:
        if len(matches) > 1:
            print(f"警告：检测到 {len(matches)} 个 CheckTMDB 标记块，仅替换第一个")
        updated_content = CHECKTMDB_MARKER_PATTERN.sub(new_block, existing_content, count=1)
        print("检测到已有 CheckTMDB 标记块，执行增量替换")
    else:
        # 追加前确保有换行分隔
        if existing_content and not existing_content.endswith("\n"):
            existing_content += "\n"
        updated_content = existing_content + "\n" + new_block + "\n"
        print("未检测到 CheckTMDB 标记块，追加至文件末尾")

    # 写入
    try:
        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"已成功更新 hosts 文件: {hosts_path}")
        return True
    except PermissionError:
        print(f"权限不足：无法写入 {hosts_path}")
        _restore_backup(backup_path, hosts_path)
        return False
    except OSError as e:
        print(f"写入 hosts 文件失败: {e}")
        _restore_backup(backup_path, hosts_path)
        return False


def main():
    args = parse_args()
    print("开始检测TMDB相关域名的最快IP...")

    ipv4_ips, ipv6_ips, ipv4_results, ipv6_results = [], [], [], []

    for domain in DOMAINS:
        print(f"\n正在处理域名: {domain}")
        ipv4_ips = get_domain_ips(domain, "A")
        ipv6_ips = get_domain_ips(domain, "AAAA")

        if not ipv4_ips and not ipv6_ips:
            print(f"无法获取 {domain} 的IP列表，跳过该域名")
            continue

        # 处理 IPv4 地址
        if ipv4_ips:
            fastest_ipv4 = find_fastest_ip(ipv4_ips)
            if fastest_ipv4:
                ipv4_results.append([fastest_ipv4, domain])
                print(f"域名 {domain} 的最快IPv4是: {fastest_ipv4}")
            else:
                ipv4_results.append([ipv4_ips[0], domain])

        # 处理 IPv6 地址
        if ipv6_ips:
            fastest_ipv6 = find_fastest_ip(ipv6_ips)
            if fastest_ipv6:
                ipv6_results.append([fastest_ipv6, domain])
                print(f"域名 {domain} 的最快IPv6是: {fastest_ipv6}")
            else:
                # 兜底：可能存在无法正确获取 fastest_ipv6 的情况，则将第一个IP赋值
                ipv6_results.append([ipv6_ips[0], domain])

        sleep(1)  # 避免请求过于频繁

    # 保存结果到文件
    if not ipv4_results and not ipv6_results:
        print(f"程序出错：未获取任何domain及对应IP，请检查接口~")
        sys.exit(1)

    # 生成更新时间
    update_time = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

    ipv4_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<27} {domain}" for ip, domain in ipv4_results),
        update_time=update_time
    ) if ipv4_results else ""

    ipv6_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<50} {domain}" for ip, domain in ipv6_results),
        update_time=update_time
    ) if ipv6_results else ""

    # 写入仓库文件（Tmdb_host_ipv4/ipv6 + README.md）
    write_file(ipv4_hosts_content, ipv6_hosts_content, update_time,
               append_github=args.github)

    # 按需更新系统 /etc/hosts
    if args.hosts:
        print("\n" + "=" * 50)
        print("开始更新系统 hosts 文件...")
        print("=" * 50)
        success = update_system_hosts(
            ipv4_results, ipv6_results, update_time, args.hosts_path
        )
        if not success:
            print("警告：系统 hosts 文件更新失败，但仓库文件已正常生成")
            sys.exit(2)
        else:
            print("系统 hosts 文件更新成功")


if __name__ == "__main__":
    main()
