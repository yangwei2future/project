#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import webbrowser
import platform
import signal
import threading

# 设置编码以支持中文输出
if platform.system() == 'Windows':
    os.system('chcp 65001')

# 彩色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 全局变量
frontend_process = None
running = True

def print_banner():
    """打印启动横幅"""
    banner = f"""
{Colors.BLUE}{Colors.BOLD}
 ██████╗ 旅游规划生成器 ████████╗
 ██╔══██╗██╔════╝██╔════╝██╔════╝
 ██████╔╝█████╗  █████╗  ███████╗
 ██╔══██╗██╔══╝  ██╔══╝  ╚════██║
 ██║  ██║███████╗███████╗███████║
 ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
{Colors.ENDC}
{Colors.GREEN}前端启动脚本 v1.0{Colors.ENDC}
"""
    print(banner)

def check_node_environment():
    """检查Node.js环境"""
    print(f"{Colors.HEADER}[1/3] 检查Node.js环境...{Colors.ENDC}")
    
    try:
        # 检查Node.js版本
        node_version = subprocess.check_output(['node', '-v'], stderr=subprocess.STDOUT).decode().strip()
        npm_version = subprocess.check_output(['npm', '-v'], stderr=subprocess.STDOUT).decode().strip()
        
        print(f"Node.js版本: {node_version}")
        print(f"npm版本: {npm_version}")
        
        # 检查版本要求
        node_version_number = node_version.lstrip('v').split('.')
        if int(node_version_number[0]) < 14:
            print(f"{Colors.WARNING}警告: Node.js版本低于推荐的v14.0.0{Colors.ENDC}")
            continue_choice = input("是否继续? (y/n): ")
            if continue_choice.lower() != 'y':
                return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.FAIL}错误: 未检测到Node.js，请先安装Node.js{Colors.ENDC}")
        print(f"{Colors.BLUE}您可以从 https://nodejs.org/ 下载并安装Node.js{Colors.ENDC}")
        return False
    
    print(f"{Colors.GREEN}✓ Node.js环境检查完成{Colors.ENDC}")
    return True

def find_frontend_directory():
    """寻找前端目录"""
    print(f"{Colors.HEADER}[2/3] 定位前端目录...{Colors.ENDC}")
    
    # 可能的前端目录路径
    possible_paths = [
        "travel-planner/frontend",
        "frontend",
        "."
    ]
    
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "package.json")):
            print(f"{Colors.GREEN}✓ 找到前端目录: {path}{Colors.ENDC}")
            return path
    
    print(f"{Colors.FAIL}错误: 未找到前端目录，请确保项目结构正确{Colors.ENDC}")
    return None

def start_frontend(frontend_dir):
    """启动前端开发服务器"""
    print(f"{Colors.HEADER}[3/3] 启动前端开发服务器...{Colors.ENDC}")
    
    global frontend_process
    
    # 检查node_modules是否存在
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print(f"{Colors.WARNING}警告: 前端依赖未安装{Colors.ENDC}")
        install = input("是否安装前端依赖? (y/n): ")
        if install.lower() == 'y':
            try:
                print(f"{Colors.BLUE}正在安装依赖，这可能需要几分钟...{Colors.ENDC}")
                subprocess.check_call(
                    ["npm", "install"], 
                    cwd=frontend_dir
                )
                print(f"{Colors.GREEN}✓ 依赖安装完成{Colors.ENDC}")
            except subprocess.CalledProcessError as e:
                print(f"{Colors.FAIL}错误: 安装依赖失败 - {e}{Colors.ENDC}")
                return False
        else:
            print(f"{Colors.FAIL}错误: 无法启动前端，缺少必要的依赖{Colors.ENDC}")
            return False
    
    # 启动前端开发服务器
    try:
        print(f"{Colors.BLUE}正在启动开发服务器...{Colors.ENDC}")
        
        if platform.system() == 'Windows':
            frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        # 等待服务启动
        print(f"{Colors.BLUE}等待服务启动，这可能需要几秒钟...{Colors.ENDC}")
        time.sleep(5)
        
        if frontend_process.poll() is not None:
            print(f"{Colors.FAIL}错误: 前端服务启动失败{Colors.ENDC}")
            return False
            
        print(f"{Colors.GREEN}✓ 前端服务启动成功{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}错误: 启动前端服务时出错 - {str(e)}{Colors.ENDC}")
        return False

def open_browser():
    """打开浏览器访问应用"""
    url = "http://localhost:3000"
    print(f"{Colors.BLUE}正在打开浏览器访问: {url}{Colors.ENDC}")
    
    # 等待片刻确保服务完全启动
    time.sleep(2)
    webbrowser.open(url)

def monitor_frontend():
    """监控前端进程状态"""
    global running
    
    while running:
        if frontend_process and frontend_process.poll() is not None:
            print(f"{Colors.FAIL}警告: 前端进程已终止{Colors.ENDC}")
            running = False
            break
        time.sleep(2)

def stop_frontend():
    """停止前端进程"""
    global running
    running = False
    
    print(f"{Colors.HEADER}正在停止前端服务...{Colors.ENDC}")
    
    if frontend_process:
        try:
            if platform.system() == 'Windows':
                frontend_process.terminate()
            else:
                os.kill(frontend_process.pid, signal.SIGTERM)
            print(f"{Colors.GREEN}前端服务已停止{Colors.ENDC}")
        except:
            print(f"{Colors.WARNING}无法正常停止前端服务{Colors.ENDC}")

def handle_keyboard_interrupt(signal, frame):
    """处理键盘中断"""
    print(f"\n{Colors.BLUE}接收到终止信号，正在关闭...{Colors.ENDC}")
    stop_frontend()
    sys.exit(0)

def main():
    """主函数"""
    print_banner()
    
    # 设置信号处理
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
    # 检查Node.js环境
    if not check_node_environment():
        input("按Enter键退出...")
        return
    
    # 寻找前端目录
    frontend_dir = find_frontend_directory()
    if not frontend_dir:
        input("按Enter键退出...")
        return
    
    # 启动前端
    if not start_frontend(frontend_dir):
        input("按Enter键退出...")
        return
    
    # 打开浏览器
    open_browser()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}前端服务已启动!{Colors.ENDC}")
    print(f"{Colors.BLUE}应用已在浏览器中打开，访问地址: http://localhost:3000{Colors.ENDC}")
    print(f"{Colors.BLUE}按Ctrl+C停止服务{Colors.ENDC}\n")
    
    # 监控进程
    try:
        monitor_thread = threading.Thread(target=monitor_frontend)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # 保持主线程运行
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_frontend()

if __name__ == "__main__":
    main() 