# Project is based on Tech With Tim - Python Sorting Algorithm Visualizer Tutorial
import pygame
import random
import math
pygame.init()

class drawInformation:
    # Initializing variables
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    LIGTH_GRAY = 128, 128, 128
    GRAY = 160, 160, 160
    DARK_GRAY = 192, 192, 192
    BACKGROUND_COLOR = WHITE

    # GRAY COLORS
    GRADIENTS = [
        LIGTH_GRAY,
        GRAY,
        DARK_GRAY
    ]

    # Font
    FONT = pygame.font.SysFont('comicsans', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # For total drawable areas
    SIDE_PAD = 100
    TOP_PAD = 150

    '''
    Initialise window
    self
    width = width of window
    height = height of window
    lst = list of elemets
    '''
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting ALgorithm Visualization")
        self.set_list(lst)

    '''
    self
    lst = list of elements
    '''
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # Calculating width of bars in visualization
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) # Total area / number of items in list
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2 # Start at an indent on the bottom of the window

'''
draw_info = contains information about initial draw values
'''
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Use font to render text and draw it in the window
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5)) # for x = screen width / 2 - text width / 2

    # Use font to render text and draw it in the window
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sort | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45)) # for x = screen width / 2 - text width / 2

    # draw sorting algorithms instructions
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75)) # for x = screen width / 2 - text width / 2

    # Draw list
    draw_list(draw_info)
    pygame.display.update()


'''
draw_info = contains information about initial draw values
color_position = set of positions of the colours
clear_bg = to overwrite the portion of the screen
'''
def draw_list(draw_info, color_position={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        # generate rectangle
        clear_rect = (
            draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        # Drawing at xth position
        x = draw_info.start_x + i * draw_info.block_width
        # Calculating y val (height)
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_position:
            color = color_position[i]

        # Draw onto the screen
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    # Update if clear_bg is True
    if clear_bg:
        pygame.display.update()

'''
n = number of elements in starting list
min_val = minimum possible value 
max_val maximum possible value
'''
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val) # Range of random values
        lst.append(val)
    
    return lst

'''
draw_info = contains information about initial draw values
ascending = True --> Sorting order
'''
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # If ascending and descending sort list
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                # Swapping without temp variable
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                # Stop function and resume it (allows to use other controls ('r',...) during sorting)
                yield True
    
    return lst

'''
draw_info = contains information about initial draw values
ascending = True --> Sorting order
'''
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            # Different conditions for way of sort
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            # Everytime swap is done, pause (yield)
            yield True

    return lst

'''
draw_info = contains information about initial draw values
ascending = True --> Sorting order
'''
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    n = len(lst)

    for i in range(n - 1):
        min_idx = i

        for j in range(i + 1, n):

            condition = (lst[j] < lst[min_idx]) if ascending else (lst[j] > lst[min_idx])

            if condition:
                min_idx = j
            
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            # Everytime swap is done, pause (yield)
            yield True

    return lst

'''
main function
'''
def main():
    run = True
    # regulate how quick loop runs
    clock = pygame.time.Clock()

    n = 25
    min_val = 0
    max_val = 100

    # Initialise screen
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = drawInformation(800, 600, lst)

    # Variables
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        # Setting up pygame event-loop (speed)
        clock.tick(60)

        # If sorting
        if sorting:
            try:
                # try to do next step of generator
                next(sorting_algorithm_generator)
            except StopIteration:
                # when its done stop sorting
                sorting = False
        # Otherwise call draw function
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # Render display
        pygame.display.update()

        # All events that occoured since last call
        for event in pygame.event.get():
            # Once the X is pressed, pygame is quit
            if event.type == pygame.QUIT:
                run = False

            # Implement key press events
            if event.type != pygame.KEYDOWN:
                continue

            # If pressing 'r' reset list
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            # If pressing 'space', start sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                # Store generator (yield function) object when we call sort function
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            # ascending order on 'a' press
            elif event.key == pygame.K_a and not sorting:
                ascending = True

            # descending order on 'd' press
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            # Insertion sort on 'i' press
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            # Bubble sort on 'b' press
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            # Selection sort on 's' press
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
    
    # Close of display
    pygame.quit()

# Call main function
if __name__ == "__main__":
    main()