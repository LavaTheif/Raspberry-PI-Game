import time
import RPi.GPIO as GPIO
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# key1
GPIO.setup(21, GPIO.OUT)
GPIO.output(21,1)

#up key
GPIO.setup(6, GPIO.OUT)
GPIO.output(6,1)

#20 is the id of key2

obstical = "||"
worldSize = 50
pre = "\n"*14#Clears the screen

record = int(open("record.txt").read())

while True:
    print("\n\nPress key1 to pause, press up on the joystick to jump")
    print("Curred record: "+str(record)+" points.  Can you beat it?\n")
    input("Press enter to start!")

    obspos = [30]
    jump = 0
    points = 0
    paused = False

    while True:
        time.sleep(0.1)#Sleep for 100 ms
        
        #Set player sprite
        player = " o\n\\|/\n/ \\"

        #Get key inputs
        key1=GPIO.input(21)==0
        key_up=GPIO.input(6)==0

        #If pressing pause key, pause/unpause the game
        if(key1):
            paused = not paused
            while(key1):#Wait until they unpress the key
                key1=GPIO.input(21)==0

        #If paused, display message and stop executing the code
        if(paused):
            print(pre+"##PAUSED##" + ("\n"*9))
            continue

        #if jump key pressed
        if(key_up):
            if(jump < 10):#if timer is less than 10
                player = player + "\n\n___"#let them jump
            jump += 1
        else:
            jump = 0#reset timer
        
        #Move obsticals
        i=0
        while i < len(obspos):
            obspos[i] -=1
            if(obspos[i]<0):
                obspos.remove(obspos[i])
                continue
            i+=1
        
        if(random.randint(0,20)==0):##If gone past player, reset it
            obspos.append(worldSize)

        take = 0
        is_hit = False
        is_jumping = "\n\n" in player
        if(is_jumping):
            world = str(points)+" points" + pre+player
        else:
            world = str(points)+" points\n\n" + pre+player
        for pos in obspos:
            if(pos < worldSize):
                if(pos == 0):
                    is_hit = True
                a = pos-take
                take += a
                world+="_"*a
                world+=obstical
        world += "_"*(worldSize-take)
        
        #Print world
        print(world)
        #print(+ ("_"*a)+obstical+("_"*(worldSize-obspos)))
        
        if(is_hit):
            #if obstical is at end
            if(not(is_jumping)):#If player not jumping
                #end game
                print("Game over.\n\nYou scored "+str(points)+" points!")
                if(points > record):
                    print("New Record!")
                    record = points
                    open("record.txt","w").write(str(points))
                break
            else:
                #add 1 to points
                points+=1
