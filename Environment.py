import random

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
        player1_action = self.choose_action(player1_strategy)
        player2_action = self.choose_action(player2_strategy)

        player1_points, player2_points = self.calculate_reward(player1_action, player2_action, self.player1_score, self.player2_score)

        self.player1_score += player1_points
        self.player2_score += player2_points

        result, done = self.determine_game_result(self.player1_score, self.player2_score, player1_points, player2_points)

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



    def choose_action(self,strategy):
        assert sum(strategy) == 1, "The sum of the probabilities in the strategy must be 1."
        
        ROCK = 0  # グー
        SCISSORS = 1  # チョキ
        PAPER = 2  # パー
    
        action = random.choices([ROCK, SCISSORS, PAPER], weights=strategy, k=1)[0]
        return action

    def determine_janken_winner(self,player1_action, player2_action):
        ROCK = 0  # グー
        SCISSORS = 1  # チョキ
        PAPER = 2  # パー
    
        # 勝敗とポイントの決定
        if player1_action == player2_action:
            return "Draw", (0, 0)
        elif (player1_action == PAPER and player2_action == ROCK) or \
             (player1_action == SCISSORS and player2_action == PAPER):
            # プレイヤー1の勝利 (パーでグーを、またはチョキでパーを)
            return "Player 1 Wins", (2, 0)
        elif (player1_action == ROCK and player2_action == PAPER) or \
             (player1_action == PAPER and player2_action == SCISSORS):
            # プレイヤー2の勝利 (グーでパーを、またはパーでチョキを)
            return "Player 2 Wins", (0, 2)
        elif player1_action == ROCK and player2_action == SCISSORS:
            # グーとチョキの勝率判定
            if random.random() < 0.25:
                return "Player 2 Wins", (0, 2)
            else:
                return "Player 1 Wins", (1, 0)
        else: # player1_action == SCISSORS and player2_action == ROCK
            # チョキとグーの勝率判定
            if random.random() < 0.25:
                return "Player 1 Wins", (2, 0)
            else:
                return "Player 2 Wins", (0, 1)

    def calculate_reward(self,player1_action, player2_action, player1_score, player2_score):
        ROCK = 0  # グー
        SCISSORS = 1  # チョキ
        PAPER = 2  # パー
    
        # 同じ手の場合、報酬は0点
        if player1_action == player2_action:
            return 0
    
        # パーとグー、チョキとパーの場合
        elif (player1_action == PAPER and player2_action == ROCK) or \
             (player1_action == SCISSORS and player2_action == PAPER):
            return 5 if player1_score >= 3 else 2
    
        # グーとパー、パーとチョキの場合
        elif (player1_action == ROCK and player2_action == PAPER) or \
             (player1_action == PAPER and player2_action == SCISSORS):
            return -5 if player2_score >= 3 else -2
    
        # グーとチョキの場合
        elif player1_action == ROCK and player2_action == SCISSORS:
            return 0.75 * (5 if player1_score >= 4 else 1) + 0.25 * (-5 if player2_score >= 3 else -2)
    
        # チョキとグーの場合
        elif player1_action == SCISSORS and player2_action == ROCK:
            return 0.25 * (5 if player1_score >= 3 else 2) + 0.75 * (-5 if player2_score >= 4 else -1)

    def determine_game_result(self,player1_score, player2_score, player1_points, player2_points):
        new_player1_score = player1_score + player1_points
        new_player2_score = player2_score + player2_points
    
        if new_player1_score >= 5:
            return "Player 1 Wins", True
        elif new_player2_score >= 5:
            return "Player 2 Wins", True
        else:
            return None, False




# 使用例
env = Environment()
state, reward, done, info = env.step([0.33, 0.33, 0.34], [0.33, 0.33, 0.34])
env.render()
