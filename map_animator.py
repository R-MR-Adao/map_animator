import json
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Animator:
    
    # class constructor

    def __init__(self) -> None:
        """ a class that allows animating a moving point over a map """

        # private class members 
        
        self._config =  self._load_json("config.json")                  # load config file
        self._bitmaps = {                                               # dict of bitmaps
            map_name:self._load_bitmap(path)                            # import from each file
            for map_name, path in self._config["path"].items()}         # in the config file

    # public methods

    def animate(self) -> None:
        """ method to create map animation """

        self._show(matrix=self._bitmaps["map_back"])                    # display map background
        input()                                                         # block Python

    # private methods

    def _show(self, m_type:str="image", matrix:np.ndarray=np.array([])) -> None:
        """ method to display the contents of an input matrix """
        
        if m_type == "image":                                           # image display 
            plt.imshow(matrix)                                          # show image
            plt.axis('off')                                             # remove axis
            plt.show(block=False)                                       # prevent block

    def _load_json(self, file_path:str) -> dict:
        """ method to load a Python dict from a json file """

        with open(file_path, 'r') as file:                              # open file in read
            return json.load(file)                                      # load contents to dict
        
    def _load_bitmap(self, path:str) -> np.ndarray:
        """ method to load a bitmap from a path"""
        
        image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)       # read the image using OpenCV
        return np.array(image)                                           # convert the image to a NumPy matrix

# test script TODO: Remove
a = Animator()                                                          # instantiate Animator object
a.animate()                                                             # launch animation
