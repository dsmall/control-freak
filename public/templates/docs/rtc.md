DS1340 I2C RTC
==============

--

The DS1340 real-time clock is in the form of an SMD chip with battery backup
mounted on a [JeeLabs RTC Plug][jlrtc] and responds to I2C address 0x68.

The `rtc.html` page normally displays the date and time, updated once a second.
Clicking **Reset** stops the clock and resets the time to 00:00:00.
Clicking **Start** starts the clock in stopwatch mode. It can then be stopped and
re-started, carrying on from where it left off.
Clicking **Set time** sets Rascal time from an NTP server, then sets the RTC.

The web page communicates with Rascal via POST requests to `/rtc`, executing
Python function `rtc()` in `server.py`. Communication with the RTC chip is via
Pytronics library functions `i2cRead` and `i2cWrite`, using Byte and I2C Block mode transfers.
The date and time are returned to the web page as a JSON encoded string.

<small>DS 20 September 2012</small>

[jlrtc]: http://jeelabs.com/products/rtc-plug
