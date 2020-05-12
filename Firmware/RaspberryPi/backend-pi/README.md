# How to install backend software

- We have tested this code with Raspberry Pi 3 B+
- Use very lite weight window manager for Raspberry Pi
- Run install.sh
- Following lines need to add to the Raspberry Pi /boot/config.txt
```
dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=2,i2c_gpio_sda=23,i2c_gpio_scl=24
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=2,i2c_gpio_sda=17,i2c_gpio_scl=27
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=2,i2c_gpio_sda=19,i2c_gpio_scl=26
```
- Reboot Raspberry Pi
- Verify i2c devices are in place using following commands
```
pi@raspberrypi:~ $ ls /dev/i2c*
/dev/i2c-1  /dev/i2c-3  /dev/i2c-4  /dev/i2c-5
pi@raspberrypi:~ $ sudo i2cdetect -l
i2c-3   i2c             3.i2c                                   I2C adapter
i2c-1   i2c             bcm2835 I2C adapter                     I2C adapter
i2c-4   i2c             4.i2c                                   I2C adapter
i2c-5   i2c             5.i2c                                   I2C adapter
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
pi@raspberrypi:~ $ sudo i2cdetect -y 3
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
pi@raspberrypi:~ $ sudo i2cdetect -y 4
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
pi@raspberrypi:~ $ sudo i2cdetect -y 5
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
```
- If everything above is successful, you can execute `start.sh`
