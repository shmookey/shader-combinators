import game
from random import random

WIDTH    = game.CANVAS_WIDTH
HEIGHT   = game.CANVAS_HEIGHT

speed    = 1  # maximum move distance per frame

black    = (0,0,0)
white    = (255,255,255)
sky_blue = (135,206,235)


def run_app():
  """Initialize and start the app."""

  # Create shader for scene
  background = game.rectangle(0, 0, WIDTH, HEIGHT, sky_blue)
  scene      = game.compose(bug, background)

  # Initial position of the bug
  init_state = {
    "x": WIDTH/2,   # note: these coordinates will not necessarily be whole numbers
    "y": HEIGHT/2
  }

  # Let's go!
  game.run(scene, update, init_state)


def bug(x, y, t, st):
  """Draw the bug at its current location."""

  current_x = int(st["x"])
  current_y = int(st["y"])
  if x == current_x and y == current_y:
    return black
  else:
    return white

def update(state, time_elapsed, events):
  """Update the position of the bug."""

  current_x  = state["x"]
  current_y  = state["y"]
  movement_x = random()*speed*2 - speed
  movement_y = random()*speed*2 - speed
  new_x      = current_x + movement_x
  new_y      = current_y + movement_y
  state["x"] = max(0, min(WIDTH - 1, new_x))
  state["y"] = max(0, min(HEIGHT - 1, new_y))


run_app()
