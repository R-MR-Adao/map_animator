# launch script begin
from animator import Animator

a = Animator()                                                          # instantiate Animator object

if a.get_config()["mode"] == "generate":                                # option execute path generation
    a.generate_path("map_road")                                         # generate path dataset

elif a.get_config()["mode"] == "animate":                               # option to execute animation build
    a.build_animation()                                                 # build animation

elif a.get_config()["mode"].lower() == "cli":                           # option to launch the CLI app
    a. launch_cli()                                                     # launch the CLI app

else:                                                                   # invalid option
    pass                                                                # used for external module consumption
