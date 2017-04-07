import zhinst.ziPython, zhinst.utils
import numpy as np
import time
import matplotlib.pyplot as plt


class HF2LI:
    def __init__(self, daq, device):
        self.daq = daq
        self.device = device
        self.meas = []
        self.R = []
        self.theta = []
        self.path = []
        self.A =  []
        self.B =  []

    def inizialize(self):
        """Disable all outputs and all demods"""
        general_setting = [
            [['/', self.device, '/demods/0/trigger'], 0],  # Demods = output 'trigger' of a demodulator
            [['/', self.device, '/demods/1/trigger'], 0],  # 0,1,2... all the bits are set to zero, meaning that the
            [['/', self.device, '/demods/2/trigger'], 0],  # demods data is sent continuously for all 6 demodulators
            [['/', self.device, '/demods/3/trigger'], 0],
            [['/', self.device, '/demods/4/trigger'], 0],
            [['/', self.device, '/demods/5/trigger'], 0],
            [['/', self.device, '/sigouts/0/enables/*'], 0],  # signal output, switches a channel of the mixer off
            [['/', self.device, '/sigouts/1/enables/*'], 0]
        ]
        self.daq.set(general_setting)

    def get_sweep(self, ndem, input1, sweep1, demodulator1,transimpedance1):  # start, stop, samplecount, frequency, tc, rate, bandwidth, order, loopcount, nsamples):
        self.frequency = 1e5  # es = 1e5
        self.auxout0 = str(0)
        self.auxout1 = str(1)
        self.input = input1
        self.sweep = sweep1
        self.demodulator = demodulator1
        self.transimpedance = transimpedance1
        self.ndem = ndem

        """Set mux test settings"""
        t1_sigIn_setting = [
            [['/', self.device, '/sigins/0/diff'], self.input[0].diff], #sigins = node of a signal input, diff = boolean value switching differential input mode # todo-vale da provare ad attivare
            [['/', self.device, '/sigins/0/imp50'], self.input[0].imp50], #boolean value enabling 50Ohm input impedance termination # todo-vale da provare ad attivare
            [['/', self.device, '/sigins/0/ac'], self.input[0].ac],  # ac = boolean value setting for AC coupling of the signal  input
            [['/', self.device, '/sigins/0/range'], 2 * self.input[0].amplitude], # voltage range of the signal input (max = 2)

            [['/', self.device, '/auxouts/', self.auxout0, '/outputselect'], 2],  # Output = R
            [['/', self.device, '/auxouts/', self.auxout1, '/outputselect'], 3],  # Output = Theta

            [['/', self.device, '/sigouts/0/on'], 0],  # signal output, switches a channel of the mixer off
            [['/', self.device, '/sigouts/1/on'], 0]
            # [['/', self.device, '/sigouts/',self.c,'/add'], 0], #switches the output adder off
            # [['/', self.device, '/sigouts/',self.c,'/on'], 1], #switches the output on
            # [['/', self.device, '/sigouts/',self.c,'/enables/',self.c], 1], #switches a channel of the mixer on
            # [['/', self.device, '/sigouts/',self.c,'/range'], 1], #selects the ouput range for the signal output
            # [['/', self.device, '/sigouts/',self.c,'/amplitudes/',self.c], self.amplitude], #fraction of the output range added to the output signal
        ]
        for i in range(0, self.ndem):
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/oscselect'],  i])
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/enable'], 1])
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/order'],
                                     self.demodulator[i].order])  # order of the low pass filter =12db/oct slope
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/timeconstant'],
                                     self.demodulator[i].tc])  # time constant fo the low pass filter (default = 0.010164)
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/rate'],
                                     self.demodulator[i].rate])  # number of the output values sent to the computer per second
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/adcselect'], i])
            t1_sigIn_setting.append([['/', self.device, '/demods/', str(i), '/harmonic'], 1])
            t1_sigIn_setting.append([['/', self.device, '/oscs/', str(i), '/freq'],self.frequency])
            

        if transimpedance != []: #devo mettere impostazioni diverse per ogni canale per ora le ho messe tutte uguali
            if transimpedance[0].nchannels == 2:
                t1_sigIn_setting.append([['/', self.device, '/sigins/1/diff'], self.input[1].diff])
                t1_sigIn_setting.append([['/', self.device, '/sigins/1/imp50'], self.input[1].imp50])
                t1_sigIn_setting.append([['/', self.device, '/sigins/1/ac'],self.input[1].ac])
                t1_sigIn_setting.append([['/', self.device, '/sigins/1/range'],2 * self.input[1].amplitude])
            for k in range(0,transimpedance[0].nchannels): 
                t1_sigIn_setting.append([['/', self.device, '/zctrls/',str(0),'/tamp/',str(k),'/offset'], self.transimpedance[k].offset])
                t1_sigIn_setting.append([['/', self.device, '/zctrls/',str(0),'/tamp/',str(k),'/voltagegain'], self.transimpedance[k].vgain])
                t1_sigIn_setting.append([['/', self.device, '/zctrls/',str(0),'/tamp/',str(k),'/dc'], self.transimpedance[k].dc])
