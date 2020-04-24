from tkinter import *
import queue
import time

# Constant
height = 100
width = 100
c = 10 # pixel size
row_size = int(width/c)
col_size = int(height/c)

first_click = True
second_click = False
click_bind = "<Button-1>"

def check_back_grid(x, y): # Correcting grid (setting edges)
    if x == 0: x = c
    if y == 0: y = c
    if x >= width-c: x = width - c
    if y >= height-c: y = height - c
    return x, y


def paint(event):
    global first_click, second_click, grid, start, end, click_bind
    x = event.x -(event.x % c)
    y = event.y -(event.y % c)

    x, y = check_back_grid(x, y)

    if first_click == True:
        first_click = False
        second_click = True
        color = "Purple"
        start = (color, x, y)
        print(start)
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color)
    elif second_click == True and (x, y) != (start[1], start[2]):
        second_click = False
        color = "Blue"
        end = (color, x, y)
        print(end)
        print("-"*20)
        click_bind = "<B1-Motion>"
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color)
    elif (x, y) != (start[1], start[2]) and (x, y) != (end[1], end[2]):
        color = "Black"
        end = (color, x, y)
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color)

    for index, i in enumerate(grid):
        for index2, j in enumerate(i):
            if (x, y) == (j[1], j[2]):
                grid[index][index2] = (color, x, y)



def paint_blank_grid():
    global grid
    grid = []
    for i in range(row_size):
        row = []
        for j in range(col_size):
            row.append(("white", j*c, i*c))
        grid.append(row)

def check_neighbours(curr):
    global grid
    possible_moves = []
    for index, i in enumerate(grid):
        for index2, j in enumerate(i):
            x, y = int(j[1]), int(j[2])
            x0, y0 = int(x+c-1), int(y+c-1)

              
            if curr[1] > c:
                if j[0] == "white" and (j[1], j[2]) == (curr[1]-c, curr[2]): #LEFT
                    possible_moves.append(("Red", j[1], j[2]))
                    grid[index][index2-1] = ("Red", j[1], j[2])
                    canvas.create_rectangle(x, y, x0, y0, fill="red", outline="red")
                elif j[0] == "Blue" and (j[1], j[2]) == (curr[1]-c, curr[2]):
                    possible_moves.append(end)
                    break

            if curr[1] < (width-c):
                if j[0] == "white" and (j[1], j[2]) == (curr[1]+c, curr[2]): #RIGHT
                    possible_moves.append(("Red", j[1], j[2]))
                    grid[index][index2+1] = ("Red", j[1], j[2])
                    canvas.create_rectangle(x, y, x0, y0, fill="red", outline="red")
                elif j[0] == "Blue" and (j[1], j[2]) == (curr[1]+c, curr[2]):
                    possible_moves.append(end)
                    break
                
            if curr[2] > c:
                if j[0] == "white" and (j[1], j[2]) == (curr[1], curr[2]-c): #UP
                    possible_moves.append(("Red", j[1], j[2]))
                    grid[index-1][index2] = ("Red", j[1], j[2])
                    canvas.create_rectangle(x, y, x0, y0, fill="red", outline="red")
                elif j[0] == "Blue" and (j[1], j[2]) == (curr[1], curr[2]-c):
                    possible_moves.append(end)
                    break
            
            if curr[2] < (height-c):
                if j[0] == "white" and (j[1], j[2]) == (curr[1], curr[2]+c): #DOWN
                    possible_moves.append(("Red", j[1], j[2]))
                    grid[index+1][index2] = ("Red", j[1], j[2])
                    canvas.create_rectangle(x, y, x0, y0, fill="red", outline="red")
                elif j[0] == "Blue" and (j[1], j[2]) == (curr[1], curr[2]+c):
                    possible_moves.append(end)
                    break
            canvas.update()
    return possible_moves
                                
def breath_first_search():

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
    path.append(start) # optional
    path.reverse() # optional
    print(path)

    end_time = time.time() - start_time
    print(end_time)
    
    

def main():
    global canvas, button
    root = Tk()
    root.title("PATH FINDING ALGORITH by ludius0")
    root.geometry(f"{width+c+c}x{height+100}")
    root.config(bg="#ecf0f1")
    root.resizable(width=False, height=False)

    canvas = Canvas(root, width=width, height=height, bg="white", borderwidth=2)
    canvas.bind(click_bind, paint)
    canvas.pack(side=TOP)

    paint_blank_grid()

    button = Button(root, text="Use alg", command=breath_first_search)
    button.pack(side=BOTTOM)

if __name__ == "__main__":
    main()
