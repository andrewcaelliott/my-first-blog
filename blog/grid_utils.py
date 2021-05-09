#import math
#import random
import cairo
#from .utils import num
#import re
#import collections
#from django.utils.datastructures import MultiValueDictKeyError
#from fractions import Fraction

default_palette = {
        'features':[
            (1.0, 0.6, 0.2, 1.0),  #Orange
            (0.6, 0.2, 1.0, 1.0),  
            (0.2, 1.0, 0.6, 1.0),  
            (0.2, 0.8, 0.8, 1.0),  
            (0.8, 0.8, 0.2, 1.0),  
            (0.8, 0.2, 0.8, 1.0),  
        ],
        'background': (0.15, 0.45, 0.075, 1.0), #Dark Green
        'canvas': (0.0, 0.0, 0.0, 1.0), #Black
        }
print_palette = {
        'features':[
            (0.75, 0.25, 0.0, 1.0), # Brick Red
            (0.25, 0.0, 0.75, 1.0), # Blue
            (0.0, 0.66, 0.15, 1.0), # Green
            (0.5, 0.5, 0.0, 1.0), #
            (0.5, 0.0, 0.5, 1.0), #
            (0.0, 0.5, 0.5, 1.0), #
            ],
        'background': (0.72, 0.9, 0.64, 1.0), #Green
        #72,125,24,
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }
monochrome_palette = {
        'features':[
        (0.2, 0.2, 0.2, 1.0), #Dark Grey
        (0.6, 0.6, 0.6, 1.0), 
        (0.4, 0.4, 0.4, 1.0), 
        (0.7, 0.7, 0.7, 1.0), 
        (0.3, 0.3, 0.3, 1.0), 
        (0.5, 0.5, 0.5, 1.0), 
        ],
        'background': (0.9, 0.9, 0.9, 1.0), #Light Grey
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }
print2_palette = {
        'features':[
        (0.7, 0.0, 0.0, 1.0),  # Red
        (0.0, 0.5, 0.0, 1.0),  # Green
        (0.0, 0.0, 0.7, 1.0),  # Blue
        (0.95, 0.7, 0.7, 1.0),  # Pale Red
        (0.65, 0.9, 0.65, 1.0),  # Pale Green 
        (0.7, 0.8, 1.0, 1.0),  # Pale Blue
        ],
        'background': (0.85, 0.85, 0.85, 1.0), #Light Grey
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }

print3_palette = {
        'features':[
        (0.7, 0.0, 0.0, 1.0),  # Red
        (0.0, 0.5, 0.0, 1.0),  # Green
        (0.0, 0.0, 0.7, 1.0),  # Blue
        (0.0, 0.3, 0.3, 1.0),  # Turquoise
        (0.95, 0.7, 0.7, 1.0),  # Pale Red
        (0.65, 0.9, 0.65, 1.0),  # Pale Green 
        (0.7, 0.8, 1.0, 1.0),  # Pale Blue
        (0.65, 0.85, 0.85, 1.0),  # Pale Turquoise
        ],
        'background': (0.85, 0.85, 0.85, 1.0), #Light Grey
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }

screen_palette = {
        'features':[
        (0.8, 0.0, 0.0, 1.0),  # Red - true positives
        (0.0, 0.5, 0.0, 1.0),  # Green - false positives
        (0.8, 0.5, 0.5, 1.0),  # Pale Red - false negatives
        (0.6, 0.7, 0.6, 1.0),  # Pale Green - true negatives
        ],
        'background': (0.6, 0.7, 0.6, 1.0), # Pale Green
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }

print4_palette = {
        'features':[
        (0.7, 0.0, 0.0, 1.0),  # Red
        (0.0, 0.4, 0.0, 1.0),  # Green
        (0.0, 0.0, 0.7, 1.0),  # Blue
        (0.3, 0.0, 0.3, 1.0),  # Magenta
        (0.0, 0.4, 0.4, 1.0),  # Turquoise
        (0.3, 0.3, 0.0, 1.0),  # Olive
        (0.2, 0.2, 0.2, 1.0),  # Dark Grey
        (0.65, 0.85, 0.85, 1.0),  
        ],
        'background': (0.85, 0.85, 0.85, 1.0), #Light Grey
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }

red_grad_palette = {
        'features':[
        (0.3, 0.0, 0.0, 1.0),  # Dark Red
        (0.7, 0.0, 0.0, 1.0),  # Red
        (0.78, 0.23, 0.23, 1.0),  # 
        (0.86, 0.46, 0.46, 1.0),  # 
        (0.94, 0.69, 0.69, 1.0),  # Pale Red
        ],
        'background': (0.85, 0.85, 0.85, 1.0), #Light Grey
        'canvas': (1.0, 1.0, 1.0, 1.0), #White
    }

palettes = {
    'default': default_palette,
    'print': print_palette,
    'print2': print2_palette,
    'print3': print3_palette,
    'print4': print4_palette,
    'red_grad': red_grad_palette,
    'mono': monochrome_palette,
    'screen': screen_palette
}

def get_palette(palette_name):
    return palettes.get(palette_name,default_palette)

def square(ctx, square_size, squash, offset_x, offset_y, fillcolour, gridcolour):

    ctx.move_to(offset_x+0, offset_y / squash +0)
    ctx.line_to(offset_x+square_size, offset_y / squash+0)  # Line to (x,y)
    ctx.line_to(offset_x+square_size, offset_y / squash+square_size / squash)  # Line to (x,y)
    ctx.line_to(offset_x+0, offset_y / squash + square_size / squash)  # Line to (x,y)
    ctx.line_to(offset_x+0, offset_y / squash+0)
    ctx.close_path()

    ctx.set_source_rgba(gridcolour[0], gridcolour[1], gridcolour[2], gridcolour[3] ) 
    ctx.set_line_width(min(square_size/20,0.002))
    ctx.stroke_preserve()
    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )
    ctx.fill()

def zoomlr(ctx, offset_x, offset_y, left_height, right_height, width, fillcolour, gridcolour, invert=False):
    ctx.move_to(offset_x+0, offset_y+right_height)
    ctx.line_to(offset_x+0, offset_y+right_height-left_height)  # Line to (x,y)
    ctx.line_to(offset_x+width, offset_y+0)  # Line to (x,y)
    ctx.line_to(offset_x+width, offset_y+right_height)  # Line to (x,y)
    ctx.line_to(offset_x+0, offset_y++right_height)
    ctx.close_path()

#    ctx.set_source_rgba(gridcolour[0], gridcolour[1], gridcolour[2], gridcolour[3] ) 
    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], 0.5 )  # Solid color
#    ctx.set_line_width(min(rect_width/20,0.002))
    ctx.stroke_preserve()
#    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
    ctx.fill()


def zoom(ctx, offset_x, offset_y, top_width, bottom_width, depth, fillcolour, gridcolour, invert=False):
    if not invert:
        ctx.move_to(offset_x+0, offset_y+0)
        ctx.line_to(top_width, offset_y+0)  # Line to (x,y)
        ctx.line_to(offset_x+bottom_width, offset_y+depth)  # Line to (x,y)
        ctx.line_to(offset_x+0, offset_y+depth)  # Line to (x,y)
        ctx.line_to(offset_x+0, offset_y+0)
        ctx.close_path()

    #    ctx.set_source_rgba(gridcolour[0], gridcolour[1], gridcolour[2], gridcolour[3] ) 
        ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
    #    ctx.set_line_width(min(rect_width/20,0.002))
        ctx.stroke_preserve()
    #    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
        ctx.fill()
    else:
        ctx.move_to(offset_x+0.8, offset_y+depth)
        ctx.line_to(offset_x+0.8 + top_width, offset_y+depth)  
        ctx.line_to(offset_x+0.8 + top_width, offset_y)  # Line to (x,y)
        ctx.line_to(offset_x+0.8 + top_width-bottom_width, offset_y)  # Line to (x,y)
        ctx.line_to(offset_x+0.8, offset_y+depth)
        ctx.close_path()

    #    ctx.set_source_rgba(gridcolour[0], gridcolour[1], gridcolour[2], gridcolour[3] ) 
        ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
    #    ctx.set_line_width(min(rect_width/20,0.002))
        ctx.stroke_preserve()
    #    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
        ctx.fill()


