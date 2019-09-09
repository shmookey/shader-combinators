from game import *
from math import pi

W = CANVAS_WIDTH
H = CANVAS_HEIGHT

def test_primitives():
  return layers([
    point(W/2, H/2, red),
    line(0, 0, W, H, 1, black),
    translate(
      rotate(line(-W/4, 0, W/4, 0, 1, green), pi/4)
      , W/2, H/2
    ),
    circle(W/2, H/2, int(0.9*(W/2)), sky_blue),
    rectangle(1, 1, W-2, H-2, blue)
  ])

def main():
  state  = {}
  shader = test_primitives()
  def update(state, time_elapsed, events):
    pass
  run(shader, update, state)

if __name__ == "__main__":
  main()
   
   
   
   
   
   
