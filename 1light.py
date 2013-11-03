#minecraft traffic lights - simple

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time

#Connect to minecraft
mc = minecraft.Minecraft.create()

#clear area
mc.setBlocks(-10,0,-10,60,50,50,block.AIR.id)
#put grass on the floor
mc.setBlocks(-10,-1,-10,60,-1,10,block.GRASS.id)

#build traffic light
# pole straight up
mc.setBlocks(0,0,0,0,5,0,block.IRON_BLOCK.id, 15)
# create 3 lights out of wool
# wool values (black - 15, red - 14, yellow - 4, green - 13)
# set all the lights to off (black)
mc.setBlock(1,5,0,block.WOOL.id,15)
mc.setBlock(1,4,0,block.WOOL.id,15)
mc.setBlock(1,3,0,block.WOOL.id,15)

#loop forever
while(True):
    #set to stop
    mc.setBlock(1,5,0,block.WOOL.id,14)
    mc.setBlock(1,4,0,block.WOOL.id,15)
    mc.setBlock(1,3,0,block.WOOL.id,15)
    # sleep for half a second
    time.sleep(0.5)
    #set to stop, prepare
    mc.setBlock(1,5,0,block.WOOL.id,14)
    mc.setBlock(1,4,0,block.WOOL.id,4)
    mc.setBlock(1,3,0,block.WOOL.id,15)
    time.sleep(0.5)
    #set to go
    mc.setBlock(1,5,0,block.WOOL.id,15)
    mc.setBlock(1,4,0,block.WOOL.id,15)
    mc.setBlock(1,3,0,block.WOOL.id,13)
    time.sleep(0.5)
    #set to prepare
    mc.setBlock(1,5,0,block.WOOL.id,15)
    mc.setBlock(1,4,0,block.WOOL.id,4)
    mc.setBlock(1,3,0,block.WOOL.id,15)
    time.sleep(0.5)
    #back to stop