def rect(ctx, rect_width, rect_depth, offset_x, offset_y, range_y, fillcolour, gridcolour):
    ctx.move_to(offset_x+0, offset_y+0)
    ctx.line_to(offset_x+rect_width, offset_y+0)  # Line to (x,y)
    ctx.line_to(offset_x+rect_width, offset_y+rect_depth)  # Line to (x,y)
    ctx.line_to(offset_x+0, offset_y+rect_depth)  # Line to (x,y)
    ctx.line_to(offset_x+0, offset_y+0)
    ctx.close_path()

    ctx.set_source_rgba(gridcolour[0], gridcolour[1], gridcolour[2], gridcolour[3] ) 
    ctx.set_line_width(min(rect_width/20,0.002))
    ctx.stroke_preserve()
    ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
    ctx.fill()


def count_cell(ctx, offset_x, offset_y, offset_frame, gridcell_x, gridcell_y, range_y, hits, exposed, count, invert=False, palette=default_palette, pale=False, colour=0):
    if invert:
        if (count < (exposed-hits)):
            fillcolour = palette['background']
        elif (count < exposed):
            if pale:
                fillcolour = palette['features'][3]
            else:
                fillcolour = palette['features'][colour]
        else:
            fillcolour = palette['canvas']
    else:
        if (count < hits):
            if pale:
                fillcolour = palette['features'][3]
            else:
                fillcolour = palette['features'][colour]
        elif (count < exposed):
            fillcolour = palette['background']
        else:
            fillcolour = palette['canvas']
    if count < exposed:
        #print(offset_x*gridcell_x, offset_y*gridcell_y)
        rect(ctx, gridcell_x, gridcell_y, offset_x*gridcell_x+offset_frame, offset_y*gridcell_y, range_y, fillcolour, palette['canvas'])

def grid_legend(ctx, hit_type, palette=default_palette):
    cell_width = 1.0
    cell_height = 1.0
    if hit_type == -1:
        fillcolour = palette['background']
    else:
        fillcolour = palette['features'][hit_type]            
    rect(ctx, cell_width, cell_height, 0, 0, 1, fillcolour, palette['canvas'])

def count_grid(ctx, range_x, range_y, aspect, hits, exposed, palette=default_palette, xy=False, invert=False, offset_frame=0, pale=False, colour=0):
    square_size = aspect * 0.09 / range_x
    gridcell_x = aspect * 0.09 / range_x
    gridcell_y = (0.09 ) / range_y
    count = 0
    if xy:
        for offset_x in range(0,range_x):
            for offset_y in range(0,range_y):
                count_cell(ctx, offset_x, offset_y, offset_frame, gridcell_x, gridcell_y, range_y, hits, exposed, count, palette=palette, invert=invert, pale=pale, colour=colour)
                count+=1
    else:
        for offset_y in range(0,range_y):
            for offset_x in range(0,range_x):
                count_cell(ctx, offset_x, offset_y, offset_frame, gridcell_x, gridcell_y, range_y, hits, exposed, count, palette=palette, invert=invert, pale=pale, colour=colour)
                count+=1

