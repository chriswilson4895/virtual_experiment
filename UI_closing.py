import tkinter as tk
#import sys

def quit_me():
    print('quit')
    window.quit()
    window.destroy()

window = tk.Tk()
window.title("Debrief")
window.protocol("WM_DELETE_WINDOW", quit_me)
# Set the window size and disable resizing
width=400
height=250
window.geometry(f"{width}x{height}")
window.resizable(True, True)
#window.protocol("WM_DELETE_WINDOW", quit_me)

paragraph_text_1 = '''
Experiment Completed!
'''

paragraph_text_2 = '''
Thank you for taking part in my experiment. The aim of this experiment 
was to test how repeated fire drills effect evacuation performance. 
A text file has been generated titled “experiment_data.csv” in the in 
the same location as the game file. Please send this file to the email
address provided below, you should be able to copy and paste the email
address from the box.
'''

paragraph_text_3 = '''
Thank you for taking part.
'''

paragraph_label_1 = tk.Label(window, text=paragraph_text_1)
paragraph_label_1.pack(pady=0,anchor="center")
paragraph_label_2 = tk.Label(window, text=paragraph_text_2,wraplength=width)
paragraph_label_2.pack(pady=0,anchor="center")
paragraph_label_3 = tk.Label(window, text=paragraph_text_3)
paragraph_label_3.pack(pady=0,anchor="center")

textbox = tk.Entry(window, width=40,disabledforeground='black', disabledbackground='white')
textbox.insert(tk.INSERT, 'virtualexperiment2023@gmail.com')
textbox.configure(state='readonly')
textbox.pack(anchor="center")



window.mainloop()
