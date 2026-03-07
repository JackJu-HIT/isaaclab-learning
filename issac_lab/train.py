# train.py
from registry import ROBOT_REGISTRY
import robots  
def main():
    # 1. 列出所有已注册的机器狗（IsaacLab中--robot参数的可选值就是这么来的）
    print("已注册的机器狗：", ROBOT_REGISTRY.list())  # 输出：['anymal_c', 'Go1Cfg']

    # 2. 通过名字获取机器狗配置（核心！不用关心配置在哪个文件夹）
    # 模拟命令行传入 --robot anymal_c
    robot_name = "anymal_c"
    robot_cfg_cls = ROBOT_REGISTRY.get(robot_name)
    robot_cfg = robot_cfg_cls()  # 实例化配置

    # 3. 使用配置参数（训练时传给环境）
    print(f"\n{robot_name} 配置：")
    print(f"关节数：{robot_cfg.joint_num}")
    print(f"最大关节力：{robot_cfg.max_force}")
    print(f"描述：{robot_cfg.description}")

    # 4. 换另一个机器狗，无需改导入路径，直接换名字即可
    robot_name = "Go1Cfg"
    robot_cfg = ROBOT_REGISTRY.get(robot_name)()
    print(f"\n{robot_name} 配置：")
    print(f"机身质量：{robot_cfg.base_mass}")
    print(f"描述：{robot_cfg.description}")

if __name__ == "__main__":
    main()