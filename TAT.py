import config
import gui

config_file = "./GUI_files/config.yaml"
config.create_default_if_nec(config_file)
gui.main(config_file)