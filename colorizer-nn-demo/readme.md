This is a demo of the colorizer neural network in action. 

To run it, download this colorizer-nn-demo directory, cd into it in the console, and install all the requirements (it's just opencv-python) with:
```pip install -r requirements.txt```

Then, run:

```wget http://eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -O ./models/colorization_release_v2.caffemodel```

This file could not be included in the directory like the others because it exceeds GitHub's maximum file size.

 Then, you can run the script with:
 ```python /path/to/colorize_nn.py```

The script will ask you for a path to a jpg or png file, then will colorize it and output a file with the same name (with -colorized added) to the same directory. We have tested with jpg and png, and the largest file we tried was a 103 mb jpg, which finished in less than a minute. Make sure the models folder is in the same directory as the script when you run it.