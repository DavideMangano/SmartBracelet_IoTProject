print "********************************************";
print "*                                          *";
print "*             TOSSIM Script                *";
print "*                                          *";
print "********************************************";

import sys;
import time;

from TOSSIM import *;

t = Tossim([]);

topofile="topology.txt";
modelfile="meyer-heavy.txt";


print "Initializing mac....";
mac = t.mac();
print "Initializing radio channels....";
radio=t.radio();
print "    using topology file:",topofile;
print "    using noise file:",modelfile;
print "Initializing simulator....";
t.init();


#simulation_outfile = "simulation.txt";
#print "Saving sensors simulation output to:", simulation_outfile;
#simulation_out = open(simulation_outfile, "w");

#out = open(simulation_outfile, "w");
out = sys.stdout;

#Add debug channel
print "Activate debug message on channel Pairing"
t.addChannel("Pairing",out);
print "Activate debug message on channel boot"
t.addChannel("boot",out);
print "Activate debug message on channel PairingSent1"
t.addChannel("PairingSent1",out);
print "Activate debug message on channel Radio"
t.addChannel("Radio",out);
print "Activate debug message on channel PairingSent2"
t.addChannel("PairingSent2",out);
print "Activate debug message on channel InfoTimer"
t.addChannel("InfoTimer",out);
print "Activate debug message on channel MissingTimer"
t.addChannel("MissingTimer",out);
print "Activate debug message on channel Info"
t.addChannel("Info",out);
print "Activate debug message on channel Sent"
t.addChannel("Sent",out);
print "Activate debug message on channel OperationalMode"
t.addChannel("OperationalMode",out);
print "Activate debug message on channel pairingEnd1"
t.addChannel("pairingEnd1",out);
print "Activate debug message on channel pairingEnd2"
t.addChannel("pairingEnd2",out);
print "Activate debug message on channel Sensors"
t.addChannel("Sensors",out);
print "Activate debug message on channel Radio_pack"
t.addChannel("Radio_pack",out);
print "Activate debug message on channel Receive"
t.addChannel("Receive",out);
print "Activate debug message on channel PairingCompleted"
t.addChannel("PairingCompleted",out);
print "Activate debug message on channel Try"
t.addChannel("try",out);

print "Creating node 1...";
node1 =t.getNode(1);
time1 = 0*t.ticksPerSecond();
node1.bootAtTime(time1);
print ">>>Will boot at time",  time1/t.ticksPerSecond(), "[sec]";

print "Creating node 2...";
node2 = t.getNode(2);
time2 = 1*t.ticksPerSecond();
node2.bootAtTime(time2);
print ">>>Will boot at time", time2/t.ticksPerSecond(), "[sec]";

print "Creating node 3...";
node3 =t.getNode(3);
time3 = 0*t.ticksPerSecond();
node3.bootAtTime(time3);
print ">>>Will boot at time",  time3/t.ticksPerSecond(), "[sec]";

print "Creating node 4...";
node4 = t.getNode(4);
time4 = 1*t.ticksPerSecond();
node4.bootAtTime(time4);
print ">>>Will boot at time", time4/t.ticksPerSecond(), "[sec]";

print "Creating radio channels..."
f = open(topofile, "r");
lines = f.readlines()
for line in lines:
  s = line.split()
  if (len(s) > 0):
    print ">>>Setting radio channel from node ", s[0], " to node ", s[1], " with gain ", s[2], " dBm"
    radio.add(int(s[0]), int(s[1]), float(s[2]))


#Creazione del modello di canale
print "Initializing Closest Pattern Matching (CPM)...";
noise = open(modelfile, "r")
lines = noise.readlines()
compl = 0;
mid_compl = 0;

print "Reading noise model data file:", modelfile;
print "Loading:",
for line in lines:
    str = line.strip()
    if (str != "") and ( compl < 10000 ):
        val = int(str)
        mid_compl = mid_compl + 1;
        if ( mid_compl > 5000 ):
            compl = compl + mid_compl;
            mid_compl = 0;
            sys.stdout.write ("#")
            sys.stdout.flush()
        for i in range(1, 5):
            t.getNode(i).addNoiseTraceReading(val)
print "Done!";

for i in range(1, 5):
    print ">>>Creating noise model for node:",i;
    t.getNode(i).createNoiseModel()

print "Start simulation with TOSSIM! \n\n\n";
node1Missing = False
for i in range(0,150000):
	t.runNextEvent()
	if(node1Missing == False and i>50000):
		node1.turnOff()
		node1Missing = True
	
			
print "\n\n\nSimulation finished!";

#throttle.printStatistics()

