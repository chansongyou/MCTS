from mcts.tictactoe import TicTacToeBoard, Player, GameResult
from mcts.tree import Tree


human_player = Player.X
ai_player = Player.O

board = TicTacToeBoard(human_player)

# wait for user input
while not board.is_terminal:
    board.draw_board()
    try:
        if board.current_player == human_player:
            move = int(input("Enter move: "))
            board.make_move(move, human_player)
        else:
            mcts = Tree(ai_player, max_iterations=10)
            move = mcts.search(board)
            board.make_move(move, ai_player)
    except ValueError:
        print("Invalid move")
        continue

    if board.is_terminal:
        board.draw_board()
        if board.result == GameResult.WINNER_EXIST:
            print(f"{board.winner} wins!")
        else:
            print("Draw!")
        break
