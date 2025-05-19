#!/usr/bin/env python3

import os
import re
import random
import subprocess
import sys
from time import sleep

def get_current_mac(interface='en0'):
    """获取当前MAC地址"""
    try:
        output = subprocess.check_output(['ifconfig', interface], stderr=subprocess.STDOUT).decode('utf-8')
        mac_match = re.search(r'ether ([\w:]+)', output)
        if mac_match:
            return mac_match.group(1)
        return None
    except subprocess.CalledProcessError as e:
        print(f"获取MAC地址时出错: {e.output.decode('utf-8')}")
        return None

def generate_random_mac():
    """生成随机的MAC地址"""
    # macOS通常使用en0接口，我们生成一个合法的随机MAC
    # 第一个字节的第二个十六进制数字应该是2, 6, A或E
    first_byte = random.choice(['02', '06', '0A', '0E'])
    return first_byte + "".join([f":{random.randint(0, 255):02x}" for _ in range(5)])

def change_mac(interface='en0', new_mac=None):
    """更改MAC地址"""
    if not new_mac:
        new_mac = generate_random_mac()
    
    print(f"尝试将MAC地址更改为: {new_mac}")
    
    try:
        # 先禁用接口
        subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
        
        # 更改MAC地址
        subprocess.run(['sudo', 'ifconfig', interface, 'ether', new_mac], check=True)
        
        # 启用接口
        subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
        
        # 等待几秒让网络重新连接
        sleep(5)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"更改MAC地址时出错: {e.output.decode('utf-8') if e.output else str(e)}")
        return False

def main():
    print("=== macOS MAC地址更改工具 ===")
    
    # 默认使用en0 (通常是Wi-Fi接口)
    interface = input(f"输入网络接口名称(默认en0): ") or 'en0'
    
    current_mac = get_current_mac(interface)
    
    if current_mac:
        print(f"\n当前MAC地址: {current_mac}")
    else:
        print(f"\n无法获取接口 {interface} 的MAC地址，请确认接口名称正确")
        sys.exit(1)
    
    choice = input("\n要随机生成MAC地址吗？(y/n): ").lower()
    
    if choice == 'y':
        new_mac = generate_random_mac()
    else:
        new_mac = input("输入新的MAC地址(格式: 00:11:22:33:44:55): ").strip()
        if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', new_mac):
            print("无效的MAC地址格式！")
            sys.exit(1)
    
    if change_mac(interface, new_mac):
        print("\nMAC地址更改成功！")
        # 验证更改
        updated_mac = get_current_mac(interface)
        if updated_mac and updated_mac.lower() == new_mac.lower():
            print(f"验证: 当前MAC地址: {updated_mac}")
        else:
            print("警告: 无法验证MAC地址是否已更改")
    else:
        print("\nMAC地址更改失败")
    
    print("\n注意: 重启后MAC地址可能会恢复原样")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("需要管理员权限，请使用sudo运行此脚本")
        print("示例: sudo python3 change_mac_mac.py")
        sys.exit(1)
    main()