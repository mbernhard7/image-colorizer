# image-colorizer
This website colorizes black and white images using a neural network backend. Created for CSCI121 at Harvey Mudd. Written for python 3.7.4. 
To run the app locally, first install the python requirement located in requiremtns.txt. We recommend setting up a pyenv virtualenv then installing requirements from requirements.txt with 
```pip install -r requirements.txt```. Then, navigate to the frontend folder and run 
```php -S localhost:8000``` 
to run the frontend locally. To run the backend locally, navigate to the backend folder and run 
```flask run```
Then, navigate to http://localhost:8000 in your browser to view the app running. 

You can view the latest deployment live on the web here:
[Image Colorizer](https://cs121-image-colorizer.herokuapp.com)
The front end application is deployed on heroku, and the backend is deployed on pythonanywhere. You cannot make direct requests to the production backend, so to run the production app just visit the heroku link above.

If you would like a demo of the colorizing neural network, download the directory 'colorizer-nn-demo' from this repo and follow the instructions in the readme.

There are currently no known bugs. Uploading corrupted image files will return an error that will be displayed on the webpage. Any bugs should be reported to mbernhard22@cmc.edu. 
