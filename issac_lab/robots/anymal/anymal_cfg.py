# robots/anymal/anymal_cfg.py
from registry import ROBOT_REGISTRY

# 用装饰器注册：把AnymalCfg注册到ROBOT_REGISTRY，名字是"anymal_c"
print("开始定义 AnymalCfg 类...")  # 类定义前打印

@ROBOT_REGISTRY.register(name="anymal_c")
class AnymalCfg:
    """Anymal C型机器狗的配置类"""
    def __init__(self):
        self.joint_num = 12        # 关节数
        self.max_force = 500.0     # 最大关节力
        self.base_mass = 20.0      # 机身质量
        self.description = "Anymal C 四足机器人"
        print(f"AnymalCfg，名字是 'anymal_c'！jcy")
print("完成定义 AnymalCfg 类...")  # 类定义前打印