def draw_count_grid(range_x, range_y, hits, exposed, aspect=10, frame_aspect=10, palette=default_palette, xy=False, invert=False, stacked=0, colour=0):
    #stack_height = int(2000/aspect * 1.4)
    #WIDTH, HEIGHT = 2000, int(2000/aspect + stacked * stack_height)
    WIDTH, HEIGHT = 2000, int(2000/ frame_aspect)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, WIDTH)  # Normalizing the canvas
    ctx.translate(0.05, 0.005)  # Changing the current transformation matrix
    offset_frame = 0
    if invert:
        offset_frame = 16/100 * stacked
    count_grid(ctx, range_x, range_y, aspect, hits, exposed, palette=palette, offset_frame=offset_frame, xy=xy, invert=invert, colour=colour)
    for i in range(stacked):
        zoomlr(ctx, ( (i+1) * 320 - 139) / WIDTH, 0, 0.009, 0.09, 138/WIDTH, palette['background'], None, invert)
        if invert:
            offset_frame = 16/100 * i 
        else:
            offset_frame = 12.5/100 * (i+1) 
        count_grid(ctx, 10, 10, aspect, 1, 100, palette=palette, offset_frame=offset_frame, pale=True, invert=invert)
    return surface



def draw_count_gridx(range_x, range_y, hits, exposed, aspect = 10, palette=default_palette, xy=False, invert=False, stacked=0, colour=0):
    stack_height = int(2000/aspect * 1.4)
    WIDTH, HEIGHT = 2000, int(2000/aspect + stacked * stack_height)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, WIDTH)  # Normalizing the canvas
    ctx.translate(0.05, 0.005)  # Changing the current transformation matrix
    offset_frame = 0
    if invert:
        offset_frame = 12.5/100 * stacked
    count_grid(ctx, range_x, range_y, aspect, hits, exposed, palette=palette, offset_frame=offset_frame, xy=xy, invert=invert, colour=colour)
    for i in range(stacked):
        zoom(ctx, 0, ((i+1)* 252 -70) / WIDTH, 0.1, 0.01, 68/WIDTH, palette['background'], None, invert)
        if invert:
            offset_frame = 12/100 * i 
        else:
            offset_frame = 12.5/100 * (i+1) 
        count_grid(ctx, 100, 10, aspect, 1, 1000, palette=palette, offset_frame=offset_frame, pale=True, invert=invert)
    return surface

def cell_drawonly(ctx, cell_value, square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, palette=default_palette):
    if cell_value is None:
        fillcolour = palette["canvas"]
    elif cell_value == 0:
        fillcolour = palette["background"]
    else:
        fillcolour = palette['features'][cell_value-1]
    square(ctx, square_size, squash, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour, palette['canvas'])


def grid_drawonly(ctx, grid, range_x, range_y, palette=default_palette, xy=False, top_down= False):
    square_size = 0.9/range_x
    gridcell_x = 0.9/range_x
    gridcell_y = gridcell_x
    squash = 1.0 * range_y / range_x
    count = 0
    alive_x = [True] * range_x
    if xy:
        for offset_x in range(0,range_x):
            for offset_y in range(0,range_y):
                if top_down:
                    cell_y = offset_y
                else:
                    cell_y = (range_y-1)-offset_y
                cell_drawonly(ctx, grid[cell_y][offset_x], square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, palette=palette)
                count+=1
    else:
        for offset_y in range(0,range_y):
            for offset_x in range(0,range_x):
                if top_down:
                    cell_y = offset_y
                else:
                    cell_y = (range_y-1)-offset_y
                cell_drawonly(ctx, grid[cell_y][offset_x], square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, palette=palette)
                count+=1


def draw_chance_grid(grid, range_x, range_y, palette=default_palette, xy=False, top_down=False):
    WIDTH, HEIGHT = 1500, int(1500.0 * range_y / range_x)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
    ctx.translate(0.05, 0.005)  # Changing the current transformation matrix
    grid_drawonly(ctx, grid, range_x, range_y, palette=palette, xy=xy, top_down=top_down)
    return surface

def draw_grid_legend(hit_type, palette=default_palette):
    WIDTH, HEIGHT = 300, 20
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
    ctx.translate(0.05, 0.005)  # Changing the current transformation matrix
    grid_legend(ctx, hit_type-1, palette=palette)
    return surface
