import gym
from gym import spaces
import numpy as np

class CustomJankenEnv(gym.Env):
    """
    カスタムじゃんけん環境
    """
    def __init__(self):
        super(CustomJankenEnv, self).__init__()

        # アクションスペース（0: グー, 1: チョキ, 2: パー）
        self.action_space = spaces.Discrete(3)

        # 観測スペース（プレイヤーのスコア）
        self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([5, 5]), dtype=np.int32)

        # 状態の初期化
        self.state = None
        self.reset()

    def reset(self):
        # スコアを初期化
        self.state = np.array([0, 0])
        return self.state

    def step(self, action):
        # プレイヤーのアクション（手）を取得
        player_action = action
        # 相手（環境）のアクション（ランダム）
        opponent_action = self.action_space.sample()

        # 勝敗を決定
        if player_action == opponent_action:
            reward = 0
        elif (player_action == 0 and opponent_action == 1) or \
             (player_action == 1 and opponent_action == 2) or \
             (player_action == 2 and opponent_action == 0):
            # プレイヤーの勝利
            reward = 1 if player_action == 0 else 2
        else:
            # プレイヤーの敗北
            reward = -1

        # スコアを更新
        self.state += reward

        # ゲーム終了の判定
        done = self.state[0] >= 5 or self.state[1] >= 5

        return self.state, reward, done, {}

    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()
        print(f"Score: {self.state}")

# カスタム環境のテスト
env = CustomJankenEnv()
env.reset()
done = False
while not done:
    action = env.action_space.sample()  # ランダムなアクション
    state, reward, done, info = env.step(action)
    env.render()

# 環境を閉じる
env.close()
