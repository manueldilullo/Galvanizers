# Galvanizers

This project uses a galvanic skin sensor and a Python GUI to track the physiological reaction of a user to images. The galvanic skin sensor measures the electrical conductance of the user's skin, which is an indication of their level of arousal. The Python GUI displays a series of images to the user and records their physiological response to each image.
Installation

1. Clone this repository to your local machine using git clone `https://github.com/manueldilullo/Galvanizers.git`.
2. Install the necessary Python packages using `pip install -r requirements.txt`.
3. Connect your galvanic skin sensor to your computer and ensure that it is working properly.
4. Run the program using `python main.py`.

# Usage

1. Launch the program by running python main.py. [to run it in a test environment (without serial readings) add the `--test y` argument]
2. Signup and then login 
3. The GUI will display a series of images to the user.
4. The galvanic skin sensor will measure the user's physiological response to each image and record the data in a SQLite DB.
5. After the user has viewed all of the images, the program will show the result of galvanic skin measurements.
6. A user, before returning to the home page, can send the results to he's email

# License

This project is licensed under the MIT License - see the LICENSE file for details.
