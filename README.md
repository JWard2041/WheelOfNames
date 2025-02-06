# WheelOfNames

## Description
This project is a wheel of names that can be used for Cru weekly meetings to pick the person for the box or dollar game. It grabs names from a Google sheet with the data from the digital contact cards and puts them into the wheel of names. 
Note: The application or executable only works on a Windows machine.

## Note
- Windows only for executable
- Code is written using Python 3.8.1 and the arcade library version 2.6.17

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
To install and run the game:
1. You need to download the folder called "Wheel_of_Names".
2. Once you have the folder installed, you can open up the folder inside called "dist".
3. There should only be one executable or application file in there that you can then open to launch the game. 

## Usage
Title Screen:
- When you launch the application it loads into the title screen which you can either click play to go to the settings screen or quit to close the application

Setting Screen:
- The setting screen is where you can the settings for the wheel such as the date and wheel speed. It also allows you to update the file with the names and then hit play when you are ready to open the wheel of names.

- Settings:
  - Wheel Speed:
    - This is how you can control how fast the wheel comes to a stop. The lower the number then the quicker the wheel stops spinning.
  - Date:
    - This is how you tell the program what the date is so it knows to grab only the names with the correct date.
    - Once you input the date, then it is good to click the update names button to update the text file with the current names
    - The date needs to be of the format YYYY-MM-DD (every blank must be filled so if it is January 2nd, 2025 then it needs to be 2025-01-02)

- Once you have inputted the date and set the speed then you can click play to go to the wheel

Wheel of Names:
- The wheel should have all the names that are currently in the file.
- You can spin the wheel by clicking the button in the middle.
- You can update the names on the wheel with more people who have filled out the contact card by clicking the update button.
- There is also a back button if you need to go back to the settings page to change settings.
- Once you have spun the wheel then it will come to a stop and show the winner in the middle of the screen. You can click on the text to stop showing the winner and then you can spin again if you want.

