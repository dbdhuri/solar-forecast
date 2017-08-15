import argparse
from dataset_models.sdo.aia import aia
import matplotlib
matplotlib.use("agg")
import pylab as pl
import csv
import datetime
import numpy as np

print "WARNING: This script is incomplete and currently assumes"
print "you will use the AIA dataset model. Please update appropriately."
print "Potential updates include the image count and the side channel selection."

# Parse the command line arguments. You can view these from the command line
# by issuing `python evaluate_network.py -h`
parser = argparse.ArgumentParser(description='Plot validation data')
parser.add_argument('network_model', metavar='N', type=str, nargs=1,
                    help='The full path of the validation result file to plot. This will be a file with the .validation.performance extension.')
args = parser.parse_args()

## Specify the data
#dataset_model = aia.AIA(side_channels=["hand_tailored"], aia_image_count=1)
#
## Load and evaluate the network
#dataset_model.evaluate_network(args.network_model[0])

#Load csv file containing validation results
data = csv.reader(open(args.network_model[0],'r'))
data = list(data)

#Picking out timestamp, true value and prediction
y_times = []
y_val_true = []
y_val_pred = []

for i in xrange(1,len(data)):
    record = data[i]
    y_times.append(record[0][9:22])
    y_val_pred.append(float(record[1]))
    y_val_true.append(float(record[3]))

#Sorting timestaps chronologically
for i in xrange(len(y_times)):
    y_times[i] = datetime.datetime.strptime(y_times[i],'%Y%m%d_%H%M')

z = zip(y_times, y_val_true, y_val_pred)

z= sorted(z, key=lambda pair:pair[0])

y_times = [x for (x, y, w) in z]
y_val_true = [y for (x, y,w) in z]
y_val_pred = [w for (x,y,w) in z]

y_min_true = min(y_val_true)
y_min_pred = min(y_val_pred)
y_min = min([y_min_true, y_min_pred]) - 0.25
y_min = np.power(10.0,y_min)
#Plotting using matplotlib
y_val_true = np.array(y_val_true, dtype=float)
y_val_pred = np.array(y_val_pred, dtype=float)
pl.title('24hr Maximum X-ray Flux Forecast Every 36 Minutes')
pl.ylabel('24hr Max X-ray Flux (W/m sq.)')
pl.semilogy(np.power(10.0,y_val_true), color = 'blue',label = 'True', lw = 1.5)
pl.semilogy(np.power(10.0,y_val_pred), color = 'red', label = 'Predicted', lw = 1.5)
pl.xticks(np.arange(0,240,40))
pl.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='on',      # ticks along the bottom edge are off
    top='on',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off

pl.text(40.0,y_min,'Jun 09',rotation=90)
pl.text(80.0,y_min,'Jun 10',rotation=90)
pl.text(120.0,y_min,'Jun 11',rotation=90)
pl.text(160.0,y_min,'Jun 12',rotation=90)
pl.text(200.0,y_min,'Jun 13',rotation=90)
pl.legend()
pl.savefig(args.network_model[0][:-27]+'jpg',format='jpg')
pl.close()