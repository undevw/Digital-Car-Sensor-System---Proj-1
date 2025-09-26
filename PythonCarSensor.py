import serial
import time
from collections import deque
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

port = "COM3"
baud = 115200

#Filter config.

N = 5               #num. of samples
temp_buffer = deque(maxlen=N)
dist_buffer = deque(maxlen=N)
speed_buffer = deque(maxlen=N)

#plot data

plot_len = 100          # num of points
temps, dists, speeds = deque(maxlen=plot_len), deque(maxlen=plot_len), deque(maxlen=plot_len)

def moving_average(buffer, new_value):
    buffer.append(new_value)
    return sum(buffer) / len(buffer)

#matplot lib

plt.ion()
fig, ax = plt.subplots()
line_temp, = ax.plot([], [], label="Temp (°C)")
line_dist, = ax.plot([], [], label="Distance (cm)")
line_speed, = ax.plot([], [], label="Speed (m/s)")
ax.set_ylim(0, 120)
ax.set_xlabel("Samples")
ax.set_ylabel("Value")
ax.legend()
plt.title("Real-Time Car Sensor Dashboard")


def main():
    try:
        ser = serial.Serial(port, baud, timeout=1)
    except serial.SerialException as e:
        print("Could not open serial port:", e)
        return
    
    time.sleep(2)
    ser.flushInput()
    print("Listening for sensor data...")

    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) == 3:
                try:
                    temp = float(parts[0])
                    dist = float(parts[1])
                    speed = float(parts[2])
                except ValueError:
                    print("Bad numbers:", line)
                    continue 

                #moving avg filter

                temp_avg = moving_average(temp_buffer, temp)
                dist_avg = moving_average(dist_buffer, dist)
                speed_avg = moving_average(speed_buffer, speed)

                #append to plot

                temps.append(temp_avg)
                dists.append(dist_avg)
                speeds.append(speed_avg)

                #update plot lines
                line_temp.set_data(range(len(temps)), list(temps))
                line_dist.set_data(range(len(dists)), list(dists))
                line_speed.set_data(range(len(speeds)), list(speeds))
                ax.relim()
                ax.autoscale_view()
                plt.pause(0.001)

                #unit conversions
                temp_f = temp_avg * 9/5 + 32        # Celsius -> Fahrenheit
                dist_m = dist_avg / 100             # cm -> meters
                speed_kmh = speed_avg * 3.6         # m/s -> km/h

                #print and test thersholds 
                print(f"Temp: {temp_avg:5.1f} °C  ({temp_f:5.1f} °F)  "
                      f"Distance: {dist_avg:6.1f} cm ({dist_m:4.2f} m)  "
                      f"Speed: {speed_avg:5.1f} m/s ({speed_kmh:5.1f} km/h)")
                
                #test thresholds/ led control to arduino
                if temp_avg > 90:
                    print("WARNING TEMP HIGH!")
                    ser.write(b"TEMP_ON\n")
               
                if dist_avg < 30:
                    print("WARNING OBJECT CLOSE!")
                    ser.write(b"DIST_ON\n")
             
                if speed_avg == 0:
                    print("Vehicle Stopped...")
                if speed_avg > 80:
                    print("HIGH SPEED - SLOW DOWN!")
                    ser.write(b"SPEED_ON\n")
                
            else:
                print("Unexpected line:", line)

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()



