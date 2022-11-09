# Reversed Reversi

By Tenshi



##  Introduction

This text is to introduce the application of **MCTS**(Monte Carlo tree search) algorithm and **MinMax Search** in game: reversed reversi, the reverse version of game Othello, i.e. the goal the player is to have the **fewest discs** turned to display its color in the final(both players have no place to place its disc).

There is no doubt that the same algorithm that solved this game can be used to solve other games in a similar way, and this is how it works in real life. What's more, MCTS can be applied to planning, optimization and other problem of determination.

Therefore, I will introduce the specific application of MCTS in this game in the following text.



## Preliminary

### Notation

$s$

state of the game

$a(s)$

action applied to the state

$f(s, a)$

next state of the game after the action is applied

$A(s)$

determined action in current game.

$u$

node $u$ of the Monte Carlo tree

$s(u)$

corresponding state of the node $u$

$Q(u)$

reward value of the node $u$

$N(u)$

number of visited times of node $u$

$P(u)$

node u's parent

$UCT(v)$

$\frac{Q(v)}{N(v)} + c\sqrt{\frac{\ln N(P(v))}{N(v)}}$

> In my code, c is fixed in value of $\sqrt 2$



### terminology

leaf

the node without son in the tree.



Function naming conventions:

- `get_candidate_list(chessboard, color)`

  This function is used to find the valid action of current state.



- `nxt(g, x, y, cur_player)`

  Indicate that next state of board g after current player drop disc in point $(x, y)$ in the board.



## Methodology

1. General workflow

- When the situation is approaching the end game, MinMax search is adopted. After making decisions on each step, all sub-situations are searched directly and the optimal situation is taken.

- If the end game has not been reached, then the decision is made by MCTS.

- In more detail, for the MCTS algorithm:

  Each search iteration uses four steps to build the search tree: selection, expansion, simulation, and backpropagation.

  Selection: Recursively select the most promising child nodes until a leaf node is selected according to the tree strategy.

  Expand: Expands the selected node to one or more child nodes.

  Simulation: One or more child nodes are simulated from the current state to the terminal state one or more times based on the default policy.

  Backpropagation: The process by which the gradient of a loss function on a parameter flows back through a network.


  ​								 Procedure of MCTS simulation and one node expanded

2. Detailed algorithm/model design

   pseudo-code:

   - MCTS

     ```
     function bestson(u)
         return u's son node u' with max UCT(u')
     
     function sel(root)
     	u ← bestson(u)
         while u is not leaf node
             u ← bestson(u)
         return u
     
     function expand(u)
         for each action a in A(s(u))
             add child node u' to u
             s(u') ← f(s(u), a)
             a(u') ← a
     
     function simulate(s)
         while s is not terminal state
             a ← randomly choice in A(s) according its weigh
             s ← f(s, a)
         return reward for state s
     
     function backup(u, Δ)
         while u is not null
             N(u) ← N(u) + 1
             Q(u) ← Δ
             Δ ← -Δ
             u ← P(u)
     
     function MCTS(s0)
     	if is first round of my turn or root have no son
     		create initial state s0
     		root ← s0
     	else
     		root ← state after opponent determined
     		
         create node u0 with state s0
         while within time limit
             ul ← sel(u0)
             if ul expanded
             	continue
             expand(ul)
             for each child node u' of ul
                 Δ ← simulate(s(u'))
                 backup(u', Δ)
         return A(bestson(u0, 0))
     ```

     

   - Min-Max Search

     ```
     function dfs(s0)
     	actions ← next state of current player's state s0
     	if no actions
     		actions ← next state of opponent's state s0'
     		if no actions
     			return game result of s0
     		return -dfs(opponent's state s0')
     	
     	res ← -1
     	for each a in actions
     		s0' ← s0's next state after actions of a
     		return_value ← -dfs(s0')
     		res ← max(res, return_value)
     	return res
     ```

     

3. Analysis

   - complexity

     Algorithms have a lot of cost in function: `get_candidate_list`, `nxt`

     Let $n$ be the length of the board($n$ is always $8$)

     Both of them need to sweep the board and find the point in eight directions.

     So the complexity is $\Theta(n^3)$

   - optimality

     Using `@jit(nopython=True)` decorator to optimize: This decorator is used to compile a Python function into native code.

     



## Experiments

1. Setup

   I generate by myself.

   I implemented a test program that supported two AI's against each other.

   Python version: 3.10.5

   numpy version: 1.23.3

   numba version: 0.56.3

   

2. Results

   In each AI battle (marked as A and B), 50 games are played, and A and B play 25 black games each.

   Find that if the winning rate of **random decision based on different weights assigned to each point** of the board is much higher than that of **equal probability decision made at each feasible point**. As a matter of fact, the winning rate of **random decision based on different weights assigned to each point** is $74\%$。

   Also, obviously, numba optimized code has a better chance of winning.

3. Analysis

   It is consistent with the expectation that the random decision based on different weights assigned to each point can achieve higher winning rate, because different points are assigned different weights to make decisions, which can make the better points expand with higher probability, so the decision nodes in the Monte Carlo tree are more excellent.

   There is no doubt that numba optimization can achieve higher efficiency, because it improves the operation efficiency of the algorithm from the hardware, so the MCTS algorithm can be extended when the point is obviously more.

   

## Conclusion

In general, I designed the AI using **heuristically optimized MCTS** and **Min Max search**.

The main optimization is **on the MCTS**.

First of all, the optimization of **numba** can improve the overall efficiency of the algorithm, but it needs to be noted that there can be no global variables inside the optimized function, and there can not be a custom class. Similarly, **any suitable part of python code** can be optimized using numba.

Then there is the decision process of using a weighted board to perform the MCTS **simulation**, which increases the hit rate of good decision points and therefore the desired win rate in the field. So it's easy to find that using reasonable methods to heuristically optimize the algorithm can achieve good results.

It can also be seen that I designed the AI in different ways for different situations, i.e., directly using Min Max search near the end game to ensure that I would not miss the winning situation; Otherwise, because the search tree is too large, MCTS is adopted to make the decision. It also works well for different scales of the problem.



## References

https://ieeexplore.ieee.org/document/6145622

http://home.ustc.edu.cn/~baj/publications/concluding2007-Bai.pdf
