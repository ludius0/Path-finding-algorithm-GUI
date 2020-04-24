from tkinter import *
import queue
import time

# Constant
height = 600
width = 600
c = 10 # pixel size
row_size = int(width/c)
col_size = int(height/c)

# Clicks
first_click = True
second_click = False
mouse_bind_click = "<Button-1>"
mouse_bind_motion = "<B1-Motion>"
mouse_bind = mouse_bind_click

# Colors
start_color = "Purple"
end_color = "Yellow"
wall_color = "Black"
checked_color = "Red"
path_color = "Blue"
empty_color = "White"


def check_back_grid(x, y): # Correcting grid (setting edges)
    if x <= 0: x = c
    if y <= 0: y = c
    if x >= width-c: x = width - c
    if y >= height-c: y = height - c
    return x, y


def paint(event):
    global first_click, second_click, grid, start, end, mouse_bind, canvas, color_
    x = event.x -(event.x % c)
    y = event.y -(event.y % c)

    x, y = check_back_grid(x, y)

    a = int(y/c) # rows
    b = int(x/c) # columns

    if first_click == True:                                                 # Draw start
        first_click = False
        second_click = True
        color_ = start_color
        start = (color_, x, y, a, b)
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)
        
    elif second_click == True and (x, y) != (start[1], start[2]):           # Draw end
        second_click = False
        color_ = end_color
        end = (color_, x, y, a, b)
        mouse_bind = mouse_bind_motion
        canvas.bind(mouse_bind, paint)
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)
        
    elif (x, y) != (start[1], start[2]) and (x, y) != (end[1], end[2]):     # Draw wall
        color_ = wall_color
        end = (color_, x, y, a, b)
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)

    canvas.update()

    for index, i in enumerate(grid):
        for index2, j in enumerate(i):
            if (x, y) == (j[1], j[2]):
                grid[index][index2] = (color_, x, y, a, b)

def paint_path(path):
    color = path_color
    for i in path:
        x, y = int(i[1]), int(i[2])
        x0, y0 = int(x+c-1), int(y+c-1)
        canvas.create_rectangle(x, y, x0, y0, fill=color, outline=color)


def paint_blank_grid():
    global grid
    grid = []
    for i in range(row_size):
        row = []
        for j in range(col_size):
            row.append((empty_color, j*c, i*c, i, j)) # (color, x, y, a, b)
        grid.append(row)


def check_neighbours(curr):
    global grid
    possible_moves = []
    color, x, y, a, b = curr[0], curr[1], curr[2], curr[3], curr[4]

    if x > c: # Left
        if grid[a][b-1][0] == empty_color and (grid[a][b-1][1], grid[a][b-1][2]) == (x-c, y):
            neighbour = (checked_color, grid[a][b-1][1], grid[a][b-1][2], grid[a][b-1][3], grid[a][b-1][4]) # (checked color, x, y, a, b)
            
            possible_moves.append(neighbour) 
            grid[a][b-1] = neighbour
            canvas.create_rectangle(grid[a][b-1][1], grid[a][b-1][2], grid[a][b-1][1]+c-1, grid[a][b-1][2]+c-1, fill=checked_color, outline=checked_color) # draw it

        if grid[a][b-1][0] == end_color and (grid[a][b-1][1], grid[a][b-1][2]) == (x-c, y):
            possible_moves.append(end)
            return possible_moves

    if x < (height-c): # Right
        if grid[a][b+1][0] == empty_color and (grid[a][b+1][1], grid[a][b+1][2]) == (x+c, y):
            neighbour = (checked_color, grid[a][b+1][1], grid[a][b+1][2], grid[a][b+1][3], grid[a][b+1][4])
            
            possible_moves.append(neighbour) 
            grid[a][b+1] = neighbour
            canvas.create_rectangle(grid[a][b+1][1], grid[a][b+1][2], grid[a][b+1][1]+c-1, grid[a][b+1][2]+c-1, fill=checked_color, outline=checked_color)
            
        if grid[a][b+1][0] == end_color and (grid[a][b+1][1], grid[a][b+1][2]) == (x+c, y):
            possible_moves.append(end)
            return possible_moves

    if y > c: # Up
        if grid[a-1][b][0] == empty_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            neighbour = (checked_color, grid[a-1][b][1], grid[a-1][b][2], grid[a-1][b][3], grid[a-1][b][4])
            
            possible_moves.append(neighbour) 
            grid[a-1][b] = neighbour
            canvas.create_rectangle(grid[a-1][b][1], grid[a-1][b][2], grid[a-1][b][1]+c-1, grid[a-1][b][2]+c-1, fill=checked_color, outline=checked_color)

        if grid[a-1][b][0] == end_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            possible_moves.append(end)
            return possible_moves

    if y < (height-c): # Down
        if grid[a+1][b][0] == empty_color and (grid[a+1][b][1], grid[a+1][b][2]) == (x, y+c):
            neighbour = (checked_color, grid[a+1][b][1], grid[a+1][b][2], grid[a+1][b][3], grid[a+1][b][4])
            
            possible_moves.append(neighbour) 
            grid[a+1][b] = neighbour
            canvas.create_rectangle(grid[a+1][b][1], grid[a+1][b][2], grid[a+1][b][1]+c-1, grid[a+1][b][2]+c-1, fill=checked_color, outline=checked_color)

        if grid[a-1][b][0] == end_color and (grid[a-1][b][1], grid[a-1][b][2]) == (x, y-c):
            possible_moves.append(end)
            return possible_moves
            
    canvas.update()
    return possible_moves
                                
def breath_first_search():
    global mouse_bind
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
        
        neighbours_list = check_neighbours(current)
        for next_ in neighbours_list:
            if next_ not in came_from:
                frontier.put(next_)
                came_from[next_] = current
    # Get path
    current = end 
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    path.pop(-1)
    print(len(path))

    end_time = time.time() - start_time
    print(end_time)

    paint_path(path)
    
    

def main():
    global canvas, button, click_bind
    root = Tk()
    root.title("PATH FINDING ALGORITH by ludius0")
    root.geometry(f"{width+c+c}x{height+100}")
    root.config(bg="#ecf0f1")
    root.resizable(width=False, height=False)

    canvas = Canvas(root, width=width, height=height, bg="white", borderwidth=2)
    canvas.bind(mouse_bind, paint)
    canvas.pack(side=TOP)

    paint_blank_grid()

    button = Button(root, text="Use alg", command=breath_first_search)
    button.pack(side=BOTTOM)

if __name__ == "__main__":
    main()
