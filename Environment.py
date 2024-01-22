import random

class Environment:
    def __init__(self,player1_strategy,player2_strategy):
        self.actions = [0, 1, 2]  # グー、チョキ、パー
        self.reset()

    def reset(self):
        self.player1_score = 0
        self.player2_score = 0
        return self.get_state()

    def get_state(self):
        return (self.player1_score, self.player2_score)

    def step(self, actions):
        player1_action, player2_action = actions
        state = self.get_state()


        reward = self.calculate_reward(state,player1_action, player2_action)
        player1_points, player2_points = self.determine_janken_winner(player1_action, player2_action)
        

        self.player1_score += player1_points
        self.player2_score += player2_points

        result, done = self.determine_game_result(self.player1_score, self.player2_score)

        self.last_player1_action = player1_action
        self.last_player2_action = player2_action

        state = self.get_state()
        reward = player1_points
        info = {"player2_reward": player2_points, "result": result}
        #print(state,reward,actions)

        return state, reward, done, info

    def render(self):
        last_player1_action = self.last_player1_action if hasattr(self, 'last_player1_action') else 'None'
        last_player2_action = self.last_player2_action if hasattr(self, 'last_player2_action') else 'None'
        action_names = {0: 'Rock', 1: 'Scissors', 2: 'Paper'}
        #print(f" Chose: {action_names.get(last_player1_action, 'None')} | Score: {self.player1_score}")
        #print(f" Chose: {action_names.get(last_player2_action, 'None')} | Score: {self.player2_score}")



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
            return (1, 1)
        elif (player1_action == PAPER and player2_action == ROCK) or \
             (player1_action == SCISSORS and player2_action == PAPER):
            # プレイヤー1の勝利 (パーでグーを、またはチョキでパーを)
            return (2, 0)
        elif (player1_action == ROCK and player2_action == PAPER) or \
             (player1_action == PAPER and player2_action == SCISSORS):
            # プレイヤー2の勝利 (グーでパーを、またはパーでチョキを)
            return (0, 2)
        elif player1_action == ROCK and player2_action == SCISSORS:
            # グーとチョキの勝率判定
            if random.random() < 0.25:
                return (0, 2)
            else:
                return (1, 0)
        else: # player1_action == SCISSORS and player2_action == ROCK
            # チョキとグーの勝率判定
            if random.random() < 0.25:
                return (2, 0)
            else:
                return (0, 1)

    def calculate_reward(self,state,player1_action, player2_action):
        ROCK = 0  # グー
        SCISSORS = 1  # チョキ
        PAPER = 2  # パー
        player1_score, player2_score = state
    
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

    def determine_game_result(self, player1_score, player2_score):
        # 両プレイヤーが同時に5点以上に達した場合、引き分けとする
        if player1_score >= 5 and player2_score >= 5:
            return "Draw", True
        elif player1_score >= 5:
            return "Player 1 Wins", True
        elif player2_score >= 5:
            return "Player 2 Wins", True
        else:
            return None, False




# 使用例
#env = Environment([0.6,0.2,0.2],[0.33, 0.33, 0.34])
#done = False
#while not done:
    #player1_strategy = [0.6,0.2,0.2]
    #player2_strategy = [0.33, 0.33, 0.34]

    #state, reward, done, info = env.step()
    #env.render()

    #if done:
        #print(f"Game Over! Result: {info['result']}")
