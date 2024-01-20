class Environment:
    def __init__(self):
        self.player1_strategy = [0.33, 0.33, 0.34]  # 例: 初期戦略
        self.player2_strategy = [0.33, 0.33, 0.34]
        self.reset()

    def reset(self):
        self.player1_score = 0
        self.player2_score = 0
        return self.get_state()

    def get_state(self):
        return (self.player1_score, self.player2_score)

    def step(self, player1_strategy, player2_strategy):
        player1_action = choose_action(player1_strategy)
        player2_action = choose_action(player2_strategy)

        player1_points, player2_points = calculate_reward(player1_action, player2_action, self.player1_score, self.player2_score)

        self.player1_score += player1_points
        self.player2_score += player2_points

        result, done = determine_game_result(self.player1_score, self.player2_score, player1_points, player2_points)

        self.last_player1_action = player1_action
        self.last_player2_action = player2_action

        state = self.get_state()
        reward = player1_points
        info = {"player2_reward": player2_points, "result": result}

        return state, reward, done, info

    def render(self):
        last_player1_action = self.last_player1_action if hasattr(self, 'last_player1_action') else 'None'
        last_player2_action = self.last_player2_action if hasattr(self, 'last_player2_action') else 'None'
        action_names = {0: 'Rock', 1: 'Scissors', 2: 'Paper'}
        print(f"Player 1 Strategy: {self.player1_strategy} | Chose: {action_names.get(last_player1_action, 'None')} | Score: {self.player1_score}")
        print(f"Player 2 Strategy: {self.player2_strategy} | Chose: {action_names.get(last_player2_action, 'None')} | Score: {self.player2_score}")

# 使用例
env = Environment()
state, reward, done, info = env.step([0.33, 0.33, 0.34], [0.33, 0.33, 0.34])
env.render()
