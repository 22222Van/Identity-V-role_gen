# Coding: UTF-8

#Naive Ver.
# import random

# def random_roles():
#     # 角色池（可根据游戏版本自行更新）
#     supervisor = [

#     ]
    
#     survivor = [

#     ]

#     try:
#         # 随机抽取1个监管者（不会重复）
#         selected_supervisor = random.choice(supervisor)
        
#         # 随机抽取4个不重复的求生者
#         selected_survivors = random.sample(survivor, 4)
        
#         # 返回格式化结果
#         return (
#             "【随机角色生成结果】\n"
#             f"监管者：{selected_supervisor}\n"
#             "求生者：" + "、".join(selected_survivors)
#         )
#     except ValueError as e:
#         # 处理求生者列表不足4人的情况
#         return f"错误：{str(e)}，请确保幸存者列表至少有4个角色"

# # 生成10组示例结果
# # for _ in range(10):
# #     print(random_roles())
# #     print("-" * 30)

# # 生成1组结果
# if __name__ == "__main__":
#     print(random_roles())
#     print("-" * 30)



#UI Ver.

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime 

# 角色数据库
ROLES = {
    "监管者": [
        "26号守卫",
        "博士",
        "噩梦",
        "歌剧演员",
        "红夫人",
        "红蝶",
        "黄衣之主",
        "记录员",
        "杰克",
        "鹿头",
        "蜡像师",
        "破轮",
        "摄影师",
        "使徒",
        "守夜人",
        "宿伞之魂",
        "小提琴家",
        "隐士",
        "渔女",
        "愚人金",
        "雕刻家",
        "爱哭鬼",
        "蜘蛛",
        "女巫",
        "孽蜥",
        "厂长",
        "孽蜥",
        "跛脚羊",
        "小丑",
        "疯眼",
        "梦之女巫",
        "时空之影",
        "喧嚣"
    ]
    ,
    "求生者": [
        "骑士",
        "飞行家",
        "病患",
        "火灾调查员",
        "慈善家",
        "大副",
        "调酒师",
        "调香师",
        "古董商",
        "击球手",
        "机械师",
        "祭司",
        "昆虫学者",
        "哭泣小丑",
        "空军",
        "盲女",
        "冒险家",
        "魔术师",
        "牛仔",
        "前锋",
        "囚徒",
        "入殓师",
        "守墓人",
        "律师",
        "舞女",
        "木偶师",
        "教授",
        "拉拉队员",
        "小说家",
        "心理学家",
        "先知",
        "野人",
        "医生",
        "佣兵",
        "邮差",
        "园丁",
        "杂技演员",
        "咒术师",
        "画家",
        "玩具商",
        "法罗女士",
        "气象学家",
        "幸运儿",
        "小女孩",
        "作曲家",
        "弓箭手",
        "勘探员",
        "记者"
    ]

}



class RoleGenerator:
    def __init__(self, master):
        self.master = master
        master.title("第五人格角色生成器 V5.0")
        master.geometry("500x500")
        
        # 初始化状态
        self.current_supervisor = ""
        self.base_survivors = []    # 基础四人组
        self.extra_survivor = ""    # 第五人
        
        self.create_widgets()

    def create_widgets(self):
        # 主按钮区域
        control_frame = ttk.Frame(self.master)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="生成完整阵容", command=self.generate_full).grid(row=0, column=0, padx=5)
        hunter_frame = ttk.LabelFrame(control_frame, text="没有这个监管")
        hunter_frame.grid(row=0, column=1, padx=5)

        ttk.Button(hunter_frame, text="换监管", command=self.generate_supervisor).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="替换所有求生", command=self.generate_base_survivors).grid(row=0, column=2, padx=5)

        # 第五人专属区域
        fifth_frame = ttk.LabelFrame(control_frame, text="没有这个求生")
        fifth_frame.grid(row=0, column=3, padx=5)
        ttk.Button(fifth_frame, text="生成新求生", command=self.generate_extra).pack(side="left")
        # ttk.Button(fifth_frame, text="清除第五人", command=self.clear_extra).pack(side="left", padx=5)

        # 结果显示区域
        display_frame = ttk.LabelFrame(self.master, text="当前阵容")
        display_frame.pack(pady=15, fill="both", expand=True, padx=20)

        # 监管者显示
        ttk.Label(display_frame, text="监管者：", font=("微软雅黑",12)).grid(row=0, column=0, sticky="w", padx=10)
        self.supervisor_label = ttk.Label(display_frame, text="待生成", foreground="#FF4500")
        self.supervisor_label.grid(row=0, column=1, sticky="w")

        # 基础四人组显示
        self.base_labels = []
        for i in range(4):
            frame = ttk.Frame(display_frame)
            frame.grid(row=i+1, column=0, columnspan=2, sticky="w", pady=3)
            ttk.Label(frame, text=f"求生者{i+1}：", width=10).pack(side="left")
            label = ttk.Label(frame, text="待分配", foreground="#1E90FF")
            label.pack(side="left")
            self.base_labels.append(label)

        # 第五人专属显示
        fifth_display = ttk.Frame(display_frame)
        fifth_display.grid(row=5, column=0, columnspan=2, sticky="w", pady=10)
        ttk.Label(fifth_display, text="替换的求生：", width=10).pack(side="left")
        self.extra_label = ttk.Label(fifth_display, text="未生成", foreground="#32CD32")
        self.extra_label.pack(side="left")
        
        # 状态栏
        self.status_bar = ttk.Label(self.master, text="就绪", foreground="gray")
        self.status_bar.pack(side="bottom", fill="x")

    def update_display(self):
        """更新所有界面元素"""
        self.supervisor_label.config(text=self.current_supervisor)
        for i in range(4):
            self.base_labels[i].config(text=self.base_survivors[i] if self.base_survivors else "待分配")
        self.extra_label.config(text=self.extra_survivor or "未生成")
        self.status_bar.config(text=f"最后更新：{datetime.now().strftime('%H:%M:%S')}")

    def generate_full(self):
        """生成完整基础阵容"""
        try:
            self.current_supervisor = random.choice(ROLES["监管者"])
            self.base_survivors = random.sample(ROLES["求生者"], 4)
            self.extra_survivor = ""
            self.update_display()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def generate_supervisor(self):
        """仅更换监管者"""
        if not self.base_survivors:
            messagebox.showinfo("注意", "请先生成完整阵容")
            return
        self.current_supervisor = random.choice(ROLES["监管者"])
        self.update_display()

    def generate_base_survivors(self):
        """更换基础四人组"""
        if not self.current_supervisor:
            messagebox.showinfo("注意", "请先生成完整阵容")
            return
        self.base_survivors = random.sample(ROLES["求生者"], 4)
        self.extra_survivor = ""  # 清除第五人
        self.update_display()

    def generate_extra(self):
        """生成不重复第五人"""
        if not self.base_survivors:
            messagebox.showinfo("注意", "请先生成完整阵容")
            return
            
        try:
            # 排除基础四人组
            available = [r for r in ROLES["求生者"] if r not in self.base_survivors]
            
            if not available:
                raise ValueError("没有可用第五人选项")
                
            # 如果已有第五人则先清除
            if self.extra_survivor:
                self.clear_extra()
                
            self.extra_survivor = random.choice(available)
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def clear_extra(self):
        """清除第五人"""
        self.extra_survivor = ""
        self.update_display()



if __name__ == "__main__":
    root = tk.Tk()
    app = RoleGenerator(root)
    root.mainloop()