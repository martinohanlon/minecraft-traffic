#minecraft traffic lights - simple

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import threading so I can asynchronous calls!
import threading

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
        #create empty junctions list
        self.junctions = []

    def run(self):
        #start up junctions
        for junction in self.junctions:
            #tell the junction to run in the background
            junction.daemon
            junction.start()

    def stop(self):
        #stop junctions
        for junction in self.junctions: junction.stop()
        #wait for junction to stop
        for junction in self.junctions: junction.join()

    def createJunction(self, posDownRoad, timeOpen, timeClosed):
        #create junction at position down the road
        junction = Junction(mc, self.x+posDownRoad, self.y, self.z, self.x+posDownRoad+self.width, self.y, self.z+self.width-1, timeOpen, timeClosed)
        
        #add junction to collection
        self.junctions.append(junction)
        
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
        #set status to 1
        self.status = 1

    def closeJunction(self):
        #set lights to stop
        light1 = self.trafficLight1.stop()
        light2 = self.trafficLight2.stop()
        #wait for lights to finish changing
        light1.join()
        light2.join()
        #set status to 0
        self.status = 0

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
            #sleep for a bit
            time.sleep(1)
    except KeyboardInterrupt:
        print("stopped")
    finally:
        #stop everything
        road.stop()
    
