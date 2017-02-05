from math import sqrt
import queue
import resource
import sys
import time

def bfs(init_board, goal):
    start_t = time.time()
    height = 0
    n_nodes_expanded = 0

    q = queue.Queue()
    r, c = find_elem(init_board)
    if r < 0: return False
    q.put( {'board': init_board, 'parent': None, 'empty_r': r, 'empty_c': c} )
    discovered_boards = {init_board}

    while not q.empty():
        curr_state = q.get()
        if curr_state.board == goal:
            path_to_goal = get_path_to_goal(curr_state)
            qsz = q.qsize()
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': n_nodes_expanded,
                'fringe_size': qsz,
                'max_fringe_size': qsz+1,
                'search_depth': len(path_to_goal),
                'max_search_depth': height,
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        old_sz = len(discovered_boards)
        for nghbr in get_nghbr_states_UDLR(curr_state): # note: not always 4 neighbors
            if nghbr.board not in discovered_boards:
                q.put( nghbr )
                discovered_boards.add(nghbr.board)

        if old_sz != len(discovered_boards): height += 1
        n_nodes_expanded += 1 # always?

    return False

def dfs():
    pass
def ast():
    pass
def ida():
    pass

def get_nghbr_states_UDLR(parent_state):
    r, c = parent_state.empty_r, parent_state.empty_c
    nghbrs = []
    if r > 0:
        up_r = r-1
        child_board = [row[:] for row in parent_state.board]
        child_board[r][c], child_board[up_r][c] = child_board[up_r][c], child_board[r][c]
        nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': up_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Up'} )
    if r < max_r:
        down_r = r+1
        child_board = [row[:] for row in parent_state.board]
        child_board[r][c], child_board[down_r][c] = child_board[down_r][c], child_board[r][c]
        nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': down_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Down'} )
    if c > 0:
        left_c = c-1
        child_board = [row[:] for row in parent_state.board]
        child_board[r][c], child_board[r][left_c] = child_board[r][left_c], child_board[r][c]
        nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': left_c, 'move_that_lead_to_this_state': 'Left'} )
    if c < max_c:
        right_c = c+1
        child_board = [row[:] for row in parent_state.board]
        child_board[r][c], child_board[r][right_c] = child_board[r][right_c], child_board[r][c]
        nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': right_c, 'move_that_lead_to_this_state': 'Right'} )

def get_path_to_goal(final_state):
    path = []
    curr_state = final_state
    while curr_state.parent:
        path.append( curr_state.move_that_lead_to_this_state )
        curr_state = curr_state.parent

    path.reverse()
    return path

def write_result(stats):
    with open('output.txt', 'w') as output_file:
        output_file.write('path_to_goal: ' + stats.path_to_goal + '\n')
        output_file.write('cost_of_path: ' + stats.cost_of_path + '\n')
        output_file.write('nodes_expanded: ' + stats.nodes_expanded + '\n')
        output_file.write('fringe_size: ' + stats.fringe_size + '\n')
        output_file.write('max_fringe_size: ' + stats.max_fringe_size + '\n')
        output_file.write('search_depth: ' + stats.search_depth + '\n')
        output_file.write('max_search_depth: ' + stats.max_search_depth + '\n')
        output_file.write('running_time: ' + stats.running_time + '\n')
        output_file.write('max_ram_usage: ' + stats.max_ram_usage)

def find_elem(board, elem = 0):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == elem:
                return i, j

    return -1, -1

# MAIN
search_type = sys.argv[1]
nums = [int(c_temp) for c_temp in sys.argv[2].split(',')]
n = int(sqrt(len(nums)))
if n != sqrt(len(nums)):
    raise ValueError('Cannot make a square matrix from the given number of numbers')

max_r = max_c = n-1
init_board = [nums[i:i+n] for i in range(0, len(nums), n)]

search_type_to_fun = {
    'bfs': bfs,
    'dfs': dfs,
    'ast': ast,
    'ida': ida
}

if search_type in search_type_to_fun:
    goal_nums = list(range(0, n))
    search_type_to_fun[search_type](init_board, [goal_nums[i:i+n] for i in range(0, len(goal_nums), n)])
else:
    raise ValueError('Invalid search method. Allowed: bfs, dfs, ast, ida')
