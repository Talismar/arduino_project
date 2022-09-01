# -*- coding: utf-8 -*-
from pyfirmata import Arduino,util
import time
from binary_sum import full_adder, comp_2

board = Arduino("/dev/ttyACM0")
iterator = util.Iterator(board)
iterator.start()

time.sleep(1)

# * Similar to pinMode *
# Buttons
btn_01 = board.get_pin("d:8:i")
btn_02 = board.get_pin("d:9:i")
btn_03 = board.get_pin("d:10:i")

# Leds
led_01 = board.get_pin("d:7:o")
led_02 = board.get_pin("d:6:o")
led_03 = board.get_pin("d:5:o")
led_04 = board.get_pin("d:4:o")

# Operations - Buttons
key_resul = board.get_pin("d:3:i")
key_to_sum = board.get_pin("d:11:i")
key_to_sub = board.get_pin("d:12:i")

# Button control - AUX
leds_click = [0, 0, 0]
leds_liber = [0, 0, 0]
list_with_info = ["", "", ""]

# Converting LEDs to List
def info(leds, ind):

  x = "0"

  for led in leds:
    if led == 1:
      x += "1"
    else: 
      x += "0"

  # List filling
  list_with_info[ind] = x

  return list_with_info[ind]

# Change LED state
def change_LED(led):
  if led.read():
    led.write(0)
  else:
    led.write(1)

# Keep button state
def keep_state(led, i):
  global leds_click
  global leds_liber
  
  if leds_click[i] == 1 and leds_liber[i] == 1:
    leds_click[i] = 0
    leds_liber[i] = 0 
    change_LED(led)

while True:
  if btn_01.read():
    leds_click[0] = 1 # on
    leds_liber[0] = 0 # off
  
  else:
    leds_liber[0] = 1

  keep_state(led_01, 0)

  if btn_02.read():
    leds_click[1] = 1
    leds_liber[1] = 0
  
  else:
    leds_liber[1] = 1

  keep_state(led_02, 1)
  
  if btn_03.read():
    leds_click[2] = 1
    leds_liber[2] = 0
  
  else:
    leds_liber[2] = 1
  
  keep_state(led_03, 2)
  
  # To add
  if key_to_sum.read():
    list_with_info[1] = "+"
    print("Adding.......:", info([led_03.read(), led_02.read(), led_01.read()], 0))
    time.sleep(0.5)

  # To subtract
  if key_to_sub.read():
    list_with_info[1] = "-"
    print("Subtracting.....:", info([led_03.read(), led_02.read(), led_01.read()], 0))
    time.sleep(0.5)

  # Process the result
  if key_resul.read():

    info([led_03.read(), led_02.read(), led_01.read()], 2)
    
    # List with operator and operand
    print(list_with_info)
    
    if list_with_info[1] == "-":
      print("*"*10, " Subtracting ", "*"*10)
      ret = full_adder(list_with_info[0], comp_2(list_with_info[2]))  
    
    elif list_with_info[1] == "+":
      print("*"*10, " Adding ", "*"*10)
      ret = full_adder(list_with_info[0], list_with_info[2])      

    # If the result is negative
    if ret[0] == "1":
      ret = "1" + comp_2(ret[1:])

    for bit, led in zip(ret, [led_04, led_03, led_02, led_01]):
      led.write(int(bit))
      time.sleep(0.2)

    list_with_info.clear()
    list_with_info = ["", "", ""]
    time.sleep(0.5)

