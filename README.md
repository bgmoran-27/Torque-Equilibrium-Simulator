# Torque-Equilibrium-Simulator
Torque is an essential concept in physics, but when you first encounter it, visualizing what it means in a real physical system can be challenging. This simulator is designed to make torque easier to understand. Change the masses, their positions, and the pivot point to see how each variable affects torque, rotational direction, and equilibrium.

## Live Demo
A deployed version of the simulator will be available here:
(STREAMLIT) //Deployment of app will occur soon

## Features

Add between 1 and 10 masses to a beam.

Enter a custom mass or select a real coin.

Organize coin presets by country.

Use multiple coins as one combined mass.

Change the position of each mass.

Move the pivot along the beam.

View an automatically updating beam diagram.

Calculate the torque produced by each mass.

Determine the net torque of the system.

Identify clockwise and counterclockwise rotation.

Solve for the position required to reach equilibrium.

Detect when the required equilibrium position is outside the beam.

## How the Physics Works

Torque measures the turning effect produced by a force around a pivot.

The basic torque equation is:

Torque = Distance × Force

In symbols:

τ = rF

The gravitational force acting on a mass is:

Force = Mass × Gravity

## Therefore, the simulator calculates torque using:

τ = rmg

where:

τ is torque in newton-meters (N·m).

r is the distance between the mass and the pivot in meters.

m is the mass in kilograms.

g is gravitational acceleration, set to 9.81 m/s².

The simulator uses the following sign convention:

A mass to the left of the pivot produces positive, counterclockwise torque.

A mass to the right of the pivot produces negative, clockwise torque.

A mass directly on the pivot produces zero torque.

The system is considered approximately balanced when the net torque is close to zero.


## How to Use the Simulator

Select the position of the pivot.

Choose the number of masses on the beam.

For each mass, choose either Custom mass or Coin.

If using a custom mass, enter its mass in grams.

If using a coin, select its country, denomination, and quantity.

Enter the position of each mass along the beam.

Examine the beam visualization and torque results.

Enable Solve for an equilibrium position if you want the simulator to calculate where one selected mass 
should be placed.

# Running the Project Locally

## Requirements:

Python

Streamlit

Installation

Download or clone this repository, then open a terminal inside the project folder.

Install Streamlit if it is not already installed:

py -m pip install streamlit

## Run the simulator

py -m streamlit run app.py

Streamlit should open the simulator in your web browser.

## Project Structure

torque-equilibrium-simulator/


├── app.py

├── requirements.txt

└── README.md

app.py contains the interface, visualization, equilibrium solver, and torque calculations.

requirements.txt tells the deployment service which Python packages the project needs.

README.md contains the project documentation.

## Technologies Used

Python

Streamlit

HTML and SVG for the beam visualization

Coin Data

Coin presets are stored by country and measured in grams. Coin specifications should be verified using 
information from the appropriate official mint or central bank.

Users can also select Custom mass to experiment with objects that are not included in the coin presets.

## Limitations

The beam is treated as rigid and massless.

The simulator does not include friction at the pivot.

All forces act straight downward because of gravity.

The visualization represents the setup but does not simulate continuous physical motion.

Coin specifications may change or differ between historical coin series.

## Possible Future Improvements

Allow the beam length to be changed.

Add more verified coins and countries.

Allow users to save custom coin presets.

Animate clockwise and counterclockwise rotation.

Add force vectors and distance labels.

Add practice problems or a quiz mode.

Improve the layout for mobile devices.

## Author

Created by Bryan Gaborit-Moran as an interactive project for learning about torque and rotational equilibrium.


