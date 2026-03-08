# isaaclab-learning
Isaac Lab框架装饰器与注册机制的极简实现与学习示例，基于四足机器人强化学习运控开发场景，复刻Isaac Lab核心的**装饰器+注册器**模块设计，帮助快速理解框架的类/配置管理逻辑、环境注册与调用机制。

## 项目简介
Isaac Lab作为英伟达针对机器人强化学习的仿真框架，其核心设计之一是通过**装饰器+注册机制**实现大规模类、配置、环境的灵活管理，解决多机器人、多环境场景下的代码复用与扩展难题。

本项目是Isaac Lab注册机制的**最小复刻版**，通过极简的Python代码实现核心逻辑：
- 实现通用的Registry注册器类（字典+装饰器）
- 模拟Isaac Lab的机器人配置注册流程
- 实现训练脚本通过**名字**动态获取配置，无需关心文件路径
- 贴合四足机器人开发场景（Anymal C、Unitree Go1）

通过本项目可快速掌握Isaac Lab源码中`registry.py`、`robot_cfg.py`、`train.py`的关联逻辑，为基于Isaac Lab开发四足机器人强化学习算法打下基础。

## 核心原理
Isaac Lab注册机制的本质是**装饰器+字典**的组合，核心分为三个阶段：
1. **定义注册器**：创建通用Registry类，提供`register`装饰器和`get`获取方法，底层通过字典存储**名字-类/配置**的映射
2. **注册目标对象**：用`@REGISTRY.register()`装饰机器人/环境配置类，自动将其加入注册器字典
3. **动态调用**：主程序通过**名字**从注册器中取出对应类/配置，实现无路径化的动态加载

该机制相比传统文件导入，具有**扩展成本低、灵活性高、支持命令行动态选择**的优势，是Isaac Lab、PyTorch、OpenAI Gym等工业级框架的通用设计。

## 项目结构
完全复刻Isaac Lab的目录组织形式，聚焦机器人配置注册的核心场景：
```
isaaclab-learning/
├── registry.py        # 核心：通用注册器实现（对应Isaac Lab的isaaclab/utils/registry.py）
├── robots/            # 机器人配置目录，存放不同机器人的配置类
│   ├── __init__.py    # 批量导入机器人配置，触发装饰器注册（关键步骤）
│   ├── anymal/        # Anymal C四足机器人配置
│   │   ├── __init__.py
│   │   └── anymal_cfg.py  # Anymal C配置类+注册装饰器
│   └── go1/           # Unitree Go1四足机器人配置
│       ├── __init__.py
│       └── go1_cfg.py     # Go1配置类+注册装饰器
└── train.py           # 训练脚本示例：通过注册器动态获取机器人配置（模拟Isaac Lab的train.py）
```

## 快速开始
### 环境要求
Python 3.8+（与Isaac Lab官方环境兼容），无额外第三方依赖，纯原生Python实现。

### 运行步骤
1. 克隆本项目
```bash
git clone https://github.com/JackJu-HIT/isaaclab-learning.git
cd isaaclab-learning
```
2. 直接运行训练脚本示例
```bash
python train.py
```
3. 查看运行结果
脚本会输出**已注册的机器人列表**和对应配置参数，效果如下：
```
已注册的机器狗： ['anymal_c', 'Go1Cfg']

anymal_c 配置：
关节数：12
最大关节力：500.0
描述：Anymal C 四足机器人

Go1Cfg 配置：
机身质量：12.0
描述：Unitree Go1 四足机器人
```

## 核心代码解析
### 1. 注册器核心实现（registry.py）
实现通用的`Registry`类，包含**装饰器注册**和**名字获取**核心方法，是整个机制的基础：
```python
class Registry:
    def __init__(self, name):
        self.name = name  # 注册器名称（如"robots"、"envs"）
        self._dict = {}   # 存储：名字 → 类/配置的映射
    
    # 装饰器：将类/配置注册到字典
    def register(self, name=None):
        def decorator(obj):
            key = name if name is not None else obj.__name__
            if key in self._dict:
                raise ValueError(f"{key} 已经在 {self.name} 注册过了！")
            self._dict[key] = obj
            return obj  # 保留原对象功能，不影响使用
        return decorator
    
    # 根据名字获取注册的类/配置
    def get(self, name):
        if name not in self._dict:
            raise KeyError(f"{name} 未注册！可选：{list(self._dict.keys())}")
        return self._dict[name]
    
    # 列出所有已注册的名字
    def list(self):
        return list(self._dict.keys())

# 实例化机器人/环境注册器（贴合Isaac Lab设计）
ROBOT_REGISTRY = Registry("robots")
ENV_REGISTRY = Registry("envs")
```

