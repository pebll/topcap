from copy import deepcopy

from topcap.agents import Human, RandomAI, HeuristicAI, GraphAI, GraphAICopilot, JanMVP, QDicter
from topcap.agents.utils import heuristic
from topcap.agents.utils.heuristic import SimpleHeuristic, ExponentialHeuristic
from topcap.core.game.arena import Arena

MAX_THINKING_TIME = 10
# heuristics
base_simple_heuristic = SimpleHeuristic()
base_exp_heuristic = ExponentialHeuristic()

VV = False
VERBOSE = False

# agents
leo = Human("Léo")
jan = Human("Jan")
randi = RandomAI("Randi")
rando = RandomAI("Rando", False)
heuri_simple = HeuristicAI(base_simple_heuristic, "Heuri Simple")
heuri_exp = HeuristicAI(base_exp_heuristic, "Heuri Expo")
jan_mvp = JanMVP("Jan's Noob AI", verbose=VV)
qheuri = QDicter("qheuri", vv=VV, epsilon = 0.1, decay = 0.95, initialization=base_exp_heuristic)
qlearni = QDicter("qlearni", vv=VV, epsilon = 0.1, decay = 0.96, initialization=10)
qrandi = QDicter("qrandi", vv=VV, epsilon = 0.3, decay = 0.9, initialization=15)
plusminus = QDicter("plusminus", vv=VV, epsilon = 0.1, decay = 0.95, initialization=0)

# qheuri.load_latest()
# qheuri.epsilon = 0
#
# qlearni.load_latest()
# qlearni.epsilon = 0
#
plusminus.load_latest()
plusminus.epsilon = 0

qheuro = deepcopy(qheuri)
qheuro.name = "qheuro"

PLAYER_1 = leo
PLAYER_2 = plusminus

NAME = "plusminus"
VERSION = 1
CONTINUE = True
GAME_COUNT = 10000
SAVE_FREQ = 500
TEST_COUNT = 100
SAMPLE_SIZE = 20
OPPONENT = heuri_exp


def main():
    arena = Arena()
    # arena.train_from_agent(plusminus, save_frequency=SAVE_FREQ, num_games=GAME_COUNT)
    # arena.train_continue(name=NAME, version=VERSION, save_frequency=SAVE_FREQ, num_games=GAME_COUNT)
    # arena.test_progress(name=NAME, version=VERSION, opponent=OPPONENT, num_test_games=TEST_COUNT, sample_size=SAMPLE_SIZE)
    # arena.test_progress_self(name=NAME, version=VERSION, verbose=VERBOSE, sample_size=SAMPLE_SIZE)
    arena.run_sample_game(PLAYER_1, PLAYER_2, vv=True)
    # arena.run_games(150, PLAYER_1, PLAYER_2, verbose=VERBOSE)
    # arena.train(name=NAME, version=VERSION, continue_training=CONTINUE, verbose=VERBOSE, save_frequency=SAVE_FREQ, num_games=GAME_COUNT)


if __name__ == "__main__":
    main()
