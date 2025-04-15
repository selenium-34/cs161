def BFS(TREE):
    """
    Performs a left-to-right breadth-first search on TREE
    and returns a tuple of leaf nodes in the order visited.

    Args:
        TREE (tuple or leaf): The tree structure to search.

    Returns:
        tuple: A tuple of visited leaf nodes in BFS order.
    """
    if not isinstance(TREE, tuple):
        return (TREE,)

    queue = [TREE]  # using list as queue
    result = []

    while queue:
        node = queue.pop(0)  # pop from front to simulate FIFO
        if isinstance(node, tuple):
            for child in node:
                queue.append(child)
        else:
            result.append(node)

    return tuple(result)

def DFS(TREE):
    """
    Performs a left-to-right depth-first search on TREE
    and returns a tuple of leaf nodes in the order visited.

    Args:
        TREE (tuple or leaf): The tree structure to search.

    Returns:
        tuple: A tuple of visited leaf nodes in DFS order.
    """
    if not isinstance(TREE, tuple):
        return (TREE,)

    result = []
    for child in TREE:
        result.extend(DFS(child))

    return tuple(result)

def DFID(TREE, D):
    """
    Performs right-to-left depth-first iterative-deepening search up to depth D.
    Nodes may appear multiple times if visited in multiple iterations.

    Args:
        TREE (tuple or leaf): Tree to search.
        D (int): Maximum depth.

    Returns:
        tuple: Leaf nodes in order of visitation.
    """
    result = []
    for limit in range(D + 1):
        result.extend(_dls(TREE, limit))
    return tuple(result)

def _dls(TREE, limit):
    """
    Depth-limited search (right-to-left) helper for DFID.

    Args:
        TREE (tuple or leaf): Tree to search.
        limit (int): Depth limit.

    Returns:
        list: Leaf nodes visited in this iteration.
    """
    if limit < 0:
        return []

    if not isinstance(TREE, tuple):
        return [TREE]

    if limit == 0:
        return []

    result = []
    for child in reversed(TREE):  # right-to-left
        result.extend(_dls(child, limit - 1))
    return result

# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).
# The main entry point for this solver is the function DFS_SOL, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS_SOL returns [].
# To call DFS_SOL to solve the original problem, one would call
# DFS_SOL((False, False, False, False), [])
# However, it should be possible to call DFS_SOL with any intermediate state (S)
# and the path from the initial state to S (PATH).
# First, we define the helper functions of DFS_SOL.
# FINAL_STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
def FINAL_STATE(S):
    return S == (True, True, True, True)
# NEXT_STATE returns the state that results from applying an operator to the
# current state. It takes two arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns [].
# NOTE that NEXT_STATE returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
def NEXT_STATE(S, A):
    homer, baby, dog, poison = S

    if A == "h":
        new = (not homer, baby, dog, poison)
    elif A == "b" and homer == baby:
        new = (not homer, not baby, dog, poison)
    elif A == "d" and homer == dog:
        new = (not homer, baby, not dog, poison)
    elif A == "p" and homer == poison:
        new = (not homer, baby, dog, not poison)
    else:
        return []

    h, b, d, p = new

    if b == d and b != h:
        return []

    if b == p and b != h:
        return []

    return [new]


    # Rule 1: Dog and baby alone without Homer
    if b == d and b != h:
        return []

    # Rule 2: Baby and poison alone without Homer
    if b == p and b != h:
        return []

    return [new]
# SUCC_FN returns all of the possible legal successor states to the current
# state. It takes a single argument (S), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
def SUCC_FN(S):
    successors = []
    for action in ["h", "b", "d", "p"]:
        result = NEXT_STATE(S, action)
        if result:
            print(f"Action '{action}' from {S} → {result[0]}")
            successors.extend(result)
        else:
            print(f"Action '{action}' from {S} → invalid")
    return successors

# ON_PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if S is a member of
# STATES and False otherwise.
def ON_PATH(S, STATES):
    return S in STATES
# MULT_DFS is a helper function for DFS_SOL. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT_DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT_DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].
def MULT_DFS(STATES, PATH):
    for state in STATES:
        result = DFS_SOL(state, PATH)
        if result:
            return result
    return []

# DFS_SOL does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to []. DFS_SOL
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or [] otherwise. DFS_SOL is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path (i.e., S is not on PATH).
def DFS_SOL(S, PATH):
    print(f"Visiting: {S}")

    if FINAL_STATE(S):
        print("Reached goal state!")
        return PATH + [S]

    if ON_PATH(S, PATH):
        print("State already on path (cycle):", S)
        return []

    return MULT_DFS(SUCC_FN(S), PATH + [S])