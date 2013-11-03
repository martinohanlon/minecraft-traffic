#minecraft traffic lights - simple

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import threading so I can make asynchronous calls!
import threading
#import random so I can randomly create cars
import random

class Road():
    def __init__(self, mc, x, y, z, width, lenght):
        #create road
        mc.setBlocks(x, y-1, z, x+lenght, y-1, z+width-1, block.BEDROCK.id)
        #create line down the middle
        mc.setBlocks(x, y-1, z+(width/2), x+lenght, y-1, z+(width/2), block.WOOL.id, 0)
        #store values
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.lenght = lenght
        #create empty junctions & cars list
        self.junctions = []
        self.cars= []

    def run(self):
        #start up junctions
        for junction in self.junctions:
            #tell the junction to run in the background
            junction.daemon
            junction.start()

    def stop(self):
        #stop junctions
        for junction in self.junctions: junction.stop()
        #stop cars
        for car in self.cars: car.stop()
        #wait for junctions to stop
        for junction in self.junctions: junction.join()
        #wait for cars to stop
        for car in self.cars: car.join()

    def createJunction(self, posDownRoad, timeOpen, timeClosed):
        #create junction at position down the road
        junction = Junction(mc, self.x+posDownRoad, self.y, self.z, self.x+posDownRoad+self.width, self.y, self.z+self.width-1, timeOpen, timeClosed)
        #add junction to collection
        self.junctions.append(junction)

    def startCar(self, direction):
        #create car
        car = Car(mc, self, direction)
        #add car to collection
        self.cars.append(car)
        #tell car to run in background
        car.daemon
        car.start()

class Car(threading.Thread):
    def __init__(self, mc, road, direction):
        #store variables
        self.mc = mc
        self.road = road
        self.direction = direction
        #set x,y,z
        #set z & x position, left or right side, top or bottom of road depending on direction
        if direction == 1:
            self.x = road.x
            self.z = road.z + 1
        if direction == -1:
            self.x = road.x + road.lenght
            self.z = road.z + road.width - 2
        self.y = road.y
        #setup threading
        threading.Thread.__init__(self)

    def run(self):
        lenghtOfCar = 4
        self.running = True
        ableToMove = True
        #find the end of the road, depending on which way the car is going
        endOfRoad = self.road.x
        if self.direction == 1: endOfRoad = endOfRoad + self.road.lenght
        #loop until i meet the end of the road
        while(self.x != endOfRoad and self.running == True):
            #draw the car
            if ableToMove: self.drawCar()
            #sleep for a bit
            time.sleep(0.5)
            #move the car
            #where will the car be moving too?
            frontOfCar = self.x + self.direction
            #if im going forwards add 3 to the x, as my car's x is at the back
            if self.direction == 1: frontOfCar = frontOfCar + lenghtOfCar
            ableToMove = True
            #am I going to enter a junction which is closed?
            for junction in self.road.junctions:
                if self.direction == 1 and junction.x1 == frontOfCar and junction.open == False: ableToMove = False
                if self.direction == -1 and junction.x2 == frontOfCar and junction.open == False: ableToMove = False
            #am I going to hit another car?
            for car in self.road.cars:
                if self.direction == 1 and frontOfCar >= car.x and frontOfCar <= (car.x + lenghtOfCar) and self.z == car.z and car.running == True: ableToMove = False
                if self.direction == -1 and frontOfCar <= (car.x + lenghtOfCar) and frontOfCar >= car.x and self.z == car.z and car.running == True: ableToMove = False
            #clear car and add 1 to the car's position
            if ableToMove:
                self.clearCar()
                self.x = self.x + self.direction

        self.running = False

    def stop(self):
        self.running = False
    
    def drawCar(self):
        self.mc.setBlocks(self.x, self.y, self.z, self.x + 3, self.y + 2, self.z, block.IRON_BLOCK.id)
        self.mc.setBlock(self.x, self.y, self.z, block.WOOL.id, 15)
        self.mc.setBlock(self.x+3, self.y, self.z, block.WOOL.id, 15)

    def clearCar(self):
        self.mc.setBlocks(self.x, self.y, self.z, self.x + 3, self.y + 2, self.z, block.AIR.id)

