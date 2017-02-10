from math import ceil, log, sqrt
from collections import deque
import queue
import resource
import sys
import time

def bfs(init_brd, goal):
    r, c = find_elem(init_brd)
    if r < 0: return False

    start_t = time.time()
    n_nodes_expanded, height = 0, 0

    q = queue.Queue()
    init_state = {'brd': init_brd, 'depth': 0, 'parent': None, 'empty_r': r, 'empty_c': c}
    q.put( init_state )
    last_enqueued = init_state
    discovered_brds = {init_brd}

    while not q.empty():
        curr_state = q.get()
        if curr_state['brd'] == goal:
            path_to_goal = get_path_to_goal(curr_state)
            qsz = q.qsize()
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': n_nodes_expanded,
                'fringe_size': qsz,
                'max_fringe_size': qsz+1,
                'search_depth': len(path_to_goal),
                'max_search_depth': last_enqueued['depth'], # ceil(log(3, 4) + log(len(n_nodes_expanded), 4) - 1), bummer, the tree's not perfect
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        for nghbr in get_nghbr_states_UDLR(curr_state): # note: not always 4 neighbors
            if nghbr['brd'] not in discovered_brds:
                q.put( nghbr )
                last_enqueued = nghbr
                discovered_brds.add( nghbr['brd'] )

        n_nodes_expanded += 1 # always?

    return False

def dfs(init_brd, goal):
    r, c = find_elem(init_brd)
    if r < 0: return False

    start_t = time.time()

    n_nodes_expanded, max_fringe_size, height = 0, 1, 0
    st = [ {'brd': init_brd, 'depth': 0, 'parent': None, 'empty_r': r, 'empty_c': c} ]
    discovered_brds = {init_brd}
    max_fringe_size = 1

    while st:
        curr_state = st.pop()
        if curr_state['brd'] == goal:
            path_to_goal = get_path_to_goal(curr_state)
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': n_nodes_expanded,
                'fringe_size': len(st),
                'max_fringe_size': max_fringe_size,
                'search_depth': len(path_to_goal),
                'max_search_depth': max(height, curr_state['depth']),
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        old_sz = len(discovered_brds)
        for nghbr in get_nghbr_states_UDLR(curr_state, True): # note: not always 4 neighbors
            if nghbr['brd'] not in discovered_brds:
                st.append( nghbr )
                discovered_brds.add( nghbr['brd'] )
        if len(discovered_brds) == old_sz:
            height = max(height, curr_state['depth'])
        else:
            max_fringe_size = max(max_fringe_size, len(st))

        n_nodes_expanded += 1 # always?

    return False

