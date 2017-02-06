from math import ceil, log, sqrt
from collections import deque
import queue
import resource
import sys
import time

def bfs(init_board, goal):
    r, c = find_elem(init_board)
    if r < 0: return False

    start_t = time.time()
    n_nodes_expanded, height = 0, 0

    q = queue.Queue()
    init_state = {'board': init_board, 'parent': None, 'empty_r': r, 'empty_c': c}
    q.put( init_state )
    last_enqueued = init_state
    discovered_boards = {init_board}

    while not q.empty():
        curr_state = q.get()
        if curr_state['board'] == goal:
            path_to_goal = get_path_to_goal(curr_state)
            qsz = q.qsize()
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': n_nodes_expanded,
                'fringe_size': qsz,
                'max_fringe_size': qsz+1,
                'search_depth': len(path_to_goal),
                'max_search_depth': get_depth(last_enqueued), # ceil(log(3, 4) + log(len(n_nodes_expanded), 4) - 1), bummer, the tree's not perfect
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        for nghbr in get_nghbr_states_UDLR(curr_state): # note: not always 4 neighbors
            if nghbr['board'] not in discovered_boards:
                q.put( nghbr )
                last_enqueued = nghbr
                discovered_boards.add( nghbr['board'] )

        n_nodes_expanded += 1 # always?

    return False

def dfs(init_board, goal):
    r, c = find_elem(init_board)
    if r < 0: return False

    start_t = time.time()

    n_nodes_expanded, height = 0, 0
    st = [ {'board': init_board, 'parent': None, 'empty_r': r, 'empty_c': c} ]
    discovered_boards = {init_board}
    max_fringe_size = 1

    while st:
        curr_state = st.pop()
        if curr_state['board'] == goal:
            path_to_goal = get_path_to_goal(curr_state)
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': n_nodes_expanded,
                'fringe_size': len(st),
                'max_fringe_size': height,
                'search_depth': len(path_to_goal),
                'max_search_depth': height,
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        old_sz = len(discovered_boards)
        for nghbr in get_nghbr_states_UDLR(curr_state, True): # note: not always 4 neighbors
            if nghbr['board'] not in discovered_boards:
                st.append( nghbr )
                discovered_boards.add( nghbr['board'] )
        if len(discovered_boards) == old_sz:
            height = max(height, get_depth(curr_state))

        n_nodes_expanded += 1 # always?

    return False

def ast():
    pass
def ida():
    pass

def get_nghbr_states_UDLR(parent_state, reverse = False):
    r, c = parent_state['empty_r'], parent_state['empty_c']
    parent_board = parent_state['board']
    nghbrs = deque()
    if r > 0:
        up_r = r-1
        t = parent_board[up_r][c]
        child_board = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['board'])
        if reverse:
            nghbrs.appendleft( {'board': child_board, 'parent': parent_state, 'empty_r': up_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Up'} )
        else:
            nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': up_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Up'} )
    if r < max_r:
        down_r = r+1
        t = parent_board[down_r][c]
        child_board = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['board'])
        if reverse:
            nghbrs.appendleft( {'board': child_board, 'parent': parent_state, 'empty_r': down_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Down'} )
        else:
            nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': down_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Down'} )

    if c > 0:
        left_c = c-1
        t = parent_board[r][left_c]
        child_board = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['board'])
        if reverse:
            nghbrs.appendleft( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': left_c, 'move_that_lead_to_this_state': 'Left'} )
        else:
            nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': left_c, 'move_that_lead_to_this_state': 'Left'} )

    if c < max_c:
        right_c = c+1
        t = parent_board[r][right_c]
        child_board = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['board'])
        if reverse:
            nghbrs.appendleft( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': right_c, 'move_that_lead_to_this_state': 'Right'} )
        else:
            nghbrs.append( {'board': child_board, 'parent': parent_state, 'empty_r': r, 'empty_c': right_c, 'move_that_lead_to_this_state': 'Right'} )


    return nghbrs

def get_path_to_goal(final_state):
    path = []
    curr_state = final_state
    while curr_state['parent']:
        path.append( curr_state['move_that_lead_to_this_state'] )
        curr_state = curr_state['parent']

    path.reverse()
    return path

def get_depth(board_state):
    depth = 0
    while board_state['parent']:
        depth += 1
        board_state = board_state['parent']

    print(depth)
    return depth


def write_result(stats):
    with open('output.txt', 'w') as output_file:
        output_file.write('path_to_goal: ' + str(stats['path_to_goal']) + '\n')
        output_file.write('cost_of_path: ' + str(stats['cost_of_path']) + '\n')
        output_file.write('nodes_expanded: ' + str(stats['nodes_expanded']) + '\n')
        output_file.write('fringe_size: ' + str(stats['fringe_size']) + '\n')
        output_file.write('max_fringe_size: ' + str(stats['max_fringe_size']) + '\n')
        output_file.write('search_depth: ' + str(stats['search_depth']) + '\n')
        output_file.write('max_search_depth: ' + str(stats['max_search_depth']) + '\n')
        output_file.write('running_time: ' + str(stats['running_time']) + '\n')
        output_file.write('max_ram_usage: ' + str(stats['max_ram_usage']))

def find_elem(board, elem = 0):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == elem:
                return i, j

    return -1, -1

# def two_d_list_to_tuple(l):
#     return tuple((tuple(row) for row in l))

# MAIN
search_type = sys.argv[1]
nums = [int(c_temp) for c_temp in sys.argv[2].split(',')]
n = int(sqrt(len(nums)))
if n != sqrt(len(nums)):
    raise ValueError('Cannot make a square matrix from the given number of numbers')

max_r = max_c = n-1
init_board = tuple(tuple(nums[i:i+n]) for i in range(0, len(nums), n))

search_type_to_fun = {
    'bfs': bfs,
    'dfs': dfs,
    'ast': ast,
    'ida': ida
}

if search_type in search_type_to_fun:
    goal_nums = tuple(range(0, len(nums)))
    search_type_to_fun[search_type](init_board, tuple(goal_nums[i:i+n] for i in range(0, len(goal_nums), n)))
else:
    raise ValueError('Invalid search method. Allowed: bfs, dfs, ast, ida')
