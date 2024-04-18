from ipywidgets import Layout, Button, Box, widgets, VBox, HBox
from IPython.display import display
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import io

selectMultipleLayout=Layout(
    width='1000px',
    height='200px'
)

course_selector = widgets.SelectMultiple(
    options=['Basics of complex Numbers', 'Properties of Complex Numbers', 'Complex Numbers on a Plane',
             'Complex Vector Spaces', 'Complex Vector Spaces: Linear Combination, Independence, Basis and Dimensions',
             'Properties and Operations on Vectors and Matrices in Complex Vector Spaces', 'Advanced Concepts in Complex Vector Spaces',
             'Overview of Tensor Analysis'],
    value=[],
    #rows=10,
    description='Modules',
    disabled=False,
    layout=selectMultipleLayout
)

submit_button = widgets.Button(
    description='Select Courses',
    disabled=False,
)
output = widgets.Output()

def on_button_clicked(b):
    with output:
        print(course_selector.value)
    
        notebook = new_notebook()

        with io.open("../Unit 01 - Quantum Computing and Cryptography/01_ Basics of Complex Numbers", 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, 4)
        # el = [x for x in nb.cells if hasattr(x, 'metadata') and hasattr (x.metadata, 'tags') and "hidden-cell" in x.metadata.tags][0]

        # notebook.cells.append(el)

        # Write the notebook to a new file
        with open('example_notebook.ipynb', 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)

        print("Notebook created successfully.")

submit_button.on_click(on_button_clicked)
Course_Selector = VBox([
HBox([course_selector]),
HBox([submit_button, output])
])

#display(submit_button, output)
