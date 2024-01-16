import gym
from gym import spaces
import numpy as np

class CustomJankenEnv(gym.Env):
    """
    カスタムじゃんけん環境
    """
    def __init__(self, player1_strategy, player2_strategy):
        self.player1_strategy = player1_strategy
        self.player2_strategy = player2_strategy
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
        self.calculate_next_state()
        reward1, reward2 = self.calculate_reward(player1_action, player2_action).values()

    
        # ゲーム終了の判定
        done = self.state[0] >= 5 or self.state[1] >= 5
    
        return self.state, {'player1': reward1, 'player2': reward2}, done, info


    def calculate_reward(self, player1_action, player2_action):
        """
        プレイヤー1とプレイヤー2の報酬を計算する関数

        :param player1_action: プレイヤー1のアクション
        :param player2_action: プレイヤー2のアクション
        :return: player1とplayer2の報酬の辞書
        """
        player1_reward = 0
        player2_reward = 0

        # 勝利、敗北、引き分けに基づいた報酬の計算
        if player1_action == player2_action:
            # 引き分けの場合（報酬なし）
            return {'player1': player1_reward, 'player2': player2_reward}
        else:
            # 勝利と敗北のケース
            if player1_action == 0 and player2_action == 2:  # プレイヤー1のグー vs プレイヤー2のパー
                # 勝者が5点に到達するか判定
                if self.state[0] + 2 >= 5:
                    player1_reward = 5
                    player2_reward = -5
                else:
                    player1_reward = 2  # パーで勝利した場合
                    player2_reward = -2

            elif player1_action == 2 and player2_action == 0:  # プレイヤー2のグー vs プレイヤー1のパー
                # 勝者が5点に到達するか判定
                if self.state[1] + 2>= 5:
                    player1_reward = -5
                    player2_reward = 5
                else:
                    player1_reward = -2
                    player2_reward = 2  # パーで勝利した場合

            #チョキでパーに勝つ場合も同様の処理
            elif player1_action == 1 and player2_action == 2:  # プレイヤー1のチョキ vs プレイヤー2のパー
                # 勝者が5点に到達するか判定
                if self.state[0] + 2 >= 5:
                    player1_reward = 5
                    player2_reward = -5
                else:
                    player1_reward = 2  # チョキで勝利した場合
                    player2_reward = -2
            
            elif player1_action == 2 and player2_action == 1:  # プレイヤー2のチョキ vs プレイヤー1のパー
                # 勝者が5点に到達するか判定
                if self.state[1] + 2 >= 5:
                    player1_reward = -5
                    player2_reward = 5
                else:
                    player1_reward = -2
                    player2_reward = 2  # チョキで勝利した場合

            # 追加: グー対チョキの勝敗に対する報酬計算
            elif player1_action == 0 and player2_action == 1:  # プレイヤー1のグー vs プレイヤー2のチョキ
                # グーが勝つ場合の報酬
                if self.state[0] + 1 >= 5:
                    reward_for_goo_winning = 5
                else:
                    reward_for_goo_winning = 1
            
                # チョキが勝つ場合の報酬
                if self.state[0] + 2 >= 5:
                    reward_for_choki_winning = 5
                else:
                    reward_for_choki_winning = 2
            
                # 期待値の計算
                player1_reward = reward_for_goo_winning * 0.75 + reward_for_choki_winning * 0.25
                player2_reward = -player1_reward
            
            elif player1_action == 1 and player2_action == 0:  # プレイヤー2のグー vs プレイヤー1のチョキ
                # グーが勝つ場合の報酬
                if self.state[1] + 1 >= 5:
                    reward_for_goo_winning = 5
                else:
                    reward_for_goo_winning = 1
            
                # チョキが勝つ場合の報酬
                if self.state[1] + 2 >= 5:
                    reward_for_choki_winning = 5
                else:
                    reward_for_choki_winning = 2
            
                # 期待値の計算
                player2_reward = reward_for_goo_winning * 0.75 + reward_for_choki_winning * 0.25
                player1_reward = -player2_reward

        return {'player1': player1_reward, 'player2': player2_reward}

    def calculate_next_state(self):
        # プレイヤー1のアクションを戦略に基づいて決定
        player1_action = np.random.choice([0, 1, 2], p=self.player1_strategy)
    
        # プレイヤー2のアクションを戦略に基づいて決定
        player2_action = np.random.choice([0, 1, 2], p=self.player2_strategy)
    
        # チョキ対グーの場合、25%の確率でチョキの勝利
        if player1_action == 1 and player2_action == 0:
            if np.random.rand() < 0.25:
                self.state[0] += 2  # プレイヤー1（チョキ）の勝利（2点）
            else:
                self.state[1] += 1  # プレイヤー2（グー）の勝利（1点）
        elif player2_action == 1 and player1_action == 0:
            if np.random.rand() < 0.25:
                self.state[1] += 2  # プレイヤー2（チョキ）の勝利（2点）
            else:
                self.state[0] += 1  # プレイヤー1（グー）の勝利（1点）
        else:
            # 通常の勝敗判定
            if player1_action == player2_action:
                pass  # 引き分け、スコア変化なし
            elif (player1_action == 0 and player2_action == 1) or \
                 (player1_action == 1 and player2_action == 2) or \
                 (player1_action == 2 and player2_action == 0):
                self.state[0] += 1 if player1_action == 0 else 2  # プレイヤー1の勝利
            else:
                self.state[1] += 1 if player2_action == 0 else 2  # プレイヤー2の勝利

# これが改訂された step 関数です。プレイヤーはそれぞれの戦略に基づいて行動を選択し、
# 特殊なルール（チョキ対グーでの25%の勝率）も適切に処理されています。


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
