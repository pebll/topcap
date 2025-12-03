from copy import deepcopy

from topcap.agents import Human, RandomAI, HeuristicAI, GraphAI, GraphAICopilot, JanMVP, QDicter
from topcap.agents.leo_agent_v1 import LeoAgentV1
from topcap.agents.utils import heuristic
from topcap.agents.utils.heuristic import SimpleHeuristic, ExponentialHeuristic
from topcap.core.game.arena import Arena
from topcap.core.common import Board, Color

MAX_THINKING_TIME = 10
# heuristics
base_simple_heuristic = SimpleHeuristic()
base_exp_heuristic = ExponentialHeuristic()

VV = False
VERBOSE = False
DECAY = 0.95
EPSILON = 0.7
ALPHA = 0.3

# agents
leo = Human("Léo")
jan = Human("Jan")
randi = RandomAI("Randi")
rando = RandomAI("Rando", False)
heuri_simple = HeuristicAI(base_simple_heuristic, "Heuri Simple")
heuri = HeuristicAI(base_exp_heuristic, "Heuri Expo")
jan_mvp = JanMVP("Jan's Noob AI", verbose=VV)
plusminus = QDicter("plusminus", vv=VV, epsilon = 0.1, decay = 0.95, initialization=0)
leo_mvp = LeoAgentV1("Léo's Baby", verbose=VERBOSE, vv=VV, decay=DECAY)
leo_other_mvp = LeoAgentV1("Léo's Other Baby", verbose=VERBOSE, vv=VV, decay=DECAY, epsilon=EPSILON, alpha=ALPHA)

leo_other_mvp.load_latest()

PLAYER_1 = leo_other_mvp
PLAYER_2 = leo

AGENT = leo_other_mvp
CONTINUE = True
GAME_COUNT = 20000
SAVE_FREQ = 500
TEST_COUNT = 100
SAMPLE_SIZE = 20
OPPONENT = randi


def main():
    arena = Arena()
    # arena.train(agent=AGENT, continue_training=CONTINUE, save_frequency=SAVE_FREQ, num_games=GAME_COUNT)
    # arena.test_progress(agent=AGENT, opponent=OPPONENT, num_test_games=TEST_COUNT, sample_size=SAMPLE_SIZE)
    # arena.test_progress_self(agent=AGENT, verbose=VERBOSE, sample_size=SAMPLE_SIZE)
    arena.run_sample_game(PLAYER_1, PLAYER_2, vv=True)
    # arena.run_games(150, PLAYER_1, PLAYER_2, verbose=VERBOSE)
    # arena.train(name=NAME, version=VERSION, continue_training=CONTINUE, verbose=VERBOSE, save_frequency=SAVE_FREQ, num_games=GAME_COUNT)
    if False:
        board = Board()
        board.move(board.get_all_valid_moves(Color.WHITE)[0])
        hash = board.to_hash()
        print(f"Hash: {hash}")
        new_board = Board()
        new_board.from_hash(hash)
        print("Board from hash:")
        print(new_board.to_str())


if __name__ == "__main__":
    main()
