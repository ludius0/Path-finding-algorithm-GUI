from tkinter import Canvas
import queue
import time

import values as v

c = v.c

### Checking neighbours through x and y coordinates
def check_neighbours(curr, grid, canvas, end):
    possible_moves = []
    color, x, y, a, b = curr[0], curr[1], curr[2], curr[3], curr[4]

    if x > c:               # Left
        if grid[a][b-1][0] == v.empty_color and (grid[a][b-1][1], grid[a][b-1][2]) == (x-c, y):
            neighbour = (v.checked_color, grid[a][b-1][1], grid[a][b-1][2], grid[a][b-1][3], grid[a][b-1][4]) # (checked color, x, y, a, b)
            
            possible_moves.append(neighbour) 
            grid[a][b-1] = neighbour
            canvas.create_rectangle(grid[a][b-1][1], grid[a][b-1][2], grid[a][b-1][1]+c-1, grid[a][b-1][2]+c-1, fill=v.checked_color, outline=v.checked_color) # draw it

        if grid[a][b-1][0] == v.end_color and (grid[a][b-1][1], grid[a][b-1][2]) == (x-c, y):   # Check if it isn't end cell/node
            possible_moves.append(end)
            return possible_moves

    if x < (v.height-c):    # Right
        if grid[a][b+1][0] == v.empty_color and (grid[a][b+1][1], grid[a][b+1][2]) == (x+c, y):
            neighbour = (v.checked_color, grid[a][b+1][1], grid[a][b+1][2], grid[a][b+1][3], grid[a][b+1][4])
            
            possible_moves.append(neighbour) 
            grid[a][b+1] = neighbour
            canvas.create_rectangle(grid[a][b+1][1], grid[a][b+1][2], grid[a][b+1][1]+c-1, grid[a][b+1][2]+c-1, fill=v.checked_color, outline=v.checked_color)
            
        if grid[a][b+1][0] == v.end_color and (grid[a][b+1][1], grid[a][b+1][2]) == (x+c, y):
            possible_moves.append(end)
            return possible_moves

    if y > c:               # Up
        if grid[a-1][b][0] == v.empty_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            neighbour = (v.checked_color, grid[a-1][b][1], grid[a-1][b][2], grid[a-1][b][3], grid[a-1][b][4])
            
            possible_moves.append(neighbour) 
            grid[a-1][b] = neighbour
            canvas.create_rectangle(grid[a-1][b][1], grid[a-1][b][2], grid[a-1][b][1]+c-1, grid[a-1][b][2]+c-1, fill=v.checked_color, outline=v.checked_color)

        if grid[a-1][b][0] == v.end_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            possible_moves.append(end)
            return possible_moves

    if y < (v.height-c):    # Down
        if grid[a+1][b][0] == v.empty_color and (grid[a+1][b][1], grid[a+1][b][2]) == (x, y+c):
            neighbour = (v.checked_color, grid[a+1][b][1], grid[a+1][b][2], grid[a+1][b][3], grid[a+1][b][4])
            
            possible_moves.append(neighbour) 
            grid[a+1][b] = neighbour
            canvas.create_rectangle(grid[a+1][b][1], grid[a+1][b][2], grid[a+1][b][1]+c-1, grid[a+1][b][2]+c-1, fill=v.checked_color, outline=v.checked_color)

        if grid[a-1][b][0] == v.end_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            possible_moves.append(end)
            return possible_moves
            
    canvas.update()
    return possible_moves

### Algorithm      
def breath_first_search(grid, canvas, start, end):
    """
    USE QUEUE -> FIFO (first in, first out)
    First we generate Queue list (frontier) and dict (came_from)
    For every loop we take current node/cell (current) and check neighbours (neighbours_list -> for loop with next_)
    And for every neighbour we check if it isn't already in dict(came_from) -> if not we add it to queue (frontier) and add to dict (came_from) with key as (current -> current node/cell)
    With every loop one element will be removed from Queue (frontier) and if it end up empty -> there isn't path
    If it find end node/cell as neighbour; it will add it and break through loop.
    Also you don't need queue module to do it: make list (frontier=[]) and pop firtst element (current = frontier.pop(0)) and frontier.put() replace for append and loop until list isn't empty or you find goal
    """
    frontier = queue.Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    
    start_time = time.time()

    # Algorithm
    while not frontier.empty():
        current = frontier.get()

        if (current[1], current[2]) == (end[1], end[2]):
            break
        
        neighbours_list = check_neighbours(current, grid, canvas, end)
        for next_ in neighbours_list:
            if next_ not in came_from:
                frontier.put(next_)
                came_from[next_] = current
    # Get path
    if not frontier.empty():
        current = end 
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
    else:
        path = None

    end_time = time.time() - start_time

    return (path, end_time)
