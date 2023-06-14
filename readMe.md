![Thirst Trap](https://i.ibb.co/gMcBTqy/Img-1460-720.png)


# Thirst Trap 

---
Thirst Trap is a user-friendly application designed to help plant enthusiasts keep track of their plants' watering 
schedules. With Thirst Trap, users can effortlessly manage their plant collection by adding their plants to their 
profiles. Our app takes care of the rest by sending timely email reminders based on each user's plant-specific 
watering frequency.

With Thirst Trap, you no longer have to worry about forgetting to water your plants or struggling to keep track of 
multiple watering schedules. Our application takes the guesswork out of plant care, allowing you to focus on enjoying 
your thriving green companions.


## Table of Contents 📝
* [Overview](#overview)
* [Considerations](#considerations)
* [Implementation / How to Use](#implementation--how-to-use)
* [Languages & Frameworks Used](#languages--frameworks-used)
* [Contributors](#contributors)
---

## Overview ☁️

---

This application aims to solve the dying plant problem. Most plant owners struggle with setting/remembering
a watering schedule for a new plant. Our goal is to assist users in keeping their plants healthy and thriving by 
providing timely reminders to water them. 

## Considerations 💭

---
To retrieve the necessary plant information for our users, we had to consider multiple plant APIs.
Here's an overview of our findings:
* Plant.id: This API offers a comprehensive plant database with a wide range of plant information. While it has the advantage of providing extensive plant details, one drawback is that it requires an image file to function effectively.
* Trefle.io: This API provides a wealth of plant data, including watering information. However, the way in which the watering data was presented did not align with our project requirements. It provided minimum and maximum millimeter values instead of a more user-friendly format.
* Garden.org: Although Garden.org seemed promising, we encountered a hurdle as its API documentation was not readily available. Without proper documentation, it became challenging to integrate their data effectively into our app.
* Houseplants by Mnai: We explored Houseplants by Mnai, but it fell short in terms of the dataset's size. The available plant information was limited, which posed limitations on the app's functionality and usefulness.
* Perenual.com: This API has a vast database of plant types and provides a plethora of watering information that contributes
to optimal plant growth. Though it has an extensive database however, it is important to note that it does not cover all plant species.

In the end, after considering all the possible weaknesses and strengths we decided on the [Perenual API](https://perenual.com).
Overall, this API provided a comprehensive dataset that was simpler to convert into a user-friendly output and aligned 
well with our project goals.


## Implementation / How to Use 🛠️

---
To properly run Thirst Trap on your own device, be sure to import the necessary libraries.
We have complied all the necessary libraries and modules into one file for ease. The file is titled "requirements.txt".
Be sure to download all the listed libraries and modules before use. As a database we used MySql Workbench. We have also
included a file "sql.txt" so that you may populate the necessary database and tables for the application to run. 

After implementing, run main.py as the main driver of the code and get ready to sign up and log your first plant!

## Languages & Frameworks Used 🖥️

---
* Flask ![Flask](https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg) 
* Git ![Git](https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg)
* HTML   
* MySQL   
* Python

## Contributors ✍🏼

---
* [Harlie](https://github.com/HarlieS) 🌼
* [Harriet](https://github.com/hgodward) 🌱
* [Tess](https://github.com/TessAfanasyeva) 🌸
* [Oviyah](https://github.com/Oviyah18) 🌹
* [Lesley](https://github.com/Lezlee-Lowpez)🌵

