##### Libraries #####
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import plotly

##### Logging Settings #####
FILENAME = ""
WRITE_FREQUENCY = 100
TEMP_H=True
TEMP_P=False
HUMIDITY=True
PRESSURE=True
ORIENTATION=False
ACCELERATION=False
MAG=False
GYRO=False
DELAY=0

##### Functions #####
def file_setup(filename):
    header =[]
    if TEMP_H:
        header.append("temp_h")
    if TEMP_P:
        header.append("temp_p")
    if HUMIDITY:
        header.append("humidity")
    if PRESSURE:
        header.append("pressure")
    if ORIENTATION:
        header.extend(["pitch","roll","yaw"])
    if MAG:
        header.extend(["mag_x","mag_y","mag_z"])
    if ACCELERATION:
        header.extend(["accel_x","accel_y","accel_z"])
    if GYRO:
        header.extend(["gyro_x","gyro_y","gyro_z"])
    header.append("timestamp")

    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")

def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)


def get_sense_data():
    sense_data=[]

    if TEMP_H:
        sense_data.append(sense.get_temperature_from_humidity())

    if TEMP_P:
        sense_data.append(sense.get_temperature_from_pressure())

    if HUMIDITY:
        sense_data.append(sense.get_humidity())

    if PRESSURE:
        sense_data.append(sense.get_pressure())

    if ORIENTATION:
        o = sense.get_orientation()
        yaw = o["yaw"]
        pitch = o["pitch"]
        roll = o["roll"]
        sense_data.extend([pitch,roll,yaw])

    if MAG:
        mag = sense.get_compass_raw()
        mag_x = mag["x"]
        mag_y = mag["y"]
        mag_z = mag["z"]
        sense_data.extend([mag_x,mag_y,mag_z])

    if ACCELERATION:
        acc = sense.get_accelerometer_raw()
        x = acc["x"]
        y = acc["y"]
        z = acc["z"]
        sense_data.extend([x,y,z])

    if GYRO:
        gyro = sense.get_gyroscope_raw()
        gyro_x = ["x"]
        gyro_y = ["y"]
        gyro_z = ["z"]
        sense_data.extend([gyro_x,gyro_y,gyro_z])

    sense_data.append(datetime.now())

    return sense_data

def timed_log():
    while True:
        log_data()
        sleep(DELAY)




##### Main Program #####
sense = SenseHat()
batch_data= []

if FILENAME == "":
    filename = "SenseLog-"+str(datetime.now())+".csv"
else:
    filename = FILENAME+"-"+str(datetime.now())+".csv"

file_setup(filename)

if DELAY > 0:
    sense_data = get_sense_data()
    Thread(target= timed_log).start()

# open plotly streams
plotly_token1 = "b29gyiuuqg"
plotly_stream1 = plotly.plotly.Stream(plotly_token1)
plotly_stream1.open()

plotly_token2 = "ddev15zx4p"
plotly_stream2 = plotly.plotly.Stream(plotly_token2)
plotly_stream2.open()

while True:
    sense_data = get_sense_data()

    if DELAY == 0:
        log_data()

    if len(batch_data) >= WRITE_FREQUENCY:
        print("Writing to file..")
        with open(filename,"a") as f:
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []

        # also write to plotly
        now = datetime.now()
        temp = round(sense.get_temperature_from_pressure(), 5)
        temp2 = round(sense.get_temperature_from_humidity(), 5)
        point1 = {
            'x' : str(now),
            'y' : temp
        }
        plotly_stream1.write(point1)

        point2 = {
            'x' : str(now),
            'y' : temp2
        }
        plotly_stream2.write(point2)

plotly_stream.close()
