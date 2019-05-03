import psutil
import platform
import datetime
import sys
import time
import socket
import fcntl
import struct
import math
import os
from papirus import PapirusComposite


#settings
mountpoint = "/"
network_adaptor = "eth0"

# requires psutil progressbar2
# screen size 2.7 264x176
def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def drawProgressBar(percent, barLen = 14):
	progress = ""
	for i in range(barLen):
		if i < int(barLen * percent / 100):
			progress += u"\u2589"
		else:
			progress += ""

	return progress

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])	
	
def uptime():
 
	try:
		f = open( "/proc/uptime" )
		contents = f.read().split()
		f.close()
	except:
		return "Cannot open uptime file: /proc/uptime"

	total_seconds = float(contents[0])

	# Helper vars:
	MINUTE  = 60
	HOUR    = MINUTE * 60
	DAY     = HOUR * 24

	# Get the days, hours, etc:
	days    = int( total_seconds / DAY )
	hours   = int( ( total_seconds % DAY ) / HOUR )
	minutes = int( ( total_seconds % HOUR ) / MINUTE )
	seconds = int( total_seconds % MINUTE )

	# Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
	string = ""
	if days > 0:
		string += str(days) + " " + (days == 1 and "d" or "d" ) + ", "
	if len(string) > 0 or hours > 0:
		string += str(hours) + " " + (hours == 1 and "h" or "h" ) + ", "
	if len(string) > 0 or minutes > 0:
		string += str(minutes) + " " + (minutes == 1 and "m" or "m" ) + ", "
		string += str(seconds) + " " + (seconds == 1 and "s" or "s" )

	return string;

def main():
	comp = PapirusComposite(False)
	comp.WriteAll()
	
	#build frame
	#comp.AddText(u"",0,0,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	#cpu
	comp.AddText(u"\u256d\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256e",2,0,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2570\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256f",2,22,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",2,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",122,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	#mem
	comp.AddText(u"\u256d\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256e",132,0,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2570\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256f",132,22,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",132,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",252,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	#hdd
	comp.AddText(u"\u256d\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256e",2,45,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2570\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u256f",2,83,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",2,57,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",250,57,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",2,70,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	comp.AddText(u"\u2502",250,70,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf')
	

	#fetch init data
	os, name, version, _, _, _ = platform.uname()
	version = version.split('-')[0]
	ipaddr = get_ip_address(network_adaptor)	
	cpupercent = str(int(psutil.cpu_percent()))
	disk_free = psutil.disk_usage(mountpoint)[2]
	disk_used = psutil.disk_usage(mountpoint)[1]
	disk_percent = str(int(psutil.disk_usage(mountpoint)[3]))
	memory_percent = psutil.virtual_memory()[2]
	disk_total = int(psutil.disk_usage(mountpoint)[1]) + int(psutil.disk_usage(mountpoint)[2])
	diskinfo = convert_size(disk_used) + ' / ' + convert_size(disk_total)
	center_diskinfo = int((264 // 2) - (len(diskinfo) // 2) - len(diskinfo) % 2) - 10
	memory_info = psutil.virtual_memory()
	mem_total = memory_info.total
	mem_used = memory_info.used
	mem_info = convert_size(mem_used) + ' / ' + convert_size(mem_total)
	center_meminfo = int((264 // 2) - (len(mem_info) // 2) - len(mem_info) % 2) + 20
	net = psutil.net_io_counters(pernic=True)
	tx_data = net[network_adaptor].bytes_sent
	rx_data = net[network_adaptor].bytes_recv
	net_data = convert_size(rx_data) + ' RX / ' + convert_size(tx_data) + ' TX' 
	
	#add text
	comp.AddText("Uptime: " + uptime(),2,108,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="uptime")
	comp.AddText("Host: " + name + ' - ' + version,2,124,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="name_version")
	comp.AddText("Net: " + net_data,2,142,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="netdata")
	comp.AddText("IP: " + ipaddr,2,160,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="ipaddr")
	
	comp.AddText(cpupercent,10,25,12,fontPath='/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',Id="cpupercentid")
	comp.AddText(drawProgressBar(psutil.cpu_percent()),10,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="cpubar")
	
	comp.AddText(drawProgressBar(memory_percent),142,10,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="membar")
	comp.AddText(mem_info,center_meminfo,25,10,fontPath='/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',Id="meminfo")
	
	comp.AddText(drawProgressBar(psutil.disk_usage(mountpoint)[3]),10,56,29,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="diskbar")
	comp.AddText(diskinfo,center_diskinfo,90,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="diskfree")

	while True:
		cpupercent = str(int(psutil.cpu_percent()))
		disk_free = psutil.disk_usage(mountpoint)[2]
		disk_used = psutil.disk_usage(mountpoint)[1]
		disk_percent = str(int(psutil.disk_usage(mountpoint)[3]))
		disk_total = int(psutil.disk_usage(mountpoint)[1]) + int(psutil.disk_usage(mountpoint)[2])
		diskinfo = convert_size(disk_used) + ' / ' + convert_size(disk_total)
		center_diskinfo = int((264 // 2) - (len(diskinfo) // 2) - len(diskinfo) % 2) - 10
		memory_info = psutil.virtual_memory()
		mem_info = convert_size(mem_used) + ' / ' + convert_size(mem_total)
		mem_total = memory_info.total
		mem_used = memory_info.used
		center_meminfo = int((264 // 2) - (len(mem_info) // 2) - len(mem_info) % 2) + 10
		net = psutil.net_io_counters(pernic=True)
		tx_data = net[network_adaptor].bytes_sent
		rx_data = net[network_adaptor].bytes_recv
		net_data = convert_size(rx_data) + ' RX / ' + convert_size(tx_data) + ' TX' 
		
		comp.UpdateText("uptime", "Uptime: " + uptime())
		comp.UpdateText("netdata", "Net: " + net_data)
		comp.UpdateText("cpubar", drawProgressBar(psutil.cpu_percent()))
		comp.UpdateText("membar", drawProgressBar(psutil.virtual_memory()[2]))
		comp.UpdateText("cpupercentid", cpupercent + '%')
		comp.RemoveText("diskfree")
		comp.AddText(diskinfo,center_diskinfo,90,14,fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf',Id="diskfree")
		comp.RemoveText("meminfo")
		comp.AddText(mem_info,center_meminfo,25,10,fontPath='/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',Id="meminfo")
		comp.UpdateText("diskbar",drawProgressBar(psutil.disk_usage(mountpoint)[3]))
		comp.WriteAll(True)
		time.sleep(0.7)

	comp.clear()
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit('interrupted')
		pass
