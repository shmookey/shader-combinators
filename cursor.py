import game
from game import white, black, red, grey
WIDTH = game.CANVAS_WIDTH
HEIGHT = game.CANVAS_HEIGHT

# Mouse events demo
# Shows a block 'cursor' which follows the mouse
# And a red 'marker' which highlights the last pixel clicked

init_state = {
  "marker_position": None,  # Usually, a tuple containing (x,y) coordinates
  "cursor_position": None   # Setting them to `None` hides the cursor/marker
}

def app():
  # Create the marker
  red_dot = game.point(0, 0, red)
  marker = game.follow(red_dot, "marker_position")

  # Create the cursor
  black_dot  = game.follow(game.point(0, 0, black), "cursor_position")
  horiz_line = game.follow(game.line(0, 0, WIDTH, 0, 1, grey), "cursor_position", axis='y', force_tuple=True)
  vert_line  = game.follow(game.line(0, 0, 0, HEIGHT, 1, grey), "cursor_position", axis='x', force_tuple=True)
  crosshair  = game.compose(horiz_line, vert_line)
  cursor     = game.compose(black_dot, crosshair)

  # Build the scene
  scene = game.compose(marker, cursor)

  # Run the app
  game.run(scene, update, init_state)


def update(state, time_elapsed, events):
  # `events` is a (possibly empty) list of tuples.
  # each tuple contains two values.
  # the first is a string identifying the type of the event e.g. "click".
  # for mouse events, the second value is a tuple (x,y) of the coordinates
  for event in events:
    if event[0] == "click":
      coords = event[1]
      state["marker_position"] = coords
    elif event[0] == "mousemove":
      coords = event[1]
      state["cursor_position"] = coords
      
app()
