import socket
import ncd_industrial_relay
from time import time, sleep
import PySimpleGUI as sg
import threading

# Define port for realy boards
port = 2101

# Set Some GUI settings
sg.theme("dark")
sg.set_options(font=("Courier New", 16))

# Define Relays and associated index on board. listed in order of board index. RELAYS[0] = relay board 1, RELAYS[1] = relay board 2, etc...
RELAYS = [
    {
        "OWS BYPASS": 1,
    },
    {
        "EMPTY": 0,
    },
    {
        "EMPTY": 0,
    },
    {
        "EMPTY": 0,
    },
    {
        "EMPTY": 0,
    },
    {
        "MPDE 1": 1,
        "MPDE 2": 2,
        "MPDE 3": 3,
        "MPDE 4": 4,
        "GEARBOX 1": 5,
        "GEARBOX 2": 6,
        "GEARBOX 3": 7,
        "GEARBOX 4": 8,
    },
    {
        "GENSET 1": 1,
        "GENSET 2": 2,
        "GENSET 3": 3,
        "START DEWATER": 4,
    }
]

# Define ADCs and associated index on board. listed in order of board index. ADCs[0] = relay board 1, ADCs[1] = relay board 2, etc...
ADCs = [
    {
        "MDPE 1: Red Lamp": 1,
        "MDPE 1: Low Oil Alarm": 2,
        "MDPE 2: Red Lamp": 3,
        "MDPE 2: Low Oil Alarm": 4,
    },
    {
        "MDPE 3: Red Lamp": 1,
        "MDPE 3: Low Oil Alarm": 2,
        "MDPE 4: Red Lamp": 3,
        "MDPE 4: Low Oil Alarm": 4,
        "Gearbox 1: High Temp": 5,
        "Gearbox 2: High Temp": 6,
        "Gearbox 3: High Temp": 7,
        "Gearbox 4: High Temp": 8,
    },
    {
        "Genset 1: High Temp": 1,
        "Genset 1: Overcrank": 2,
        "Genset 1: Overspeed": 3,
        "Genset 2: High Temp": 4,
        "Genset 2: Overcrank": 5,
        "Genset 2: Overspeed": 6,
        "Genset 3: High Temp": 7,
        "Genset 3: Overcrank": 8,
    },
    {
        "Genset 3: Overspeed": 1,
        "Fuel Transfer Pump Overload": 2,
        "Fuel Tank 7 Low": 3,
        "Fuel Tank 8 Low": 4,
        "Air Compressor 1 Overload": 5,
        "Air Compressor 2 Overload": 6,
        "Pneumatic Header Pressure low": 7,
        "Fire Detected": 8,
    },
    {
        "Bilge Pump Overload": 1,
    },
    {
        "MDPE 1: High Oil Temp": 1,
        "MDPE 2: High Oil Temp": 2,
        "MDPE 3: High Oil Temp": 3,
        "MDPE 4: High Oil Temp": 4,
    },
    {
        "EMPTY": 0,
    }
]

# Define ANALOG Inputs and associated index on board. listed in order of board index. ANALOGS[0] = relay board 1, ANALOGS[1] = relay board 2, etc...
ANALOGS = [
    {
        "Bilge Level - Forepeak": 5,
        "Bilge Level - Fuel Tank Area": 6,
    },
    {
        "EMPTY": 0,
    },
    {
        "EMPTY": 0,
    },
    {
        "EMPTY": 0,
    },
    {
        "Secure Room Temperature": 4,
        "Pilot House Temperature": 3,
    },
    {
        "Engine Room Bilge Level": 5,
        "Hold Tank Bilge Level": 6,
        "Generator Room Bilge Level": 7,
    },
    {
        "EMPTY": 0,
    }
]

# Relay board addresses, ordered by realy baord index
ADDRESSES = [
    "192.168.10.31",
    "192.168.10.32",
    "192.168.10.33",
    "192.168.10.34",
    "192.168.10.35",
    "192.168.10.36",
    "192.168.10.37"
]

# List of colors to be used for text, etc
COLORS = [
        "green",
        "red",
        "yellow",
]

