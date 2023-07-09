import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import imageio
from tqdm import tqdm

class Animator:
    
    # class constructor

    def __init__(self) -> None:
        """ a class that allows animating a moving point over a map """

        # private class members 
        
        self._config =  self._load_json("config.json")                  # load config file
        self._bitmaps = {                                               # dict of bitmaps
            map_name:self._load_bitmap(path)                            # import from each file
            for map_name, path in self._config["maps"].items()}         # in the config file

    # public methods

    def generate_path(self, im:str) -> np.ndarray:
        """ method to generate the path to follow from an input bitmap """

        color = self._config["resources"]["path_color"]                 # user-defined color for path
        mat = self._bitmaps[im]                                         # image matrix
        mask = np.all(mat == color, axis=2)                             # color-filtering mask
        xy = np.array(np.where(mask)[::-1]).T                           # determine path coordinates
        
        smooth_size = self._config["filters"]["smooth_size"]            # get smooth size
        if smooth_size > 0:                                             # if not deactivated
            self._smooth(xy, smooth_size)                               # apply smooth to path
        
        xy = self._filter_position(xy)                                  # apply positional filter
        self._show(xy, m_type="line")                                   # show identified path
        if self._get_user_response("Save coordinates to data file?"):   # ask user if to save file
            self._save(xy, m_type="line")                               # save to file
        plt.clf()                                                       # clear plotted figure
        return xy

    def import_path(self, im:str) -> np.ndarray:
        """ method to import path to follow from an input data file """

        return self._load(self._config["path"][im], m_type="line")      # return imported data
    
    def animate(self, ims:list, path:np.ndarray=np.array([[0,0]])) -> None:
        """ method to create image animation """

        skip = self._config["path"]["skip"]                             # points to skip from the original dataset
        lw = self._config["path"]["line_width"]                         # plot line width
        output_mode = self._config["output"]["mode"]                    # save or show mode
        figure_size = tuple(self._config["output"]["size"])             # otuput figure size

        plt.figure(figsize=figure_size)                                 # set figure dize
        plt.get_current_fig_manager().window.state('zoomed')            # maximize window
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)           # adjust margins
        fig = plt.gcf()                                                 # current figure handle

        frames = []                                                      # list of frames if output_mode is set to save
        filename = ""                                                   # filename to save animation
        [self._show(self._bitmaps[im]) for im in ims]                   # display map background        
        line, = plt.plot(path[0], "--", linewidth=lw)                   # draw first point
        
        total = len(path[1::skip])                                      # total number of iterations
        for i, pos in tqdm(enumerate(path[1::skip]), total=total):      # iterate over path to follow
            line.set_data(path[:i*skip,0], path[:i*skip,1])             # update data
            self.set_FoV(pos)                                           # set current Field of View
            fig.canvas.draw()                                           # update drawing             
            plt.pause(0.001)                                            # time to allow visualization
            if output_mode == "save":                                   # update frame to output
                frames.append(self._get_frame(fig))                     # get current frame
        
        if output_mode == "save":                                       # output to file
            frames.append(self._get_frame(fig))                         # get current frame
            filename = self._save(frames,                               # update file saving requirements
                                    filename=filename)                  # save frame to specified filename

    def set_FoV(self, current_pos:np.ndarray=np.array([0,0])) -> None:
        """ method to dynamically set the current Field of View """

        fov = np.array(self._config["display"]["FoV"])                  # get default FoV
        x_lim = current_pos[0] + fov[0]/2*np.array([-1, 1])             # plot xy limits
        y_lim = current_pos[1] + fov[1]/2*np.array([1, -1])             # plot xy limits
        plt.xlim(x_lim)                                                 # set x limits
        plt.ylim(y_lim)                                                 # set y limits
    
    # private methods

    def _get_frame(sefl, fig):
        """ metho to get current plotted grame """

        return Image.frombytes(                                         # get frame
                    'RGB',                                              # color type
                    fig.canvas.get_width_height(),                      # figure dimensions
                    fig.canvas.tostring_rgb())                          # figure contents

    def _smooth(self, xy:np.ndarray, box_pts:int=10) ->None:
        """ method to smooth a curve dataset"""
        
        box = np.ones(box_pts)/box_pts
        xy[:,0] = np.convolve(xy[:,0], box, mode='same')
        xy[:,1] = np.convolve(xy[:,1], box, mode='same')

    def _filter_position(self, xy:np.ndarray, n:int=0) -> np.ndarray:
        """ method to apply a coherence positional filter on a list of coordinates """

        th = self._config["filters"]["diff_threshold"]                  # derivative filter acceptance threshold
        rec_limit = self._config["filters"]["recursion_limit"]          # filter recursion limit
        start_dir = self._config["resources"]["starting_direction"]     # get starting direction

        print(f"Apllying recursive positional filter {n}/{rec_limit}")  # notify user

        dist = lambda pt, pts:np.sqrt(                                  # function to calculate distance
            (pt[0] - pts[:,0])**2 + (pt[1] - pts[:,1])**2)              # euclidean distance between points
        
        if start_dir.lower() == "north":                                # moving north
            start_point = np.argmax(xy[:,1])                            # bottommost point
        elif start_dir.lower() == "east":                               # moving east
            start_point = np.argmin(xy[:,0])                            # leftmost point
        elif start_dir.lower() == "south":                              # moving south
            start_point = np.argmin(xy[:,1])                            # topmost point
        elif start_dir.lower() == "west":                               # moving 
            start_point = np.argmax(xy[:,0])                            # rightmost point
        else:                                                           # incorrect setting
            start_point = np.argmin(xy[:,0])                            # leftmost point
        
        xy_out = np.array([xy[start_point]])                            # output list of coordinates
        pt = xy_out[-1]                                                 # reference point
        rem = np.delete(xy, start_point, axis=0)                        # copy of remaining points
        while len(rem) > 0:                                             # iterate over input list of coordinates
            closest_idx = np.argmin(dist(pt, rem))                      # identify the closest neighbor
            pt = rem[closest_idx]                                       # store it for next iteration
            xy_out = np.concatenate((xy_out, [pt]), axis=0)             # append to list of output points
            rem = np.delete(rem, closest_idx, axis=0)                   # remove it from the remaining points list

        x_diff = np.diff(xy_out[:, 0])                                  # x derivative
        y_diff = np.diff(xy_out[:, 1])                                  # y derivative
        d_filt = np.sqrt(x_diff ** 2 + y_diff ** 2) < th                # derivative filter
        d_filt = np.insert(d_filt, 0, True)                             # correct array length
        xy_out = xy_out[d_filt]                                         # apply filter
        if np.sum(d_filt == False) > 0 and n < rec_limit:               # filtering occurrences found
            xy_out = self._filter_position(xy_out, n+1)                 # recursive filtering
        return xy_out                                                   # output filtered coordinates
    
    def _get_user_response(self, query:str="") -> bool:
        """ method to ask boolean question to user """
        
        options = ['y', 'n']                                            # answer options
        print(f"{query} ({','.join(options)}) :", end="")               # prompt user
        answer = input().lower()                                        # get user answer
        while answer not in options:                                    # invalid answer
            print(f"Invalid answer. Please use {'or'.join(options)}:",  # inform user
                  end="")                                               # same like
            answer = input().lower()                                    # get new answer
        return answer == options[0]                                     # return boolean selection

    def _show(self, matrix:np.ndarray, m_type:str="image") -> None:
        """ method to display the contents of an input matrix """
        
        if m_type == "image":                                           # image display 
            plt.imshow(matrix)                                          # show image
            plt.axis('off')                                             # remove axis
        
        if m_type == "line":                                            # line plot
            plt.plot(matrix[:,0], matrix[:,1])                          # show plot

        plt.show(block=False)                                           # update visualization

    def _load_json(self, file_path:str) -> dict:
        """ method to load a Python dict from a json file """

        with open(file_path, 'r') as file:                              # open file in read
            return json.load(file)                                      # load contents to dict
        
    def _load_bitmap(self, path:str) -> np.ndarray:
        """ method to load a bitmap from a path"""
        
        image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)       # read the image using OpenCV
        return np.array(image)                                          # convert the image to a NumPy matrix
    
    def _save(self, matrix, m_type:str="frames", filename:str='', frame_writer=None) -> str:
        """ method to save the contents of an input matrix to file """

        if filename == '':
            default_extensions = {                                      # default file extensions
                "image":("PNG Image", ".png"),                          # image
                "line": ('Text File', ".dat"),                          # line datasets
                "frames":('Animated GIF', '.gif')}                      # animated gifs
            extension = default_extensions[m_type]                      # select the specified one
            
            root = tk.Tk()                                              # Create a Tkinter root window
            root.withdraw()                                             # Hide the main window
            filename = filedialog.asksaveasfilename(                    # Prompt the user to select a file location
                filetypes=[extension])                                  # set default extension

        if m_type == "line":                                            # save matrix to dat file
            np.savetxt(filename, matrix)                                # save to text

        if m_type == "frames":                                          # save as animated gif
            if filename [-4:] != ".gif":                                # incorrect or missing extension
                filename += ".gif"                                      # add .gif to file name
            matrix[0].save(filename,                                    # save to file
                           format='GIF',                                # file name
                           append_images=matrix[1:],                    # append files
                           save_all=True,                               # save all frames
                           duration=self._config["output"]["frame_duration"],   # frame duration
                           loop=self._config["output"]["loop"])         # number of loops

        return filename, frame_writer

    def _load(self, filename:str, m_type:str="image") -> np.ndarray:
        """ method to load the contents of a file into and ndarray """
    
        if m_type == "line":
            return np.loadtxt(filename)

# test script TODO: Remove
a = Animator()                                                          # instantiate Animator object
#road = a.generate_path("map_road")                                      # generate path dataset
road = a.import_path("path_road")                                       # import path dataset
a.animate(["map_all"], road)                                            # launch animation
