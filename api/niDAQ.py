from ctypes import sizeof
import nidaqmx
from nidaqmx.task import AUTO_START_UNSET
import numpy as np
from numpy.lib import average
from scipy import signal
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType, DataJustification, TaskMode

class nidaqController:

    def __init__(self) -> None:

        self.DEFAULT_AVERAGING = 7
        self.DEFAULT_FREQUENCY = 20
        self.DEFAULT_AMPLITUDE = 0.02
        self.DEFAULT_SQUARE_WAVE_DUTY_CYCLE = 0.5
        self.DEFAULT_HOLDING_VOLTAGE = 0

        self.Averaging = self.DEFAULT_AVERAGING
        self.frequency = self.DEFAULT_FREQUENCY
        self.amplitude = self.DEFAULT_AMPLITUDE
        self.square_wave_duty_cycle = self.DEFAULT_SQUARE_WAVE_DUTY_CYCLE
        
        self.holding_voltage = self.DEFAULT_HOLDING_VOLTAGE
        self.Proportion = self.DEFAULT_SQUARE_WAVE_DUTY_CYCLE # not defined
        self.multiclamp_args = [50, 2000] #[2.5e9, 0.1]] #default / 1 ?

        self.t = np.linspace(0, 1 / self.frequency * self.Averaging, 1000, endpoint=False) # parameter: 0, 1/frequency * Averaging, samples 
        self.s = signal.square(2 * np.pi * self.frequency * self.t, duty=self.square_wave_duty_cycle)# the first parameter is 2 * np.pi * frequency * t
        
        self.squarewave = []
        for i in self.s:
            i = i + 1
            self.squarewave.append(i * self.amplitude / 2 * self.multiclamp_args[0])

        self.waveform_data = self.squarewave
        self.waveform_duration = 0.35 #unit? dx?

        self.Sample_number = 1000 
        self.Sample_clock_rate = 1000
        self.Timeout = 1000
    


    def set_averaging(self, avg) -> None:
        self.Averaging = avg

    def set_frequency(self, frq) -> None:
        self.frequency = frq

    def set_amplitude(self, amp) -> None:
        self.amplitude = amp

    def set_holding_voltage(self, v) -> None:
        self.holding_voltage = v
        
    def gen_new_squarewave(self) -> None:
        self.t = np.linspace(0, 1 / self.frequency * self.Averaging, 1000, endpoint=False) # parameter: 0, 1/frequency * Averaging, samples 
        self.s = signal.square(2 * np.pi * self.frequency * self.t, duty=self.square_wave_duty_cycle)# the first parameter is 2 * np.pi * frequency * t
        
        self.squarewave = []
        for i in self.s:
            i = i + 1
            self.squarewave.append(i * self.amplitude / 2 * self.multiclamp_args[0])

        self.waveform_data = self.squarewave
        self.waveform_duration = 1 / self.frequency * self.Averaging #unit? dx?

    def set_clamp_args(self, opt) -> None:
        if (opt not in range(0, 2)): return
        if (opt == 0): self.multiclamp_args = [50, 2000]
        else: self.multiclamp_args = [2.5e9, 0.1]
    

    def set_clock_args(self, samples, rate) -> None:
        self.Sample_number = samples 
        self.Sample_clock_rate = rate

    # generate square waveform

    def filter(self, step_length): # not complete yet
        print("wave filter")
        sum = 0
        win = []
        for i in self.squarewave:
            win.append(self.squarewave[i])
            if len(win) > step_length:
                tmp = win.pop(0)
                sum = sum - tmp
            self.squarewave[i] = sum / step_length

    def get_data(self) -> list:
        with nidaqmx.Task() as master_task, nidaqmx.Task() as slave_task:

            master_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            slave_task.ao_channels.add_ao_voltage_chan("Dev1/ao0") 

            master_task.timing.cfg_samp_clk_timing(
                                                    self.Sample_clock_rate, 
                                                    sample_mode=AcquisitionType.FINITE, 
                                                    samps_per_chan= self.Sample_number) 

            slave_task.timing.cfg_samp_clk_timing(
                                                    self.Sample_clock_rate, 
                                                    sample_mode=AcquisitionType.FINITE, 
                                                    samps_per_chan= self.Sample_number) 

            slave_task.write(
                            self.waveform_data, 
                            auto_start = AUTO_START_UNSET,
                            timeout = self.waveform_duration * 2 + 5
                            ) 


            slave_task.control(TaskMode.TASK_COMMIT)  # analog output port is committed

            master_task.control(TaskMode.TASK_COMMIT)  # analog input port is committed

            slave_task.start()
            master_task.start()

            data = master_task.read(
                                    number_of_samples_per_channel = self.Sample_number,
                                    timeout = self.waveform_duration * 2 + 5
                                    # not decided yet
                                    )
            
            # print(data)


            data[:] = [x * self.multiclamp_args[1] for x in data]

            slave_task.wait_until_done(
                                        timeout = self.waveform_duration * 2 + 5)

            master_task.wait_until_done(
                                        timeout = self.waveform_duration * 2 + 5)

            master_task.stop()
            slave_task.stop()

            # master_task.close()
            # slave_task.close()

            # function hasn't be complete yet
            # self.filter(10)
            

            data1 = data

            sum = 0
            win = []
            for i in range(0, len(data1)):
                win.append(data1[i])
                sum += data1[i]
                if len(win) > 10:
                    tmp = win.pop(0)
                    sum = sum - tmp
                data1[i] = sum / 10


            #cal resistence form

            data_avg = np.average(data) # mean

            data1[:] = [data_avg - x for x in data1] 

            data1[:] = [(self.amplitude * 1000000) / x for x in data1] #waveform graph && resistence2

            # print(data) #resistence form2

            # cal resistence
 
            """ 
            import numpy as np
            arr = np.array([1, 2, 3, 4, 5, 6])
            newarr = np.array_split(arr, 3)
            print(newarr)

            """

            data_form = np.array_split(data, self.Averaging)
            

            # print(data_form)

            data_mean = []

            for i in range (0, self.Averaging):
                """ 
                A = [1,2,3,4,5,6]
                B = A[:len(A)//2]
                C = A[len(A)//2:] 
                method
                """
                # print(data_form[i].size)
                cur_data = data_form[i]
                # print(cur_data)
                f_data = cur_data[:len(cur_data)//2] # preceding half waveform
                b_data = cur_data[len(cur_data)//2:] # rest half waveform

                # print(f_data)

                split_arg = int((1 - self.Proportion) * (len(cur_data) / 2)) # comfirm the args

                # print(split_arg, len(f_data), len(b_data))

                """ 
                output = [1,2,3]
                print(output[-2:])
                """

                # print(f_data)

                fb_data = f_data[split_arg : len(f_data)]
                bb_data = b_data[split_arg : len(b_data)] #??


                # print(fb_data)

                fb_data_avg = np.average(fb_data)
                bb_data_avg = np.average(bb_data)


                data_mean.append(fb_data_avg - bb_data_avg)
            
            new_data_mean = np.average(data_mean)

            #print(new_data_mean)

            resistence = self.amplitude * 1000000 / new_data_mean #resistence

            d = {"resistence2" : 0, "resistence" : 0}
            d['resistence2'] = data[0]
            d['resistence'] = resistence


            return d


if __name__ == '__main__':
    testObj = nidaqController()
    for i in range(0, 1):
        print(testObj.get_data())

    
    