# Defind First column. Includes first 17 Digital inputs
col1 = [    
    [sg.Text(text='\u2B24  ' + list(ADCs[0])[0], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[0])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[0])[1], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[0])[1])],
    [sg.Text(text='\u2B24  ' + list(ADCs[0])[2], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[0])[2])],
    [sg.Text(text='\u2B24  ' + list(ADCs[0])[3], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[0])[3])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[0], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[1], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[1])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[2], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[2])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[3], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[3])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[4], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[4])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[5], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[5])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[6], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[6])],
    [sg.Text(text='\u2B24  ' + list(ADCs[1])[7], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[1])[7])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[0], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[1], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[1])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[2], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[2])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[3], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[3])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[4], text_color=COLORS[2], size=(30, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[4])],
]

# Define Second Column. Includes remainder of digital inputs
col2 = [
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[5], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[5])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[6], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[6])],
    [sg.Text(text='\u2B24  ' + list(ADCs[2])[7], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[2])[7])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[0], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[1], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[1])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[2], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[2])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[3], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[3])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[4], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[4])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[5], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[5])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[6], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[6])],
    [sg.Text(text='\u2B24  ' + list(ADCs[3])[7], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[3])[7])],
    [sg.Text(text='\u2B24  ' + list(ADCs[4])[0], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[4])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[5])[0], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[5])[0])],
    [sg.Text(text='\u2B24  ' + list(ADCs[5])[1], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[5])[1])],
    [sg.Text(text='\u2B24  ' + list(ADCs[5])[2], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[5])[2])],
    [sg.Text(text='\u2B24  ' + list(ADCs[5])[3], text_color=COLORS[2], size=(35, 1), justification='left', font=("Courier New", 14), key=list(ADCs[5])[3])],
]
# Set an initial string value for analog data
value = 'INIT'
# Define third column. Includes All analog inputs as well as a button to unlock other buttons and 3 buttons to toggle multiple relays at once: all MDPSs, All gensets, and all gearboxes
col3 = [
    [sg.Text(text=list(ANALOGS[0])[0] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[0])[0])],
    [sg.Text(text=list(ANALOGS[0])[1] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[0])[1])],
    [sg.Text(text=list(ANALOGS[4])[0] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[4])[0])],
    [sg.Text(text=list(ANALOGS[4])[1] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[4])[1])],
    [sg.Text(text=list(ANALOGS[5])[0] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[5])[0])],
    [sg.Text(text=list(ANALOGS[5])[1] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[5])[1])],
    [sg.Text(text=list(ANALOGS[5])[2] + ' :  ' + value, text_color='white', size=(45, 1), justification='left', font=("Courier New", 14), key=list(ANALOGS[5])[2])],
    [sg.Text(text="")],
    [sg.HorizontalSeparator()],
    [sg.Text(text="")],
    [sg.Button('UNLOCK RELAY BUTTONS')],
    [sg.Text(text="")],
    [sg.HorizontalSeparator()],
    [sg.Text(text="")],
    [sg.Button('TOGGLE ALL MDPES', disabled=True)],
    [sg.Text(text="")],
    [sg.Button('TOGGLE ALL GENSETS', disabled=True)],
    [sg.Text(text="")],
    [sg.Button('TOGGLE ALL GEARBOXES', disabled=True)],
    [sg.Text(text="")],
]

# Define Fourth column. Includes buttons forall individual relays
col4 = [
    [sg.Button(list(RELAYS[0])[0], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[0], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[1], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[2], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[3], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[4], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[5], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[6], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[5])[7], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[6])[0], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[6])[1], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[6])[2], button_color='green', disabled=True)],
    [sg.Button(list(RELAYS[6])[3], button_color='green', disabled=True)],
]

# Function that is called by the unlock button, that enables the buttons, then disables the buttons after 5 seconds
def timer_thread(window):
    window["UNLOCK RELAY BUTTONS"].update(disabled=True)
    for RB in RELAYS:
        for button in RB:
            if not button == "EMPTY":
                window[button].update(disabled=False)
    window['TOGGLE ALL MDPES'].update(disabled=False)
    window['TOGGLE ALL GENSETS'].update(disabled=False)
    window['TOGGLE ALL GEARBOXES'].update(disabled=False)
    sleep(5)
    window["UNLOCK RELAY BUTTONS"].update(disabled=False)
    for RB in RELAYS:
        for button in RB:
            if not button == "EMPTY":
                window[button].update(disabled=True)
    window['TOGGLE ALL MDPES'].update(disabled=True)
    window['TOGGLE ALL GENSETS'].update(disabled=True)
    window['TOGGLE ALL GEARBOXES'].update(disabled=True)

