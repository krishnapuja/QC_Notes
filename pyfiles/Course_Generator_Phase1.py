import io
import nbformat
from nbformat.v4 import new_notebook
from IPython.display import display
from ipywidgets import Layout, Button, Box, widgets, VBox, HBox, Output, Label, Text
from openai import OpenAI
import heapq
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
excluded_cells = ["learningoutcomes", "warmup", "summary", "finalquiz", "conclusions"]

class NotebookGenerator:
    def __init__(self, modules):
        self.modules = modules
        self.selected_concepts = set()
        self.notebook_cells = {}
        self.notebook_metadata =  {}
        self.accordion = self.create_accordion()
        self.output = Output()
        self.output2 = Output()
        self.submit_button = Button(description='Submit', disabled=False)
        self.clear_selection_button = Button(description='Clear Selection', disabled=False)
        self.pre_req_concepts = []
        self.setup_ui()
    
    def fractionalKnapsack(self, total_time, arr):
        arr.sort(key=lambda x: (x.profit/int(x.metadata.cell_details.cell_estimated_time)), reverse=True)    
    
        finalvalue = []
        W = int(total_time)
        prev_profit = 100
    
        for item in arr:
            estimated_time = int(item.metadata.cell_details.cell_estimated_time)
            if estimated_time <= W:
                W -= estimated_time
                if prev_profit == item.profit:
                    finalvalue.append(item)
                else:
                    finalvalue.insert(0,item)
                prev_profit = item.profit
    
            # # If we can't add current Item, 
            # # add fractional part of d
            # else:
            #     finalvalue += item.profit * W / item.fracProfit
            #     break
        
        # Returning final value
        return finalvalue

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

    def create_accordion(self):
        accordion_children = []
        for module_name in self.modules.keys():
            select_multiple = widgets.SelectMultiple(
                options=self.get_outcomes_for_module(module_name),
                value=[],
                description='Concepts',
                disabled=False,
                layout=Layout(width='960px', height='175px')
            )
            accordion_children.append(select_multiple)
        accordion = widgets.Accordion(children=accordion_children,layout=Layout(width='1000px'))
        for i, module_name in enumerate(self.modules.keys()):
            accordion.set_title(i, module_name)
        return accordion

    def get_outcomes_for_module(self, module_name):
        with io.open(modules[module_name], 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, 4)
            
        #module_title = [x.metadata.cell_details.cell_ID for x in nb.cells]
        #concept_list = list(filter(lambda x: x.split('-')[1].lower() not in excluded_cells, module_title))
        self.notebook_cells[module_name] = nb.cells
        self.notebook_metadata[module_name] = nb.metadata.module_details
        #print(nb.metadata.module_details)
        return nb.metadata.module_details.module_outcomes

    def on_change(self, change):
        with self.output:
            if change['type'] == 'change' and change['name'] == 'value':
                selected_outcome = change['new'][-1]
                for i,notebook_metadata in enumerate(self.notebook_metadata.values()):
                    module_outcomes = notebook_metadata.module_outcomes
                    if selected_outcome in module_outcomes:
                        module_index = module_outcomes.index(selected_outcome)
                        cell_concepts = notebook_metadata.module_outcomes_mapping[module_index]
                        for cell in cell_concepts:
                            if "final-quiz" in cell:
                                print(cell)
                                module_final_quiz = list(final_quiz.values())[i]
                                notebook = new_notebook()
                                with io.open(module_final_quiz, 'r', encoding='utf-8') as f:
                                    nb = nbformat.read(f, 4)
                                for quiz_cell in nb.cells:
                                    notebook.cells.append(quiz_cell)
                                with open(f'Modules/{cell}.ipynb', 'w', encoding='utf-8') as f:
                                    nbformat.write(notebook, f)
            
                            elif cell not in self.selected_concepts:
                                self.selected_concepts.add(cell)
                                print(cell)

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
            selected_notebook_cells = []
            seen = set()
            visited = set()
            total_time = (self.estimated_time.value and int(self.estimated_time.value)) or 10000

            '''
            Below two blocks of code iterates through all nodes using DFS approach and caluculate the total Profit for each node using
            profits of child nodes. 
            '''
            def dfsWeightCalc(cellId, curr_profit):
                '''
                This Method iterates through the neighbouring (or child) nodes using DFS approach and caluculate the total 
                profit for all the nodes using profits of child nodes. 
                profit of a cell = profit of the level/ estimated time. (profit = 1 for all levels at present) = 1 / estimated time
                profit of parent cell =  sum of profit of all child cells + profit of current cell
                '''  
                totlfracProfit = 0
                neighbours = self.get_notebook_cells_from_cell_id(cellId).metadata.cell_details.cell_prereqs
                
                for neighbour in neighbours:
                    fracProfit = 0
                    neighbour_cell = self.get_notebook_cells_from_cell_id(neighbour)
                    if neighbour not in visited:
                        visited.add(neighbour)
                        next_profit = curr_profit
                        fracProfit += next_profit*int(neighbour_cell.metadata.cell_details.cell_estimated_time) + dfsWeightCalc(neighbour, next_profit)
                        neighbour_cell.profit = next_profit
                        neighbour_cell.fracProfit = fracProfit
                        totlfracProfit += fracProfit
                    elif neighbour in visited:
                        totlfracProfit += neighbour_cell.fracProfit
                return totlfracProfit

            '''
                Below block of code process the concepts for the selected outcome and caluculate the total 
                profit for all the nodes. 
                profit of a cell = profit of the level / estimated time. (profit = 1 for all levels at present) = 1 / time
                profit of parent cell =  sum of profit of all child cells + profit of current cell
            '''
            for concept in self.selected_concepts:
                concept_cell = self.get_notebook_cells_from_cell_id(concept)
                if  concept not in visited:
                    visited.add(concept)
                    curr_profit = 1
                    fracProfit = dfsWeightCalc(concept,curr_profit)
                    concept_cell.profit = curr_profit
                    concept_cell.fracProfit = fracProfit+ curr_profit*int(concept_cell.metadata.cell_details.cell_estimated_time)
                    #print(concept,concept_cell.metadata.cell_details.cell_estimated_time, concept_cell.fracProfit)

            '''
            Below two blocks of code iterates through all nodes using DFS approach and pick the cells using the given available time.  
            '''    
            def dfs(cellId, total_time):
                neighbours = self.get_notebook_cells_from_cell_id(cellId).metadata.cell_details.cell_prereqs
                neighbour_cells = []

                # get the cell content using cellId
                for neighbour in neighbours:
                    neighbour_cells.append(self.get_notebook_cells_from_cell_id(neighbour))
                #print(neighbour_cells)
                # sort the cells using profit such that cells with more profit is prioritized first    
                neighbour_cells = sorted(neighbour_cells, reverse=True, key=lambda x: x.fracProfit if total_time - x.fracProfit > 0 else total_time - x.fracProfit )

                ''' 
                iterate through child cells for each cell and pick the cells if the cell time is less than total time available.
                After picking subtract the cell time from available time.
                '''
                for neighbour_cell in neighbour_cells:
                    neighbour = neighbour_cell.metadata.cell_details.cell_ID
                    if total_time > 0 and neighbour not in seen and neighbour_cell.metadata.cell_details.cell_concepts[0] not in self.pre_req_concepts:
                        seen.add(neighbour)
                        total_time = dfs(neighbour, total_time)
                        #print(neighbour, neighbour_cell.metadata.cell_details.cell_estimated_time, neighbour_cell.fracProfit)
                        print(neighbour)
                        cell_time = int(neighbour_cell.metadata.cell_details.cell_estimated_time)
                        if cell_time <= total_time:
                            total_time -= cell_time
                            selected_notebook_cells.append(neighbour_cell)
                return total_time

            ''' 
                iterate through the cells for every outcome and iterate through the child cells and pick the cells 
                if the cell time is less than total time available.
                After picking subtract the cell time from available time.
            '''
            
            concept_cells = []
            # get the cell content using cellIds
            for concept in self.selected_concepts:
                concept_cells.append(self.get_notebook_cells_from_cell_id(concept))

            # sort the cells using profit such that cells with more profit is prioritized first 
            concept_cells = sorted(concept_cells, reverse=True, key=lambda x: x.fracProfit)                    
            
            ''' 
                iterate through child cells for each cell and pick the cells if the cell time is less than total time available.
                After picking subtract the cell time from available time.
            '''
            for concept_cell in concept_cells:
                concept = concept_cell.metadata.cell_details.cell_ID
                

                if total_time > 0 and concept not in seen and concept_cell.metadata.cell_details.cell_concepts[0] not in self.pre_req_concepts:
                    #print('dddd',concept)
                    seen.add(concept)
                    total_time = dfs(concept,total_time)
                    print(concept)
                    cell_time = int(concept_cell.metadata.cell_details.cell_estimated_time)
                    if cell_time <= total_time:
                        total_time -= cell_time
                        selected_notebook_cells.append(concept_cell)

            for item in selected_notebook_cells:
                notebook.cells.append(item) 

            with open(f'Modules/Course.ipynb', 'w', encoding='utf-8') as f:
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

    def multi_checkbox_widget(self, descriptions):
        """ Widget with a search field and lots of checkboxes """
        search_widget = widgets.Text()
        options_dict = {description: widgets.Checkbox(description=description, value=False) for description in descriptions}
        options = [options_dict[description] for description in descriptions]
        #options_widget = widgets.VBox(options)
        widge = []
        for i in range(0, len(options), 3):
            row = options[i:i+3]
            widge.append(widgets.HBox(row, layout={'width': '1000px'}))
        options_widget = widgets.VBox(widge)       
        multi_select = widgets.VBox([search_widget, options_widget])
        
        def on_check_select_change(change):
            if change['type'] == 'change' and change['name'] == 'value' and change['new'] == True:
                self.pre_req_concepts.append(change['owner'].description)
                print(self.pre_req_concepts)

        for option in options:
            option.observe(on_check_select_change)

        # Wire the search field to the checkboxes
        def on_text_change(change):
            search_input = change['new']
            if search_input == '':  
                # Reset search field
                new_options = [options_dict[description] for description in descriptions]
            else:
                # Filter by search field using difflib.
                close_matches = difflib.get_close_matches(search_input, descriptions, cutoff=0.0)
                new_options = [options_dict[description] for description in close_matches]
            #options_widget. = new_options
            widge = []
            for i in range(0, len(new_options), 3):
                row = new_options[i:i+3]
                widge.append(widgets.HBox(row, layout={'width': '1000px'}))
            options_widget.children = widge

        search_widget.observe(on_text_change, names='value')
        return multi_select
    
    def grade_firstquiz(self, n):
        with io.open(list(final_quiz.values())[0], 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, 4)
        prompt = ''
        questionflip = True
        prompts = []
        for quiz_cell in nb.cells[1:]:
            if questionflip:
                prompts.append('Question: '+ quiz_cell.source)
            else:
                prompts.append('Answer: '+ quiz_cell.source)
            questionflip = not questionflip
        print(prompts)
        with self.output2:
            self.output2.clear_output()
            if prompts:
                response = self.query_openai(prompts)
                print(response)
            else:
                print("Please enter a prompt.")

        

    def setup_ui(self):
        for selectedMultiple in self.accordion.children:
            selectedMultiple.observe(self.on_change)

        self.clear_selection_button.on_click(self.clear_selection_clicked)
        self.submit_button.on_click(self.on_submit_clicked)

        self.estimated_time = Text(placeholder='Estimated Time', disabled=False, layout=Layout(width='500px'))
        self.estimated_time_label = Label(value='Estimated Time: ')

        self.select_mode = widgets.RadioButtons(
            options=['Concept - Driven Learning Mode', 'Quiz - Driven Learning Mode'],
            description='Select Mode: '
        )

        # self.quizzes = widgets.SelectMultiple(
        #         options=self.notebook_metadata.keys(),
        #         value=[],
        #         disabled=False,
        #         layout=Layout(width='1000px', height='175px')
        #     )
        self.notebooks_concepts = [
          x for concepts in self.notebook_metadata.values()
          for x in concepts.module_concepts 
        ]
        self.pre_reqs_label = Label(value='Let us know if already know below topics: ')

        self.pre_reqs = self.multi_checkbox_widget(self.notebooks_concepts)
        self.prompt_input = Text(placeholder='Enter your prompt here', layout=Layout(width='400px'))
        self.query_button = Button(description='Ask OpenAI', disabled=False)
        self.query_button.on_click(self.handle_query)

        self.grade_button = Button(description='Grade', disabled=False)
        self.grade_button.on_click(self.grade_firstquiz)
        
        display(VBox([
            #HBox([self.select_mode]),
            HBox([self.pre_reqs_label]),
            HBox([self.pre_reqs]),
            HBox([self.accordion]),
            # HBox([self.quizzes]),
            HBox([self.estimated_time_label, self.estimated_time]),
            HBox([self.submit_button, self.clear_selection_button]),
            # HBox([self.prompt_input, self.query_button]),
            # HBox([self.grade_button]),
            HBox([self.output2]),
        ]))

NotebookGenerator(modules)