### 2. 机器人配置注册（robots/xxx/xxx_cfg.py）
用`@ROBOT_REGISTRY.register()`装饰配置类，支持**指定注册名**和**默认类名**两种方式：
```python
# Anymal C配置示例（指定注册名：anymal_c）
from registry import ROBOT_REGISTRY

@ROBOT_REGISTRY.register(name="anymal_c")
class AnymalCfg:
    def __init__(self):
        self.joint_num = 12    # 关节数
        self.max_force = 500.0 # 最大关节力
        self.base_mass = 20.0  # 机身质量
        self.description = "Anymal C 四足机器人"

# Go1配置示例（默认注册名：Go1Cfg，使用类名）
from registry import ROBOT_REGISTRY

@ROBOT_REGISTRY.register()
class Go1Cfg:
    def __init__(self):
        self.joint_num = 12
        self.max_force = 300.0
        self.base_mass = 12.0
        self.description = "Unitree Go1 四足机器人"
```

### 3. 触发注册（robots/__init__.py）
**批量导入所有配置类**，触发装饰器执行，将配置类加入注册器字典（Isaac Lab核心步骤）：
```python
# 导入所有机器人配置，触发装饰器注册
from .anymal import anymal_cfg
from .go1 import go1_cfg
```

### 4. 动态调用（train.py）
通过注册器的`list()`和`get()`方法，**按名字动态获取配置**，无需写冗长的文件导入路径：
```python
from registry import ROBOT_REGISTRY

def main():
    # 1. 列出所有已注册的机器人
    print("已注册的机器狗：", ROBOT_REGISTRY.list())
    # 2. 通过名字获取Anymal C配置并实例化
    robot_cfg = ROBOT_REGISTRY.get("anymal_c")()
    # 3. 直接使用配置参数
    print(f"Anymal C 关节数：{robot_cfg.joint_num}")
    # 4. 切换机器人仅需修改名字，无需改导入代码
    robot_cfg = ROBOT_REGISTRY.get("Go1Cfg")()
    print(f"Go1 机身质量：{robot_cfg.base_mass}")

if __name__ == "__main__":
    main()
```

## 与Isaac Lab官方框架的关联
本项目的极简实现完全对应Isaac Lab的核心设计，可无缝衔接官方源码学习：
1. **注册器对应**：本项目`registry.py` → Isaac Lab `isaaclab/utils/registry.py`
2. **机器人注册对应**：本项目`ROBOT_REGISTRY` → Isaac Lab `isaaclab.assets.robot.RobotRegistry`
3. **环境注册对应**：本项目`ENV_REGISTRY` → Isaac Lab `isaaclab.envs.EnvRegistry`
4. **调用逻辑对应**：本项目`train.py` → Isaac Lab `scripts/reinforcement_learning/rsl_rl/train.py`

Isaac Lab中通过`--robot`/`--task`命令行参数指定名字，底层就是通过本项目的注册机制实现动态加载。

## 扩展示例
基于本项目的注册机制，**新增机器人配置（如Aliengo）** 仅需3步，主程序无需任何修改：
1. 在`robots/`下新建`aliengo/`目录，创建`aliengo_cfg.py`并添加装饰器；
2. 在`aliengo/__init__.py`中导出配置类；
3. 在`robots/__init__.py`中导入`aliengo_cfg`。

运行`train.py`即可自动识别新注册的机器人，完美复现Isaac Lab的扩展逻辑。

## 相关资料
- **Isaac Lab官方文档**：https://isaac-sim.github.io/IsaacLab/main/
- **核心学习文章**：[【四足机器人强化学习运控基础】Isaac Lab框架深入理解](https://mp.weixin.qq.com/s/-CRl_me2POQjhjga6-OyIw)
- **Isaac Lab官方源码**：https://github.com/NVIDIA-Omniverse/IsaacLab

## 许可证
本项目基于BSD-3-Clause许可证，与Isaac Lab官方许可证保持一致，可自由用于学习和商业开发。
