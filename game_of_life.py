#Definitions
DEAD_CELL_COLOR = (1, 1, 1, 1) #white
ALIVE_CELL_COLOR = (0, 0, 0, 1) #black 
CELL_BORDER_COLOR = (0, 0, 0, 1) #black
CELL_BORDER_WIDTH = 1 
COLONY_NUMBER_OF_ROWS = 30
COLONY_NUMBER_OF_COLS = 50

GENERATION_UPDATE_INTERVAL = 0.5 # in seconds

# Classic Game of Life
# The rules, which compare the behaviour of the automaton to real life, can be condensed into the following:
#     1) Any live cell with two or three live neighbours survives.
#     2) Any dead cell with three live neighbours becomes a live cell.
#     3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.

# Define a custom widget class that inherits from BoxLayout
class GameOfLife():
    # Build and return the root widget of the app
    def build(self):
        Window.size = (APP_SCREEN_WIDTH, APP_SCREEN_HEIGHT)
    
        # create a box layout with vertical orientation for the app window
        self.box_layout = BoxLayout(orientation='vertical', padding=WIDGET_PADDING_DEFAULT)#, spacing=WIDGET_SPACING_DEFAULT)
        self.box_layout.background_color = WIDGET_BACKGROUND_COLOR

        # Create the Colony widget and add it to the layout
        self.colony = Colony()
        self.box_layout.add_widget(self.colony)

        # Create a horizontal box layout for the buttons
        self.button_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=50, pos_hint={"center_x": 0.75}) #, spacing=0, padding=(10,10,10,10)) 
        self.button_layout.background_color = WIDGET_BACKGROUND_COLOR

        # Create a Start button widget and add it to the button_layout; limit the size of the button to 100px by 50px
        self.button1 = Button(text="Start", size_hint=(None, None), size=(100, 50)) #, pos_hint={"center_x":  0.2})
        self.button_layout.add_widget(self.button1) 

        # create a Clear button widget size 100px by 50px and add it to the layout to the right of the Reverse Text button
        self.button2 = Button(text="Clear", size_hint=(None, None), size=(100, 50)) #, pos_hint={"center_x": 0.8})
        self.button_layout.add_widget(self.button2)

        # create a text string widget and add it to the button layout at the very right of the layout 
        self.label = Label(text="Generation: 0", pos_hint={"center_x": 0.8})

        self.button_layout.add_widget(self.label)

        # add the button layout to the box layout
        self.box_layout.add_widget(self.button_layout)

        # Bind the button1's on_press event to a callback function
        self.button1.bind(on_press=self.start_btn)

        # Bind the button2's on_press event to a callback function named reset_btn
        self.button2.bind(on_press=self.clear_btn)

        # Create a Clock event to update the game board to the next generation on a timer
        Clock.schedule_interval(self.next_generation_update, GENERATION_UPDATE_INTERVAL)

        #Prepare the game to start
        self.running = False #flag to indicate if the game is running through colony cell generations
        self.update_generation_label(self.colony.generation_number)

        return self.box_layout

    # Define a callback function that reverses the text in the text input widget
    def start_btn(self, instance):
        # Get the current text from the text input widget
        if self.button1.text == "Start" or self.button1.text == "Continue":
            self.button1.text = "Pause"
            self.running = True #start the game
        else:
            self.button1.text = "Continue"
            self.running = False #pause the game

    # Define a callback function that changes the color of the text in the text input widget
    def clear_btn(self, instance):
        self.running = False #stop the game
        self.button1.text = "Start"
        self.colony.clear_board() #Clear the board
        self.colony.reset_generation_number()
        self.update_generation_label(self.colony.generation_number)

    # Update the generation label   
    def update_generation_label(self, generation):
        self.label.text = "Generation: " + str(generation)

    # Define a callback function that updates the game board to the next generation on a timer
    def next_generation_update(self, dt):
        if self.running:
            self.colony.go_through_one_generation()
            self.update_generation_label(self.colony.generation_number)

    

# Define class Cell representing a single cell in the game board
class Cell():
    def __init__(self, cell_col, cell_row):        
        self.col = cell_col
        self.row = cell_row
        self.cell_id = "cell-" + str(self.row) + "-" + str(self.col)
        self.alive = False
        self.alive_next = False
        self.state_changed = False
    
    # Define a function that changes the state of the cell when it is clicked
    def on_touch_down(self):
        self.alive = not self.alive

# Define class Colony representing the entire game board    
class Colony():
    def __init__(self):
        # Set the number of columns and rows for the GridLayout
        self.cols = COLONY_NUMBER_OF_COLS
        self.rows = COLONY_NUMBER_OF_ROWS
        self.generation_number = 0
        self.cells = [] #create an empty list to hold the cells
        for i in range(self.cols):
            cells_row = [] #create an empty list to temporarily hold a row the cells
            for j in range(self.rows):
                cell = Cell(i,j)
                cells_row.append(cell)
            self.cells.append(cells_row)

    # Clear the board
    def clear_board(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.alive = False
                cell.alive_next = False
                cell.state_changed = False

    # For the provided cell position return the number of live neighbors within the 3x3 grid centered on the cell and including the cell
    def get_live_neighbors(self, cell_col, cell_row):
        live_neighbors = 0
        # calculate x and y index boundaries
        row_min = cell_row - 1 if cell_row > 0 else 0
        row_max = cell_row + 1 if cell_row < self.rows - 1 else self.rows - 1
        col_min = cell_col - 1 if cell_col > 0 else 0
        col_max = cell_col + 1 if cell_col < self.cols - 1 else self.cols - 1
        # count the number of live neighbors
        live_neighbors = sum([self.cells[col][row].alive for row in range(row_min, row_max+1) for col in range(col_min, col_max+1)])
        return live_neighbors
    
    # Calculate the next generation of cells
    #     1) Any live cell with two or three live neighbours survives.
    #     2) Any dead cell with three live neighbours becomes a live cell.
    #     3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    # Thus, if the sum of all nine fields in a given neighbourhood is three, the inner field state for the next generation will be life;
    # if the all-field sum is four, the inner field retains its current state; and every other sum sets the inner field to death.    
    def calculate_next_cell_generation(self):
        # cells_next = [] #create an empty lists to hold the generation cells        
        for i in range(self.cols):
            for j in range(self.rows):
                # calculate the number of live neighbors for the cell
                live_neighbors = self.get_live_neighbors(i, j)
                alive = self.cells[i][j].alive
                if live_neighbors == 3:
                    self.cells[i][j].alive_next = True
                elif live_neighbors == 4:
                    self.cells[i][j].alive_next = alive
                else: #live_neighbors < 3 or live_neighbors > 4
                    self.cells[i][j].alive_next = False
                # mark the cell for the grid update if the cell state changed
                self.cells[i][j].state_changed = self.cells[i][j].alive_next != self.cells[i][j].alive

    # Update the cells to the next generation
    def update_cells_to_next_generation(self):
        cell_ids = []  # list of cell IDs for the cell grid update
        cell_states = []  # list of cell states for the cell grid update       
        for i in range(self.cols):
            for j in range(self.rows):
                self.cells[i][j].alive = self.cells[i][j].alive_next
                sell_ids.append(self.cells[i][j].cell_id)
                cell_states.append(self.cells[i][j].alive)
        return cell_ids, cell_states

    # Go through one generation of cells
    def go_through_one_generation(self):
        self.calculate_next_cell_generation()
        cell_ids, cell_states = self.update_cells_to_next_generation()
        return cell_ids, cell_states

    # Reset generation number to 0
    def reset_generation_number(self):
        self.generation_number = 0
    
