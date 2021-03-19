import serial
from time import sleep

def main():
    current_prices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    last_prices = [1,4,3,3,5,6,7,8,9,10,11,12,13,14,15]

    alarm = False
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

    for idx in range(0,len(current_prices)):
        print("current:",current_prices[idx],", last:",last_prices[idx])
        if ((current_prices[idx] > last_prices[idx]) and alarm):
            ser.write('n'.encode())
            print('turn off light')
            alarm = False
        if ((current_prices[idx] < last_prices[idx]) and not alarm):
            ser.write('l'.encode())
            print("turn on light")
            alarm = True
        sleep(2)

    # while True:
    #     ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
    #     user_input = input("Enter something:")
    #     if user_input == "a":
    #         ser.write('a'.encode())
    #     if user_input == "s":
    #         ser.write('s'.encode())
    #     if user_input == "quit":
    #         break

if __name__ == '__main__':
    main()
    