import serial
import io
import time

"""

Below are imput commands.

All additional commands should be tranfer from string to bit number.

All additional commands should use ser.write() function.

There is unknown bug in pyserial that will stuck all the tasks,
make sure to add reset function and time.sleep to clear the obstacles on the path.

"""

# Establish connection
def sys_connect():
    global ser   
    ser = serial.Serial(port = 'COM4', timeout = 1)             # Set communication port and timeout
    global sio
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))         # Set input to text
    
    if ser.is_open == True:
        print(ser.name + " has now established connection with bias control module.")
    else:
        print("Device not detected in " + ser.name + ", please try another port.")
    
    #initial setting global variable add and mode

    global add

    add = 1

    global mode

# Open connection once for all purposes
def sys_open():
    if ser.is_open == True:
        print('The control module is open successfully.')
    else:
        ser.open()
        print('The control module is open successfully.')

# Read bias voltage DAC
def read_v():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    byte_string = "READ{}V\r\n".format(add).encode()
    ser.write(byte_string)

    # Read file
    line = ser.readline()
    print(line)
    # bit-string
    V_DAC = line.decode(encoding='ascii').rstrip('\r\n')
    V = int(V_DAC)
    V_out = 11 - V * 22 / 16383
    V_out = round(V_out, 2)

    if V_out == 0.26:
        print("Your voltage is now: " + str(V_out) + "V, but that is also the default value.")
        print("Make sure if the module is working in desired mode.")
    else:
        print("Your voltage is now: " + str(V_out) + "V.\n")

    ser.reset_input_buffer
    ser.reset_output_buffer
    
    return V_out

# Read Vpi voltage
def read_vpi():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    byte_string = "READ{}VPI\r\n".format(add).encode()
    ser.write(byte_string)

    # Read file
    line = ser.readline()
    # bit-string
    V_DAC = line.decode(encoding = 'ascii').rstrip('\r\n')
    V = int(V_DAC)
    V_pi = 11 - V * 22 / 16383
    V_pi = round(V_pi, 2)
    print("Vpi is: " + str(V_pi) + "V.\n")

    ser.reset_input_buffer
    ser.reset_output_buffer

    return V_pi

# Read address/mode/optical value of the module
def read_add():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    byte_string = "READ{}S\r\n".format(add).encode()
    ser.write(byte_string)

    # Read file
    line = ser.readline()
    # bit-string
    info = line.decode(encoding='ascii').rstrip('\r\n')
    ADD = int(info[:1])
    print("Your address now is: " + str(add) +".\n")

    ser.reset_input_buffer
    ser.reset_output_buffer

    return ADD

# Read mode setting now of the module
def read_mode():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)
    
    byte_string = "READ{}S\r\n".format(add).encode()
    ser.write(byte_string)

    # Read file
    line = ser.readline()
    # bit-string
    print(line)
    info = line.decode(encoding='ascii').rstrip('\r\n')
    print(info)
    MODE = int(info[1:2])

    if MODE == 1:
        print("Your mode is now set 1: Q+.\n")
    elif MODE == 2:
        print("Your mode is now set 2: Q-.\n")
    elif MODE == 3:
        print("Your mode is now set 3: MAX.\n")
    elif MODE == 4:
        print("Your mode is now set 4: MIN.\n")
    elif MODE == 5:
        print("Your mode is now set 5: MANUAL.\n")
    else:
        print("Not matched, please check your code.\n")
    
    ser.reset_input_buffer
    ser.reset_output_buffer
    
    return MODE

# Read light_power of the module
def read_light():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    byte_string = "READ{}S\r\n".format(add).encode()
    ser.write(byte_string)

    # Read file
    line = ser.readline()
    # bit-string
    info = line.decode(encoding='ascii').rstrip('\r\n')
    power_DAC = int(info[2:])
    power = power_DAC * 0.226
    print("Your optical power detected in diode is: " + str(power) + "uW.\n")
    
    ser.reset_input_buffer
    ser.reset_output_buffer
    
    return power

# Set address, value: 0-9, default: 1
def set_address(ADD):
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    if ADD == 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9:
        byte_string = "SETADD:{}\r\n".format(ADD).encode()
        ser.write(byte_string)
        print("Device address now is " + str(ADD) + "\n")                # Inform the user
        line = ser.readline()
        print(line)
        
        ser.reset_input_buffer
        ser.reset_output_buffer

        return ADD                                                       # Return address for other usage
    else:
        print("Entering wrong number, the address is set to default 1.\n")
        byte_string = "SETADD:1\r\n".encode('ascii')
        ser.write(byte_string)
        ADD = 1
        line = ser.readline()
        print(line)

        ser.reset_input_buffer
        ser.reset_output_buffer

        return ADD


# Set mode: 1-5, Q+, Q-, MAX, MIN, MANUAL
def set_mode(MODE):
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    if MODE == 1 or 2 or 3 or 4 or 5:
        byte_string = "SET{}M:{}\r\n".format(add, MODE).encode()
        ser.write(byte_string)
        line = ser.readline()
        print(line)

        ser.reset_input_buffer
        ser.reset_output_buffer

        if MODE == 1:
            print("Your mode is now set 1: Q+\n")
        elif MODE == 2:
            print("Your mode is now set 2: Q-\n")
        elif MODE == 3:
            print("Your mode is now set 3: MAX\n")
        elif MODE == 4:
            print("Your mode is now set 4: MIN\n")
        else:
            print("Your mode is now set 5: MANUAL\n")
        return MODE
    else:
        print("Wrong number setting in mode.\n")
    

# Set manual voltage: -11 to +11V
def set_v(V_set):
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    if mode != 5:
        print("Your mode is not set in manual input.\n")
    elif abs(V_set) > 11:
        print("Your voltage is too high.\n")
    else:
        V = round(-16383 * (V_set - 11) / 22)
        V_DAC = "{}".format(V)
        V_DAC = V_DAC.zfill(5)
        byte_string = "SET{}V:{}\r\n".format(add, V_DAC).encode()
        ser.write(byte_string)
        line = ser.readline()
        print(line)
        mes = line.decode(encoding='ascii').rstrip('\r\n')
        print(mes)

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        return V_set
    
# Set correction value (offset)
def set_offset(off):
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    if mode == 5:
        print("Manual mode is not allowed to set offset.\n")
    else:
        byte_string = "SETOFS{}:{}\r\n".format(mode, off).encode()
        ser.write(byte_string)
        line = ser.readline()
        print(line)
        print("An offset " + str(off) + " is added to mode " + str(mode) + ".")

        ser.reset_input_buffer
        ser.reset_output_buffer

# Reset device
def set_reset():
    ser.reset_input_buffer
    ser.reset_output_buffer
    time.sleep(1)

    byte_string = "RESET{}\r\n".format(add).encode()
    ser.write(byte_string)
    print("Your device is now reset.\n")

    line = ser.readline()
    print(line)

    #inform address
    # byte_string = "READ{}S\r\n".format(add).encode()
    # ser.write(byte_string)
    # line = ser.readline()
    # info = line.decode(encoding='ascii').rstrip('\r\n')
    # add = int('info[:1]')
    # print("Your address now is: " + str(add) +".\n")
    # return add

# Close port
def sys_close():
    ser.reset_input_buffer
    ser.reset_output_buffer

    ser.close()
    if ser.is_open == False:
        print(ser.name + " is now disconnected to bias control module.\n")
    else:
        print(ser.name + " is still connected to bias control module.\n")

sys_connect()
sys_open()
mode = set_mode(1)
# time.sleep(1)
# set_v(6)
# time.sleep(1)
v = read_v()