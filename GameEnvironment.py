import gym
from gym import spaces
import numpy as np

class CustomJankenEnv(gym.Env):
    """
    カスタムじゃんけん環境
    """
    def __init__(self, player1_strategy, player2_strategy):
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

    def step(self, player1_action=None):
        # 初期報酬とinfoの設定
        reward = 0
        info = {}

       # プレイヤー1のアクションを戦略に基づいて決定（指定されていない場合）
        if player1_action is None:
            player1_action = np.random.choice([0, 1, 2], p=self.player1_strategy)

        # プレイヤー2（対戦相手）のアクションを戦略に基づいて決定
        player2_action = np.random.choice([0, 1, 2], p=self.player2_strategy)


        # チョキ対グーの場合、25%の確率でチョキの勝利
        if player_action == 1 and opponent_action == 0:
            if np.random.rand() < 0.25:
                self.state[0] += 2  # チョキの勝利（2点）
            else:
                self.state[1] += 1  # グーの勝利（1点）
        else:
            # 通常の勝敗判定
            if player_action == opponent_action:
                pass  # 引き分け、スコア変化なし
            elif (player_action == 0 and opponent_action == 1) or \
                 (player_action == 1 and opponent_action == 2) or \
                 (player_action == 2 and opponent_action == 0):
                self.state[0] += 1 if player_action == 0 else 2  # プレイヤーの勝利
            else:
                self.state[1] += 1 if opponent_action == 0 else 2  # 対戦相手の勝利

        # ゲーム終了の判定
        done = self.state[0] >= 5 or self.state[1] >= 5

        return self.state, reward, done, info

    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()
        print(f"Score: {self.state}")

# カスタム環境のテスト
# テスト
player1_strategy = [0.4, 0.4, 0.2]  # プレイヤー1の戦略
player2_strategy = [0.3, 0.3, 0.4]  # プレイヤー2の戦略
env = CustomJankenEnv(player1_strategy, player2_strategy)

env.reset()
done = False
while not done:
    action = env.action_space.sample()  # ランダムなアクション
    state, reward, done, info = env.step(action)
    env.render()

# 環境を閉じる
env.close()