# function that handles all the main logic.  Takes in all values and modifies the GUI with them.
def the_thread(window):
    while True:
        # Cycle through each of ADCs, ANALOGS, and ADDRESSES. Each loop is a new board.
        for address, adc, analog in zip(ADDRESSES, ADCs, ANALOGS):
            # Define the board and connection params, then connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            board = ncd_industrial_relay.Relay_Controller(sock)
            try:
                sock.connect((address, port))
            except Exception as e:
                print (e)
                continue
            sock.settimeout(.5)
            # Cucle through each digital input. each loop is the next DI on the same board
            for x in adc:
                if x == 'EMPTY':
                    continue
                try:
                    # Take brackets off of the incoming data
                    value = str(board.read_single_ad8(adc[x]))[1:-1]
                    # Handle rare cases of getting non-numeric data back. Just redo until you get good data
                    while not value.isnumeric() and not x == "EMPTY":
                        value = str(board.read_single_ad8(adc[x]))[1:-1]
                except Exception as e:
                    print (e)
                    continue
                # Set DI state based on the value returned. 255 = normal, 0 = alarmed, so setting a value of 255  to mean a state of 0 means: 0 -> no alarm, 1 -> alarm.
                try:
                    if int(value) > 125:
                        state = 0
                    elif int(value) < 125:
                        state = 1
                    else:
                        break
                except Exception as e:
                    print (e)
                    state = 2
                # Define data to write and trigger GUI event to write it
                data = [x, state]
                window.write_event_value("-ADC-THREAD-", data)
            # Cucle through each analog input. each loop is the next AI on the same board
            for y in analog:
                if y == 'EMPTY':
                    continue
                try:
                    # Take brackets off of the incoming data
                    value = str(board.read_single_ad8(analog[y]))[1:-1]
                    # Handle rare cases of getting non-numeric data back. Just redo until you get good data
                    while not value.isnumeric() and not y == "EMPTY":
                        value = str(board.read_single_ad8(analog[y]))[1:-1]
                except Exception as e:
                    print (e)
                    continue
                # If the value is a temperature, convert to degrees C
                if "Temp" in y:
                    value = str(round((float(value) * 110) / 255) - 30) + ' C'
                # If the value is a bilge sensor reading, convert to inces of water
                elif "Bilge" in y:
                    value = str(round((float(value) * 5 * 2.31 * 12) / 255)) + ' inches h20'
                # Define data to write and trigger GUI event to write it
                data = [y, value]
                window.write_event_value("-ANALOG-THREAD-", data)
        # close the socket connection to get ready for the next board
        sock.close()

# Arrange Collumns and Definte the GUI Window
layout = [[sg.Column(col1), sg.Column(col2), sg.VerticalSeparator(), sg.Column(col3), sg.VerticalSeparator(), sg.Column(col4)]]
window = sg.Window('BlackPearl Safety Network Monitoring Station', layout, resizable=True, size=(1600, 650))

# Start main Function Thread. The GUI requires its onw dedicated thread, so anything else needs to be on a different thread
threading.Thread(target=the_thread, args=(window,), daemon=True).start()

# Function for toggling buttons
def buttonToggle(button, address, relayIndex):
    # I'm using spaces at the end of the button text to know whether it's toggled on or not.
    # ToDo:  Read state from relay board instead
    if not window[button].get_text()[-1] == " ":
        window[button].update(text = button + ' ', button_color='red')
    else:
        window[button].update(text = button, button_color='green')
    sendRelay(address, relayIndex)

# Function for sending realy toggle commmands
def sendRelay(address, relayIndex):
    # Define the board and connection params, then connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    board = ncd_industrial_relay.Relay_Controller(sock)
    try:
        sock.connect((address, port))
    except Exception as e:
        print (e)
    # Toggles relay then close the socket and sleep for a bit(sleep is for the master toggle buttons to go slower)
    board.toggle_relay_by_index(relayIndex)
    sock.close()
    sleep(.05)

