import time, serial

class Controller(object):
    def __init__(self):
        self.serial_option = {
                'port': 'test', 'baudrate': self.baudrate, 'parity': self.parity, 'stopbits': self.stopbits, 
                'bytesize': serial.EIGHTBITS
            }
        self.delimiter = '\r\n'

    def __enter__(self):
        self.log_on()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.log_off()

    def log_on(self):
        if self.serial_option['port'] == 'test':
            return
        """serial port handle"""
        self.ser = serial.Serial(
            **self.serial_option
        )

    def log_off(self):
        if self.serial_option['port'] == 'test':
            return
        """close the port"""
        self.ser.close()

    def send_command(self, command):
        if self.serial_option['port'] == 'test':
            print(command)
            return
        """ Send a text command"""
        self.ser.write((command+'\r\n').encode())
        time.sleep(0.2)
        message = self.ser.read(self.ser.inWaiting()).decode()
        tle = 0
        while not message:
            time.sleep(0.2)
            message = self.ser.read(self.ser.inWaiting()).decode()
            print('waiting for reply...')
            tle = tle + 0.2
            if tle > 2 :
                break~
        print (command, message)
        return message


class PriorES10ZE(Controller):
    def __init__(self, serial_option = dict()):
        self.serial_option = {
                'port': 'COM9', 'baudrate': 9600, 'parity': serial.PARITY_NONE, 'stopbits': serial.STOPBITS_ONE, 
                'bytesize': serial.EIGHTBITS
            }
        self.serial_option.update(serial_option)
        self.position_list = [
                -1500, ## useless 
                -1370, -290, -120, -43, -51
            ]

if __name__ == '__main__':
    p = PriorES10ZE()
    p.log_on()
    p.send_command('C 100')
    p.send_command('U')
    res = p.send_command('$')
    print(res)