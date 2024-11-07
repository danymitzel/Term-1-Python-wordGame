from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import random
from PIL import ImageTk, Image
import os
import pygame as pg

HEIGHT = 980
WIDTH = 843
geoString = str(WIDTH)+"x"+str(HEIGHT)

TITLE = "Word Game"

#lightmode
bg_color ="#f2f2f2"
correct_color ="#7593af"
close_color ="#a3b7ca"
wrong_color ="ffb380"
accent_color ="#dededd"
font_color ="black"

#darkmode
bg_color ="#616161"
correct_color ="#8dcac5"
close_color ="#6d5094"
wrong_color ="#612e5c"
accent_color ="#404040"
font_color ="white"