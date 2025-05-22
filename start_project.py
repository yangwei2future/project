#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import webbrowser
import json
import platform
import signal
import threading
from pathlib import Path

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
backend_process = None
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
{Colors.GREEN}一键启动脚本 v1.0{Colors.ENDC}
"""
    print(banner)

def check_requirements():
    """检查项目依赖"""
    print(f"{Colors.HEADER}[1/5] 检查环境依赖...{Colors.ENDC}")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print(f"{Colors.FAIL}错误: 需要Python 3.6或更高版本{Colors.ENDC}")
        return False
    
    # 检查必要的Python包
    required_packages = ['flask', 'requests', 'pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Colors.WARNING}警告: 缺少以下Python包: {', '.join(missing_packages)}{Colors.ENDC}")
        install = input(f"是否安装这些包? (y/n): ")
        if install.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        else:
            print(f"{Colors.FAIL}错误: 缺少必要的依赖包{Colors.ENDC}")
            return False
    
    # 检查Node.js (如果需要启动前端)
    if os.path.exists('travel-planner/frontend'):
        try:
            node_version = subprocess.check_output(['node', '-v'], stderr=subprocess.STDOUT).decode().strip()
            print(f"Node.js版本: {node_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.WARNING}警告: 未检测到Node.js，前端可能无法启动{Colors.ENDC}")
            frontend_choice = input("是否仍然尝试启动前端? (y/n): ")
            if frontend_choice.lower() != 'y':
                return False
    
    print(f"{Colors.GREEN}✓ 环境依赖检查完成{Colors.ENDC}")
    return True

def setup_directories():
    """设置必要的目录"""
    print(f"{Colors.HEADER}[2/5] 设置项目目录...{Colors.ENDC}")
    
    # 创建必要的目录
    os.makedirs("images", exist_ok=True)
    os.makedirs("plans", exist_ok=True)
    
    # 检查配置文件
    if not os.path.exists("config.json"):
        print(f"{Colors.WARNING}警告: 未找到config.json，创建默认配置文件{Colors.ENDC}")
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({"deepseek_api_key": ""}, f, ensure_ascii=False, indent=4)
    
    print(f"{Colors.GREEN}✓ 项目目录设置完成{Colors.ENDC}")
    return True

def start_backend():
    """启动后端服务"""
    print(f"{Colors.HEADER}[3/5] 启动后端服务...{Colors.ENDC}")
    
    global backend_process
    
    # 检查是使用主目录的main.py还是travel-planner/backend/app.py
    if os.path.exists("main.py"):
        backend_cmd = [sys.executable, "main.py"]
        backend_dir = "."
    elif os.path.exists("travel-planner/backend/app.py"):
        backend_cmd = [sys.executable, "app.py"]
        backend_dir = "travel-planner/backend"
    else:
        print(f"{Colors.FAIL}错误: 未找到后端入口文件{Colors.ENDC}")
        return False
    
    # 启动后端
    try:
        print(f"启动命令: {' '.join(backend_cmd)}")
        if platform.system() == 'Windows':
            backend_process = subprocess.Popen(
                backend_cmd, 
                cwd=backend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            backend_process = subprocess.Popen(
                backend_cmd,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        # 等待后端启动
        time.sleep(2)
        if backend_process.poll() is not None:
            print(f"{Colors.FAIL}错误: 后端启动失败{Colors.ENDC}")
            return False
            
        print(f"{Colors.GREEN}✓ 后端服务启动成功{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}错误: 启动后端时出错 - {str(e)}{Colors.ENDC}")
        return False

def start_frontend():
    """启动前端服务"""
    print(f"{Colors.HEADER}[4/5] 检查前端服务...{Colors.ENDC}")
    
    global frontend_process
    
    # 检查是否存在前端目录
    if not os.path.exists("travel-planner/frontend"):
        print(f"{Colors.WARNING}警告: 未找到前端目录，将只启动后端服务{Colors.ENDC}")
        return True
    
    # 检查node_modules是否存在
    if not os.path.exists("travel-planner/frontend/node_modules"):
        print(f"{Colors.WARNING}警告: 前端依赖未安装{Colors.ENDC}")
        install = input("是否安装前端依赖? (y/n): ")
        if install.lower() == 'y':
            try:
                subprocess.check_call(
                    ["npm", "install"], 
                    cwd="travel-planner/frontend"
                )
            except subprocess.CalledProcessError:
                print(f"{Colors.FAIL}错误: 安装前端依赖失败{Colors.ENDC}")
                return False
    
    # 启动前端
    try:
        print(f"{Colors.HEADER}[5/5] 启动前端服务...{Colors.ENDC}")
        if platform.system() == 'Windows':
            frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd="travel-planner/frontend",
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd="travel-planner/frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        # 等待前端启动
        time.sleep(5)
        if frontend_process.poll() is not None:
            print(f"{Colors.FAIL}错误: 前端启动失败{Colors.ENDC}")
            return False
            
        print(f"{Colors.GREEN}✓ 前端服务启动成功{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.WARNING}警告: 启动前端时出错 - {str(e)}{Colors.ENDC}")
        print(f"{Colors.WARNING}将只启动后端服务{Colors.ENDC}")
        return True

def open_browser():
    """打开浏览器访问应用"""
    # 如果前端启动成功，打开前端URL
    if frontend_process and frontend_process.poll() is None:
        url = "http://localhost:3000"
    else:
        # 否则打开后端URL
        url = "http://localhost:5000"
    
    print(f"{Colors.BLUE}正在打开浏览器访问: {url}{Colors.ENDC}")
    webbrowser.open(url)

def monitor_processes():
    """监控进程状态"""
    while running:
        if backend_process and backend_process.poll() is not None:
            print(f"{Colors.FAIL}警告: 后端进程已终止{Colors.ENDC}")
            stop_all()
            break
            
        if frontend_process and frontend_process.poll() is not None:
            print(f"{Colors.WARNING}警告: 前端进程已终止{Colors.ENDC}")
        
        time.sleep(2)

def stop_all():
    """停止所有进程"""
    global running
    running = False
    
    print(f"{Colors.HEADER}正在停止所有服务...{Colors.ENDC}")
    
    # 停止后端
    if backend_process:
        try:
            if platform.system() == 'Windows':
                backend_process.terminate()
            else:
                os.kill(backend_process.pid, signal.SIGTERM)
            print(f"{Colors.GREEN}后端服务已停止{Colors.ENDC}")
        except:
            print(f"{Colors.WARNING}无法正常停止后端服务{Colors.ENDC}")
    
    # 停止前端
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
    stop_all()
    sys.exit(0)

def main():
    """主函数"""
    print_banner()
    
    # 设置信号处理
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 设置目录
    if not setup_directories():
        return
    
    # 启动后端
    if not start_backend():
        return
    
    # 启动前端
    start_frontend()
    
    # 打开浏览器
    open_browser()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}所有服务已启动!{Colors.ENDC}")
    print(f"{Colors.BLUE}按Ctrl+C停止所有服务{Colors.ENDC}\n")
    
    # 监控进程
    try:
        monitor_thread = threading.Thread(target=monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # 保持主线程运行
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_all()

if __name__ == "__main__":
    main() 