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
    width='400px',
    height='175px'
)

strInputLayout2=Layout(
    width='500px'
)

excluded_cells = ["background", "learningoutcomes", "warmup", "summary", "quiz", "finalquiz", "conclusions"]

def get_concepts_for_module(module_name):
    with io.open(modules[module_name], 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, 4)
            
    module_title = [x.metadata.cell_details.cell_ID for x in nb.cells]
    concept_list = list(filter(lambda x: x.split('-')[1].lower() not in excluded_cells, module_title))
    return concept_list

accordion = widgets.Accordion(children=[ widgets.SelectMultiple(
    options=get_concepts_for_module(module_name),
    value=[],
    description='Concepts',
    disabled=False,
    layout=selectMultipleLayout) for module_name in modules.keys()])

selected_concepts = set()
notebook_cells = []

def on_change(change):
    with output:
        if change['type'] == 'change' and change['name'] == 'value':
            if change['new'][-1] not in selected_concepts:
                selected_concepts.add(change['new'][-1])
                print(change['new'][-1])

for selectedMultiple in accordion.children:
    selectedMultiple.observe(on_change)

for i, module_name in enumerate(modules.keys()):
    accordion.set_title(i, module_name)

    with io.open(modules[module_name], 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, 4)
    
    for cell in nb.cells:
        notebook_cells.append(cell)

estimatedTime =  widgets.Text(
    placeholder='Estimated Time',
    disabled=False,
    layout = strInputLayout2
)

estimatedTimeLabel =  widgets.Label(
    value='Estimated Time: ',
)


submit_button = widgets.Button(
    description='Submit',
    disabled=False,
)
def clear_selection_clicked(b):
    with output:
        output.clear_output()
        selected_concepts.clear()
    with output2:
        output2.clear_output()
        print("Selection cleared")

    
clear_selection_button = widgets.Button(
    description='Clear Selection',
    disabled=False,
)
clear_selection_button.on_click(clear_selection_clicked)

output = widgets.Output()
output2 = widgets.Output()

def on_submit_clicked(b):
    with output2:
        #print(notebook_cells)
        notebook = new_notebook()  
        seen = set()

        def dfs(cellId):
            neighbours = next(x.metadata.cell_details.cell_prereqs for x in notebook_cells if x.metadata.cell_details.cell_ID == cellId)

            for neighbour in neighbours:
                if neighbour not in seen:
                    seen.add(neighbour)
                    dfs(neighbour)
                    print(neighbour)
                    cell = next(x for x in notebook_cells if x.metadata.cell_details.cell_ID == neighbour)
                    notebook.cells.append(cell)

        for concept in selected_concepts:
            if concept not in seen:
                seen.add(concept)
                dfs(concept)
                print(concept)
                cell = next(x for x in notebook_cells if x.metadata.cell_details.cell_ID == concept)
                notebook.cells.append(cell)
                
        # Write the notebook to a new file
        with open(f'Modules/Course.ipynb', 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)

        print("Notebook created successfully.")

submit_button.on_click(on_submit_clicked)
Course_Selector = VBox([
HBox([accordion, output]),
#HBox([estimatedTimeLabel, estimatedTime]),
HBox([submit_button, clear_selection_button]),
HBox([output2]),
])

#display(submit_button, output)
