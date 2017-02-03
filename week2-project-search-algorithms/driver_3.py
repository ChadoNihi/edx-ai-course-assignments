import queue
import resource
import time

def bfs(init_board, goal):
    start_t = time.time()
    n_nodes_expanded = 0

    q = queue.Queue()
    q.put( {board: init_board, parent: None} )
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
                'search_depth': ,
                'max_search_depth': ,
                'running_time': time.time() - start_t,
                'max_ram_usage': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) #assuming kb (as for Linux)
            })
            return True

        for nghbr in get_nghbrs_UDLR(curr_state.board):
            if nghbr not in discovered_boards:
                q.put( {board: nghbr, parent: curr_state} )

        n_nodes_expanded += 1

    return False

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
