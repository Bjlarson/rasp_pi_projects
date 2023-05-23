from machine import Pin, UART

# Configure UART
uart = UART(1, baudrate=9600, tx=None, rx=Pin(7))  # Replace Pin(1) with the appropriate UART RX pin

# Receiving loop
while True:
    # Read data from UART
    data = uart.readline()

    # Decode and process received data
    if data:
        received_data = str(data, 'utf-8').strip()
        variables = received_data.split(',')
        if len(variables) == 4:
            var1 = int(variables[0])
            var2 = int(variables[1])
            var3 = int(variables[2])
            var4 = int(variables[3])

            # Process the received variables
            # ...
