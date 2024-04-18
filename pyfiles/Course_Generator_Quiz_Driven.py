import io
import nbformat
from nbformat.v4 import new_notebook
from IPython.display import display
from ipywidgets import Layout, Button, Box, widgets, VBox, HBox, Output, Label, Text
from openai import OpenAI
from dotenv import load_dotenv
import difflib

load_dotenv()
client = OpenAI()

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

final_quiz = {
  "The Basics of Complex Numbers":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/01_ Basics of Complex Numbers/finalquiz01.ipynb",
  "Properties of Complex Numbers":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/02_ Properties of Complex Numbers/finalquiz02.ipynb",
  "Complex Numbers on a Plane":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/03_ Complex Numbers on a Plane/finalquiz03.ipynb",
  "Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/04_ Complex Vector Spaces/finalquiz04.ipynb",
  "Complex Vector Spaces Linear Combination, Independence, Basis and Dimensions":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/05_ Complex Vector Spaces_ Linear Combination, Independence, Basis and Dimensions/finalquiz05.ipynb",
  "Properties and Operations on Vectors and Matrices in Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/06_ Properties and Operations on Vectors and Matrices in Complex Vector Spaces/finalquiz06.ipynb",
  "Advanced Concepts in Complex Vector Spaces":"Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/07_ Advanced Concepts in Complex Vector Spaces/finalquiz07.ipynb",
  "Overview of Tensor Analysis": "Quantum Computing Notes/Unit 01 - Quantum Computing and Cryptography/08_ Tensor Analysis/finalquiz08.ipynb"
}

class NotebookGenerator:
    def __init__(self, modules):
        self.modules = modules
        self.selected_concepts = set()
        self.notebook_cells = {}
        self.notebook_metadata =  {}
        self.output = Output()
        self.output2 = Output()
        self.submit_button = Button(description='Submit', disabled=False)
        self.clear_selection_button = Button(description='Clear Selection', disabled=False)
        self.pre_req_concepts = []
        self.selected_quizzes = []
        self.setup_ui()

    def query_openai(self, prompts):
        messages = [ {"role": "system", "content": "You are a grading assistant. User will provide a list of questions and answers. When user prompt to grade, grade all the answers from 0-100 based on their answers to the questions and reply the final grade"}]
        for prompt in prompts:
            messages.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": "Grade my answers"})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or another available model
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_notebook_cells_from_cell_id(self, cell_id):
        return next(
                cell
                for notebook_cell in self.notebook_cells.values()
                for cell in notebook_cell
                if cell.metadata.cell_details.cell_ID == cell_id
                )
    
    def on_submit_clicked(self, b):
        with self.output2:
            notebook = new_notebook()
            for module in self.selected_quizzes:
                with io.open(final_quiz[module], 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, 4)
                for quiz_cell in nb.cells:
                    notebook.cells.append(quiz_cell)

                with open(f'Modules/{module}-final-quiz.ipynb', 'w', encoding='utf-8') as f:
                    nbformat.write(notebook, f)

            print("Notebook created successfully.")

    def clear_selection_clicked(self, b):
        with self.output:
            self.output.clear_output()
            self.selected_concepts.clear()
        with self.output2:
            self.output2.clear_output()
            print("Selection cleared")
    
    def handle_query(self, b):
        with self.output2:
            self.output2.clear_output()
            prompt = self.prompt_input.value
            if prompt:
                response = self.query_openai(prompt)
                print(response)
            else:
                print("Please enter a prompt.")

    def grade_firstquiz(self, n):
        for module in self.selected_quizzes:
            with io.open(f'Modules/{module}-final-quiz.ipynb', 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, 4)
            questionflip = True
            prompts = []
            for quiz_cell in nb.cells[1:]:
                if questionflip:
                    prompts.append('Question: '+ quiz_cell.source)
                else:
                    prompts.append('Answer: '+ quiz_cell.source)
                questionflip = not questionflip
            with self.output2:
                self.output2.clear_output()
                if prompts:
                    response = self.query_openai(prompts)
                    print(response)
                else:
                    print("Please enter a prompt.")

    def on_module_selection(self,change):
        if change['type'] == 'change' and change['name'] == 'value':
            selected_module = change['new'][-1]
            if selected_module  not in self.selected_quizzes:
                self.selected_quizzes.append(selected_module)

    def on_generating_course(self, n):
        with self.output2:
            notebook = new_notebook()
            selected_notebook_cells = []
            seen = set()

            def dfs(cellId, curr_profit):
                neighbours = self.get_notebook_cells_from_cell_id(cellId).metadata.cell_details.cell_prereqs

                for neighbour in neighbours:
                    neighbour_cell = self.get_notebook_cells_from_cell_id(neighbour)
                    if neighbour not in seen and neighbour_cell.metadata.cell_details.cell_concepts[0] not in self.pre_req_concepts:
                        seen.add(neighbour)
                        next_profit = curr_profit / 2 
                        dfs(neighbour, next_profit)
                        neighbour_cell.profit = next_profit
                        selected_notebook_cells.append(neighbour_cell)
                        #notebook.cells.append(neighbour_cell)

            for module in self.selected_quizzes:
                with io.open(modules[module], 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, 4)

                for cell in nb.cells:
                    notebook.cells.append(cell) 

            with open(f'Modules/Course.ipynb', 'w', encoding='utf-8') as f:
                nbformat.write(notebook, f)

            print("Notebook created successfully.")

    def setup_ui(self):
        for module in modules.keys():
                with io.open(modules[module], 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, 4)
                    
                    self.notebook_cells[module] = nb.cells
                    self.notebook_metadata[module] = nb.metadata.module_details

        self.module_selector = widgets.SelectMultiple(
                options=list(final_quiz.keys()),
                value=[],
                description='Concepts',
                disabled=False,
                layout=Layout(width='960px', height='175px')
            )
        self.module_selector.observe(self.on_module_selection)

        self.clear_selection_button.on_click(self.clear_selection_clicked)
        self.submit_button.on_click(self.on_submit_clicked)

        self.select_mode = widgets.RadioButtons(
            options=['Concept - Driven Learning Mode', 'Quiz - Driven Learning Mode'],
            description='Select Mode: '
        )

        self.notebooks_concepts = [
          x for concepts in self.notebook_metadata.values()
          for x in concepts.module_concepts 
        ]

        self.grade_button = Button(description='Grade', disabled=False)
        self.grade_button.on_click(self.grade_firstquiz)
        
        self.generate_course_button = Button(description='Generate Course', disabled=False)
        self.generate_course_button.on_click(self.on_generating_course)
        display(VBox([
            HBox([self.module_selector]),
            HBox([self.submit_button, self.clear_selection_button]),
            HBox([self.grade_button, self.generate_course_button]),
            HBox([self.output2]),
        ]))

NotebookGenerator(modules)
