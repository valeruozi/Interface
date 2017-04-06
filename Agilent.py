
import visa
import numpy as np
import matplotlib.pyplot as plt


class HP4294A:
    def __init__(self,myinst):
        self.myinst = myinst
        
    def inizialize(self):
        '''Timeout set at 5 sec'''
        self.myinst.timeout = 5000 #it has to be longer than any operation
        self.myinst.read_termination = '\n'
        self.myinst.write_termination = '\n'
        '''Get and display the device IDN'''
        self.Idn = self.myinst.query("*IDN?") 
        print ("Device IDN: ", self.Idn)
        '''Clear status and load the default setup'''
        self.myinst.write("*CLS")
        self.myinst.write("*RST")
        '''Set the ASCII format as the data transfer format'''
        self.myinst.write("FORM4") 

    def check_errors(self):
        '''Reads out the oldest error among errors stored in the error queue of the 4294A. The size of the error queue is 10'''
        self.Errors = self.myinst.query("OUTPERRO?")
        print ("Errors: ", self.Errors)
#    
    def trigger(self,trig,numbert):
        self.trig = trig
        self.numbert = numbert
        if self.trig == 'internal':
            self.myinst.write("TRGS INT")
        elif self.trig == 'external':
            self.myinst.write("TRGS EXT")
        elif self.trig == 'bus':
            self.myinst.write("TRGS BUS")
            
        if self.numbert == 'single':
            self.myinst.write("SING")
        elif self.numbert == 'continuous':
            self.myinst.write("CONT")
            
        '''If the trigger is set to BUS it needs the execution command'''
        if self.trig == 'bus':
            self.myinst.write("*TRG")
        pass
    
    def hold(self):
        self.myinst.write("HOLD")
        pass
   
    def calibration(self,cal):
        
        '''Selects the adapter in the adapter setting'''
        adapter = myinst.query("E4TP?")
        
        if adapter == 'NONE':
            if cal == "open":
                self.myinst.write("CALA")
            elif cal == "short":
                self.myinst.write("CALB")
            elif cal == "load":
                self.myinst.write("CALC")
                
#        elif adapter == 'M2': #Adapter 16494F #No compensation if Adapter is connected
#            if cal == "phase":
#                self.myinst.write("ECALP")
#            elif cal == "load":
#                self.myinst.write("ECALC")
#            elif cal == "open":          #Not needed for adapter M2
#                self.myinst.write("ECALA")
#            elif cal == "short":
#                self.myinst.write("ECALB")
        pass
 
    def get_measure(self,sweep,number_type):
        self.sweep = sweep
        self.number_type = number_type
        '''Sets the value of Instrument Event Status Enable Register '''
        self.myinst.write("ESNB 1")
        '''Sets the value of the Service Request Enable Register.'''
        self.myinst.write("*SRE 4")
        
        if self.number_type == 'absolute':
            self.myinst.write("MEAS IMPH")
        elif self.number_type == 'complex':
            self.myinst.write("MEAS COMP")
        
        self.sweep1 = sweep
        
        '''Sets the graphs type'''
        if self.sweep1.scale_type == "linear":
            self.myinst.write("SWPT LIN")
        elif self.sweep1.scale_type == "log":
            self.myinst.write("SWPT LOG")
            
        '''Sets the sweep type'''
        if self.sweep1.sweep_type == "span":
            self.myinst.write("CENT " + self.sweep1.center)
            self.myinst.write("SPAN " + self.sweep1.span)
        elif self.sweep1.sweep_type == "start_stop":
            self.myinst.write("STAR " + self.sweep1.start)
            self.myinst.write("STOP " + self.sweep1.stop)
        
        self.myinst.write("POIN " + str(self.sweep1.npoints))
        
        '''Enables/disables the vertically separate display for traces A and B.'''
        self.myinst.write("SPLD OFF")
        
        '''Specifies the frequency sweep'''
        self.myinst.write("SWPP FREQ")
        
        '''Sets the active trace.'''
        self.myinst.write("TRAC A")
        
        '''Start of the sweep'''
        self.myinst.write("SING")
        
        '''Reads out the values of all measurement points in a data trace array (refer to “Internal data arrays” on page 81). (Query only)'''
        self.Values = self.myinst.query("OUTPDTRC?")
        self.Measure1 = eval(self.Values)
        self.Measure2 = [str(x) for x in self.Measure1]
        self.Measure3= np.array(self.Measure2)
        
        self.A = self.Measure3[0:200:2]
#        self.A = self.A.tolist()
        
        '''Sets the active trace.'''
        self.myinst.write("TRAC B")
        
        '''Start of the sweep'''
        self.myinst.write("SING")
        
        '''Reads out the values of all measurement points in a data trace array (refer to “Internal data arrays” on page 81). (Query only)'''
        self.Values = self.myinst.query("OUTPDTRC?")
        self.Measure1 = eval(self.Values)
        self.Measure2 = [str(x) for x in self.Measure1]
        self.Measure3= np.array(self.Measure2)
        
        self.B = self.Measure3[0:200:2]
#        self.B = self.B.tolist()
        
        self.measuref = Measure(self.A,self.B)
        return self.measuref
    
class Measure: 
    def __init__(self,A,B):
        self.A = A
        self.B = B

class Sweep: 
    def __init__(self,a,b,npoints,sweep_type,scale_type): #Unit Hz
        self.start = a
        self.stop = b 
        self.center = a
        self.span = b
        self.npoints = npoints
        '''Sets the sweep type'''
        self.sweep_type = sweep_type 
        self.scale_type = scale_type

rm = visa.ResourceManager()
resources = rm.list_resources()
print ("Resources avaiable: ", resources)
#gpib_adress = raw_input("Type the choosen resource name: ") #"GPIB:17::INSTR"
#myinst = rm.get_instrument(gpib_adress)
myinst = rm.get_instrument("GPIB0::17::INSTR")  #addr of the instrument, found on visa's resources
impAnalyzer = HP4294A(myinst)
impAnalyzer.inizialize()
impAnalyzer.check_errors()
impAnalyzer.calibration('load')
#load = myinst.query("OUTPCOMC3?")
impAnalyzer.check_errors()
impAnalyzer.trigger('internal','single')
sweep1 = Sweep('40HZ','1MHZ',100,'start_stop','log')
measure1 = impAnalyzer.get_measure(sweep1,'amplitude')
impAnalyzer.check_errors()
Results = [measure1.A, measure1.B]

'''Results plot'''
freq = np.linspace(40,1000000,100)

plt.figure(1)
plt.subplot(211)
plt.plot(freq,Results[0])
plt.ylabel('Results[0]')
plt.show()

plt.subplot(212)
plt.plot(freq,Results[1])
plt.ylabel('Results[1]')
plt.show()