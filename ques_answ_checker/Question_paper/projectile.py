import turtle
import math
import time

# ========== 1. USER INPUT ==========
velocity = float(input("Enter the initial velocity (m/s): "))
angle_deg = float(input("Enter the launch angle (degrees): "))
angle_rad = math.radians(angle_deg)

# ========== 2. PHYSICS CONSTANTS ==========
g = 9.81  # acceleration due to gravity
v_x = velocity * math.cos(angle_rad)
v_y = velocity * math.sin(angle_rad)
t_flight = 2 * v_y / g

# ========== 3. SCALE SETUP ==========
scale = 10  # pixels per meter (adjust as needed)
screen_width = 800
screen_height = 600

# ========== 4. SETUP TURTLE SCREEN ==========
win = turtle.Screen()
win.setup(screen_width, screen_height)
win.title("Projectile Motion with Turtle")
win.setworldcoordinates(0, 0, screen_width, screen_height)
win.bgcolor("lightblue")

# Axes
axis = turtle.Turtle()
axis.penup()
axis.goto(0, 0)
axis.pendown()
axis.forward(screen_width)
axis.penup()
axis.goto(0, 0)
axis.setheading(90)
axis.pendown()
axis.forward(screen_height)
axis.hideturtle()

# ========== 5. SETUP TURTLE OBJECT FOR PROJECTILE ==========
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.pendown()

# ========== 6. SIMULATE MOTION ==========
t = 0
dt = 0.05  # time step (smaller = smoother animation)

while True:
    x = v_x * t
    y = v_y * t - 0.5 * g * t**2

    if y < 0:
        break  # Stop if projectile hits the ground

    ball.goto(x * scale, y * scale)
    time.sleep(dt)
    t += dt

# Finish
ball.hideturtle()
turtle.done()
