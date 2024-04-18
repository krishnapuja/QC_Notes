import io
import nbformat
from nbformat.v4 import new_notebook
from IPython.display import display
from ipywidgets import Layout, Button, Box, widgets, VBox, HBox, Output, Label, Text

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

excluded_cells = ["background", "learningoutcomes", "warmup", "summary", "quiz", "finalquiz", "conclusions"]


class NotebookGenerator:
    def __init__(self, modules):
        self.modules = modules
        self.selected_concepts = set()
        self.notebook_cells = {}
        self.notebook_metadata = {}
        self.accordion = self.create_accordion()
        self.output = Output()
        self.output2 = Output()
        self.estimated_time = Text(placeholder='Estimated Time', disabled=False, layout=Layout(width='500px'))
        self.estimated_time_label = Label(value='Estimated Time: ')
        self.submit_button = Button(description='Submit', disabled=False)
        self.clear_selection_button = Button(description='Clear Selection', disabled=False)
        self.setup_ui()

    def create_accordion(self):
        accordion_children = []
        for module_name in self.modules:
            select_multiple = widgets.SelectMultiple(
                options=self.get_outcomes_for_module(module_name),
                value=[],
                description='Concepts',
                disabled=False,
                layout=Layout(width='600px', height='175px')
            )
            accordion_children.append(select_multiple)
        accordion = widgets.Accordion(children=accordion_children)
        for i, module_name in enumerate(self.modules):
            accordion.set_title(i, module_name)
        return accordion

    def get_outcomes_for_module(self, module_name):
        with io.open(self.modules[module_name], 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        self.notebook_cells[module_name] = nb.cells
        self.notebook_metadata[module_name] = nb.metadata.get('module_details', {})
        return self.notebook_metadata[module_name].get('module_outcomes', [])

    def on_change(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            with self.output:
                new_value = change['new'][-1] if change['new'] else None
                if new_value and new_value not in self.selected_concepts:
                    self.selected_concepts.add(new_value)
                    print(f"Selected concept: {new_value}")

    def on_submit_clicked(self, b):
        with self.output2:
            self.output2.clear_output()
            notebook = new_notebook()
            # Your logic for creating a notebook goes here
            print("Notebook creation logic goes here.")

    def clear_selection_clicked(self, b):
        with self.output:
            self.output.clear_output()
            self.selected_concepts.clear()
        with self.output2:
            self.output2.clear_output()
            print("Selection cleared")

    def setup_ui(self):
        
        for index, child in enumerate(self.accordion.children):
            child.observe(self.on_change, names='value')

        self.clear_selection_button.on_click(self.clear_selection_clicked)
        self.submit_button.on_click(self.on_submit_clicked)

        display(VBox([
            HBox([self.accordion, self.output]),
            HBox([self.estimated_time_label, self.estimated_time]),
            HBox([self.submit_button, self.clear_selection_button]),
            self.output2,
        ]))

# Instantiate and display the notebook generator UI
NotebookGenerator(modules)