class Junction(threading.Thread):
    def __init__(self, mc, x1, y1, z1, x2, y2, z2, timeOpen, timeClosed):
        #create junction
        mc.setBlocks(x1,y1-1,z1,x2,y2-1,z2,block.BEDROCK.id)
        #create lines
        mc.setBlocks(x1,y1-1,z1,x2,y2-1,z1,block.WOOL.id,0)
        mc.setBlocks(x2,y1-1,z1,x2,y2-1,z2,block.WOOL.id,0)
        mc.setBlocks(x2,y1-1,z2,x1,y2-1,z2,block.WOOL.id,0)
        mc.setBlocks(x1,y1-1,z2,x1,y2-1,z1,block.WOOL.id,0)
        #create traffic lights
        self.trafficLight1 = TrafficLight(mc, x1, y1, z1-1, -1)
        self.trafficLight2 = TrafficLight(mc, x2, y2, z2+1, 1)
        #set to open
        self.openJunction()
        #store times
        self.timeOpen = timeOpen
        self.timeClosed = timeClosed
        #setup threading
        threading.Thread.__init__(self)
        #store variables
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        
    def run(self):
        #start the Junction
        self.running = True
        while(self.running):
            self.openJunction()
            time.sleep(self.timeOpen)
            self.closeJunction()
            time.sleep(self.timeClosed)

    def stop(self):
        #stop the junction
        self.running = False

    def openJunction(self):
        #set lights to go
        light1 = self.trafficLight1.go()
        light2 = self.trafficLight2.go()
        #wait for lights to finish changing
        light1.join()
        light2.join()
        #set open status to True
        self.open = True

    def closeJunction(self):
        #set lights to stop
        light1 = self.trafficLight1.stop()
        light2 = self.trafficLight2.stop()
        #wait for lights to finish changing
        light1.join()
        light2.join()
        #set open status to False
        self.open = False

class TrafficLight():
    def __init__(self, mc, x, y, z, direction):
        #build traffic light
        # pole straight up
        mc.setBlocks(x,y,z,x,y+5,z,block.IRON_BLOCK.id, 15)
        # create 3 lights out of wool
        # wool values (black - 15, red - 14, yellow - 4, green - 13)
        # set all the lights to off (black)
        mc.setBlock(x+direction,y+5,z,block.WOOL.id,15)
        mc.setBlock(x+direction,y+4,z,block.WOOL.id,15)
        mc.setBlock(x+direction,y+3,z,block.WOOL.id,15)
        #set to stop
        mc.setBlock(x+direction,y+5,z,block.WOOL.id,14)
        #store x,y,z
        self.x = x
        self.y = y
        self.z = z
        #sotre direction
        self.direction = direction
        #store mc
        self.mc = mc
        
    def go(self):
        thread = threading.Thread(target=self.setToGo)
        thread.start()
        return thread

    def setToGo(self):
        #set to stop, prepare
        self.mc.setBlock(self.x+self.direction,self.y+5,self.z,block.WOOL.id,14)
        self.mc.setBlock(self.x+self.direction,self.y+4,self.z,block.WOOL.id,4)
        self.mc.setBlock(self.x+self.direction,self.y+3,self.z,block.WOOL.id,15)
        time.sleep(0.5)
        #set to go
        self.mc.setBlock(self.x+self.direction,self.y+5,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+self.direction,self.y+4,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+self.direction,self.y+3,self.z,block.WOOL.id,13)
        time.sleep(0.5)

    def stop(self):
        thread = threading.Thread(target=self.setToStop)
        thread.start()
        return thread

    def setToStop(self):
        #set to prepare
        self.mc.setBlock(self.x+self.direction,self.y+5,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+self.direction,self.y+4,self.z,block.WOOL.id,4)
        self.mc.setBlock(self.x+self.direction,self.y+3,self.z,block.WOOL.id,15)
        time.sleep(0.5)
        #set to stop
        self.mc.setBlock(self.x+self.direction,self.y+5,self.z,block.WOOL.id,14)
        self.mc.setBlock(self.x+self.direction,self.y+4,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+self.direction,self.y+3,self.z,block.WOOL.id,15)
        time.sleep(0.5)

if __name__ == "__main__":
    #MAIN PROGRAM

    #Connect to minecraft
    mc = minecraft.Minecraft.create()

    #clear area
    mc.setBlocks(-10,0,-10,60,50,10,block.AIR.id)
    #put grass on the floor
    mc.setBlocks(-10,-1,-10,60,-1,10,block.GRASS.id)

    #create road
    road = Road(mc, 0,0,0,9,50)
    #create junction, 20 blocks down, open for 10 seconds, closed for 5
    road.createJunction(20,10,5)
    #start the road
    road.run()
    #loop until Ctrl C
    try:
        while(True):
            #create a car in a random direction, unless its 0 then we wont create a car
            direction = random.randint(-1, 1)
            if direction != 0:
                road.startCar(direction)
            #sleep for a bit
            time.sleep(3)
    except KeyboardInterrupt:
        print("stopped")
    finally:
        #stop everything
        road.stop()
    
