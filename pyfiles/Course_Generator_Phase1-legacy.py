from ipywidgets import Layout, Button, Box, widgets, VBox, HBox
from IPython.display import display
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import io

modules = {
  "The Basics of Complex Numbers":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/01_ Basics of Complex Numbers/nanomod01-unit01.ipynb",
  "Properties of Complex Numbers":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/02_ Properties of Complex Numbers/nanomod02-unit01.ipynb",
  "Complex Numbers on a Plane":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/03_ Complex Numbers on a Plane/nanomod03-unit01.ipynb",
  "Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/04_ Complex Vector Spaces/nanomod04-unit01.ipynb",
  "Complex Vector Spaces Linear Combination, Independence, Basis and Dimensions":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/05_ Complex Vector Spaces_ Linear Combination, Independence, Basis and Dimensions/nanomod05-unit01.ipynb",
  "Properties and Operations on Vectors and Matrices in Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/06_ Properties and Operations on Vectors and Matrices in Complex Vector Spaces/nanomod06-unit01.ipynb",
  "Advanced Concepts in Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/07_ Advanced Concepts in Complex Vector Spaces/nanomod07-unit01.ipynb",
  "Overview of Tensor Analysis": "Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/08_ Tensor Analysis/nanomod08-unit01.ipynb"
}   

selectMultipleLayout=Layout(
    width='1000px',
    height='200px'
)

course_selector = widgets.SelectMultiple(
    options=['The Basics of Complex Numbers', 'Properties of Complex Numbers', 'Complex Numbers on a Plane',
             'Complex Vector Spaces', 'Complex Vector Spaces Linear Combination, Independence, Basis and Dimensions',
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
        
        for module_name in modules.keys():
            notebook = new_notebook()
            with io.open(modules[module_name], 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, 4)
            
            module_title = nb.cells[0].metadata.cell_details.module_title[0]

            if module_title in course_selector.value:
                for x in nb.cells:
                    notebook.cells.append(x) 

                # Write the notebook to a new file
                with open(f'Modules/{module_title}.ipynb', 'w', encoding='utf-8') as f:
                    nbformat.write(notebook, f)

                print("Notebook created successfully.")

submit_button.on_click(on_button_clicked)
Course_Selector = VBox([
HBox([course_selector]),
HBox([submit_button]),
HBox([output])
])

#display(submit_button, output)
