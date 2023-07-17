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
        
        self._config =  self._load("config.json", m_type="json")        # load config file
        self._bitmaps = {                                               # dict of bitmaps
            map_name:self._load(path, m_type="image")                   # import from each file
            for map_name, path in self._config["maps"].items()}         # in the config file

    # public methods

    def generate_path(self, im:str) -> np.ndarray:
        """ method to generate the path to follow from an input bitmap
        args: (1) im: str containing the name of the image that encodes
                      the path to follow
        rets: (1) xy: array containing xy coordinates of the identified
                      path
        Note: after a successful execution, the user is prompted to
              store the generated coordinate array into a text file """

        color = self._config["resources"]["path_color"]                 # user-defined color for path
        mat = self._bitmaps[im]                                         # image matrix
        mask = np.all(mat == color, axis=2)                             # color-filtering mask
        xy = np.array(np.where(mask)[::-1]).T                           # determine path coordinates
        
        smooth_size = self._config["filters"]["smooth_size"]            # get smooth size
        if smooth_size > 0:                                             # if not deactivated
            self._smooth(xy, smooth_size)                               # apply smooth to path
        
        xy = self._filter_position(xy)                                  # apply positional filter
        self._show(xy, m_type="line")                                   # show identified path
        query = "Save coordinates to data file?"                        # question to ask user
        if self._get_user_response(query).lower() == "y":               # ask user if to save file
            self._save(xy, m_type="line")                               # save to file
        plt.clf()                                                       # clear plotted figure
        return xy
    
    def animate(self, ims:list, path:np.ndarray=np.array([[0,0]])) -> None:
        """ method to create image animation
        args: (1) ims: list of images to show stacked
              (2) path: array containing the trajectory to follow
        rets: none
        Note: after a successful execution, the user is prompted to
              store the generated animation into a gif file """

        skip = self._config["path"]["skip"]                             # points to skip from the original dataset
        lw = self._config["path"]["line_width"]                         # plot line width
        output_mode = self._config["output"]["mode"]                    # save or show mode
        figure_size = self._config["display"]["figure_size"]            # output figure size
        color = self._config["display"]["line_color"]                   # plot line color
        ls = self._config["display"]["line_style"]                      # plot line style
        smooth = self._config["display"]["camera_smooth"]               # smoothing coefficient for camera motion

        plt.get_current_fig_manager().window.wm_geometry(               # set figure geometry
            f"{figure_size[0]}x{figure_size[1]}+{0}+{0}")               # as defined by user
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)           # adjust margins
        fig = plt.gcf()                                                 # current figure handle

        frames = []                                                     # list of frames if output_mode is set to save
        filename = ""                                                   # filename to save animation
        [self._show(self._bitmaps[im]) for im in ims]                   # display map background        
        line, = plt.plot(path[0], ls, linewidth=lw, color=color)        # draw first point
        
        total = len(path[1::skip])                                      # total number of iterations
        for i, pos in tqdm(enumerate(path[1::skip]), total=total):      # iterate over path to follow
            
            line.set_data(path[:i*skip,0], path[:i*skip,1])             # update data
            m = max(0,(i-smooth)*skip)                                  # start of averaging range
            M = min(len(path), (i+smooth)*skip)                         # end of averaging range
            cam_pos = [np.mean(path[m:M,0]), np.mean(path[m:M,1])]      # smooth camera position
            self._set_FoV(np.array(cam_pos))                            # set current Field of View
            fig.canvas.draw()                                           # update drawing             
            plt.pause(0.001)                                            # time to allow visualization
            
            if output_mode == "save":                                   # update frame to output
                frame = np.array(fig.canvas.renderer.buffer_rgba())     # get frame
                frames.append(Image.fromarray(frame))                   # append it to frame list
        
        if output_mode == "save":                                       # output to file
            filename = self._save(frames,                               # update file saving requirements
                                    filename=filename)                  # save frame to specified filename

    # private methods
    
    def _set_FoV(self, current_pos:np.ndarray=np.array([0,0])) -> None:
        """ method to dynamically set the current Field of View
        args: (1) current_pos: array containing the current position
        rets: none """

        fov = np.array(self._config["display"]["FoV"])                  # get default FoV
        x_lim = current_pos[0] + fov[0]/2*np.array([-1, 1])             # plot xy limits
        y_lim = current_pos[1] + fov[1]/2*np.array([1, -1])             # plot xy limits
        plt.xlim(x_lim)                                                 # set x limits
        plt.ylim(y_lim)                                                 # set y limits

    def _smooth(self, xy:np.ndarray, box_pts:int=10) ->None:
        """ method to smooth a curve dataset
        args: (1) xy: array containing the list of coordinates to smooth
              (2) box_pts: int width of the smooth filter
        rets: none
        note: the input xy array modified directly """
        
        box = np.ones(box_pts)/box_pts                                  # smooth window
        xy[:,0] = np.convolve(xy[:,0], box, mode='same')                # filter x coordinates
        xy[:,1] = np.convolve(xy[:,1], box, mode='same')                # filter y coordinates

    def _filter_position(self, xy:np.ndarray, n:int=0) -> np.ndarray:
        """ method to apply a coherence positional filter on a list of coordinates
        args: (1) xy: array containing the list of coordinates to filter
              (2) n: int current recursion depth
        rets: (1) xy_out: filtered array """

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

        d_filt = np.sqrt(np.diff(xy_out[:, 0]) ** 2 +                   # derivative mask
                         np.diff(xy_out[:, 1]) ** 2) < th               # filter against threshold
        d_filt = np.insert(d_filt, 0, True)                             # correct array length
        xy_out = xy_out[d_filt]                                         # apply filter
        if np.sum(d_filt == False) > 0 and n < rec_limit:               # filtering occurrences found
            xy_out = self._filter_position(xy_out, n+1)                 # recursive filtering
        return xy_out                                                   # output filtered coordinates
    
    def _get_user_response(self, query:str="", options:list=['y','n'])->str:
        """ method to ask a question to the user
        args: (1) query: str containing the question to ask the user
              (2) options: list of options to present the user with
        rets: (1) answer: str with user-inserted answer"""
        
        print(f"{query} ({','.join(options)}) :", end="")               # prompt user
        answer = input().lower()                                        # get user answer
        while answer not in options:                                    # invalid answer
            print(f"Invalid answer. Please use {'or'.join(options)}:",  # inform user
                  end="")                                               # same like
            answer = input().lower()                                    # get new answer
        return answer                                                   # return answer

    def _show(self, matrix:np.ndarray, m_type:str="image") -> None:
        """ method to display the contents of an input matrix
        args: (!) matrix: array containing data to be shown
              (2) m_type: str describing the type of data to show
                          options: "image", "line"
        rets: none """
        
        if m_type == "image":                                           # image display 
            plt.imshow(matrix)                                          # show image
            plt.axis('off')                                             # remove axis
        
        if m_type == "line":                                            # line plot
            plt.plot(matrix[:,0], matrix[:,1])                          # show plot

        plt.show(block=False)                                           # update visualization        
    
    def _save(self, matrix, m_type:str="frames", filename:str='') -> str:
        """ method to save the contents of an input matrix to file
        args: (1) matrix; array containing data to save
              (2) m_type: str describing the type of data
                  options: "image", "line", "frames"
              (3) filename: str containing name of file to save to
        rets: (1) filename: user-selected filename, in the case of an
                            empty input """

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

        if filename == '':                                              # canceled by user
            return filename                                             # abort file saving
            
        if m_type == "line":                                            # save matrix to dat file
            np.savetxt(filename, matrix)                                # save to text

        if m_type == "frames":                                          # save as animated gif
            if filename [-4:] != ".gif":                                # incorrect or missing extension
                filename += ".gif"                                      # add .gif to file name
            
            duration = self._config["output"]["frame_duration"]         # get frame duration config
            loop = self._config["output"]["loop"]                       # get number of loops config

            matrix[0].save(filename,                                    # save to file
                           format='GIF',                                # file name
                           mode="P",                                    # independent colormap
                           append_images=matrix[1:],                    # append files
                           save_all=True,                               # save all frames
                           optimize=False,                              # maximize quality
                           lossless=True,                               # maximize quality
                           duration=duration,                           # frame duration
                           loop=loop)                                   # number of loops

        return filename

    def _load(self, filename:str, m_type:str="image") -> np.ndarray:
        """ method to load the contents of a file into and ndarray
        args: (1) filename: str containing the name of the file to load
              (2) m_type: str type of the matrix to be loaded from file
                          options: "image", "json", "path" 
        rets: (1) matrix; array containing the imported data"""

        if m_type == "image":                                           # load bitmap image
            image = cv2.imread(filename)                                # import image file
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)              # convert to RGB
            return np.array(image)                                      # convert the image to a NumPy matrix
        
        if m_type == "json":                                            # load config files
            with open(filename, 'r') as file:                           # open file in read
                return json.load(file)                                  # load contents to dict
            
        if m_type == "path":                                            # load pre-generated path
            return np.loadtxt(filename)                                 # load from text

# test script TODO: Remove
a = Animator()                                                          # instantiate Animator object
if a._config["mode"] == "generate":
    filename = self._config["path"]["map_road"]                         # get file name from config
    road = a.generate_path(filename)                                    # generate path dataset
elif a._config["mode"] == "animate":
    road = a._load("path_road", m_type="path")                          # import path dataset
    a.animate(["map_all"], road)                                        # launch animation
