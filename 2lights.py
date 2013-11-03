#minecraft traffic lights - simple

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time

class TrafficLight():
    def __init__(self, mc, x, y, z):
        #build traffic light
        # pole straight up
        mc.setBlocks(x,y,z,x,y+5,z,block.IRON_BLOCK.id, 15)
        # create 3 lights out of wool
        # wool values (black - 15, red - 14, yellow - 4, green - 13)
        # set all the lights to off (black)
        mc.setBlock(x+1,y+5,z,block.WOOL.id,15)
        mc.setBlock(x+1,y+4,z,block.WOOL.id,15)
        mc.setBlock(x+1,y+3,z,block.WOOL.id,15)
        #set to stop
        mc.setBlock(x+1,y+5,z,block.WOOL.id,14)
        #store x,y,z
        self.x = x
        self.y = y
        self.z = z
        #store mc
        self.mc = mc
        
    def go(self):
        #set to stop, prepare
        self.mc.setBlock(self.x+1,self.y+5,self.z,block.WOOL.id,14)
        self.mc.setBlock(self.x+1,self.y+4,self.z,block.WOOL.id,4)
        self.mc.setBlock(self.x+1,self.y+3,self.z,block.WOOL.id,15)
        time.sleep(0.5)
        #set to go
        self.mc.setBlock(self.x+1,self.y+5,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+1,self.y+4,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+1,self.y+3,self.z,block.WOOL.id,13)
        time.sleep(0.5)

    def stop(self):
        #set to prepare
        self.mc.setBlock(self.x+1,self.y+5,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+1,self.y+4,self.z,block.WOOL.id,4)
        self.mc.setBlock(self.x+1,self.y+3,self.z,block.WOOL.id,15)
        time.sleep(0.5)
        #set to stop
        self.mc.setBlock(self.x+1,self.y+5,self.z,block.WOOL.id,14)
        self.mc.setBlock(self.x+1,self.y+4,self.z,block.WOOL.id,15)
        self.mc.setBlock(self.x+1,self.y+3,self.z,block.WOOL.id,15)
        # sleep for half a second
        time.sleep(0.5)

#MAIN PROGRAM

#Connect to minecraft
mc = minecraft.Minecraft.create()

#clear area
mc.setBlocks(-5,0,-5,5,50,5,block.AIR.id)

#create traffic light
trafficLight1 = TrafficLight(mc,0,0,0)

trafficLight2 = TrafficLight(mc,0,0,3)


#loop forever
while(True):
    trafficLight2.stop()
    trafficLight1.go()
    time.sleep(2)
    trafficLight1.stop()
    trafficLight2.go()
    time.sleep(2)
