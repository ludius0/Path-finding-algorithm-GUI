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
    global canvas, grid, color_, start, end, walls_list
    # Get coordinates of x and y
    x = event.x -(event.x % c)
    y = event.y -(event.y % c)

    x, y = check_back_grid(x, y)

    if v.first_click == True:                                                   # Draw start
        v.first_click = False
        v.second_click = True
        
        start = (x, y)
        color_ = v.start_color
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=v.start_color, outline=v.start_color)
        
    elif v.second_click == True and (x, y) != start:             # Draw end
        v.second_click = False
        v.mouse_bind = v.mouse_bind_motion
        canvas.bind(v.mouse_bind, paint)
        
        end = (x, y)
        
        color_ = v.end_color
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=v.end_color, outline=v.end_color)
        
    elif (x, y) != start and (x, y) != end:       # Draw wall
        color_ = v.wall_color
        
        canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=v.wall_color, outline=v.wall_color)

        grid[int(y/c)][int(x/c)] = (9999, 9999)             # Save wall to the grid

    canvas.update()


### GENERATE & PAINT ON CANVAS & USE ALGORITHM
def paint_blank_grid():         # Generate blank grid of width*height lenght of cells
    global grid
    grid = []
    for i in range(v.row_size):
        row = []
        for j in range(v.col_size):
            row.append((j*c, i*c)) # (x, y)
        grid.append(row)

def paint_path(path, canvas):   # Paint path to end cell/node on canvas
    global start
    if path != None:
        for i in path:
            x, y = int(i[0]), int(i[1])
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


def use_algorithm(choice):            # Use breath first algorithm to get 
    global grid, canvas, start, end, save_color
    # Breath first search algorithm
    if choice == 0:
        try:
            path, end_time = bfsa.breath_first_search(canvas, grid, start, end)
            paint_path(path, canvas)
            results(path, end_time)
            v.show_color, v.wall_color = v.wall_color, v.show_color # Highlighting
        except:
         print("Start and end nodes are missing.")
    # A* algorithm
    elif choice == 1:
        pass
        

### TKINTER GUI
def restart_window():
    global root, canvas, save_color, walls_list
    v.first_click = True
    v.second_click = False
    v.mouse_bind = v.mouse_bind_click
    v.wall_color, v.show_color = v.show_color, v.wall_color
    walls_list = []
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

    button1 = Button(root, text="Use breath first search algorithm", command=lambda:use_algorithm(0))
    button1.pack(side=TOP)

    button2 = Button(root, text="Use A* algorithm", command=lambda:use_algorithm(1))
    button2.pack(ipadx=41, side=TOP)

    button3 = Button(root, text="Restart window", command=restart_window)
    button3.pack(ipadx=45, side=TOP)
    
    root.mainloop()

if __name__ == "__main__":
    main()
