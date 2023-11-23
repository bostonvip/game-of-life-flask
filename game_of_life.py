#Definitions
GENERATION_UPDATE_INTERVAL = 0.5 # in seconds

# Classic Game of Life
# The rules, which compare the behaviour of the automaton to real life, can be condensed into the following:
#     1) Any live cell with two or three live neighbours survives.
#     2) Any dead cell with three live neighbours becomes a live cell.
#     3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.


# # Define a callback function that updates the game board to the next generation on a timer
# def next_generation_update(self, dt):
#     if self.running:
#         self.colony.go_through_one_generation()
#         self.update_generation_label(self.colony.generation_number)

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
    def __init__(self, cols, rows):
        # Set the number of columns and rows for the GridLayout
        self.cols = cols
        self.rows = rows
        self.generation_number = 0
        self.cells = [] #create an empty list to hold the cells
        for i in range(self.cols):
            cells_row = [] #create an empty list to temporarily hold a row the cells
            for j in range(self.rows):
                cell = Cell(i,j)
                cells_row.append(cell)
            self.cells.append(cells_row)

    # Set the state of the cell at the provided row and column
    def set_cell_state(self, cell_col, cell_row, alive):
        self.cells[cell_col][cell_row].alive = alive

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
    
