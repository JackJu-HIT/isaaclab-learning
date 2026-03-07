# registry.py（修复后，保证有list()方法）
# 注册器核心：字典 + 装饰器
class Registry:
    def __init__(self, name):
        self.name = name  # 注册器名称（比如"robots"、"envs"）
        self._dict = {}   # 存储：名字 → 类/配置

    # 装饰器：把类/配置注册到字典中
    def register(self, name=None):
        def decorator(obj):
            # 如果没指定name，用类/配置的__name__
            key = name if name is not None else obj.__name__
            if key in self._dict:
                raise ValueError(f"{key} 已经在 {self.name} 注册过了！")
            self._dict[key] = obj
            print(f"注册 {key} 到 {self.name} 注册器成功！")     

            return obj  # 装饰器要返回原对象，不影响使用
        return decorator

    # 根据名字获取注册的类/配置
    def get(self, name):
        if name not in self._dict:
            raise KeyError(f"{name} 未注册！可选：{list(self._dict.keys())}")
        return self._dict[name]

    # 关键：修复list()方法（必须正确定义，无缩进错误）
    def list(self):
        return list(self._dict.keys())

# 实例化两个注册器（对应IsaacLab中的机器人、环境注册器）
ROBOT_REGISTRY = Registry("robots")  # 注册机器狗类/配置
ENV_REGISTRY = Registry("envs")      # 注册环境类/配置