import ctypes
import sys
import os.path

NO_USBDAQ = -1
DevIndex_Overflow = -2
Bad_Firmware = -3
USBDAQ_Closed = -4
Transfer_Data_Fail = -5
NO_Enough_Memory = -6
Time_Out = -7
Not_Reading = -8

class SmacqException(Exception):
    def __init__(self, err = 'SmacqException'):
        Exception.__init__(self, err)

class NoUSBDAQ(SmacqException):
    def __init__(self, err = 'NO_USBDAQ'):
        SmacqException.__init__(self, err)

class DevIndexOverflow(SmacqException):
    def __init__(self, err = 'DevIndex_Overflow'):
        SmacqException.__init__(self, err)

class BadFirmware(SmacqException):
    def __init__(self, err = 'Bad_Firmware'):
        SmacqException.__init__(self, err)

class USBDAQClosed(SmacqException):
    def __init__(self, err = 'USBDAQ_Closed'):
        SmacqException.__init__(self, err)

class TransferDataFail(SmacqException):
    def __init__(self, err = 'Transfer_Data_Fail'):
        SmacqException.__init__(self, err)

class NOEnoughMemory(SmacqException):
    def __init__(self, err = 'NO_Enough_Memory'):
        SmacqException.__init__(self, err)

class TimeOut(SmacqException):
    def __init__(self, err = 'Time_Out'):
        SmacqException.__init__(self, err)

class NotReading(SmacqException):
    def __init__(self, err = 'Not_Reading'):
        SmacqException.__init__(self, err)


def SmacqCustomizeRaise( error_code ):
    if error_code == NO_USBDAQ:
        raise NoUSBDAQ()
    elif error_code == DevIndex_Overflow:
        raise DevIndexOverflow()
    elif error_code == Bad_Firmware:
        raise BadFirmware()
    elif error_code == USBDAQ_Closed:
        raise USBDAQClosed()
    elif error_code == Transfer_Data_Fail:
        raise TransferDataFail()
    elif error_code == NO_Enough_Memory:
        raise NOEnoughMemory()
    elif error_code == Time_Out:
        raise TimeOut()
    elif error_code == Not_Reading:
        raise NotReading()
    else:
        print("processing......")


""" if __name__ == '__main__':
    for num in range(-8, 0):
        try:
            SmacqCustomizeRaise( num )
        except SmacqException as e:
            print( e )
        else:
            print("processing...")
 """
