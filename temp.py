import machine
import utime

from machine import ADC
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x3F   #LCD1602的I2C位址 
I2C_NUM_ROWS = 2      #LCD1602列數
I2C_NUM_COLS = 16     #LCD1602行數

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)   #設定I2C
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    

utime.sleep(2)
to_volts = 3.3 / 65535
temper_sensor = ADC(4)   #從ADC(4)取得溫度感測器的電壓值

while True:
    lcd.clear()
    time = utime.localtime()
    
    # 顯示日期及時間
    lcd.putstr("{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}:{SS:>02d}".format(
        month=time[1], day=time[2], HH=time[3], MM=time[4], SS=time[5]))

    temper_volts = temper_sensor.read_u16() * to_volts  #取得當時溫度的電壓
   
    celsius_degrees = 27 - (temper_volts - 0.706) / 0.001721    #計算攝氏溫度
#   fahrenheit_degrees = celsius_degrees * 9 / 5 + 32           #計算華氏溫度

    lcd.move_to(0,1)      #游標跳至第二列第一行
    lcd.putstr('TEMP:')    
    lcd.putstr(str(round(celsius_degrees,3)))
    lcd.putstr(' oC')       #用小寫O代替度的符號    
    utime.sleep(3)          #暫停3秒鐘