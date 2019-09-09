from game import *

def test_primitives():
  return layers([
    point(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, red),
    line(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 1, black),
    circle(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, int(0.9*(CANVAS_WIDTH/2)), sky_blue),
    rectangle(1, 1, CANVAS_WIDTH-2, CANVAS_HEIGHT-2, blue)
  ])

def main():
  state  = {}
  shader = test_primitives()
  def update(state, time_elapsed, events):
    pass
  run(shader, update, state)

if __name__ == "__main__":
  main()
   
   
   
   
   
   
