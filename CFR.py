from Environment import Environment

def __init__(self, player1_initial_strategy, player2_initial_strategy):
        # 初期戦略を設定
        self.player1_strategy = player1_initial_strategy
        self.player2_strategy = player2_initial_strategy
        # Environmentインスタンスを初期化
        self.env = Environment(self.player1_strategy, self.player2_strategy)
        self.actions = env.actions  # 可能な行動
        self.num_actions = len(self.actions)  # 行動の数
        self.cumulative_regrets = {}  # 累積後悔値
        self.strategy_profile = {}  # 戦略プロファイル

    def get_strategy(self, state):
        """特定の状態における現在の戦略を取得または初期化する"""
        if state not in self.strategy_profile:
            # すべての行動に対して均等な確率を割り当てる初期戦略を設定
            self.strategy_profile[state] = [1.0 / self.num_actions] * self.num_actions
        return self.strategy_profile[state]

    def calculate_current_regret(self, state, actual_action, player_score, opponent_action, opponent_score):
        # 実際の行動による報酬を計算
        actual_reward = self.env.calculate_reward(actual_action, opponent_action, player_score, opponent_score)

        # 最大の代替報酬を計算
        max_counterfactual_reward = max(
            self.env.calculate_reward(action, opponent_action, player_score, opponent_score)
            for action in range(self.num_actions) if action != actual_action
        )

        # 現在の後悔値を計算
        current_regret = max(0, max_counterfactual_reward - actual_reward)
        return current_regret


    def update_cumulative_regrets(self, state, actual_action, player_score, opponent_action, opponent_score):
        # 現在の後悔値を計算
        current_regret = self.calculate_current_regret(state, actual_action, player_score, opponent_action, opponent_score)

        # 累積後悔値を更新
        if state not in self.cumulative_regrets:
            self.cumulative_regrets[state] = [0] * self.num_actions
        self.cumulative_regrets[state][actual_action] += current_regret


    def update_strategy(self, state):
        """戦略プロファイルを更新する"""
        # ...

    def train(self, num_iterations):
        """CFRアルゴリズムを使用して戦略をトレーニングする"""
        # ...
