#!/usr/bin/env python3
# Consume api via python

import requests
import json

import asyncio

import cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.util import degrees, distance_mm

# Get the token
# url = "http://localhost:8000/api/token/"
# payload = {'username': 'admin', 'password': 'admin'}
# headers = {'Content-Type': 'application/json'}
# response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
# token = response.json()['access']

# Get the data
indegredientsUrl = "https://www.thecocktaildb.com/api/json/v2/9973533/list.php?i=list"
response = requests.request("GET", indegredientsUrl)

#create array of ingredients
ingredients = []
for ing in response.json()['drinks']:
    ingredients.append(ing['strIngredient1'])
for i in range(len(ingredients)):
    print("{} {}".format(i,ingredients[i]) , end="\n")


#prompt user to pick ingredient and append to cocktailUrl
cocktailUrl = "https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?i="
cocktailUrl += ingredients[int(input("Enter an ingredient -> Choose number: "))]
response = requests.request("GET", cocktailUrl).json()['drinks']

#clear the screen
print("\033c")

#parse json response
drinks = []

if(response == "None Found"):
    response = []

for drink in response:
    drinks.append(drink['strDrink'])
for i in range(len(drinks)):
    print("{} {}".format(i,drinks[i]) , end="\n")

    
if(drinks == []):
    print("No drinks found")
else:
    #prompt user to pick drink
    chosen_drink = drinks[int(input("Enter a drink -> Choose number: "))]
    #clear the screen
    print("\033c")

    #Divide drinks into 3 groups of arrays
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

    # print(drinksGroups)

    #assign each group to a cube
    cubeId = LightCube1Id
    for i in range(len(drinksGroups)):

        print(drinksGroups)


    for i in range(len(drinksGroups)):
        print("Group {}".format(i + 1))
        g = drinksGroups[i]
        g.sort()
        for drink in g:
            print(drink, end=", ")
        print("\n")


    if(chosen_drink in drinksGroups[0]):
        print("\n\nYou chose {} which is in group 1: Cozmo should bring back the cube that looks like a paperclip \n".format(chosen_drink)) 
        cubeId = LightCube1Id # looks like a paperclip
    elif(chosen_drink in drinksGroups[1]):
        print("\n\nYou chose {} which is in group 2: Cozmo should bring back the cube that looks like a lamp / heart\n".format(chosen_drink)) 
        cubeId = LightCube2Id # looks like a lamp / heart
    else:
        print("\n\nYou chose {} which is in group 3 onwards : Cozmo should bring back the cube that looks like the letters 'ab' over 'T'\n".format(chosen_drink)) 
        cubeId = LightCube3Id # looks like the letters 'ab' over 'T'


def go_to_object_test(robot: cozmo.robot.Robot):
    '''The core of the go to object test program'''

    # requiredCube = robot.world.get_light_cube(drinks["sundowner"])

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # look around and try to find a cube
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    cube = None

    try:
        # cube = robot.world.wait_for_observed_light_cube(timeout=30)
        cube = robot.world.get_light_cube(cubeId)

        print("Found cube: %s" % cube)
    except asyncio.TimeoutError:
        print("Didn't find a cube")
    finally:
        # whether we find it or not, we want to stop the behavior
        look_around.stop()

    if cube:
        # Drive to 70mm away from the cube (much closer and Cozmo
        # will likely hit the cube) and then stop.
        action = robot.go_to_object(cube, distance_mm(70.0))
        action.wait_for_completed()
        print("Completed action: result = %s" % action)
        print("Done.")


# cozmo.run_program(go_to_object_test)

