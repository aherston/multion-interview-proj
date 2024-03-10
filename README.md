# Image to Web Actions using MultiOn API

## Overview
A web application enabling the user to input an image URL which automatically spawns a MultiOn window and completes a task based on the image uploaded. There are currently 3 supported use cases:
  1. Image of a text conversation scheduling a meeting or event -> MultiOn will automatically put that event in your Google Calendar
  2. Image of any food item -> MultiOn will put it in your shopping cart on either InstaCart or DoorDash depending on if it is a prepared or grocery item.
  3. Image of a grocery list or recipe ingredients list -> MultiOn will put all of the items in their designated quantities in your cart on InstaCart.

The backend is written in Python using FastAPI, and there is a simple frontend written in HTML and JavaScript. This implementation uses several different VLMs using Replicate's API, and uses MultiOn to complete the browser commands. 

## Running the Application
To run the application, you need to start the servers. Run the following command to start the FastAPI Server at http://localhost:8000 :
```
uvicorn main:app --reload
```
In a separate terminal, use the following command to start the app locally:
```
python -m http.server [any server number]
```
Now, navigate to this server in your web browser to start the app.
