# robots/go1/go1_cfg.py
from registry import ROBOT_REGISTRY
print("开始定义 Go1Cfg 类...")  # 类定义前打印

# 用装饰器注册：名字是"go1"（省略name参数，默认用类名Go1Cfg）
@ROBOT_REGISTRY.register()  # 等价于 register(name="Go1Cfg")
class Go1Cfg:
    """Unitree Go1机器狗的配置类"""
    def __init__(self):
        self.joint_num = 12
        self.max_force = 300.0
        self.base_mass = 12.0
        self.description = "Unitree Go1 四足机器人"
        print(f"Go1Cfg，名字是 'Go1Cfg'！jcy")
print("完成定义 Go1Cfg 类...")  # 类定义前打印