import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
import time

# 创建存储目录
os.makedirs("images", exist_ok=True)
os.makedirs("plans", exist_ok=True)

# 定义颜色方案
COLORS = {
    "primary": "#3498db",    # 主色调
    "secondary": "#2ecc71",  # 次要色调
    "accent": "#e74c3c",     # 强调色
    "bg": "#f5f7fa",         # 背景色
    "text": "#2c3e50",       # 文本色
    "light_text": "#7f8c8d", # 浅色文本
    "light_bg": "#ecf0f1",   # 浅色背景
    "hover": "#2980b9",      # 悬停色
    "card_bg": "#ffffff",    # 卡片背景色
    "border": "#dfe4ea"      # 边框颜色
}

class TravelPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("旅游规划生成器")
        self.root.geometry("1100x750")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(1000, 700)  # 设置最小窗口大小
        
        # 设置字体
        self.title_font = font.Font(family="Heiti SC", size=28, weight="bold")
        self.subtitle_font = font.Font(family="Heiti SC", size=14)
        self.button_font = font.Font(family="Heiti SC", size=12)
        self.card_title_font = font.Font(family="Heiti SC", size=16, weight="bold")
        self.content_font = font.Font(family="Heiti SC", size=12)
        
        # 加载动画图片
        self.loading_frames = []
        try:
            # 如果没有加载动画图片，我们将使用简单的进度条
            pass
        except:
            pass
        
        # 初始化城市和分类数据
        self.load_city_data()
        
        # 创建主界面
        self.create_main_page()
        
        # 存储用户选择
        self.selected_city = None
        self.selected_category = None
        self.selected_subcategory = None
        
        # 创建页面导航历史
        self.navigation_history = []

    def load_city_data(self):
        """加载城市和分类数据"""
        self.city_data = {}
        
        # 解析induction.me文件
        try:
            with open("induction.me", "r", encoding="utf-8") as f:
                content = f.read()
                
            current_city = None
            current_category = None
            
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是新城市
                if not line.startswith("人文景观") and not line.startswith("自然景观") and not line.startswith("饮食文化") and not any(c.isdigit() for c in line):
                    current_city = line.replace("：", "").strip()
                    if current_city not in self.city_data:
                        self.city_data[current_city] = {
                            "人文景观": [], 
                            "自然景观": [], 
                            "饮食文化": []
                        }
                
                # 检查是否是新分类
                elif line.startswith("人文景观"):
                    current_category = "人文景观"
                elif line.startswith("自然景观"):
                    current_category = "自然景观"
                elif line.startswith("饮食文化"):
                    current_category = "饮食文化"
                
                # 处理分类内容
                elif current_city and current_category and "：" not in line:
                    items = [item.strip() for item in line.replace("，", ",").split(",")]
                    for item in items:
                        if item and not item.isdigit() and item not in self.city_data[current_city][current_category]:
                            if item.strip():  # 确保不添加空字符串
                                self.city_data[current_city][current_category].append(item.strip())
        
        except Exception as e:
            print(f"加载城市数据出错: {e}")
            # 如果出错，使用默认数据
            self.city_data = {
                "北京": {
                    "人文景观": ["故宫博物院", "八达岭长城", "颐和园"],
                    "自然景观": ["百里画廊", "京东大峡谷", "八达岭国家森林公园"],
                    "饮食文化": ["北京烤鸭", "稻香村糕点", "涮羊肉"]
                }
            }

    def create_main_page(self):
        """创建主页面"""
        # 清除当前页面内容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建欢迎标题区域
        title_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        title_frame.pack(pady=(10, 30))
        
        # 添加应用标题
        title_label = tk.Label(
            title_frame, 
            text="旅游规划生成器", 
            font=self.title_font, 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        )
        title_label.pack()
        
        # 添加应用副标题
        subtitle_label = tk.Label(
            title_frame, 
            text="选择一个城市开始您的旅程规划", 
            font=self.subtitle_font, 
            bg=COLORS["bg"], 
            fg=COLORS["light_text"]
        )
        subtitle_label.pack(pady=8)
        
        # 创建城市选择标题
        city_title_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        city_title_frame.pack(fill=tk.X, pady=(0, 15))
        
        city_title = tk.Label(
            city_title_frame,
            text="目的地选择",
            font=self.card_title_font,
            bg=COLORS["bg"],
            fg=COLORS["text"]
        )
        city_title.pack(side=tk.LEFT)
        
        # 城市选择提示线
        separator = ttk.Separator(city_title_frame, orient='horizontal')
        separator.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # 创建城市选择区域（使用网格布局）
        city_container = tk.Frame(main_frame, bg=COLORS["bg"])
        city_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动区域
        canvas = tk.Canvas(city_container, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(city_container, orient="vertical", command=canvas.yview)
        
        city_frame = tk.Frame(canvas, bg=COLORS["bg"])
        
        # 配置滚动
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas_frame = canvas.create_window((0, 0), window=city_frame, anchor="nw")
        
        # 更新canvas滚动区域
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # 同时调整窗口宽度
            canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
            
        city_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=canvas.winfo_width()))
        
        # 启用鼠标滚轮滚动
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 创建城市网格
        cities = sorted(list(self.city_data.keys()))
        row, col = 0, 0
        max_cols = 4  # 每行显示的城市数量
        
        # 配置网格
        for i in range(20):  # 预设更多行
            city_frame.grid_rowconfigure(i, weight=1)
            
        for i in range(max_cols):
            city_frame.grid_columnconfigure(i, weight=1)
        
        # 添加城市卡片
        for city in cities:
            # 创建城市卡片容器
            city_card = tk.Frame(
                city_frame, 
                bg=COLORS["card_bg"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=15,
                pady=15,
                width=200,
                height=150
            )
            city_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            city_card.grid_propagate(False)  # 保持卡片大小固定
            
            # 添加城市名称
            city_name = tk.Label(
                city_card,
                text=city,
                font=self.card_title_font,
                bg=COLORS["card_bg"],
                fg=COLORS["text"],
                anchor="center"
            )
            city_name.pack(pady=(10, 15))
            
            # 添加选择按钮
            select_button = tk.Button(
                city_card,
                text="选择此城市",
                font=self.button_font,
                bg=COLORS["primary"],
                fg="white",
                activebackground=COLORS["hover"],
                activeforeground="white",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda c=city: self.show_city_detail(c)
            )
            select_button.pack(pady=5)
            
            # 更新行列索引
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
        # 添加底部版权信息
        footer_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 旅游规划生成器 - 使用AI技术定制您的旅行计划",
            font=("Heiti SC", 10),
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        footer_text.pack()

    def show_city_detail(self, city):
        """显示城市详情页面"""
        self.selected_city = city
        self.navigation_history.append("main")
        
        # 清除当前页面内容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建顶部导航栏
        nav_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 添加返回按钮
        back_button = tk.Button(
            nav_frame,
            text="← 返回城市选择",
            font=self.button_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.create_main_page
        )
        back_button.pack(side=tk.LEFT)
        
        # 创建城市标题区域
        title_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        title_frame.pack(fill=tk.X, pady=15)
        
        # 城市标题
        title_label = tk.Label(
            title_frame, 
            text=f"{city} · 旅游规划", 
            font=self.title_font, 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        )
        title_label.pack(side=tk.LEFT)
        
        # 添加提示
        guide_frame = tk.Frame(main_frame, bg=COLORS["light_bg"], padx=15, pady=15)
        guide_frame.pack(fill=tk.X, pady=15)
        
        guide_text = tk.Label(
            guide_frame,
            text=f"请选择您在{city}感兴趣的旅游类别",
            font=self.subtitle_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"]
        )
        guide_text.pack()
        
        # 创建分类选择区域
        categories_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # 添加三个分类
        categories = ["人文景观", "自然景观", "饮食文化"]
        category_icons = ["🏛️", "🏞️", "🍲"]  # 使用Emoji作为图标
        category_desc = [
            "探索历史文化遗迹和人文景点",
            "领略壮美自然风光和地理奇观",
            "品尝当地特色美食和餐饮文化"
        ]
        
        for i, (category, icon, desc) in enumerate(zip(categories, category_icons, category_desc)):
            # 创建分类卡片
            category_card = tk.Frame(
                categories_frame, 
                bg=COLORS["card_bg"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=20,
                pady=20
            )
            category_card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            
            # 添加图标
            icon_label = tk.Label(
                category_card,
                text=icon,
                font=("Heiti SC", 36),
                bg=COLORS["card_bg"],
                fg=COLORS["primary"]
            )
            icon_label.pack(pady=(5, 10))
            
            # 添加分类标题
            category_title = tk.Label(
                category_card,
                text=category,
                font=self.card_title_font,
                bg=COLORS["card_bg"],
                fg=COLORS["text"]
            )
            category_title.pack(pady=(0, 10))
            
            # 添加分类描述
            desc_label = tk.Label(
                category_card,
                text=desc,
                font=self.content_font,
                bg=COLORS["card_bg"],
                fg=COLORS["light_text"],
                wraplength=220
            )
            desc_label.pack(pady=(0, 15))
            
            # 添加选择按钮
            category_button = tk.Button(
                category_card,
                text="查看详情",
                font=self.button_font,
                bg=COLORS["secondary"],
                fg="white",
                activebackground="#27ae60",  # 深绿色
                activeforeground="white",
                relief=tk.FLAT,
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda c=category: self.show_subcategory(c)
            )
            category_button.pack(pady=5)
        
        # 添加底部版权信息
        footer_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 旅游规划生成器 - 使用AI技术定制您的旅行计划",
            font=("Heiti SC", 10),
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        footer_text.pack()

    def show_subcategory(self, category):
        """显示子类别选择页面"""
        self.selected_category = category
        self.navigation_history.append("city")
        
        # 清除当前页面内容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建顶部导航栏
        nav_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 添加返回按钮
        back_button = tk.Button(
            nav_frame,
            text="← 返回分类选择",
            font=self.button_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: self.show_city_detail(self.selected_city)
        )
        back_button.pack(side=tk.LEFT)
        
        # 添加当前路径
        path_label = tk.Label(
            nav_frame,
            text=f"{self.selected_city} > {category}",
            font=self.content_font,
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        path_label.pack(side=tk.RIGHT)
        
        # 创建标题区域
        title_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        title_frame.pack(fill=tk.X, pady=15)
        
        # 添加标题
        title_label = tk.Label(
            title_frame, 
            text=f"{self.selected_city} · {category}", 
            font=self.title_font, 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        )
        title_label.pack(side=tk.LEFT)
        
        # 添加提示
        guide_frame = tk.Frame(main_frame, bg=COLORS["light_bg"], padx=15, pady=15)
        guide_frame.pack(fill=tk.X, pady=15)
        
        guide_text = tk.Label(
            guide_frame,
            text=f"请选择您在{self.selected_city}感兴趣的{category}",
            font=self.subtitle_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"]
        )
        guide_text.pack()
        
        # 获取子类别
        subcategories = self.city_data[self.selected_city][category]
        
        # 如果没有子类别，显示提示信息
        if not subcategories:
            no_data_frame = tk.Frame(main_frame, bg=COLORS["bg"], pady=50)
            no_data_frame.pack(fill=tk.BOTH, expand=True)
            
            no_data_label = tk.Label(
                no_data_frame,
                text=f"抱歉，暂无{self.selected_city}的{category}数据",
                font=self.subtitle_font,
                bg=COLORS["bg"],
                fg=COLORS["text"]
            )
            no_data_label.pack()
            return
        
        # 创建子类别选择区域（使用滚动区域）
        container = tk.Frame(main_frame, bg=COLORS["bg"])
        container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建滚动区域
        canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        subcategories_frame = tk.Frame(canvas, bg=COLORS["bg"])
        
        # 配置滚动
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas_frame = canvas.create_window((0, 0), window=subcategories_frame, anchor="nw")
        
        # 更新canvas滚动区域
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # 同时调整窗口宽度
            canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
            
        subcategories_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=canvas.winfo_width()))
        
        # 启用鼠标滚轮滚动
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 设置网格
        max_cols = 3  # 每行显示的子类别数量
        row, col = 0, 0
        
        for i in range(10):  # 预设更多行
            subcategories_frame.grid_rowconfigure(i, weight=1)
            
        for i in range(max_cols):
            subcategories_frame.grid_columnconfigure(i, weight=1)
        
        # 添加子类别卡片
        for subcategory in subcategories:
            # 创建子类别卡片
            subcategory_card = tk.Frame(
                subcategories_frame, 
                bg=COLORS["card_bg"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=20,
                pady=20
            )
            subcategory_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # 添加子类别标题
            subcategory_title = tk.Label(
                subcategory_card,
                text=subcategory,
                font=self.card_title_font,
                bg=COLORS["card_bg"],
                fg=COLORS["text"]
            )
            subcategory_title.pack(pady=(5, 15))
            
            # 添加选择按钮
            subcategory_button = tk.Button(
                subcategory_card,
                text="生成旅游规划",
                font=self.button_font,
                bg=COLORS["accent"],
                fg="white",
                activebackground="#c0392b",  # 深红色
                activeforeground="white",
                relief=tk.FLAT,
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda sc=subcategory: self.generate_plan(sc)
            )
            subcategory_button.pack(pady=5)
            
            # 更新行列索引
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 添加底部版权信息
        footer_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 旅游规划生成器 - 使用AI技术定制您的旅行计划",
            font=("Heiti SC", 10),
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        footer_text.pack()

    def generate_plan(self, subcategory):
        """生成旅游规划"""
        self.selected_subcategory = subcategory
        self.navigation_history.append("subcategory")
        
        # 清除当前页面内容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建加载页面
        loading_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        loading_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加加载标题
        loading_title = tk.Label(
            loading_frame,
            text="正在生成您的专属旅游规划...",
            font=self.title_font,
            bg=COLORS["bg"],
            fg=COLORS["primary"]
        )
        loading_title.pack(pady=(150, 20))
        
        # 添加当前选择信息
        selection_info = tk.Label(
            loading_frame,
            text=f"城市：{self.selected_city} | 类别：{self.selected_category} | 特色：{self.selected_subcategory}",
            font=self.subtitle_font,
            bg=COLORS["bg"],
            fg=COLORS["text"]
        )
        selection_info.pack(pady=(0, 30))
        
        # 添加进度条
        progress_frame = tk.Frame(loading_frame, bg=COLORS["bg"])
        progress_frame.pack(pady=10)
        
        progress_style = ttk.Style()
        progress_style.theme_use('default')
        progress_style.configure(
            "TProgressbar",
            thickness=10,
            troughcolor=COLORS["light_bg"],
            background=COLORS["primary"]
        )
        
        progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            length=400,
            mode="indeterminate",
            style="TProgressbar"
        )
        progress.pack()
        progress.start(15)
        
        # 添加加载提示
        loading_tips = [
            "正在为您分析目的地交通情况...",
            "正在为您筛选最佳旅游路线...",
            "正在为您整理当地特色美食...",
            "正在为您规划合理的游玩时间...",
            "正在为您推荐舒适的住宿选择..."
        ]
        
        tip_label = tk.Label(
            loading_frame,
            text=loading_tips[0],
            font=self.content_font,
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        tip_label.pack(pady=20)
        
        # 定时更新提示文字
        def update_tip(index=0):
            if index < len(loading_tips):
                tip_label.config(text=loading_tips[index])
                self.root.after(2000, update_tip, (index+1) % len(loading_tips))
        
        update_tip()
        
        # 添加取消按钮
        cancel_button = tk.Button(
            loading_frame,
            text="取消",
            font=self.button_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2",
            command=lambda: self.show_subcategory(self.selected_category)
        )
        cancel_button.pack(pady=30)
        
        # 在后台线程中生成规划
        threading.Thread(target=self.process_plan_generation).start()

    def process_plan_generation(self):
        """在后台处理旅游规划生成"""
        # 模拟加载时间
        time.sleep(3)
        
        # 调用DeepSeek API生成旅游规划
        plan = self.call_deepseek_api()
        
        # 在主线程中更新UI
        self.root.after(0, lambda: self.show_plan_result(plan))

    def call_deepseek_api(self):
        """调用DeepSeek API生成旅游规划"""
        try:
            # 从配置文件中读取API密钥
            api_key = ""
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("deepseek_api_key", "")
            except:
                pass
            
            prompt = f"""
            请根据以下信息生成一个详细的三天旅游行程规划：
            城市：{self.selected_city}
            选择的旅游类别：{self.selected_category}
            特别兴趣点：{self.selected_subcategory}
            
            请提供一个包含以下内容的旅游规划：
            1. 每天的行程安排（上午、下午、晚上）
            2. 推荐的景点和活动，包括游玩时间
            3. 餐饮推荐，包括当地特色美食
            4. 交通建议
            5. 住宿推荐
            
            格式要求：分三天详细规划，每天的行程清晰列出，内容要丰富实用，使用Markdown格式。
            """
            
            # 如果没有配置API密钥，返回模拟数据
            if not api_key:
                return self.generate_mock_plan()
            
            # 实际API调用逻辑
            # 使用DeepSeek API生成旅游规划
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"API调用失败: {response.status_code} - {response.text}")
                return self.generate_mock_plan()
                
        except Exception as e:
            print(f"生成旅游规划时出错: {e}")
            return self.generate_mock_plan()

    def generate_mock_plan(self):
        """生成模拟的旅游规划数据"""
        return f"""
# {self.selected_city}三日游 - {self.selected_category}特色行程

## 第一天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 游览{self.selected_subcategory}，这是{self.selected_city}最著名的{self.selected_category}之一
  - 推荐在此处停留约2.5小时，可以深入了解当地文化特色

### 下午
- 12:30-13:30 在附近的"老字号餐厅"享用午餐
  - 推荐菜品：当地特色小吃
- 14:00-17:00 参观{self.selected_city}博物馆
  - 了解{self.selected_city}的历史文化发展

### 晚上
- 18:00-19:30 在"夜市美食街"品尝当地特色美食
- 20:00-21:30 欣赏{self.selected_city}夜景
- 22:00 返回酒店休息

## 第二天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 前往{self.city_data[self.selected_city][self.selected_category][0] if len(self.city_data[self.selected_city][self.selected_category]) > 0 else "景点A"}
  - 建议请当地导游讲解，更好地了解当地文化

### 下午
- 12:30-13:30 在"人气餐厅"享用午餐
- 14:00-17:00 游览{self.city_data[self.selected_city][self.selected_category][1] if len(self.city_data[self.selected_city][self.selected_category]) > 1 else "景点B"}
  - 这里是{self.selected_city}的另一处著名{self.selected_category}

### 晚上
- 18:00-20:00 参加当地文化体验活动
- 20:30 返回酒店休息

## 第三天

### 上午
- 8:00-9:00 酒店早餐
- 9:30-12:00 参观{self.city_data[self.selected_city][self.selected_category][2] if len(self.city_data[self.selected_city][self.selected_category]) > 2 else "景点C"}

### 下午
- 12:30-13:30 享用午餐
- 14:00-16:00 购物时间，推荐前往当地特色商业街
- 16:30-18:00 自由活动，可以再次游览最喜欢的景点

### 晚上
- 18:30-20:00 告别晚餐，品尝尚未尝试过的当地美食
- 20:30 返回酒店，准备第二天离开

## 住宿推荐
- 豪华选择：{self.selected_city}国际大酒店
- 中档选择：{self.selected_city}舒适酒店
- 经济选择：{self.selected_city}青年旅舍

## 交通建议
- 市内交通：建议使用地铁或出租车
- 景点间交通：可以使用公共交通或打车，部分景点可步行到达
- 特别提示：周末和节假日期间，部分景点人流量大，建议提前规划行程

## 实用提示
- 最佳旅游季节：春秋两季
- 推荐携带物品：舒适的鞋子、相机、水和零食
- 当地紧急电话：110（警察）、120（救护车）
        """

    def show_plan_result(self, plan):
        """显示旅游规划结果"""
        # 清除当前页面内容
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建顶部导航栏
        nav_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 添加返回按钮
        back_button = tk.Button(
            nav_frame,
            text="← 返回选择页面",
            font=self.button_font,
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=lambda: self.show_subcategory(self.selected_category)
        )
        back_button.pack(side=tk.LEFT)
        
        # 添加路径
        path_label = tk.Label(
            nav_frame,
            text=f"{self.selected_city} > {self.selected_category} > {self.selected_subcategory}",
            font=self.content_font,
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        path_label.pack(side=tk.RIGHT)
        
        # 创建标题区域
        title_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        title_frame.pack(fill=tk.X, pady=15)
        
        # 添加标题
        title_label = tk.Label(
            title_frame, 
            text=f"{self.selected_city} · 旅游规划", 
            font=self.title_font, 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        )
        title_label.pack(side=tk.LEFT)
        
        # 添加保存按钮
        save_button = tk.Button(
            title_frame,
            text="保存规划",
            font=self.button_font,
            bg=COLORS["secondary"],
            fg="white",
            activebackground="#27ae60",  # 深绿色
            activeforeground="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self.save_plan(plan)
        )
        save_button.pack(side=tk.RIGHT)
        
        # 创建规划内容区域
        content_frame = tk.Frame(main_frame, bg=COLORS["card_bg"], padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # 创建文本框和滚动条
        text_frame = tk.Frame(content_frame, bg=COLORS["card_bg"])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # 设置文本样式
        text_style = tk.Text(text_frame, bg=COLORS["card_bg"], fg=COLORS["text"], wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_style.yview)
        text_style.configure(yscrollcommand=scrollbar.set)
        
        # 设置标题和段落标签
        text_style.tag_configure("title", font=("Heiti SC", 20, "bold"), foreground=COLORS["primary"], spacing1=10, spacing3=10)
        text_style.tag_configure("heading1", font=("Heiti SC", 18, "bold"), foreground=COLORS["text"], spacing1=10, spacing3=6)
        text_style.tag_configure("heading2", font=("Heiti SC", 16, "bold"), foreground=COLORS["text"], spacing1=8, spacing3=4)
        text_style.tag_configure("normal", font=("Heiti SC", 12), foreground=COLORS["text"], spacing1=3, spacing3=3)
        text_style.tag_configure("bullet", font=("Heiti SC", 12), foreground=COLORS["text"], spacing1=2, lmargin1=20, lmargin2=30)
        
        # 解析Markdown格式并展示
        lines = plan.strip().split('\n')
        for line in lines:
            if line.startswith('# '):
                text_style.insert(tk.END, line[2:] + '\n', "title")
            elif line.startswith('## '):
                text_style.insert(tk.END, line[3:] + '\n', "heading1")
            elif line.startswith('### '):
                text_style.insert(tk.END, line[4:] + '\n', "heading2")
            elif line.startswith('- '):
                text_style.insert(tk.END, "• " + line[2:] + '\n', "bullet")
            elif line.startswith('  - '):
                text_style.insert(tk.END, "   ◦ " + line[4:] + '\n', "bullet")
            else:
                text_style.insert(tk.END, line + '\n', "normal")
        
        text_style.config(state="disabled")  # 设置为只读
        
        text_style.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加底部版权信息
        footer_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 旅游规划生成器 - 使用AI技术定制您的旅行计划",
            font=("Heiti SC", 10),
            bg=COLORS["bg"],
            fg=COLORS["light_text"]
        )
        footer_text.pack()

    def save_plan(self, plan):
        """保存旅游规划到文件"""
        try:
            # 创建保存目录
            os.makedirs("plans", exist_ok=True)
            
            # 生成文件名
            filename = f"plans/{self.selected_city}_{self.selected_category}_{self.selected_subcategory}规划.md"
            
            # 保存规划
            with open(filename, "w", encoding="utf-8") as f:
                f.write(plan)
            
            # 显示保存成功信息
            messagebox.showinfo("保存成功", f"旅游规划已保存至 {filename}")
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存规划时出错: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelPlannerApp(root)
    root.mainloop()
