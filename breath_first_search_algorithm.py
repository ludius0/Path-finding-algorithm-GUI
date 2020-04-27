from tkinter import Canvas
import queue
import time

import values as v

c = v.c

### Checking neighbours through x and y coordinates
def check_neighbours(curr, grid, canvas, end):
    global checked_list
    possible_moves = []
    x, y = curr[0], curr[1]
    x0, y0 = x+c-1, y+c-1
    xn, yn = int(x/c), int(y/c)

    if x > c:
        if (x-c, y) not in checked_list and (grid[yn][xn-1][0], grid[yn][xn-1][1]) == (x-c, y): # LEFT
            possible_moves.append((x-c, y))
            checked_list.append((x-c, y))
                
            canvas.create_rectangle(x-c, y, x0-c, y0, fill=v.checked_color, outline=v.checked_color)
            if (x-c, y) == end:
                return possible_moves

    if x < (v.height-c):
        if (x+c, y) not in checked_list and (grid[yn][xn+1][0], grid[yn][xn+1][1]) == (x+c, y): # RIGHT
            possible_moves.append((x+c, y))
            checked_list.append((x+c, y))
            
            canvas.create_rectangle(x+c, y, x0+c, y0, fill=v.checked_color, outline=v.checked_color)
            if (x+c, y) == end:
                return possible_moves

    if y > 0:
        if (x, y-c) not in checked_list and (grid[yn-1][xn][0], grid[yn-1][xn][1]) == (x, y-c): # UP
            possible_moves.append((x, y-c))
            checked_list.append((x, y-c))
            
            canvas.create_rectangle(x, y-c, x0, y0-c, fill=v.checked_color, outline=v.checked_color)
            if (x, y-c) == end:
                return possible_moves

    if y < (v.height-c):
        if (x, y+c) not in checked_list and (grid[yn+1][xn][0], grid[yn+1][xn][1]) == (x, y+c): # DOWN
            possible_moves.append((x, y+c))
            checked_list.append((x, y+c))
            
            canvas.create_rectangle(x, y+c, x0, y0+c, fill=v.checked_color, outline=v.checked_color)
            if (x, y+c) == end:
                return possible_moves     
    canvas.update()
    return possible_moves

### Algorithm      
def breath_first_search(canvas, grid, start, end):
    global checked_list
    """
    USE QUEUE -> FIFO (first in, first out)
    First we generate Queue list (frontier) and dict (came_from)
    For every loop we take current node (current) and check neighbours (neighbours_list -> for loop with next_)
    And for every neighbour we check if it isn't already in dict(came_from) -> if not we add it to queue (frontier) and add to dict (came_from) with key as (current -> current node/cell)
    With every loop one element will be removed from Queue (frontier) and if it end up empty -> there isn't path
    If it find end node as neighbour; it will add it and break through loop.
    Also you don't need queue module to do it: make list (frontier=[]) and pop firtst element (current = frontier.pop(0)) and frontier.put() replace for append and loop until list isn't empty or you find goal
    """
    frontier = queue.Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    checked_list = []           # To insure it won't compute already checked nodes again
    
    start_time = time.time()

    # Algorithm
    while not frontier.empty():
        current = frontier.get()

        if current == end:
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

    # End timer
    end_time = round(time.time() - start_time, 7)

    return (path, end_time)
