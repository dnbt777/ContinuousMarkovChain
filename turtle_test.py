from CMC.ContinuousMarkovChain import ContinuousMarkovChain

import math
import turtle
import random

def generate_circle_points(num_points, radius):
    return [(radius * math.cos(2 * math.pi * i / num_points), radius * math.sin(2 * math.pi * i / num_points)) for i in range(num_points)]

def turtle_test():
    num_points = 100
    radius = 100
    sequence = generate_circle_points(num_points, radius)

    # Set up turtle
    turtle.speed(0)
    turtle.hideturtle()
    turtle.color("black")

    # Draw the sequence
    turtle.penup()
    turtle.goto(sequence[0])
    turtle.pendown()
    for point in sequence[1:]:
        turtle.goto(point)
    turtle.penup()

    # Create Markov chain
    cmc = ContinuousMarkovChain(sequence)

    # Pick a random start state
    start_state = random.choice(sequence)
    turtle.goto(start_state)
    turtle.pendown()
    turtle.color("red")

    # Move according to Markov chain
    current_state = start_state
    for _ in range(500):
        next_state = cmc.get_next_state(current_state)
        if next_state is None:
            break
        print(next_state)
        turtle.goto(next_state)
        current_state = next_state

    turtle.done()

if __name__ == "__main__":
    turtle_test()