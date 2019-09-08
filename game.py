import random, sys, pygame, traceback
from math import sqrt
from functools import reduce


#
# CONSTANTS
#

WINDOW_SIZE   = (512, 512)
CANVAS_HEIGHT = 32
CANVAS_WIDTH  = 32
MAX_FPS       = 60


#
#  COLOURS
#

black      = (0,0,0)
white      = (255,255,255)
red        = (255,0,0)
grey       = (196,196,196)
brown      = (165,42,42)
dark_brown = (101,67,33)
green      = (0,255,0)
yellow     = (255,255,153)
blue       = (0,0,255)
sky_blue   = (135,206,235)


#
#  DRAWING PRIMITIVES
#

def rectangle(left, top, width, height, colour):
  right = left + width
  bottom = top + height
  def shader(x, y, t, st):
    if x >= left and x < right and y >= top and y < bottom: return colour
    else: return white
  return shader

def point(left, top, colour):
  return lambda x, y, t, st: colour if x==left and y==top else white

def circle(left, top, radius, colour):
  def shader(x, y, t, st):
    dx = abs(x - left)
    dy = abs(y - top)
    dist = sqrt(dx**2 + dy**2)
    if dist < radius: return colour
    else: return white
  return shader

def line(x1, y1, x2, y2, thickness, colour):
  """Draw a line from (X1,Y1) to (X2,Y2) with given thickness and colour."""

  # Helper variables for bounds checking
  span = x2 - x1
  rise = y2 - y1 
  sgnX = sign(span)
  sgnY = sign(rise)

  # Handle vertical lines specially to avoid divide-by-zero errors
  if span == 0: 
    def shader(x, y, t, st):
      dx = (x - x1) * sgnX
      dy = (y - y1) * sgnY
      if dx <= thickness and dy <= abs(rise): return colour
      else: return white
    return shader
 
  m = rise / span
  def shader(x, y, t, st):
    dx = x - x1
    if dx < (0-thickness) or dx > (x2+thickness): return white
    ry = y1 + (dx * m)
    if abs(y-ry) < thickness: return colour
    else: return white

  return shader


#
#  SHADER COMBINATORS
#

def compose(a, b):
   """Create a composite shader by layering one shader "on top" of another.

   Takes two shaders as arguments, `a` and `b`. For each pixel, try using `a`
   first. If `a` returns white for that pixel, use the result from `b` instead.
   """
   def shader(x, y, t, st):
     colour_a = a(x, y, t, st)
     colour_b = b(x, y, t, st)
     return colour_a if colour_a != white else colour_b

   return shader

def layers(xs):
  """Compose a list of shaders such that the first is on top."""
  return reduce(lambda acc, x: compose(acc, x), xs)

def translate(shader, x_offset, y_offset):
  """Shift the output of a shader by an offset."""
  return lambda x,y,t: shader(x-x_offset, y-y_offset, t)


#
# APP LAUNCHER
#

def run(shader, update, state):
  """Run an app safely and clean up after exit."""

  try:
    start_app(shader, update, state)
  except:
    traceback.print_exc()
    pygame.quit()

def start_app(shader, update, state):
  """Start an app. Do not use this directly, call `run` instead."""

  # Initialize pygame, create surfaces and pixel array
  pygame.init()
  window       = pygame.display.set_mode(WINDOW_SIZE)
  canvas       = pygame.Surface((CANVAS_WIDTH,CANVAS_HEIGHT))
  frame        = pygame.Surface(WINDOW_SIZE)
  parray       = pygame.PixelArray(canvas)

  # Initialize timers and frame counter
  start_time   = pygame.time.get_ticks()   # Time at program start
  frame_number = 0                         # Current frame
  fps          = 0                         # Average frames per second
  min_frame_t  = 1000 / MAX_FPS            # Minimum milliseconds per frame
  fps_update_t = start_time                # Time of last FPS update

  # Main loop
  while 1:

    # Update timers
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - start_time

    # Process input
    events = []
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          return
        elif event.key == pygame.K_i:
          print(f"FPS: {fps}")


    update(state, time_elapsed, events)

    # Draw frame
    for x in range(CANVAS_WIDTH):
      for y in range(CANVAS_HEIGHT):
        parray[x][y] = shader(x, y, time_elapsed, state)

    pygame.transform.scale(canvas, WINDOW_SIZE, frame)

    # Refresh display
    window.fill((0,0,0))
    window.blit(frame, (0,0))
    pygame.display.flip()

    # Count frames
    frame_number += 1
    if frame_number % 100 == 0:
       period_duration = (current_time - fps_update_t) / 1000
       fps = 100 / period_duration
       fps_update_t = current_time


    # Wait until the minimum frame time has elapsed
    frame_time = pygame.time.get_ticks() - current_time
    if frame_time < min_frame_t:
      pygame.time.delay(int(min_frame_t - frame_time))


#
#  HELPER FUNCTIONS
#

sign = lambda n: 0 if n==0 else (1 if n > 0 else -1)


#
#  TESTS
#

test1 = lambda x, y, t, st: (0,0,0) if x==y or (CANVAS_WIDTH-x)==y else (255,255,255)
test2 = lambda x, y, t, st: (x*SIZE%255, y*CANVAS_HEIGHT%255, (t/50)%255)
def test3(x,y,t):
  tt = int(t/125) % 256
  mx, my = tt%CANVAS_WIDTH, int(tt/CANVAS_HEIGHT)
  return black if x==mx and y==my else white

test_array_good = [[white if x==y else black for y in range(CANVAS_HEIGHT)] for x in range(CANVAS_WIDTH)]
test_array_bad_1 = [[white if x==y else black for y in range(CANVAS_HEIGHT-1)] for x in range(CANVAS_WIDTH)]
test_array_bad_2 = [[white if x==y else black for y in range(CANVAS_HEIGHT)] for x in range(CANVAS_WIDTH-1)]
test_array_bad_3 = []

def test_primitives():
  return layers([
    point(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, red),
    line(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 1, black),
    circle(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, int(0.9*(CANVAS_WIDTH/2)), sky_blue),
    rectangle(1, 1, CANVAS_WIDTH-2, CANVAS_HEIGHT-2, blue)
  ])


#
#  ENTRY POINT
#

def main():
  state  = {}
  shader = test_primitives()

  

  def update(state, time_elapsed, events):
    return state
  
  run(shader, update, state)

if __name__ == "__main__":
  main()
