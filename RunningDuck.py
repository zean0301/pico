import machine
import utime
import random
from machine import ADC
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
I2C_ADDR = 0x3F
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()

duck = bytearray([0x00,0x06,0x17,0x1E,0x1E,0x0E,0x04,0x00])

to_volts = 3.3 / 65535
temper_sensor = ADC(4)

while True:
    lcd.clear()
    time = utime.localtime()
    
    lcd.putstr("{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}:{SS:>02d}".format(
        month=time[1], day=time[2], HH=time[3], MM=time[4], SS=time[5]))

    temper_volts = temper_sensor.read_u16() * to_volts  
    celsius_degrees = 27 - (temper_volts - 0.706) / 0.001721           

    lcd.move_to(0,1)      
    lcd.putstr('TEMP:')    
    lcd.putstr(str(round(celsius_degrees,3)))
    lcd.putstr(' oC')           
    utime.sleep(2)
    for i in range(0,16,1):
        lcd.clear()
        lcd.move_to(i,random.randint(0,1))
        lcd.custom_char(0, duck)
        lcd.putchar(chr(0))
        utime.sleep(0.25)
        lcd.clear()