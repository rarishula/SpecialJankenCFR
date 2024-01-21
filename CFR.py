from Environment import Environment
import random
import pdb
import traceback

class CFR:
        
        def __init__(self, player1_initial_strategy, player2_initial_strategy):
                # 初期戦略を設定
                self.player1_strategy = player1_initial_strategy
                self.player2_strategy = player2_initial_strategy
                # Environmentインスタンスを初期化
                self.env = Environment(self.player1_strategy, self.player2_strategy)
                self.actions = self.env.actions  # 可能な行動
                self.num_actions = len(self.actions)  # 行動の数
                self.player1_cumulative_regrets = {}  # プレイヤー1の累積後悔値
                self.player2_cumulative_regrets = {}  # プレイヤー2の累積後悔値
                self.player1_strategy_profile = {}  # プレイヤー1の戦略プロファイル
                self.player2_strategy_profile = {}  # プレイヤー2の戦略プロファイル



        def choose_action(self,strategy):
                assert sum(strategy) == 1, "The sum of the probabilities in the strategy must be 1."
                
                ROCK = 0  # グー
                SCISSORS = 1  # チョキ
                PAPER = 2  # パー
            
                action = random.choices([ROCK, SCISSORS, PAPER], weights=strategy, k=1)[0]
                return action


        def get_strategy(self, player, state):
                """特定のプレイヤーと状態における現在の戦略を取得または初期化する"""
                original_strategy = self.player2_strategy_profile.copy()
                
                strategy_profile = self.player1_strategy_profile if player == 1 else self.player2_strategy_profile
                if state not in strategy_profile:
                    # 初期戦略を設定
                    strategy_profile[state] = [1.0 / self.num_actions] * self.num_actions
                if original_strategy != self.player2_strategy_profile:
                    print(f"get_strategy: Strategy changed from {original_strategy} to {self.player2_strategy_profile}")

                return strategy_profile[state]
                
        def calculate_current_regret(self, player, state, actual_action, opponent_action):
            if player == 1:
                player1_action = actual_action
                player2_action = opponent_action
                actual_reward = self.env.calculate_reward(state, player1_action, player2_action)
        
                max_counterfactual_reward = max(
                    self.env.calculate_reward(state, action, player2_action)
                    for action in range(self.num_actions) if action != player1_action
                )
            else:
                player1_action = opponent_action
                player2_action = actual_action
                actual_reward = self.env.calculate_reward(state, player1_action, player2_action) * -1
        
                max_counterfactual_reward = max(
                    self.env.calculate_reward(state, player1_action, action) * -1
                    for action in range(self.num_actions) if action != player2_action
                )
        
            current_regret = max(0, max_counterfactual_reward - actual_reward)
            return current_regret



        
        
        def update_cumulative_regrets(self, player, state, player1_action, player2_action):
            player_score, opponent_score = state
        
            # プレイヤーごとに行動を選択
            if player == 1:
                actual_action = player1_action
                opponent_action = player2_action
                cumulative_regrets = self.player1_cumulative_regrets
            else:
                actual_action = player2_action
                opponent_action = player1_action
                cumulative_regrets = self.player2_cumulative_regrets
        
            # 現在の後悔値を計算
            current_regret = self.calculate_current_regret(player, state, actual_action, opponent_action)
        
            # 累積後悔値を更新
            if state not in cumulative_regrets:
                cumulative_regrets[state] = [0] * self.num_actions
            cumulative_regrets[state][actual_action] += current_regret

        """

        def update_strategy(self, player, state):
                original_strategy = self.player2_strategy_profile.copy()  # コピーを作成
                
                # プレイヤーに応じた累積後悔値を取得
                cumulative_regrets = self.player1_cumulative_regrets if player == 1 else self.player2_cumulative_regrets
                # 状態に対する累積後悔値を取得
                regrets = cumulative_regrets.get(state, [0] * self.num_actions)
        
                # 正の累積後悔値の合計を計算
                positive_regret_sum = sum(max(regret, 0) for regret in regrets)
        
                # 新しい戦略を計算
                if positive_regret_sum > 0:
                    new_strategy = [max(regret, 0) / positive_regret_sum for regret in regrets]
                else:
                    # すべての行動に対して均等な確率を割り当てる
                    new_strategy = [1.0 / self.num_actions] * self.num_actions
        
                # プレイヤーに応じた戦略プロファイルを更新
                if player == 1:
                    self.player1_strategy_profile[state] = new_strategy
                else:
                    self.player2_strategy_profile[state] = new_strategy

                print(f"State: {state}, Player: {player}, Cumulative Regrets: {regrets}, Positive Regret Sum: {positive_regret_sum}")
        
                return new_strategy
        """

        def update_strategy(self, player, state):
            # プレイヤーに応じた戦略プロファイルを選択
            if player == 1:
                strategy_profile = self.player1_strategy_profile
            else:
                strategy_profile = self.player2_strategy_profile
        
            # その状態の戦略が未定義の場合、均等な確率で初期化
            if state not in strategy_profile:
                strategy_profile[state] = [1.0 / self.num_actions] * self.num_actions
        
            # 戦略を更新
            strategy_profile[state] = strategy_profile[state]
        
            return strategy_profile[state]

        
        def train(self, num_iterations):
            for iteration in range(1, num_iterations + 1):
                # プレイヤー1の戦略を固定し、プレイヤー2の戦略を更新
                for _ in range(100):
                    current_state = self.env.reset()
                    self.play_game(current_state, fixed_player=1)
        
                # プレイヤー2の戦略を固定し、プレイヤー1の戦略を更新
                for _ in range(100):
                    current_state = self.env.reset()
                    self.play_game(current_state, fixed_player=2)

        
        def play_game(self, state, fixed_player):
           while True:
                # 現在の状態における戦略を取得
                strategy1 = self.get_strategy(1, state)
                strategy2 = self.get_strategy(2, state)
                
        
                # 戦略に基づいて行動を選択
                action1 = self.choose_action(strategy1)
                action2 = self.choose_action(strategy2)
                actions = action1, action2
        
                # 行動を実行し、新しい状態と報酬を取得
                new_state, reward, done, _ = self.env.step(actions)
        
                # 固定されていないプレイヤーの累積後悔値を更新
                if fixed_player != 1:
                    self.update_cumulative_regrets(1, state, action1, action2)
                if fixed_player != 2:
                    self.update_cumulative_regrets(2, state, action1, action2)
        
                if done:
                    break
                print("Actions:", actions)
                print("Player 1 Cumulative Regrets:", self.player1_cumulative_regrets)
                print("Player 2 Cumulative Regrets:", self.player2_cumulative_regrets)
        
                
                state = new_state
        
                # 固定されていないプレイヤーの戦略を更新
                if fixed_player != 1:
                    self.update_strategy(1, state)
                if fixed_player != 2:
                    self.update_strategy(2, state)


# 初期戦略を定義（例：各行動に均等な確率を割り当てる）
player1_initial_strategy = [1/3, 1/3, 1/3]
player2_initial_strategy = [1/3, 1/3, 1/3]

# CFRインスタンスの作成とトレーニングの実行
cfr = CFR(player1_initial_strategy, player2_initial_strategy)
cfr.train(1)  # 1000反復でトレーニング

