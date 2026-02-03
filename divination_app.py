import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import random

class LunarCalendar:
    """农历查询类"""
    LUNAR_MONTHS = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    
    @classmethod
    def get_lunar_date(cls):
        """获取今日农历日期"""
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        
        lunar_month = cls.LUNAR_MONTHS[(month - 1) % 12]
        
        # 计算时辰
        if hour < 1 or hour >= 23:
            shichen = "子时"
            shichen_num = 1
        elif hour < 3:
            shichen = "丑时"
            shichen_num = 2
        elif hour < 5:
            shichen = "寅时"
            shichen_num = 3
        elif hour < 7:
            shichen = "卯时"
            shichen_num = 4
        elif hour < 9:
            shichen = "辰时"
            shichen_num = 5
        elif hour < 11:
            shichen = "巳时"
            shichen_num = 6
        elif hour < 13:
            shichen = "午时"
            shichen_num = 7
        elif hour < 15:
            shichen = "未时"
            shichen_num = 8
        elif hour < 17:
            shichen = "申时"
            shichen_num = 9
        elif hour < 19:
            shichen = "酉时"
            shichen_num = 10
        elif hour < 21:
            shichen = "戌时"
            shichen_num = 11
        else:
            shichen = "亥时"
            shichen_num = 12
        
        return {
            "月数字": month % 12 or 12,
            "日数字": day % 9 or 9,
            "时数字": shichen_num % 9 or 9,
            "时辰": shichen,
            "农历": f"{lunar_month}"
        }

class DivinationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ 隧三小六壬占卜器 v3.1 ✨")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 700)
        
        # 颜色方案
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'primary': '#e94560',
            'secondary': '#533483',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'text_light': '#ffffff',
            'text_muted': '#b0b0b0',
            'accent_gold': '#FFD700',
            'accent_blue': '#2196F3',
            'accent_purple': '#9C27B0'
        }
        
        # 设置窗口背景
        self.root.configure(bg=self.colors['bg_dark'])
        
        # 初始化数据
        self.elements = ["大安", "留连", "速喜", "赤口", "小吉", "空亡", "病符", "桃花", "天德"]
        
        # 掌诀颜色映射
        self.element_colors = {
            "大安": self.colors['success'],
            "留连": self.colors['warning'],
            "速喜": self.colors['danger'],
            "赤口": self.colors['accent_purple'],
            "小吉": self.colors['accent_blue'],
            "空亡": "#607D8B",
            "病符": "#795548",
            "桃花": "#E91E63",
            "天德": self.colors['accent_gold']
        }
        
        # 当前占卜结果
        self.current_result = None
        self.current_summary = ""
        
        # 创建界面
        self.create_menu()
        self.create_interface()
        
        # 窗口居中
        self.center_window()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        menubar.add_cascade(label="📁 文件", menu=file_menu)
        file_menu.add_command(label="💾 保存结果", command=self.save_result, accelerator="Ctrl+S")
        file_menu.add_command(label="📤 导出为文本", command=self.export_text)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 退出", command=self.root.quit, accelerator="Ctrl+Q")
        
        # 解读菜单 - 新增的综合解读菜单
        analysis_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        menubar.add_cascade(label="📖 综合解读", menu=analysis_menu)
        analysis_menu.add_command(label="📊 查看详细解读", command=self.show_summary_analysis, accelerator="Ctrl+A")
        analysis_menu.add_command(label="📈 运势趋势分析", command=self.show_trend_analysis)
        analysis_menu.add_command(label="💡 开运建议", command=self.show_luck_suggestions)
        analysis_menu.add_separator()
        analysis_menu.add_command(label="🔄 刷新解读", command=self.refresh_analysis)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        menubar.add_cascade(label="🔧 工具", menu=tools_menu)
        tools_menu.add_command(label="📅 今日农历", command=self.show_lunar_calendar, accelerator="Ctrl+L")
        tools_menu.add_command(label="🌙 使用农历占卜", command=self.use_lunar_for_divination)
        tools_menu.add_command(label="🎲 随机占卜", command=self.random_divination)
        tools_menu.add_command(label="⚡ 快速占卜", command=self.quick_divination)
        tools_menu.add_separator()
        tools_menu.add_command(label="🎨 更换主题", command=self.change_theme)
        
        # 历史菜单
        history_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        menubar.add_cascade(label="📜 历史", menu=history_menu)
        history_menu.add_command(label="📋 查看历史记录", command=self.show_history)
        history_menu.add_command(label="🗑️ 清除历史", command=self.clear_history)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg_medium'], fg=self.colors['text_light'])
        menubar.add_cascade(label="❓ 帮助", menu=help_menu)
        help_menu.add_command(label="📚 使用教程", command=self.show_tutorial)
        help_menu.add_command(label="📖 掌诀详解", command=self.show_element_guide)
        help_menu.add_separator()
        help_menu.add_command(label="⚖️ 版权信息", command=self.show_copyright)
        help_menu.add_command(label="ℹ️ 关于", command=self.show_about)
        
        # 绑定快捷键
        self.root.bind('<Control-s>', lambda e: self.save_result())
        self.root.bind('<Control-a>', lambda e: self.show_summary_analysis())
        self.root.bind('<Control-l>', lambda e: self.show_lunar_calendar())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def create_interface(self):
        """创建主界面"""
        # 创建主容器
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # 1. 标题区域
        self.create_title_section(main_container)
        
        # 2. 输入区域 - 确保可见
        self.create_input_section(main_container)
        
        # 3. 掌诀结果区域
        self.create_result_section(main_container)
        
        # 4. 快捷操作区域（替代原来的综合解读区域）
        self.create_quick_actions_section(main_container)
        
        # 5. 状态栏
        self.create_status_bar()
    
    def create_title_section(self, parent):
        """创建标题区域"""
        title_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        title_frame.pack(fill="x", pady=(0, 15))
        
        # 主标题
        title_label = tk.Label(title_frame,
                              text="✨ 隧三小六壬占卜器 ✨",
                              font=('Microsoft YaHei UI', 30, 'bold'),
                              bg=self.colors['bg_dark'],
                              fg=self.colors['accent_gold'])
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(title_frame,
                                 text="六壬神课 · 掌诀推演 · 运势预测",
                                 font=('Microsoft YaHei UI', 14),
                                 bg=self.colors['bg_dark'],
                                 fg=self.colors['text_muted'])
        subtitle_label.pack()
        
        # 装饰线
        sep = tk.Frame(title_frame, height=2, bg=self.colors['primary'])
        sep.pack(fill="x", pady=10)
        
        # 今日时间
        time_frame = tk.Frame(title_frame, bg=self.colors['bg_medium'], relief="ridge", bd=2)
        time_frame.pack(pady=8)
        
        now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        time_label = tk.Label(time_frame,
                             text=f"📅 当前时间：{now}",
                             font=('Microsoft YaHei UI', 12),
                             bg=self.colors['bg_medium'],
                             fg=self.colors['text_light'],
                             padx=15,
                             pady=8)
        time_label.pack()
    
    def create_input_section(self, parent):
        """创建输入区域"""
        input_frame = tk.LabelFrame(parent,
                                   text="🔢 输入三个数字 (1-9)",
                                   font=('Microsoft YaHei UI', 14, 'bold'),
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['text_light'],
                                   relief="groove",
                                   bd=2)
        input_frame.pack(fill="x", pady=15, padx=5)
        
        # 输入框容器
        input_container = tk.Frame(input_frame, bg=self.colors['bg_medium'])
        input_container.pack(pady=20, padx=30)
        
        # 创建三个输入框
        self.num_vars = []
        self.entry_widgets = []
        
        for i in range(3):
            box_frame = tk.Frame(input_container, bg=self.colors['bg_medium'])
            box_frame.pack(side="left", padx=35, pady=10)
            
            # 数字标签
            label = tk.Label(box_frame,
                            text=f"数字 {i+1}",
                            font=('Microsoft YaHei UI', 13, 'bold'),
                            bg=self.colors['bg_medium'],
                            fg=self.colors['accent_blue'])
            label.pack()
            
            # 输入框
            entry = tk.Entry(box_frame,
                           font=('Microsoft YaHei UI', 20, 'bold'),
                           width=6,
                           justify='center',
                           bd=4,
                           relief="solid",
                           bg=self.colors['bg_light'],
                           fg=self.colors['text_light'],
                           insertbackground='white')
            entry.pack(pady=10, ipady=8)
            self.entry_widgets.append(entry)
            
            # 提示文字
            tip_text = ["月", "日", "时"][i]
            tip = tk.Label(box_frame,
                          text=f"(通常对应农历{tip_text})",
                          font=('Microsoft YaHei UI', 11),
                          bg=self.colors['bg_medium'],
                          fg=self.colors['text_muted'])
            tip.pack()
        
        # 按钮区域
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_medium'])
        button_frame.pack(pady=15)
        
        # 按钮列表
        buttons = [
            ("🎯 开始占卜", self.calculate_divination, self.colors['primary']),
            ("🎲 随机数字", self.fill_random_numbers, self.colors['secondary']),
            ("🌙 农历数字", self.use_lunar_for_divination, self.colors['accent_blue']),
            ("🗑️ 清空", self.clear_inputs, self.colors['warning']),
            ("📖 查看解读", self.show_summary_analysis, self.colors['accent_purple'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Microsoft YaHei UI', 12),
                          bg=color,
                          fg='white',
                          bd=0,
                          padx=20,
                          pady=10,
                          relief="raised",
                          cursor="hand2",
                          activebackground=self.lighten_color(color, 20))
            btn.pack(side="left", padx=8, pady=5)
    
    def create_result_section(self, parent):
        """创建结果展示区域"""
        result_frame = tk.LabelFrame(parent,
                                    text="📊 掌诀推演结果",
                                    font=('Microsoft YaHei UI', 14, 'bold'),
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text_light'],
                                    relief="groove",
                                    bd=2)
        result_frame.pack(fill="both", expand=True, pady=10, padx=5)
        
        # 使用Frame容器
        container = tk.Frame(result_frame, bg=self.colors['bg_medium'])
        container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # 配置网格布局
        container.grid_rowconfigure(0, weight=1)
        for i in range(3):
            container.grid_columnconfigure(i, weight=1, uniform="result_cols")
        
        # 三个掌诀显示区域
        self.result_labels = []
        self.detail_texts = []
        
        for i in range(3):
            # 每个掌诀的容器
            element_frame = tk.Frame(container, 
                                   bg=self.colors['bg_light'],
                                   relief="ridge",
                                   bd=3)
            element_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            element_frame.grid_rowconfigure(2, weight=1)
            element_frame.grid_columnconfigure(0, weight=1)
            
            # 标题
            title_label = tk.Label(element_frame,
                                 text=f"第{i+1}掌",
                                 font=('Microsoft YaHei UI', 16, 'bold'),
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['accent_gold'])
            title_label.grid(row=0, column=0, pady=(15, 10), sticky="n")
            
            # 掌诀名称显示
            result_label = tk.Label(element_frame,
                                  text="待推算",
                                  font=('Microsoft YaHei UI', 24, 'bold'),
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['text_light'],
                                  width=10,
                                  height=2,
                                  relief="solid",
                                  bd=4)
            result_label.grid(row=1, column=0, pady=15, padx=15, sticky="n")
            self.result_labels.append(result_label)
            
            # 详细信息框架
            detail_frame = tk.Frame(element_frame, bg=self.colors['bg_light'])
            detail_frame.grid(row=2, column=0, pady=10, padx=15, sticky="nsew")
            detail_frame.grid_rowconfigure(0, weight=1)
            detail_frame.grid_columnconfigure(0, weight=1)
            
            # 详细信息文本区域
            detail_text = scrolledtext.ScrolledText(detail_frame,
                                                   height=15,
                                                   font=('Microsoft YaHei UI', 12),
                                                   bg=self.colors['bg_light'],
                                                   fg=self.colors['text_light'],
                                                   relief="flat",
                                                   bd=2,
                                                   wrap="word",
                                                   spacing1=3)
            detail_text.grid(row=0, column=0, sticky="nsew")
            detail_text.config(state='disabled')
            self.detail_texts.append(detail_text)
    
    def create_quick_actions_section(self, parent):
        """创建快捷操作区域（替代原来的综合解读区域）"""
        actions_frame = tk.LabelFrame(parent,
                                     text="⚡ 快捷操作与提示",
                                     font=('Microsoft YaHei UI', 14, 'bold'),
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['text_light'],
                                     relief="groove",
                                     bd=2)
        actions_frame.pack(fill="x", pady=10, padx=5)
        
        # 创建提示文本区域
        self.hint_text = scrolledtext.ScrolledText(actions_frame,
                                                  height=10,
                                                  font=('Microsoft YaHei UI', 13),
                                                  bg=self.colors['bg_light'],
                                                  fg=self.colors['text_light'],
                                                  relief="solid",
                                                  bd=2,
                                                  wrap="word",
                                                  spacing1=8,
                                                  spacing3=5)
        self.hint_text.pack(fill="both", expand=True, padx=15, pady=15)
        self.hint_text.config(state='disabled')
        
        # 设置默认提示信息
        self.set_default_hints()
        
        # 快捷按钮区域
        quick_buttons_frame = tk.Frame(actions_frame, bg=self.colors['bg_medium'])
        quick_buttons_frame.pack(fill="x", pady=(0, 10), padx=15)
        
        quick_buttons = [
            ("📖 查看综合解读", self.show_summary_analysis, self.colors['primary']),
            ("💾 保存结果", self.save_result, self.colors['success']),
            ("📅 今日农历", self.show_lunar_calendar, self.colors['accent_blue']),
            ("🔄 重新占卜", self.clear_inputs, self.colors['warning'])
        ]
        
        for text, command, color in quick_buttons:
            btn = tk.Button(quick_buttons_frame,
                          text=text,
                          command=command,
                          font=('Microsoft YaHei UI', 11),
                          bg=color,
                          fg='white',
                          bd=0,
                          padx=15,
                          pady=8,
                          relief="raised",
                          cursor="hand2")
            btn.pack(side="left", padx=8)
    
    def set_default_hints(self):
        """设置默认提示信息"""
        hints = """✨ 欢迎使用隧三小六壬占卜器 v3.1 ✨

💡 使用提示：
1. 在左侧输入三个1-9的数字
2. 点击【开始占卜】按钮进行推算
3. 查看三个掌诀的详细解释
4. 使用【综合解读】菜单查看深度分析

🎯 快捷操作：
• 点击【随机数字】快速生成数字
• 点击【农历数字】使用当前农历时间
• 使用【综合解读】菜单查看详细运势分析
• 使用快捷键 Ctrl+A 快速查看解读

📚 功能亮点：
• 精美的界面设计
• 详细的掌诀解释
• 农历时间查询
• 综合运势分析
• 结果保存功能

🔮 温馨提示：
占卜结果仅供参考，命运掌握在自己手中。
请以积极心态面对生活，创造美好未来。"""
        
        self.hint_text.config(state='normal')
        self.hint_text.delete(1.0, tk.END)
        self.hint_text.insert(1.0, hints)
        self.hint_text.config(state='disabled')
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.root, 
                               bg=self.colors['bg_light'],
                               height=35,
                               relief="sunken",
                               bd=2)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)
        
        # 状态信息
        self.status_label = tk.Label(status_frame,
                                    text="🟢 准备就绪 | 请输入三个数字进行占卜",
                                    font=('Microsoft YaHei UI', 10),
                                    bg=self.colors['bg_light'],
                                    fg=self.colors['text_light'],
                                    anchor='w')
        self.status_label.pack(side="left", padx=15, fill="x", expand=True)
        
        # 快捷提示
        hint_label = tk.Label(status_frame,
                             text="💡 提示：按 Ctrl+A 查看综合解读，Ctrl+S 保存结果",
                             font=('Microsoft YaHei UI', 9),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_muted'])
        hint_label.pack(side="left", padx=10)
        
        # 版权信息
        copyright_label = tk.Label(status_frame,
                                  text="© 2024 小六壬占卜器 v3.1 | 仅供娱乐参考",
                                  font=('Microsoft YaHei UI', 9),
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['text_muted'])
        copyright_label.pack(side="right", padx=15)
    
    def get_elements(self, n1, n2, n3):
        """核心占卜算法"""
        first_index = (n1 - 1) % len(self.elements)
        second_index = (n1 + n2 - 2) % len(self.elements)
        third_index = (n1 + n2 + n3 - 3) % len(self.elements)
        
        return (self.elements[first_index], 
                self.elements[second_index], 
                self.elements[third_index])
    
    def calculate_divination(self):
        """计算占卜结果"""
        try:
            # 获取输入的数字
            numbers = []
            for i, entry in enumerate(self.entry_widgets):
                num_str = entry.get().strip()
                if not num_str:
                    self.status_label.config(text=f"❌ 请输入第{i+1}个数字")
                    return
                
                try:
                    num = int(num_str)
                    if not 1 <= num <= 9:
                        self.status_label.config(text=f"❌ 第{i+1}个数字必须在1-9之间")
                        return
                    numbers.append(num)
                except ValueError:
                    self.status_label.config(text=f"❌ 第{i+1}个输入不是有效的数字")
                    return
            
            n1, n2, n3 = numbers
            
            # 计算掌诀
            elements = self.get_elements(n1, n2, n3)
            self.current_result = elements
            
            # 显示掌诀结果
            for i, element in enumerate(elements):
                color = self.element_colors.get(element, self.colors['text_light'])
                
                # 更新掌诀显示
                self.result_labels[i].config(
                    text=element,
                    fg=color,
                    bg=self.colors['bg_light']
                )
                
                # 更新详细解释
                details = self.get_element_details(element)
                detail_text = f"【{element}】\n\n"
                detail_text += f"📊 吉凶：{details.get('吉凶', '未知')}\n"
                detail_text += f"🏷️ 属性：{details.get('属性', '未知')}\n"
                detail_text += f"🧭 方位：{details.get('方位', '未知')}\n"
                detail_text += f"🎲 数字：{details.get('数字', '未知')}\n"
                detail_text += f"🌈 颜色：{details.get('颜色', '未知')}\n"
                detail_text += f"⏰ 时辰：{details.get('时辰', '未知')}\n\n"
                detail_text += f"📖 含义：\n{details.get('含义', '未知')}\n\n"
                detail_text += f"💡 建议：\n{details.get('建议', '未知')}"
                
                self.detail_texts[i].config(state='normal')
                self.detail_texts[i].delete(1.0, tk.END)
                self.detail_texts[i].insert(1.0, detail_text)
                self.detail_texts[i].config(state='disabled')
            
            # 生成综合解读
            self.generate_summary_analysis(n1, n2, n3, elements)
            
            # 更新提示信息
            self.update_hint_text(n1, n2, n3, elements[2])
            
            self.status_label.config(
                text=f"✅ 占卜完成 | 数字：{n1}, {n2}, {n3} | 结果：{elements[2]} | 按 Ctrl+A 查看详细解读"
            )
            
        except Exception as e:
            self.status_label.config(text=f"❌ 计算过程中发生错误：{str(e)}")
            messagebox.showerror("错误", f"占卜计算失败：{str(e)}")
    
    def generate_summary_analysis(self, n1, n2, n3, elements):
        """生成综合解读分析"""
        final_element = elements[2]
        details = self.get_element_details(final_element)
        
        summary = f"🔮 【{final_element}】综合运势深度解读 🔮\n"
        summary += "═" * 65 + "\n\n"
        
        # 基本信息
        summary += "📊 基本分析\n"
        summary += f"• 占卜数字：{n1}, {n2}, {n3}\n"
        summary += f"• 最终掌诀：{final_element}\n"
        summary += f"• 吉凶等级：{details.get('吉凶', '未知')}\n"
        summary += f"• 五行属性：{details.get('属性', '未知')}\n"
        summary += f"• 有利方位：{details.get('方位', '未知')}\n"
        summary += f"• 吉利数字：{details.get('数字', '未知')}\n"
        summary += f"• 幸运颜色：{details.get('颜色', '未知')}\n"
        summary += f"• 推算时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 运势分析
        summary += "🌟 运势分析\n"
        summary += f"{details.get('运势分析', '暂无详细分析')}\n\n"
        
        # 详细解读
        summary += "📖 掌诀深度解读\n"
        summary += f"{details.get('详细解读', details.get('含义', '暂无详细解读'))}\n\n"
        
        # 建议与提醒
        summary += "💡 建议与提醒\n"
        summary += f"• 适宜事项：{details.get('宜', '暂无建议')}\n"
        summary += f"• 忌讳事项：{details.get('忌', '暂无建议')}\n"
        summary += f"• 开运方法：{details.get('开运', '保持积极心态')}\n\n"
        
        summary += "═" * 65 + "\n"
        summary += "🔮 温馨提示：命运掌握在自己手中，占卜结果仅供参考\n"
        
        self.current_summary = summary
    
    def update_hint_text(self, n1, n2, n3, final_element):
        """更新提示文本"""
        hints = f"✨ 占卜完成 ✨\n\n"
        hints += f"📊 输入数字：{n1}, {n2}, {n3}\n"
        hints += f"🎯 最终结果：{final_element}\n\n"
        hints += "💡 操作提示：\n"
        hints += "• 点击【综合解读】菜单查看详细分析\n"
        hints += "• 使用快捷键 Ctrl+A 快速打开解读窗口\n"
        hints += "• 点击【保存结果】将占卜记录保存到文件\n"
        hints += "• 点击【今日农历】查询农历时间\n\n"
        hints += "📚 掌诀简要：\n"
        hints += self.get_brief_element_info(final_element)
        
        self.hint_text.config(state='normal')
        self.hint_text.delete(1.0, tk.END)
        self.hint_text.insert(1.0, hints)
        self.hint_text.config(state='disabled')
    
    def get_element_details(self, element_name):
        """获取掌诀详情"""
        details = {
            "大安": {
                "吉凶": "★★★★★ 大吉",
                "属性": "青龙星君",
                "方位": "东方",
                "数字": "1, 5, 7",
                "颜色": "青色、绿色",
                "时辰": "寅卯时",
                "含义": "身未动时，属木青龙，凡谋事主一、五、七。象征稳定安宁，如沐春风，万事亨通。",
                "运势分析": "整体运势极佳，如龙得水，势不可挡。事业顺利，贵人相助；感情美满，家庭和睦；财运亨通，投资有利；健康良好，精力充沛。",
                "宜": "求财、出行、婚嫁、动土、上任",
                "忌": "诉讼、争吵",
                "开运": "多穿绿色衣物，佩戴木制饰品，在东方摆放绿植",
                "建议": "适合求财、出行、婚嫁等事宜，宜积极进取"
            },
            "留连": {
                "吉凶": "★★☆☆☆ 凶",
                "属性": "玄武星君",
                "方位": "南方",
                "数字": "2, 8, 10",
                "颜色": "黑色、蓝色",
                "时辰": "巳午时",
                "含义": "卒未归时，属水玄武，凡谋事主二、八、十。象征停滞不前，如陷泥潭，难以自拔。",
                "运势分析": "整体运势不佳，阻碍重重，进展缓慢。事业多阻碍，合作不顺；感情易误会，沟通困难；财运平平，不宜投资；健康需注意肠胃问题。",
                "宜": "静守、等待、学习、反思",
                "忌": "出行、投资、签约",
                "开运": "多喝水，佩戴蓝色水晶，保持耐心",
                "建议": "需耐心等待时机，不宜冒进，宜静心思考"
            },
            "速喜": {
                "吉凶": "★★★★☆ 吉",
                "属性": "朱雀星君",
                "方位": "南方",
                "数字": "3, 6, 9",
                "颜色": "红色、紫色",
                "时辰": "巳午时",
                "含义": "人便至时，属火朱雀，凡谋事主三、六、九。象征喜事临门，如沐春风，万事亨通。",
                "运势分析": "整体运势顺畅，喜事连连，进展迅速。机会来临，宜快速行动；感情升温，喜事将近；财运亨通，投资获利；精神饱满，状态良好。",
                "宜": "求财、考试、婚嫁、出行、签约",
                "忌": "诉讼、争吵、拖延",
                "开运": "多穿红色衣物，佩戴火属性饰品，保持热情",
                "建议": "机会来临，宜快速行动，把握时机"
            }
        }
        return details.get(element_name, {
            "吉凶": "未知",
            "属性": "未知",
            "方位": "未知",
            "数字": "未知",
            "颜色": "未知",
            "时辰": "未知",
            "含义": "暂无详细解释",
            "运势分析": "暂无运势分析",
            "宜": "暂无建议",
            "忌": "暂无建议",
            "开运": "保持积极心态",
            "建议": "谨慎行事，多思考"
        })
    
    def get_brief_element_info(self, element_name):
        """获取掌诀简要信息"""
        details = self.get_element_details(element_name)
        return f"【{element_name}】\n吉凶：{details.get('吉凶', '未知')}\n含义：{details.get('含义', '未知')[:50]}...\n建议：{details.get('建议', '暂无建议')}"
    
    def show_summary_analysis(self):
        """显示综合解读窗口"""
        if not self.current_result:
            messagebox.showinfo("提示", "请先进行占卜再查看综合解读")
            return
        
        # 创建解读窗口
        summary_window = tk.Toplevel(self.root)
        summary_window.title("📖 综合运势解读")
        summary_window.geometry("900x700")
        summary_window.configure(bg=self.colors['bg_dark'])
        summary_window.transient(self.root)
        
        # 窗口居中
        summary_window.update_idletasks()
        width = summary_window.winfo_width()
        height = summary_window.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        summary_window.geometry(f'+{x}+{y}')
        
        # 标题
        title_frame = tk.Frame(summary_window, bg=self.colors['bg_dark'])
        title_frame.pack(fill="x", pady=(20, 15))
        
        title_label = tk.Label(title_frame,
                              text="📖 综合运势深度解读",
                              font=('Microsoft YaHei UI', 24, 'bold'),
                              bg=self.colors['bg_dark'],
                              fg=self.colors['accent_gold'])
        title_label.pack()
        
        # 内容区域
        content_frame = tk.Frame(summary_window, bg=self.colors['bg_medium'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 滚动文本区域
        text_area = scrolledtext.ScrolledText(content_frame,
                                            font=('Microsoft YaHei UI', 13),
                                            bg=self.colors['bg_light'],
                                            fg=self.colors['text_light'],
                                            wrap="word",
                                            spacing1=8,
                                            spacing3=5,
                                            padx=20,
                                            pady=20)
        text_area.pack(fill="both", expand=True)
        
        # 插入内容
        text_area.insert(1.0, self.current_summary)
        text_area.config(state='disabled')
        
        # 按钮区域
        button_frame = tk.Frame(summary_window, bg=self.colors['bg_dark'])
        button_frame.pack(pady=15)
        
        buttons = [
            ("💾 保存解读", lambda: self.save_summary_to_file(text_area), self.colors['success']),
            ("🖨️ 打印", lambda: self.print_summary(text_area), self.colors['accent_blue']),
            ("🔄 刷新", self.refresh_analysis, self.colors['warning']),
            ("❌ 关闭", summary_window.destroy, self.colors['danger'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Microsoft YaHei UI', 11),
                          bg=color,
                          fg='white',
                          padx=20,
                          pady=8,
                          cursor="hand2")
            btn.pack(side="left", padx=8)
    
    def save_summary_to_file(self, text_widget):
        """保存解读到文件"""
        try:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"综合解读_{now}.txt"
            
            text_widget.config(state='normal')
            content = text_widget.get(1.0, tk.END)
            text_widget.config(state='disabled')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("保存成功", f"解读已保存到文件：\n{filename}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存解读时出错：{str(e)}")
    
    def print_summary(self, text_widget):
        """打印解读"""
        messagebox.showinfo("打印", "打印功能正在开发中...")
    
    def refresh_analysis(self):
        """刷新解读"""
        if self.current_result:
            elements = self.current_result
            # 重新生成解读
            self.generate_summary_analysis(
                self.get_current_numbers(),
                elements[0], elements[1], elements[2]
            )
            messagebox.showinfo("刷新", "解读已刷新")
    
    def get_current_numbers(self):
        """获取当前输入的数字"""
        numbers = []
        for entry in self.entry_widgets:
            try:
                num = int(entry.get())
                numbers.append(num)
            except:
                numbers.append(0)
        return numbers[:3]
    
    def fill_random_numbers(self):
        """填充随机数字"""
        for entry in self.entry_widgets:
            entry.delete(0, tk.END)
            entry.insert(0, str(random.randint(1, 9)))
        self.status_label.config(text="🎲 已生成随机数字 | 点击【开始占卜】进行计算")
    
    def clear_inputs(self):
        """清空输入框"""
        for entry in self.entry_widgets:
            entry.delete(0, tk.END)
        
        for label in self.result_labels:
            label.config(text="待推算", fg=self.colors['text_light'])
        
        for text_widget in self.detail_texts:
            text_widget.config(state='normal')
            text_widget.delete(1.0, tk.END)
            text_widget.config(state='disabled')
        
        self.current_result = None
        self.current_summary = ""
        self.set_default_hints()
        self.status_label.config(text="🟢 输入已清空 | 请输入三个数字进行占卜")
    
    def show_lunar_calendar(self):
        """显示今日农历"""
        try:
            lunar_info = LunarCalendar.get_lunar_date()
            
            lunar_window = tk.Toplevel(self.root)
            lunar_window.title("📅 今日农历时间")
            lunar_window.geometry("500x350")
            lunar_window.configure(bg=self.colors['bg_medium'])
            lunar_window.transient(self.root)
            
            # 居中
            lunar_window.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
            y = (self.root.winfo_screenheight() // 2) - (350 // 2)
            lunar_window.geometry(f'+{x}+{y}')
            
            # 标题
            title = tk.Label(lunar_window,
                           text="🌙 今日农历时间",
                           font=('Microsoft YaHei UI', 20, 'bold'),
                           bg=self.colors['bg_medium'],
                           fg=self.colors['accent_gold'])
            title.pack(pady=20)
            
            # 卡片
            card = tk.Frame(lunar_window,
                          bg=self.colors['bg_light'],
                          relief="ridge",
                          bd=3)
            card.pack(pady=10, padx=30, fill="both", expand=True)
            
            now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
            info_text = f"\n📅 公历时间：{now}\n\n"
            info_text += f"🌙 农历：{lunar_info['农历']}\n"
            info_text += f"⏰ 时辰：{lunar_info['时辰']}\n\n"
            info_text += "━" * 30 + "\n\n"
            info_text += "🔢 可用于占卜的数字：\n\n"
            info_text += f"   月数字：{lunar_info['月数字']:2d}\n"
            info_text += f"   日数字：{lunar_info['日数字']:2d}\n"
            info_text += f"   时数字：{lunar_info['时数字']:2d}\n\n"
            info_text += "💡 提示：点击下方按钮使用这些数字进行占卜"
            
            info_label = tk.Label(card,
                                text=info_text,
                                font=('Microsoft YaHei UI', 12),
                                bg=self.colors['bg_light'],
                                fg=self.colors['text_light'],
                                justify=tk.LEFT,
                                padx=20,
                                pady=20)
            info_label.pack()
            
            # 按钮
            btn_frame = tk.Frame(lunar_window, bg=self.colors['bg_medium'])
            btn_frame.pack(pady=15)
            
            btn_use = tk.Button(btn_frame,
                              text="✨ 使用这些数字占卜",
                              command=lambda: self.use_lunar_numbers(lunar_info, lunar_window),
                              font=('Microsoft YaHei UI', 11),
                              bg=self.colors['primary'],
                              fg='white',
                              padx=20,
                              pady=10,
                              cursor="hand2")
            btn_use.pack(side="left", padx=5)
            
            btn_close = tk.Button(btn_frame,
                                text="关闭",
                                command=lunar_window.destroy,
                                font=('Microsoft YaHei UI', 11),
                                bg=self.colors['secondary'],
                                fg='white',
                                padx=20,
                                pady=10,
                                cursor="hand2")
            btn_close.pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取农历信息失败：{str(e)}")
    
    def use_lunar_numbers(self, lunar_info, window):
        """使用农历数字进行占卜"""
        for i, entry in enumerate(self.entry_widgets):
            entry.delete(0, tk.END)
        
        self.entry_widgets[0].insert(0, str(lunar_info['月数字']))
        self.entry_widgets[1].insert(0, str(lunar_info['日数字']))
        self.entry_widgets[2].insert(0, str(lunar_info['时数字']))
        window.destroy()
        self.calculate_divination()
    
    def use_lunar_for_divination(self):
        """使用农历数字进行占卜的快捷方式"""
        lunar_info = LunarCalendar.get_lunar_date()
        for i, entry in enumerate(self.entry_widgets):
            entry.delete(0, tk.END)
        
        self.entry_widgets[0].insert(0, str(lunar_info['月数字']))
        self.entry_widgets[1].insert(0, str(lunar_info['日数字']))
        self.entry_widgets[2].insert(0, str(lunar_info['时数字']))
        self.calculate_divination()
    
    def random_divination(self):
        """随机占卜"""
        self.fill_random_numbers()
        self.calculate_divination()
    
    def quick_divination(self):
        """快速占卜"""
        self.fill_random_numbers()
        self.calculate_divination()
    
    def show_trend_analysis(self):
        """显示运势趋势分析"""
        if not self.current_result:
            messagebox.showinfo("提示", "请先进行占卜再查看趋势分析")
            return
        messagebox.showinfo("趋势分析", "运势趋势分析功能正在开发中...")
    
    def show_luck_suggestions(self):
        """显示开运建议"""
        if not self.current_result:
            messagebox.showinfo("提示", "请先进行占卜再查看开运建议")
            return
        messagebox.showinfo("开运建议", "开运建议功能正在开发中...")
    
    def save_result(self):
        """保存结果到文件"""
        try:
            if not self.current_result:
                messagebox.showwarning("无结果", "请先进行占卜再保存结果")
                return
            
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"占卜结果_{now}.txt"
            
            content = "小六壬占卜结果\n"
            content += "=" * 50 + "\n\n"
            
            numbers = []
            for entry in self.entry_widgets:
                num = entry.get()
                numbers.append(num if num else "未记录")
            
            content += f"输入数字：{', '.join(numbers)}\n\n"
            content += "掌诀结果：\n"
            for i in range(3):
                element = self.result_labels[i].cget("text")
                content += f"  第{i+1}掌：{element}\n"
            
            content += f"\n综合解读：\n{self.current_summary}\n"
            content += f"保存时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += "=" * 50
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.status_label.config(text=f"💾 结果已保存到文件：{filename}")
            messagebox.showinfo("保存成功", f"占卜结果已保存到：\n{filename}")
            
        except Exception as e:
            messagebox.showerror("保存失败", f"保存结果时发生错误：{str(e)}")
    
    def export_text(self):
        """导出为文本"""
        self.save_result()
    
    def change_theme(self):
        """更换主题"""
        messagebox.showinfo("主题更换", "主题更换功能正在开发中...")
    
    def show_history(self):
        """显示历史记录"""
        messagebox.showinfo("历史记录", "历史记录功能正在开发中...")
    
    def clear_history(self):
        """清除历史记录"""
        messagebox.showinfo("清除历史", "清除历史功能正在开发中...")
    
    def show_tutorial(self):
        """显示使用教程"""
        tutorial = """
📚 小六壬占卜器使用教程

一、基本操作：
1. 在三个输入框中分别输入1-9的数字
2. 点击【开始占卜】按钮
3. 查看三个掌诀结果和详细解读
4. 使用【综合解读】菜单查看深度分析

二、数字选择方法：
• 传统方法：使用农历月、日、时辰对应的数字
• 随机方法：随心默想三个数字
• 快捷方法：点击【随机数字】或【农历数字】

三、快捷键：
• Ctrl+A：查看综合解读
• Ctrl+S：保存结果
• Ctrl+L：查看今日农历
• Ctrl+Q：退出程序

四、注意事项：
• 占卜时保持心诚
• 结果仅供参考
• 命运掌握在自己手中
"""
        messagebox.showinfo("使用教程", tutorial)
    
    def show_element_guide(self):
        """显示掌诀详解"""
        guide = """
📖 小六壬掌诀详解

【大安】
• 属性：青龙星君
• 吉凶：★★★★★ 大吉
• 方位：东方
• 数字：1, 5, 7
• 颜色：青色、绿色
• 含义：身未动时，主平安吉祥
• 宜：求财、出行、婚嫁

【留连】
• 属性：玄武星君
• 吉凶：★★☆☆☆ 凶
• 方位：南方
• 数字：2, 8, 10
• 颜色：黑色、蓝色
• 含义：卒未归时，主拖延停滞
• 宜：静守、等待

【速喜】
• 属性：朱雀星君
• 吉凶：★★★★☆ 吉
• 方位：南方
• 数字：3, 6, 9
• 颜色：红色、紫色
• 含义：人便至时，主快速喜讯
• 宜：求财、考试、婚嫁
"""
        messagebox.showinfo("掌诀详解", guide)
    
    def show_copyright(self):
        """显示版权信息"""
        copyright_info = """
⚖️ 版权信息

软件名称：隧三小六壬占卜器 v3.1
版本号：3.1.0
发布日期：2026年

版权所有 © 2026 Thedustye
保留所有权利。

免责声明：
1. 本软件仅供娱乐参考，不作为专业占卜工具。
2. 占卜结果仅供参考，命运掌握在自己手中。
3. 请勿将占卜结果用于商业决策或法律事务。
4. 开发者不对使用本软件产生的任何后果负责。

传统文化传承：
小六壬是中国传统占卜文化的一部分，
本软件旨在推广和传承这一传统文化。

联系邮箱：thedustye1@outlook.com
官方网站：https://thedustye.com
"""
        messagebox.showinfo("版权信息", copyright_info)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
ℹ️ 关于小六壬占卜器

隧三小六壬占卜器 v3.1
基于传统小六壬算法开发

功能特点：
• 精美现代化的用户界面
• 详细的掌诀解释系统
• 综合运势深度解读
• 农历时间查询功能
• 多种占卜方式选择
• 结果保存与导出

技术特点：
• 使用Python和Tkinter开发
• 响应式界面设计
• 模块化代码结构
• 支持快捷键操作

开发理念：
• 传承中华传统文化
• 提供便捷的占卜工具
• 注重用户体验和界面美观
• 保持软件的易用性和功能性

特别感谢：
• 所有使用者的支持与反馈
• 传统文化的传承者
• 开源社区的贡献者

版本：v3.1
更新日期：2026年
"""
        messagebox.showinfo("关于", about_text)
    
    def lighten_color(self, color, amount=30):
        """颜色变亮"""
        return color

def main():
    """主函数"""
    root = tk.Tk()
    app = DivinationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()