def ast(init_brd, goal):
    r, c = find_elem(init_brd)
    if r < 0: return False

    start_t = time.time()

    height, max_fringe_size = 0, 1

    pq = queue.PriorityQueue()
    init_state = {'brd': init_brd, 'depth': 0, 'parent': None, 'empty_r': r, 'empty_c': c}
    pq.put( (h(init_brd), time.time(), init_state) )
    frontier = {init_brd}
    explored = set()

    while not pq.empty():
        curr_g, _t, curr_state = pq.get()
        if curr_state['brd'] in explored:
            continue
        frontier.remove(curr_state['brd'])
        explored.add(curr_state['brd'])

        if curr_state['brd'] == goal:
            path_to_goal = get_path_to_goal(curr_state)
            write_result({
                'path_to_goal': path_to_goal,
                'cost_of_path': len(path_to_goal),
                'nodes_expanded': len(explored),
                'fringe_size': len(frontier),
                'max_fringe_size': max(max_fringe_size, len(frontier)),
                'search_depth': len(path_to_goal),
                'max_search_depth': max(height, curr_state['depth']),
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True
        old_sz = len(frontier)
        for nghbr in get_nghbr_states_UDLR(curr_state): # note: not always 4 neighbors
            if nghbr['brd'] not in frontier and nghbr['brd'] not in explored:
                pq.put( (h(nghbr['brd'])+curr_g, time.time(), nghbr) )
                frontier.add( nghbr['brd'] )
            elif nghbr['brd'] in frontier:
                pq.put( (h(nghbr['brd'])+curr_g, time.time(), nghbr) )
        if len(frontier) <= old_sz:
            max_fringe_size = max(max_fringe_size, len(frontier))
            height = max(height, curr_state['depth'])


    return False

def ida(init_brd, goal):
    r, c = find_elem(init_brd)
    if r < 0: return False

    start_t = time.time()

    bound = h(init_brd)
    mem = {'n_nodes_expanded': 0}

    while 'path_to_goal' not in mem:
        mem = hdls(init_brd, goal, r, c, bound, mem)
        bound += 1

    write_result({
        'path_to_goal': mem['path_to_goal'],
        'cost_of_path': len(mem['path_to_goal']),
        'nodes_expanded': mem['n_nodes_expanded'],
        'fringe_size': mem['fringe_size'],
        'max_fringe_size': mem['max_fringe_size'],
        'search_depth': len(mem['path_to_goal']),
        'max_search_depth': mem['max_search_depth'],
        'running_time': time.time() - start_t,
        'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
    })
    return True

def hdls(init_brd, goal, empty_r, empty_c, bound, mem):
    if init_brd[empty_r][empty_c]: raise ValueError("Wrong coordinates of an empty cell.")

    height, max_fringe_size = 0, 1

    pq = queue.PriorityQueue()
    init_state = {'brd': init_brd, 'depth': 0, 'parent': None, 'empty_r': empty_r, 'empty_c': empty_c}
    pq.put( (h(init_brd), time.time(), init_state) )
    frontier = {init_brd}
    explored = set()

    while not pq.empty():
        curr_g, _t, curr_state = pq.get()
        if curr_state['brd'] in explored:
            continue
        frontier.remove(curr_state['brd'])
        explored.add(curr_state['brd'])

        if curr_state['brd'] == goal:
            mem['path_to_goal'] = get_path_to_goal(curr_state)
            mem['n_nodes_expanded'] += len(explored)
            mem['fringe_size'] = len(frontier)
            mem['max_fringe_size'] = max(max_fringe_size, len(frontier))
            mem['max_search_depth'] = max(height, curr_state['depth'])

            return mem
        old_sz = len(frontier)
        for nghbr in get_nghbr_states_UDLR(curr_state): # note: not always 4 neighbors
            f = h(nghbr['brd'])+curr_g
            if f > bound:
                continue
            elif nghbr['brd'] not in frontier and nghbr['brd'] not in explored:
                pq.put( (f, time.time(), nghbr) )
                frontier.add( nghbr['brd'] )
            elif nghbr['brd'] in frontier:
                pq.put( (f, time.time(), nghbr) )
        if len(frontier) <= old_sz:
            max_fringe_size = max(max_fringe_size, len(frontier))
            height = max(height, curr_state['depth'])


    return mem

def h(brd):
    n = len(brd)
    dists = []
    #return sum([abs(r-v//n)+abs(c-v%n) for c, v in enumerate(row) for r, row in enumerate(brd)])
    for r, row in enumerate(brd):
        for c, v in enumerate(row):
            dists.append(abs(r-v//n)+abs(c-v%n))

    return sum(dists)

def get_nghbr_states_UDLR(parent_state, reverse = False):
    r, c = parent_state['empty_r'], parent_state['empty_c']
    parent_brd = parent_state['brd']
    next_depth = parent_state['depth']+1
    nghbrs = deque()
    if r > 0:
        up_r = r-1
        t = parent_brd[up_r][c]
        child_brd = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['brd'])
        if reverse:
            nghbrs.appendleft( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': up_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Up'} )
        else:
            nghbrs.append( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': up_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Up'} )
    if r < max_r:
        down_r = r+1
        t = parent_brd[down_r][c]
        child_brd = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['brd'])
        if reverse:
            nghbrs.appendleft( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': down_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Down'} )
        else:
            nghbrs.append( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': down_r, 'empty_c': c, 'move_that_lead_to_this_state': 'Down'} )

    if c > 0:
        left_c = c-1
        t = parent_brd[r][left_c]
        child_brd = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['brd'])
        if reverse:
            nghbrs.appendleft( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': r, 'empty_c': left_c, 'move_that_lead_to_this_state': 'Left'} )
        else:
            nghbrs.append( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': r, 'empty_c': left_c, 'move_that_lead_to_this_state': 'Left'} )

    if c < max_c:
        right_c = c+1
        t = parent_brd[r][right_c]
        child_brd = tuple(tuple(0 if elem == t else t if elem == 0 else elem for elem in row) for row in parent_state['brd'])
        if reverse:
            nghbrs.appendleft( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': r, 'empty_c': right_c, 'move_that_lead_to_this_state': 'Right'} )
        else:
            nghbrs.append( {'brd': child_brd, 'depth': next_depth, 'parent': parent_state, 'empty_r': r, 'empty_c': right_c, 'move_that_lead_to_this_state': 'Right'} )


    return nghbrs

def get_path_to_goal(final_state):
    path = []
    curr_state = final_state
    while curr_state['parent']:
        path.append( curr_state['move_that_lead_to_this_state'] )
        curr_state = curr_state['parent']

    path.reverse()
    return path

# def get_depth(brd_state):
#     depth = 0
#     while brd_state['parent']:
#         depth += 1
#         brd_state = brd_state['parent']
#
#     print(depth)
#     return depth


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

def find_elem(brd, elem = 0):
    for i, row in enumerate(brd):
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
init_brd = tuple(tuple(nums[i:i+n]) for i in range(0, len(nums), n))

search_type_to_fun = {
    'bfs': bfs,
    'dfs': dfs,
    'ast': ast,
    'ida': ida
}

if search_type in search_type_to_fun:
    goal_nums = tuple(range(0, len(nums)))
    search_type_to_fun[search_type](init_brd, tuple(goal_nums[i:i+n] for i in range(0, len(goal_nums), n)))
else:
    raise ValueError('Invalid search method. Allowed: bfs, dfs, ast, ida')
