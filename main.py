from tkinter import *

import breath_first_search_algorithm as bfsa
import values as v
c = v.c

### USER PAINT
def check_back_grid(x, y): # Correcting grid (setting edges)
    if x <= 0: x = c
    if y <= 0: y = c
    if x >= v.width-c: x = v.width - c
    if y >= v.height-c: y = v.height - c
    return x, y

def paint(event):   # Paint on canvas and save x and y to grid
    global grid, canvas, start, end, color_
    # Get coordinates of x and y
    x = event.x -(event.x % c)
    y = event.y -(event.y % c)

    x, y = check_back_grid(x, y)

    a = int(y/c) # rows
    b = int(x/c) # columns

    if v.first_click == True:                                                   # Draw start
        v.first_click = False
        v.second_click = True
        
        color_ = v.start_color
        start = (color_, x, y, a, b)
        
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)
        
    elif v.second_click == True and (x, y) != (start[1], start[2]):             # Draw end
        v.second_click = False
        v.mouse_bind = v.mouse_bind_motion
        canvas.bind(v.mouse_bind, paint)
        
        color_ = v.end_color
        end = (color_, x, y, a, b)
        
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)
        
    elif (x, y) != (start[1], start[2]) and (x, y) != (end[1], end[2]):       # Draw wall
        color_ = v.wall_color
        
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)

    canvas.update()

    # Write new nodes/cells/coordinates to grid
    for index, i in enumerate(grid):
        for index2, j in enumerate(i):
            if (x, y) == (j[1], j[2]):
                grid[index][index2] = (color_, x, y, a, b)


### GENERATE & PAINT ON CANVAS & USE ALGORITHM
def paint_blank_grid():         # Generate blank grid of width*height lenght of cells
    global grid
    grid = []
    for i in range(v.row_size):
        row = []
        for j in range(v.col_size):
            row.append((v.empty_color, j*c, i*c, i, j)) # (color, x, y, a, b)
        grid.append(row)

def paint_path(path, canvas):   # Paint path to end cell/node on canvas
    if path != None:
        for i in path:
            x, y = int(i[1]), int(i[2])
            x0, y0 = int(x+c-1), int(y+c-1)
            canvas.create_rectangle(x, y, x0, y0, fill=v.path_color, outline=v.path_color)

def results(path, time):        # Write result data (steps and time of finishing)
    global root
    if path != None:
        label1 = Label(root, text=f"It took {len(path)} steps. Time: {time} seconds")
        label1.pack()
    else:
        label2 = Label(root, text=f"There can't be path. Time: {time} seconds")
        label2.pack()


def use_algorithm():            # Use breath first algorithm to get 
    global grid, canvas, start, end, save_color
    try:
        path, end_time = bfsa.breath_first_search(grid, canvas, start, end)
        paint_path(path, canvas)
        results(path, end_time)
        # After computationing -> user paint show_color (to highlight)
        save_color = v.wall_color
        v.wall_color = v.show_color
    except:
        pass

### TKINTER GUI
def restart_window():
    global root, canvas, save_color
    v.first_click = True
    v.second_click = False
    v.mouse_bind = v.mouse_bind_click
    v.wall_color = save_color
    root.destroy()
    main()
    

def main():
    global root, canvas, button
    root = Tk()
    root.title("PATH FINDING ALGORITH by ludius0")
    root.geometry(f"{v.width+c+c}x{v.height+100}")
    root.config(bg="#ecf0f1")
    root.resizable(width=False, height=False)

    canvas = Canvas(root, width=v.width, height=v.height, bg="white", borderwidth=2)
    canvas.bind(v.mouse_bind, paint)
    canvas.pack(side=TOP)

    paint_blank_grid()

    button1 = Button(root, text="Use breath first search algorithm", command=use_algorithm)
    button1.pack()

    button2 = Button(root, text="Restart window", command=restart_window)
    button2.pack(side=BOTTOM)

if __name__ == "__main__":
    main()
