"""
Adapted from https://github.com/g-sam/polly
Removed unused functionality; return sensor data from read() rather than transmit on MQTT.
"""
import machine
import ustruct as struct
import sys
import utime as time

def init_uart(x):
    uart = machine.UART(x, 9600)
    uart.init(9600, bits=8, parity=None, stop=1)
    return uart

def process_measurement(packet):
    try:
        *data, checksum, tail = struct.unpack('<HHBBBs', packet)

        # WARNING: the SDS011 spec says that we should divide these values by 10 to get their true measure.
        # The seller of my sensor (Flashtree) appears to have recoded the firmware so the value returned
        # has already been divided.
        pm25 = data[0]
        pm10 = data[1]
        
        # device_id = str(data[2]) + str(data[3])
        checksum_OK = checksum == (sum(data) % 256)
        tail_OK = tail == b'\xab'
        return (pm25, pm10) if (checksum_OK and tail_OK) else None
        
    except Exception as e:
        sys.print_exception(e)

def read(allowed_time=0):
    uart = init_uart(0)
    start_time = time.ticks_ms()
    delta_time = 0
    while (delta_time <= allowed_time * 1000):
        try:
            header = uart.read(1)
            if header == b'\xaa':
                command = uart.read(1)
                
                if command == b'\xc0':
                    packet = uart.read(8)
                    return process_measurement(packet)
                    
                elif command == b'\xc5':
                    packet = uart.read(8)
                    process_reply(packet)
            delta_time = time.ticks_diff(time.ticks_ms(), start_time) if allowed_time else 0
            
        except Exception as e:
            sys.print_exception(e)