#                t1_sigIn_setting.append([['/', self.device, '/zctrls/',str(k),'/camp/',str(k),'/r'], self.transimpedance[k].resistor])

        self.daq.set(t1_sigIn_setting)

        '''Wait 1s to get a settled lowpass filter'''
        time.sleep(10 * self.demodulator[0].tc)

        '''Clean queue'''
        self.daq.flush()

        self.sweeper = self.daq.sweep()

        # Configure the Sweeper Module's parameters.
        # Set the device that will be used for the sweep - this parameter must be set.
        self.sweeper.set('sweep/device', self.device)

        # Set the `start` and `stop` values of the gridnode value interval we will use in the sweep.
        self.sweeper.set('sweep/start', self.sweep.start)
        self.sweeper.set('sweep/stop', self.sweep.stop)
        # Set the number of points to use for the sweep, the number of gridnode
        # setting values will use in the interval (`start`, `stop`).
        self.sweeper.set('sweep/samplecount', self.sweep.samplecount)
        # Specify logarithmic spacing for the values in the sweep interval.
        self.sweeper.set('sweep/xmapping', 1)
        # Settiling time before measurement is performed
        self.sweeper.set('sweep/settling/time', 0)
        # The sweep/settling/inaccuracy' parameter defines the settling time the
        # sweeper should wait before changing a sweep parameter and recording the next
        # sweep data point. The settling time is calculated from the specified
        # proportion of a step response function that should remain. The value
        # provided here, 0.001, is appropriate for fast and reasonably accurate
        # amplitude measurements. For precise noise measurements it should be set to
        # ~100n.
        # Note: The actual time the sweeper waits before recording data is the maximum
        # time specified by sweep/settling/time and defined by
        # sweep/settling/inaccuracy.
        self.sweeper.set('sweep/settling/inaccuracy', 0.001)
        # Sets the bandwidth overlap mode (default 0). If enabled, the bandwidth of
        # a sweep point may overlap with the frequency of neighboring sweep
        # points. The effective bandwidth is only limited by the maximal bandwidth
        # setting and omega suppression. As a result, the bandwidth is independent
        # of the number of sweep points. For frequency response analysis bandwidth
        # overlap should be enabled to achieve maximal sweep speed (default: 0). 0 =
        # Disable, 1 = Enable.
        self.sweeper.set('sweep/bandwidthoverlap', 0)
        # Sequential scanning mode (as opposed to binary or bidirectional).
        self.sweeper.set('sweep/scan', 0)
        # Set the minimum time to record and average data to 10 demodulator
        # filter time constants.
        self.sweeper.set('sweep/averaging/tc', 10)

        for i in range(0, self.ndem):
            self.osc_index = i
            # Specify the `gridnode`: The instrument node that we will sweep, the device
            # setting corresponding to this node path will be changed by the sweeper.
            self.sweeper.set('sweep/gridnode', 'oscs/%d/freq' % self.osc_index)
            # Automatically control the demodulator bandwidth/time constants used.
            # 0=manual, 1=fixed, 2=auto
            # Note: to use manual and fixed, sweep/bandwidth has to be set to a value > 0.
            self.sweeper.set('sweep/bandwidthcontrol', self.demodulator[i].bandwidth)
            # Specify the number of sweeps to perform back-to-back.
            self.sweeper.set('sweep/loopcount', self.demodulator[i].loopcount)
            # Minimal number of samples that we want to record and average is 100. Note,
            # the number of samples used for averaging will be the maximum number of
            # samples specified by either sweep/averaging/tc or sweep/averaging/sample.
            self.sweeper.set('sweep/averaging/sample', self.demodulator[i].nsamples)
            # Now subscribe to the nodes from which data will be recorded. Note, this is
            # not the subscribe from ziDAQServer; it is a Module subscribe. The Sweeper
            # Module needs to subscribe to the nodes it will return data for.x
            self.path.append('/%s/demods/%d/sample' % (self.device, i))
            self.sweeper.subscribe(self.path[i])
            # Start the Sweeper's thread.
            self.sweeper.execute()

            self.start = time.time()
            self.timeout = 120  # [s]
            print "Will perform ", self.demodulator[i].loopcount, "sweeps with demodulator", i+1, "of", self.ndem
            while not self.sweeper.finished():  # Wait until the sweep is complete, with timeout.
                time.sleep(1)
                progress = self.sweeper.progress()
                print("Individual sweep progress: {:.2%}.".format(progress[0]))
                if (time.time() - self.start) > self.timeout:
                    # If for some reason the sweep is blocking, force the end of the measurement.
                    print("\nSweep still not finished, forcing finish...")
                    self.sweeper.finish()
            print("")
            # Read the sweep data. This command can also be executed whilst sweeping
            # (before finished() is True), in this case sweep data up to that time point
            # is returned. It's still necessary still need to issue read() at the end to
            # fetch the rest.
            return_flat_dict = True
            self.data = self.sweeper.read(return_flat_dict)
            self.sweeper.unsubscribe(self.path[i])

            # Stop the sweeper thread and clear the memory.
            # Check the dictionary returned is non-empty.
            assert self.data, "read() returned an empty data dictionary, did you subscribe to any paths?"
            # Note: data could be empty if no data arrived, e.g., if the demods were
            # disabled or had rate 0.
            # return self.data
            assert self.path[i] in self.data, "No sweep data in data dictionary: it has no key '%s'" % self.path
            self.samples = self.data[self.path[i]]
            print
            "Returned sweeper data contains", len(self.samples), "sweeps."
            assert len(self.samples) == self.demodulator[i].loopcount, \
                "The sweeper returned an unexpected number of sweeps: `%d`. Expected: `%d`." % (
                len(self.samples), self.loopcount)
            del self.A[:]
            del self.B[:]
            for j in range(0, len(self.samples)):  # todo-vale da sistemare
                line1 = np.abs(self.samples[j][0]['x'] + 1j * self.samples[j][0]['y'])
                line2 = np.angle(self.samples[j][0]['x'] + 1j * self.samples[j][0]['y'])
                self.A.extend(line1)
                self.B.extend(line2)
            self.meas.append(Measure(self.A,self.B))
        return self.meas


    def do_plot(self):
        frequency = [] 
        for j in range(0,len(self.samples)):
            frequency.extend(self.samples[j][0]['frequency'])
        for i in range(0, self.ndem):
            plt.subplot(2, 1, 1)
            plt.semilogx(frequency, self.meas[i].A)
            plt.subplot(2, 1, 2)
            plt.semilogx(frequency, self.meas[i].B)
            plt.subplot(2, 1, 1)
            plt.title('Results of %d sweeps with demodulator %d.' %(len(self.samples),i+1))
            plt.grid(True)
            plt.ylabel(r'Demodulator R ($V_\mathrm{RMS}$)')
            plt.autoscale()
            plt.subplot(2, 1, 2)
            plt.grid(True)
            plt.xlabel('Frequency ($Hz$)')
            plt.ylabel(r'Demodulator Phi (radians)')
            plt.autoscale()
            plt.draw()
            plt.show()


