import serial

def main():
    while True:
        ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        user_input = input("Enter something:")
        if user_input == "a":
            ser.write('a'.encode())
        if user_input == "s":
            ser.write('s'.encode())
        if user_input == "quit":
            break

if __name__ == '__main__':
    main()
    