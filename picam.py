from RPIO import PWM 
import time
import atexit
from flask import Flask, render_template, request
app = Flask(__name__)

# This function maps the angle we want to move the servo to, to the needed PWM value
def angleMap(angle):
	return int((round((1950.0/180.0),0)*angle) +550)

# Create a dictionary called pins to store the pin number, name, and angle
pins = {
    23 : {'name' : 'pan', 'angle' : 90},
    22 : {'name' : 'tilt', 'angle' : 90}
    }

# Create two servo objects using the RPIO PWM library
servoPan = PWM.Servo()
servoTilt = PWM.Servo()

# Setup the two servos and turn both to 90 degrees
servoPan.set_servo(23, angleMap(90))
servoPan.set_servo(22, angleMap(90))

# Cleanup any open objects
def cleanup():
    servo.stop_servo(23)
    servo.stop_servo(22)

# Load the main form template on webrequest for the root page
@app.route("/")
def main():

    # Create a template data dictionary to send any data to the template
    templateData = {
        'title' : 'PiCam'
        }
    # Pass the template data into the template picam.html and return it to the user
    return render_template('picam.html', **templateData)

# The function below is executed when someone requests a URL with a move direction
@app.route("/<direction>")
def move(direction):
    # Choose the direction of the request
    if direction == 'left':
	    # Increment the angle by 10 degrees
        na = pins[23]['angle'] + 10
        # Verify that the new angle is not too great
        if int(na) <= 180:
            # Change the angle of the servo
            servoPan.set_servo(23, angleMap(na))
            # Store the new angle in the pins dictionary
            pins[23]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'right':
        na = pins[23]['angle'] - 10
        if na >= 0:
            servoPan.set_servo(23, angleMap(na))
            pins[23]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'up':
        na = pins[22]['angle'] + 10
        if na <= 180:
            servoTilt.set_servo(22, angleMap(na))
            pins[22]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))
    elif direction == 'down':
        na = pins[22]['angle'] - 10
        if na >= 0:
            servoTilt.set_servo(22, angleMap(na))
            pins[22]['angle'] = na
        return str(na) + ' ' + str(angleMap(na))

# Function to manually set a motor to a specific pluse width
@app.route("/<motor>/<pulsewidth>")
def manual(motor,pulsewidth):
    if motor == "pan":
        servoPan.set_servo(23, int(pulsewidth))
    elif motor == "tilt":
        servoTilt.set_servo(22, int(pulsewidth))
    return "Moved"

# Clean everything up when the app exits
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


