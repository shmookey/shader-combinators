from game import *
from math import sin, cos, tan, pi

W, H = CANVAS_WIDTH, CANVAS_HEIGHT
PINCH_MIN, PINCH_MAX, PINCH_SPEED = -50, 50, 2.5

init_state = {
  "pos":   (0,0),
  "pinch": 0
}

colourmod = lambda x, y, t, st: (
  rangebounce(0,255,x),
  rangebounce(0,255,y),
  rangebounce(0,255,x*y)
) if st["pinch"] >= 0 else (
  rangebounce(0,255,x*sin(x)),
  rangebounce(0,255,y*cos(y)),
  rangebounce(0,255,x*y*tan(x*y))
)

scene = layers([
#  follow(point(0, 0, grey), "pos"),

  translate(
      pinch(
    mask(
        tile(
          compose(
            line(2, 0, 2, 5, 1, green),
            line(0, 2, 5, 2, 1, green)),
          5, 5),
      colourmod),
        "pinch"),
    W/2, H/2),


  rectangle(0, 0, W, H, black)
])

def rangebounce(lo, hi, x):
  span  = hi - lo
  cycle = 2 * span
  phase  = abs(x) % cycle
  return ((lo + phase) if phase < hi 
     else (lo + cycle - phase - 1))

def update(state, time_elapsed, events):
  seconds = time_elapsed / 1000

  for event in events:
    if event[0] == "mousemove": state["pos"] = event[1]

  pinch_range    = PINCH_MAX - PINCH_MIN
  pinch_cycle    = 2 * pinch_range
  pinch_phase    = (seconds * PINCH_SPEED) % pinch_cycle
  state["pinch"] = (PINCH_MIN + pinch_phase if pinch_phase < pinch_range 
               else PINCH_MIN + pinch_cycle - pinch_phase - 1)

run(scene, update, init_state)

