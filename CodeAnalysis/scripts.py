import radon_loop

scripts1 = ["../" + f for f in """analyseComments.py
analyseNotes.py
config.py
examNotes.py
linkComments.py
scrapeClassLists.py
shredComments.py
students.py
updateComments.py""".split("\n")]

scripts2 = ["../GUI/" + f for f in """class_view.py
control_view.py
desk_functions.py
events.py
gui.py
icons.py
link_gui_backend.py""".split("\n")]

results1 = radon_loop.analyse(scripts1)
results2 = radon_loop.analyse(scripts2)

print("\nCode with TDD")
radon_loop.display(*results1)

print("\nCode without TDD")
radon_loop.display(*results2)
