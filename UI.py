import tkinter as tk
#import sys
import csv
from pandas import DataFrame,concat

def quit_me():
    #print('quit')
    window.quit()
    window.destroy()

def refresh_window():
    # Destroy existing widgets
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Questionaire")

    # Create a new paragraph label
    paragraph_text = '''
    Before starting the experiment, please provide your gender and your age.
    '''
    paragraph_label = tk.Label(window, text=paragraph_text)
    paragraph_label.pack(pady=10,anchor="center")

    # Create a label for radio buttons
    radio_label = tk.Label(window, text="What is your gender?")
    radio_label.pack(anchor="w")

    # Create a variable to hold the selected radio button value
    global radio_var
    radio_var = tk.StringVar()

    # Create radio buttons
    radio_button1 = tk.Radiobutton(window, text="Male", variable=radio_var, value="M", command=check_button_state_2)
    radio_button1.pack(anchor=tk.W)

    radio_button2 = tk.Radiobutton(window, text="Female", variable=radio_var, value="F", command=check_button_state_2)
    radio_button2.pack(anchor=tk.W)

    radio_button3 = tk.Radiobutton(window, text="Other", variable=radio_var, value="O", command=check_button_state_2)
    radio_button3.pack(anchor=tk.W)

    radio_button4 = tk.Radiobutton(window, text="Prefer not to say", variable=radio_var, value="PN", command=check_button_state_2)
    radio_button4.pack(anchor=tk.W)

    # Create a label for the text box
    text_label = tk.Label(window, text="What's your age in years? (if you'd rather not say, put 0)")
    text_label.pack(anchor="w")

    # Create a text box
    global text_box
    text_box = tk.Text(window, height=1, width=5)
    text_box.pack(anchor="w")
    text_box.bind("<KeyRelease>", check_button_state_2)

    # Create a button
    global submit_button
    submit_button = tk.Button(window, text="Submit", command=button_click_2, state=tk.DISABLED)
    submit_button.pack(pady=10,side="bottom")

    # Check the initial state of the button
    check_button_state_2()

def check_button_state_2(event=None):
    if radio_var.get() and text_box.get("1.0", "end-1c"):
        submit_button.config(state=tk.NORMAL)
    else:
        submit_button.config(state=tk.DISABLED)
        
def check_button_state():
    if checkbox1.get() and checkbox2.get() and checkbox3.get() and checkbox4.get():
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)

def button_click():
    selected_options = []
    if checkbox1.get() == 1:
        selected_options.append(checkbox_texts[0])
    if checkbox2.get() == 1:
        selected_options.append(checkbox_texts[1])
    if checkbox3.get() == 1:
        selected_options.append(checkbox_texts[2])
    if checkbox4.get() == 1:
        selected_options.append(checkbox_texts[3])
    #print("Selected options:", selected_options)

    # Refresh the window
    refresh_window()

def button_click_2():
    global age
    global gender
    global allSatisfied
    gender = radio_var.get()
    age = text_box.get("1.0", "end-1c")
    #print("Selected option:", selected_option)
    #print("Entered text:", entered_text)

    allSatisfied = True
    #print(allSatisfied)
    # Destroy Tkinter window
    quit_me()

# Create the main window
window = tk.Tk()
window.title("Consent Form")


# Set the window size and disable resizing
width=400
height=400
window.geometry(f"{width}x{height}")
window.resizable(True, True)
window.protocol("WM_DELETE_WINDOW", quit_me)

# Create a label with paragraph text
paragraph_text = '''
Welcome to the experiment. Before taking part in the experiment, 
please make sure that you have read the Participant Information 
Sheet for “A virtual experiment on pedestrian behaviour” so that 
you know exactly what data we will collect, how it will be used 
and stored, as well as what this experiment will entail and what 
you will be expected to do.
'''

paragraph_label = tk.Label(window, text=paragraph_text,wraplength=width)
paragraph_label.pack(pady=0)

instruction_text = '''
Before taking part in the experiment, please confirm the following:
'''

instruction_label = tk.Label(window, text=instruction_text)
instruction_label.pack(pady=0,anchor="w")


checkbox3text = '''
I understand that after the study the data will be made “open data” as 
defined in the Participant Information Sheet. 
'''
checkbox2text = '''
I confirm that I have had an opportunity to ask questions about the 
study.
'''

# Create a dictionary to store the checkboxes and their corresponding text
checkbox_texts = ["I confirm that I have read the participant information sheet.", 
                  checkbox2text, 
                  checkbox3text,
                  "I hereby fully and freely consent to my participation in this study."]
checkbox1 = tk.BooleanVar()
checkbox2 = tk.BooleanVar()
checkbox3 = tk.BooleanVar()
checkbox4 = tk.BooleanVar()

checkbox1.set(False)
checkbox2.set(False)
checkbox3.set(False)
checkbox4.set(False)

# Create four checkboxes with labels
checkboxes = []
for i, text in enumerate(checkbox_texts):
    checkbox = tk.Checkbutton(window, text=text, variable=eval(f"checkbox{i+1}"), command=check_button_state)
    checkbox.pack(anchor="w", padx=0, pady=0)
    checkboxes.append(checkbox)

# Create a button
button = tk.Button(window, text="Submit", command=button_click, state=tk.DISABLED)
button.pack(pady=0)


allSatisfied = False
age = 0
gender = ""

# Start the main event loop
window.mainloop()
age = str(age)
gender = str(gender)
#print(allSatisfied)
#print(age)
#print(gender)
if allSatisfied == True:
    from sol import df,evacs,treatment
    treatment = str(treatment)
    if evacs == 3:
        file_path = 'experiment_data.csv'
    
    
        # Data to add as new columns
        data_to_add = {
            "age": age,
            "gender": gender,
            "treatment": treatment
        }
        
        # Create a DataFrame from the data_to_add dictionary
        new_data_df = DataFrame(data_to_add, index=[1, 2, 3])
        
        # Concatenate the original DataFrame (df) with the new_data_df along the columns (axis=1)
        df = concat([df, new_data_df], axis=1)
        
        # Save the DataFrame with the new columns to the CSV file
        file_path = 'experiment_data.csv'
        df.to_csv(file_path, index_label='Index')
    
        """
        df.to_csv(file_path, index_label='Index')
        
        with open(file_path, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
        
            # Data to add as a new row
            data_to_add = [["age",age],
                           ["gender",gender],
                           ["treatment",treatment]]
            
            for row in data_to_add:
                csv_writer.writerow(row)
        """
        import UI_closing
#else:
#    print("early exit")
    #sys.exit()


