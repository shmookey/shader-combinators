import game
from game import compose, line, translate, follow, tile, rotate, layers, point
from game import black, white, blue, red, yellow, green, sky_blue, brown, dark_brown
from math import sqrt, pi, sin, cos, atan2
from random import random, randint
import math

RPM          = 6
SCENE_RPM    = 3
SCENE_ROT_CHANGE_CHANCE = 0.2
ACCEL_DECAY  = 0.035     # Lose this much velocity per second per second
ACCEL_CHANCE = 0.25    # 1-second probabilty of an acceleration bump occuring
ACCEL_BUMP   = 0.1     # How much to bump acceleration by
DRAG         = 0.3     # % velocity reduction per second

init_state = {
  "rot": 0,
  "scene_rot": 0,
  "scene_rot_cw": True,
  "drift_displacement": (0, 0),
  "drift_velocity": (0, 0),
  "drift_acceleration": (0, 0),
  "last_frame": 0
}

def app():
  shape = translate(
            rotate(
              layers([
                line(-6, 0, 12, 0, 1, blue),
                line(0, -6, 0, 12, 1, blue)
              ]),
              "rot"
            ),
            6, 6)
  scene = rotate(
            follow(
              tile(shape, 12, 12),
              "drift_displacement"
            ),
            "scene_rot")

  game.run(compose(scene,background), update, init_state)

def background(x,y,t,st):
  tt = t/60
  p = tt % 512
  pp = p if p < 256 else 512-p
  return (pp,pp,255)

def update(state, time_elapsed, events):
  frame_time   = time_elapsed - state["last_frame"]
  frame_time_s = frame_time / 1000 
  mins         = time_elapsed / 1000 / 60

  # increment the inner rotation
  turns = mins * RPM
  state["rot"] = turns * pi * 2

  # increment the scene rotation
  scene_rot_dir = 1 if state["scene_rot_cw"] else -1
  turn_amt = (frame_time_s / 60) * SCENE_RPM * scene_rot_dir * pi * 2
  state["scene_rot"] += turn_amt

  # roll the dice for a scene rotation direction change
  p_changedir = frame_time_s * SCENE_ROT_CHANGE_CHANCE
  if random() <= p_changedir:
    state["scene_rot_cw"] = not state["scene_rot_cw"]

  # roll the dice for an acceleration bump
  cur_accel = state["drift_acceleration"]
  p_bump = frame_time_s * ACCEL_CHANCE
  if random() <= p_bump:
    direction = random() * 2 * pi
    new_accel = (cur_accel[0] + cos(direction)*ACCEL_BUMP, cur_accel[1] + sin(direction)*ACCEL_BUMP)
    state["drift_acceleration"] = new_accel

  # apply acceleration
  cur_accel = state["drift_acceleration"]
  cur_veloc = state["drift_velocity"]
  new_veloc = (cur_veloc[0] + cur_accel[0], cur_veloc[1] + cur_accel[1])
  state["drift_velocity"] = new_veloc
  
  # apply velocity
  cur_displ = state["drift_displacement"]
  cur_veloc = state["drift_velocity"]
  new_displ = (cur_displ[0] + cur_veloc[0], cur_displ[1] + cur_veloc[1])
  state["drift_displacement"] = new_displ

  # apply drag
  drag      = 1 - (DRAG * frame_time_s)
  speed     = sqrt(cur_veloc[0]**2 + cur_veloc[1]**2)
  veloc_dir = atan2(cur_veloc[1], cur_veloc[0])
  new_speed = speed * drag
  new_veloc = (cos(veloc_dir) * new_speed, sin(veloc_dir) * new_speed)
  state["drift_velocity"] = new_veloc

  # decay acceleration
  decay     = ACCEL_DECAY * frame_time_s
  accel_amt = sqrt(cur_accel[0]**2 + cur_accel[1]**2)
  accel_dir = atan2(cur_accel[1], cur_accel[0])
  new_magnt = diminish(accel_amt, decay)
  new_accel = (cos(accel_dir) * new_magnt, sin(accel_dir) * new_magnt)
  state["drift_acceleration"] = new_accel

  state["last_frame"] = time_elapsed

def diminish(n,amt):
  sgn = sign(n)
  lim = max if sgn==1 else min
  return lim(0, n - sgn*amt)
  

sign = lambda n: -1 if n<0 else 0 if n==0 else 1
app()