class SmacqController:

    def __init__(self) -> None:
        self.dllName = "gusb.dll"
        self.DevIndex = 0
        self.Range = 10
        self.SampleRate = 1000
        self.TrigSource = 0
        self.Trig = 1
        self.DioChanSel = 255
        self.ResetVolt = 0
        self.ResetDioOut = 0
        self.ResetTrig = 0
        self.DANum = 0
        self.ChSel = 1


        # DioOut = 96 # 01100000
        # High_Pressure_Dio_Out = 96       # 01100000
        # High_Minus_Pressure_Dio_Out = 72 # 01001000
        # Low_Pressure_Dio_Out = 16        # 00010000
        # Low_Minus_Pressure_Dio_Out = 4   # 00000100
        self.DioOut = {0 : 96, 1 : 72, 2 : 16, 3 : 4}
        self.ChaSel = {0 : 1, 1 : 2, 2 : 4, 3 : 8}

        self.dllABSPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + self.dllName
        try:
            self.lib = ctypes.cdll.LoadLibrary(self.dllABSPath)
        except FileNotFoundError:
            print("dll not found!")
            sys.exit(1)


        # init work
    def open_device_and_init_avgs(self) -> None:
        try:
            SmacqCustomizeRaise(
                self.lib.OpenDevice(
                    ctypes.c_int(self.DevIndex)))

            SmacqCustomizeRaise(
                self.lib.SetUSB2AiRange(
                    ctypes.c_int(self.DevIndex),
                    ctypes.c_float(self.Range)))

            SmacqCustomizeRaise(
                self.lib.SetSampleRate(
                    ctypes.c_int(self.DevIndex), 
                    ctypes.c_uint(self.SampleRate)))

            SmacqCustomizeRaise(
                self.lib.SetTrigSource(
                    ctypes.c_int(self.DevIndex), 
                    ctypes.c_ubyte(self.TrigSource)))

            SmacqCustomizeRaise(
                self.lib.SetSoftTrig(
                    ctypes.c_int(self.DevIndex), 
                    ctypes.c_ubyte(self.Trig)))

            SmacqCustomizeRaise(
                self.lib.InitDA(
                    ctypes.c_int(self.DevIndex)))

        except SmacqException as e:
            print(e)
            sys.exit(1)
        else:
            print("device init successfully!")
    
    def input_process(self, DAVolt, DANum) -> float:
        if DANum == 0:
            return DAVolt / 3
        elif DANum == 1:
            return DAVolt / -1.004
        elif DANum == 2:
            return DAVolt * 2.564
        elif DANum == 3:
            return DAVolt * -2.294
        else:
            return 0

    def init_DA(self, DAVolt) -> None: #DANum = 0, 1, 2, 3; DAVolt = 0
        for i in range(0, 3):
            try:
                SmacqCustomizeRaise(
                    self.lib.SetDA(
                        ctypes.c_int(self.DevIndex),
                        ctypes.c_ubyte(i),
                        ctypes.c_float(self.input_process(DAVolt, i))))
            except SmacqException as e:
                print(e, " when init DA")
                os.exit(1)
    
    def change_DA(self, DANum, DAVolt) -> None:
        self.DANum = DANum
        try:
            SmacqCustomizeRaise(
                self.lib.SetDA(
                    ctypes.c_int(self.DevIndex),
                    ctypes.c_ubyte(DANum),
                    ctypes.c_float(self.input_process(DAVolt, DANum))))
        except SmacqException as e:
            print(e, " when change DA")
            os.exit(1)

    def start_read_pressure(self) -> None:
        try:
            SmacqCustomizeRaise(
                self.lib.StartRead(
                    ctypes.c_int(self.DevIndex)))
        except SmacqException as e:
            print(e, " when start read")
            os.exit(1)

    def set_pressure_channel(self, DANum):
        self.DANum = DANum
        try:
            SmacqCustomizeRaise(
                self.lib.SetDioOut(
                    ctypes.c_int(self.DevIndex), 
                    ctypes.c_uint(self.DioChanSel),
                    ctypes.c_uint(self.DioOut[DANum])))
        except SmacqException as e:
            print(e, " when set pressure channel")
            os.exit(1)

    def output_process(self, DAVolt, DANum) -> float:
        if DANum == 0:
            return DAVolt * 3
        elif DANum == 1:
            return DAVolt * -1.004
        elif DANum == 2:
            return DAVolt / 2.564
        elif DANum == 3:
            return DAVolt / -2.294
        else:
            return 0

    def read_data(self) -> float:    
        Num = 1
        data = ctypes.c_float * 1
        Ai = data()
        TimeOut = 1000

        try:
            SmacqCustomizeRaise(
                self.lib.GetAiChans(
                    ctypes.c_int(self.DevIndex),
                    ctypes.c_ulong(Num), 
                    ctypes.c_short(self.ChSel), 
                    Ai, TimeOut))
        except SmacqException as e:
            print(e, " when read data")
            self.stop_process()
            os._exit(1)

        return self.output_process(Ai[0], self.DANum)

    def reset_DA(self) -> None:
        for i in range(0, 3):
            try:
                SmacqCustomizeRaise(
                    self.lib.SetDA(
                        ctypes.c_int(self.DevIndex),
                        ctypes.c_ubyte(self.DANum),
                        ctypes.c_float(self.ResetVolt)))

            except SmacqException as e:
                print(e, " when stop precess")
                self.lib.CloseDevice(ctypes.c_int(self.DevIndex))

    def stop_process(self) -> None:
        try:
            SmacqCustomizeRaise(
                self.lib.SetDioOut(
                    ctypes.c_int(self.DevIndex), 
                    ctypes.c_uint(self.DioChanSel),
                    ctypes.c_uint(self.ResetDioOut)))

            SmacqCustomizeRaise(
                self.lib.StopRead(
                    ctypes.c_int(self.DevIndex)))

            SmacqCustomizeRaise(
                self.lib.SetSoftTrig(
                    ctypes.c_int(self.DevIndex),
                    ctypes.c_ubyte(self.ResetTrig)))

            SmacqCustomizeRaise(
                self.lib.ClearTrigger(
                    ctypes.c_int(self.DevIndex)))

            SmacqCustomizeRaise(
                self.lib.ClearBufs(
                    ctypes.c_int(self.DevIndex)))

        except SmacqException as e:
            print(e, " when stop precess")
            self.lib.CloseDevice(ctypes.c_int(self.DevIndex))

        self.lib.CloseDevice(ctypes.c_int(self.DevIndex))   

testObj = SmacqController()
num = 0
val = 0

if __name__ == '__main__':
    data = []
    testcase = SmacqController()
    testcase.open_device_and_init_avgs()
    testcase.init_DA(-2)

    testcase.start_read_pressure()
    testcase.set_pressure_channel(0)
    for i in range(0, 5):
        data.append(testcase.read_data())
    print(data)

    testcase.reset_DA()
    testcase.stop_process()