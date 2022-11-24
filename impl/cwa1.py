#!/usr/bin/env python3
# Consume api via python

import requests
import json

import asyncio

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm, speed_mmps

text = "hello"
def cozmo_speak(robot:cozmo.robot.Robot):
    robot.say_text(text = text, voice_pitch=0, duration_scalar=0.7).wait_for_completed()

# Get ingredients
indegredientsUrl = "https://www.thecocktaildb.com/api/json/v2/9973533/list.php?i=list"
response = requests.request("GET", indegredientsUrl)

# create array of ingredients
ingredients = []
for ing in response.json()['drinks']:
    ingredients.append(ing['strIngredient1'])
for i in range(len(ingredients)):
    print("{} {}".format(i + 1, ingredients[i]), end="\n")


# prompt user to pick ingredient and get available drinks
cocktailUrl = "https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?i="
text = "hello"
cozmo_speak
ingredientIndex = int(input("\nEnter an ingredient -> Choose number: ")) - 1
cocktailUrl += ingredients[ingredientIndex]
response = requests.request("GET", cocktailUrl).json()['drinks']

# clear the screen
print("\033c")


drinks = []
if(response == "None Found"):
    response = []

for drink in response:
    drinks.append(drink['strDrink'])
print("Drinks containing {}:\n".format(ingredients[ingredientIndex]))   

for i in range(len(drinks)):
    print("{} {}".format(i + 1, drinks[i]), end="\n")

if(drinks == []):
    print("\nNo drinks found")
else:
    # prompt user to pick drink
    chosen_drink = drinks[int(input("\nEnter a drink -> Choose number: ")) - 1]
   
    # print("\033c")
    print("\n")

    # Divide drinks into groups of arrays for assigning to cubes
    def divide_chunks(l, n):
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]

    drinksGroups = []
    if(len(drinks) > 3):
        drinksGroups = list(divide_chunks(drinks, len(drinks)//3))
    else:
        for i in range(len(drinks)):
            drinksGroups.append([drinks[i]])


    # assign each group to a cube
    cubeDictioanry = {
        1: "PaperClip Cube",
        2: "Lamp / Heart Cube",
        3: "ab over T Cube"
    }

    for i in range(len(drinksGroups)):
        try:
            print("Group {} - {}".format(i + 1, cubeDictioanry[i + 1]))
        except:
            print("Group {} - {}".format(i + 1, cubeDictioanry[3]))

        g = drinksGroups[i]
        g.sort()
        for drink in g:
            print(drink, end=", ")
        print("\n")

    if(chosen_drink in drinksGroups[0]):
        print("\n\nYou chose {} which is in group 1: Cozmo should bring back the cube that looks like a paperclip - {}\n".format(chosen_drink, LightCube1Id)) 
        cubeId = LightCube1Id # looks like a paperclip - LightCube1ID
    elif(chosen_drink in drinksGroups[1]):
        print("\n\nYou chose {} which is in group 2: Cozmo should bring back the cube that looks like a lamp / heart - {}\n".format(chosen_drink, LightCube2Id)) 
        cubeId = LightCube2Id # looks like a lamp / heart - LightCube2ID
    else:
        print("\n\nYou chose {} which is in group 3 onwards : Cozmo should bring back the cube that looks like the letters 'ab' over 'T' - {}\n".format(chosen_drink, LightCube3Id)) 
        cubeId = LightCube3Id # looks like the letters 'ab' over 'T' - LightCube3ID




def go_get_drink(robot: cozmo.robot.Robot):
    # will try to implement this later
    # look around and try to find a cube
    # look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    # Turn 180 degrees
    robot.turn_in_place(degrees(180)).wait_for_completed()

    cube = None

    try:
        # cube = robot.world.wait_for_observed_light_cube(timeout=30)
        print("Looking for cube - {}".format(cubeId))
        cube = robot.world.get_light_cube(cubeId)

        print("Found cube: %s" % cube)
    except asyncio.TimeoutError:
        print("Didn't find a cube")
    # finally:
        # whether we find it or not, we want to stop the behavior
        # look_around.stop()

    if cube:
        current_action = robot.pickup_object(cube, num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            code, reason = current_action.failure_reason
            result = current_action.result
            print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
            return

        # Turn 180 degrees
        robot.turn_in_place(degrees(180)).wait_for_completed()

        robot.drive_straight(distance_mm(300), speed_mmps(50)).wait_for_completed()    


async def connect_to_cubes(robot: cozmo.robot.Robot):
    await robot.world.connect_to_cubes()


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(connect_to_cubes)
cozmo.run_program(go_get_drink)

