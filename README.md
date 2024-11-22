# MCTS
Monte Carlo Tree Search

## TicTacToe 게임으로 구현

## 알고리즘 정리

1. Root 노드에서 Selection(선택) 시작.
2. 확장 가능한 노드에 도달할 때 까지 선택.
    - 확장 가능한 노드란, non-terminal state 이거나 아직 방문하지(확장되지) 않은 children.
    - Terminal Node는 표시를 해서 selection에서 제외시키는 듯.
3. 확장 (확장 가능한 노드에서 child node 추가)
4. Default policy를 이용해 그 이후의 수를 시뮬레이션 후, backpropagation 진행.

Search Algorithm: UCT

Default Policy: Random

## 이해를 돕는 Visulization

https://vgarciasc.github.io/mcts-viz/