while True:
    # Reads the GUI for events and data
    event, values = window.read()
    # Close button event
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    # Digital Input event to update texts
    elif event == "-ADC-THREAD-":
        key, currentState = values[event]
        window[key].update(text_color=COLORS[currentState])
    # Analog Input event to update texts
    elif event == "-ANALOG-THREAD-":
        key, currentState= values[event]
        window[key].update(str(key) + '  :  ' + currentState)
    # Event for unlock button
    elif event == "UNLOCK RELAY BUTTONS":
        threading.Thread(target=timer_thread, args=(window,), daemon=True).start()
    # Event for master mdpe toggle
    elif event == "TOGGLE ALL MDPES":
        # All buttons for mdpes
        mdpe_buttons = [list(RELAYS[5])[0], list(RELAYS[5])[1], list(RELAYS[5])[2], list(RELAYS[5])[3]]
        # Address for relay board connected to all mdpes
        address = '192.168.10.36'
        # Indexes of mdpe relays on the realy board with the above address
        indexes = [1,2,3,4]
        # Toggle all mdpe relays
        for mdpe_button, index in zip(mdpe_buttons, indexes):
            buttonToggle(mdpe_button, address, index)
    # Event for master genset toggle
    elif event == "TOGGLE ALL GENSETS":
        # All buttons for gensets
        gen_buttons = [list(RELAYS[6])[0], list(RELAYS[6])[1], list(RELAYS[6])[2]]
        # Address for relay board connected to all gensets
        address = '192.168.10.37'
        # Indexes of genset relays on the realy board with the above address
        indexes = [1,2,3]
        for gen_button in gen_buttons:
            buttonToggle(gen_button, address, index)
    elif event == "TOGGLE ALL GEARBOXES":
        # All buttons for gearboxes
        gear_buttons = [list(RELAYS[5])[4], list(RELAYS[5])[5], list(RELAYS[5])[6], list(RELAYS[5])[7]]
        # Address for relay board connected to all gearboxes
        address = '192.168.10.36'
        # Indexes of gearbox relays on the realy board with the above address
        indexes = [5,6,7,8]
        # Toggle all genset relays
        for gear_button, index in zip(gear_buttons, indexes):
            buttonToggle(gear_button, address, index)
    # Individual relay buttons
    elif event == list(RELAYS[0])[0]:
        button = list(RELAYS[0])[0]
        buttonToggle(button, '192.168.10.31', 1)
    elif event == list(RELAYS[5])[0]:
        button = list(RELAYS[5])[0]
        buttonToggle(button, '192.168.10.36', 1)
    elif event == list(RELAYS[5])[1]:
        button = list(RELAYS[5])[1]
        buttonToggle(button, '192.168.10.36', 2)
    elif event == list(RELAYS[5])[2]:
        button = list(RELAYS[5])[2]
        buttonToggle(button, '192.168.10.36', 3)
    elif event == list(RELAYS[5])[3]:
        button = list(RELAYS[5])[3]
        buttonToggle(button, '192.168.10.36', 4)
    elif event == list(RELAYS[5])[4]:
        button = list(RELAYS[5])[4]
        buttonToggle(button, '192.168.10.36', 5)
    elif event == list(RELAYS[5])[5]:
        button = list(RELAYS[5])[5]
        buttonToggle(button, '192.168.10.36', 6)
    elif event == list(RELAYS[5])[6]:
        button = list(RELAYS[5])[6]
        buttonToggle(button, '192.168.10.36', 7)
    elif event == list(RELAYS[5])[7]:
        button = list(RELAYS[5])[7]
        buttonToggle(button, '192.168.10.36', 8)
    elif event == list(RELAYS[6])[0]:
        button = list(RELAYS[6])[0]
        buttonToggle(button, '192.168.10.37', 1)
    elif event == list(RELAYS[6])[1]:
        button = list(RELAYS[6])[1]
        buttonToggle(button, '192.168.10.37', 2)
    elif event == list(RELAYS[6])[2]:
        button = list(RELAYS[6])[2]
        buttonToggle(button, '192.168.10.37', 3)
    elif event == list(RELAYS[6])[3]:
        button = list(RELAYS[6])[3]
        buttonToggle(button, '192.168.10.37', 4)
window.close()