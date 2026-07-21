import pygame
import os
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TILE_SIZE = 64 
FRAMERATE = 60
BG_COLOR = '#fcdfcd'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XP_BASE = 100
PLAYER_MAX_HP = 100
PLAYER_ATTACK = 30
MOVE_SPEED = 400
BULLET_COOLDOWN = 1500

# Mapping compatibility dari Project 1
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT
COL_GOLD = (255, 210, 50)
COL_ACCENT = (0, 210, 200)

# State Game Konstanta
STATE_INTRO       = "intro"
# Menu & screens
STATE_MENU        = "menu"
STATE_PLAYING     = "playing"
STATE_BOSS        = "boss"
STATE_STAGE_CLEAR = "stage_clear"
STATE_SHOP        = "shop"
STATE_GAME_OVER   = "game_over"
STATE_WIN         = "win"
STATE_MAP         = "map"
STATE_DIALOGUE    = "dialogue"