class Measure:
    def __init__(self, A, B):
        self.A = A
        self.B = B


class Sweep:
    def __init__(self, a, b, samplecount):  # Unit Hz
        self.start = a
        self.stop = b
        self.center = a
        self.samplecount = samplecount

class inputC:
    def __init__(self, diff, imp50, ac, amplitude):
        self.diff = diff #if = 0 single-ended
        self.imp50 = imp50 # if = 0 high impedance
        self.ac = ac # if = 0 is dc
        self.amplitude = amplitude # voltage range of the signal input (max = 2)

class Demodulator:
    def __init__(self, tc, rate, bandwidth, order, loopcount, nsamples):
        self.tc = tc
        self.rate = rate
        self. bandwidth = bandwidth
        self.order = order
        self.loopcount = loopcount
        self.nsamples = nsamples

class HF2TA:
    def __init__(self, nchannels, offset, dc, vgain, resistor): # todo-vale non ho il comando per settare il resistore in tamp
        self.nchannels = nchannels
        self.offset = offset
        self.dc = dc
        self.vgain = vgain
        self.resistor = resistor


'''Open connection to ziServer'''  # Data Server Port = 8005
daq = zhinst.ziPython.ziDAQServer('localhost', 8005)
device = 'dev555'
LockIn = HF2LI(daq, device)
LockIn.inizialize()

input = []
input.append(inputC(0,1,0,1)) #1
input.append(inputC(0,1,0,1)) #2

sweep1 = Sweep(1e3, 1e6, 10)

ndemodulators = 3
demodulator = []
demodulator.append(Demodulator( 0.01, 200, 2, 8, 1, 100)) #1
demodulator.append(Demodulator( 0.01, 200, 2, 8, 1, 100)) #2
demodulator.append(Demodulator( 0.01, 200, 2, 8, 1, 100)) #3

transimpedance = []
transimpedance.append(HF2TA(2, 10, 1, 10, 10000)) # ch1
transimpedance.append(HF2TA(2, 0, 0, 1, 1000)) # ch2

measure1 = LockIn.get_sweep(ndemodulators, input, sweep1, demodulator, transimpedance)
ResultsA = []
ResultsB = []
for i in range(0,ndemodulators):
    ResultsA.append(measure1[i].A)
    ResultsB.append(measure1[i].B)
Results = [ResultsA, ResultsB]

LockIn.do_plot()

# todo-vale Settare reference mode auto o internal





