# Lightning-ATM

The Lightning-ATM is an ATM where you can insert coins from 5 cents to 2 euros and exchange them for satoshis. This is made possible by the Lightning Network. 

## Installation

To set up the Lightning-ATM, please follow the steps outlined below:

1. **Install Raspberry Pi Operating System**

   Begin by installing a new Raspberry Pi operating system on your Raspberry Pi device. You can refer to the [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/getting-started.html) for a guide on how to install the operating system.

2. **Install Node.js**

   Next, you need to install Node.js on your Raspberry Pi. Open the console and execute the following command:

   ```shell
   curl -sL https://deb.nodesource.com/setup_16.x | bash -
   apt-get install -y nodejs
   ```
   This command will download and install Node.js version 16.x on your Raspberry Pi.

3. **Clone the GitHub Project**

   Clone the Lightning-ATM project repository from GitHub. Open the console and navigate to the desired location, then execute the following command:

   ```shell
   git clone <repository_url>
   ```
   Replace <repository_url> with the URL of the GitHub repository you want to clone.

4. **Install Python Dependencies**

   Navigate to the ln-app folder of the cloned project in the console, then execute the following commands:

   ```shell
   cd ln-app
   pip install -r backend/requirements.txt
   ```
   
   These commands will change the directory to ln-app and install the required Python dependencies specified in the requirements.txt file.

 4. **Configure Coin Checker GPIO**

   Check if the coin checker on the Raspberry Pi is connected to GPIO 15. If it is not connected to GPIO 15, you need to modify the backend/coin.py file. Open the file and locate the following line:

   ```python
   coin_pin = 15
   ```
   If your coin checker is connected to a different GPIO pin, change the value of coin_pin to the corresponding GPIO number.

 4. **Start the Program**

   Once you have completed the previous steps and are inside the ln-app folder in the console, you can start the Lightning-ATM program by executing the following command:

   ```shell
   python start.py
   ```
   This command will initiate the program, allowing you to interact with the Lightning-ATM system.

   Congratulations! You have successfully installed and set up the Lightning-ATM on your Raspberry Pi. You can now insert coins ranging from 5 cents to 2 euros and exchange them for satoshis using the Lightning Network. Enjoy!
