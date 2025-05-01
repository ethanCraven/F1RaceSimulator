import tkinter as tk
from tkinter import *
from constants import PREV_RACE_RESULTS, PREV_RACE_OVERTAKES , AVAILABLE_RACES
import pandas as pd
import pandas as pd
import importlib
import tkinter as tk
from PIL import Image, ImageTk
import threading
import The_Simulation
importlib.reload(The_Simulation)




loading_label = None
results_frame = None
loading_frame = None
simulated_order_frame = None

#Clears the previous results from the file.
def clear_previous_results(race_name):
    filename = f"Data/{race_name}_preliminary_results.csv"
    f = open(filename, "w+")
    f.close()   

    filename = f"Data/{race_name}_final_results.csv"
    f = open(filename, "w+")
    f.close()   


def generate_real_order_text(race_name):
    text = ""
    i=1
    real_result_list = PREV_RACE_RESULTS[race_name]
    for item in real_result_list:
        text = text + str(i) + f": {item}\n"
        i += 1
    return text


def generate_real_order_frame(root, race_name):

    real_order_frame = Frame(root, highlightbackground="white", highlightthickness=1)
    real_order_frame.pack(side=LEFT, anchor="nw")
    real_order_frame.configure(background="#0e0033")


    real_order_title_label = Label(real_order_frame, background="#0e0033", text="Real Life Order:", fg="Red", font=('Arial', 18), justify="left").pack(padx=10, pady=10)


    real_order = generate_real_order_text(race_name)
    real_order_label = Label(real_order_frame, background="#0e0033", fg="white", text=real_order, font=('Arial', 14), justify="left").pack(padx=10, pady=10)

    number_of_overtakes = PREV_RACE_OVERTAKES[race_name]
    overtakes_label = Label(real_order_frame, background="#0e0033", fg="white", text=f"Number of Overtakes: {number_of_overtakes}", font=('Arial', 12), justify="left")
    overtakes_label.pack()
    


    return real_order_frame

#Calculates the average simulated order. 
def generate_average_simulated_order(race_name):
    results_df = pd.read_csv(f'Data/{race_name}_final_results.csv')
    refined_results_df = results_df[["Driver", "finishing_position", "race_time", "overtakes"]]

    averages = refined_results_df.groupby("Driver").mean()
    averages = averages.rename(columns={
        "finishing_position": "avg_finishing_position",
        "race_time": "avg_race_time",
        "overtakes": "avg_overtakes"
    })
    average_results = averages.sort_values(by=['avg_finishing_position'])
    return average_results


def generate_simulated_order_frame(root, simulated_results):

    results_frame = Frame(root, highlightbackground="white", highlightthickness=1)
    results_frame.pack(side="top", anchor="n", fill="x")
    results_frame.configure(background="#0e0033")


    if simulated_results.empty:
        return results_frame
    else:
        results_title = Label(results_frame, text="Simulated Order:", background="#0e0033", fg="Red", font=('Arial', 18), justify="left")
        results_title.pack(pady=10)

        header = f"{"":<15} {'Driver'} {'Avg Pos':<5} {'Avg Time (s)'}"
        header_label = Label(results_frame, text=header, background="#0e0033", fg="white", font=('Arial', 12, 'bold'), anchor="w", justify="left")
        header_label.pack(padx=10, anchor="w")


        presentable_results = ""

        for i, (driver, row) in enumerate(simulated_results.iterrows(), start=1):
            avg_pos = round(row["avg_finishing_position"], 2)
            avg_time = round(row["avg_race_time"], 2)
            presentable_results += (f"{i}: {driver}: {avg_pos}, {avg_time}s \n")


        simulated_order_label = Label(results_frame, text=presentable_results, fg="white", background="#0e0033", font=('Arial', 10), justify="left").pack(padx=10, pady=(1,0), side="top")

        simulated_overtakes = round(sum(simulated_results["avg_overtakes"]), 2)
        
        simulated_overtakes_label = Label(results_frame, fg="white", background="#0e0033",  text=f"\n Number of Overtakes: {simulated_overtakes}", font=('Arial', 12), justify="left")
        simulated_overtakes_label.pack(anchor="s")
        return results_frame



def generate_right_container_frame(root):
    right_frame = Frame(root, bg="#0e0033")
    right_frame.pack(side=RIGHT, anchor="e", fill="y")
    image_frame = Frame(right_frame, width=300, height=300, bg="#0e0033")
    image_frame.pack(side=TOP, anchor="n")

    img = Image.open("Data/F1_car_image.jpg")
    img = img.resize((320, 180), Image.LANCZOS)
    
    f1_car_image = ImageTk.PhotoImage(img)
    image_label = Label(image_frame, image=f1_car_image)
    image_label.pack()
    image_label.image = f1_car_image



    resimulate_frame = Frame(right_frame, bg="#0e0033")
    resimulate_frame.pack(side=TOP, anchor="n")

 

    default_race = tk.StringVar(root, AVAILABLE_RACES[0])
    race_label = Label(resimulate_frame, text="Select Race To Simulate:", font=('calibre',10, 'bold'), background="#0e0033", fg="white")
    race_label.pack()
    race_selector = OptionMenu(resimulate_frame, default_race, *AVAILABLE_RACES)
    race_selector.pack()

    preliminary_simulation_label = Label(resimulate_frame, text="Number of Preliminary Simulations:", font=('calibre',10, 'bold'), background="#0e0033", fg="white")
    preliminary_simulation_label.pack(pady=(20,0))
    preliminary_simulation_entry = Entry(resimulate_frame)
    preliminary_simulation_entry.pack()

    final_simulation_label = Label(resimulate_frame, text="Number of Optimised Simulations:", font=('calibre',10, 'bold'), background="#0e0033", fg="white")
    final_simulation_label.pack(pady=(20,0))
    final_simulation_entry = Entry(resimulate_frame)
    final_simulation_entry.pack()

    simulate_button = Button(resimulate_frame, text="Simulate Races", command=lambda: rerun_simulations(root, default_race, preliminary_simulation_entry, final_simulation_entry), bg="white")
    simulate_button.pack(pady=25)

    return right_frame


#Re runs the simulations from the main window. 
def rerun_simulations(root, default_race, preliminary_sim_entry, final_sim_entry):
    race_name = default_race.get()
    clear_previous_results(race_name)
    init_sims = int(preliminary_sim_entry.get())
    final_sims = int(final_sim_entry.get())
    for widget in root.winfo_children():
        widget.destroy()
    
    loading_label = Label(root, text="Simulation Loading Please Wait", background="#0e0033", fg="White", font=('calibre', 20))
    loading_label.pack(pady=50)
    root.update_idletasks()
    The_Simulation.run_simulation(race_name, init_sims, final_sims)
    show_main_window(root, race_name)

def generate_loading_label(root):
    global loading_label
    global loading_frame
    if loading_label:
        loading_label.config(text="Running Simulation...")
        return loading_frame, loading_label
    loading_frame = Frame(root, highlightbackground="white", highlightthickness=1)
    loading_frame.pack(side="bottom")


    loading_label = Label(loading_frame, text="Loading test", fg="white", background="#0e0033", font=('Arial', 14))
    loading_label.pack()
    return loading_frame, loading_label


#Main method that runs the initial window. 
def run_intial_window():
    root = tk.Tk()
    root.geometry("800x400")
    root.configure(background="#414643")
    root.title("Simulation Menu")

    title_label = Label(root, background="#414643", fg="white", text="Formula One Race Simulator", font=('Arial', 18))
    title_label.pack(padx=40)
    default_race = tk.StringVar(root, AVAILABLE_RACES[0])



    race_label = Label(root, text="Select Race To Simulate:", font=('calibre',10, 'bold'), background="#414643", fg="white")
    race_label.pack()
    race_selector = OptionMenu(root, default_race, *AVAILABLE_RACES)
    race_selector.pack()

    preliminary_simulation_label = Label(root, text="Number of Preliminary Simulations:", font=('calibre',10, 'bold'), background="#414643", fg="white")
    preliminary_simulation_label.pack(pady=(20,0))
    preliminary_simulation_entry = Entry(root)
    preliminary_simulation_entry.pack()

    final_simulation_label = Label(root, text="Number of Optimised Simulations:", font=('calibre',10, 'bold'), background="#414643", fg="white")
    final_simulation_label.pack(pady=(20,0))
    final_simulation_entry = Entry(root)
    final_simulation_entry.pack()
    


    #Uses threading to update the GUI and run the simulations.
    def run_simulations():
        def simulation_thread():
            try:
                race_name = default_race.get()
                clear_previous_results(race_name)
                init_sims = int(preliminary_simulation_entry.get())
                final_sims = int(final_simulation_entry.get())
                preliminary_simulation_entry.destroy()
                final_simulation_entry.destroy()
                final_simulation_label.destroy()
                preliminary_simulation_label.destroy()
                race_selector.destroy()
                race_label.destroy()
                simulate_button.destroy()
                loading_label = Label(root, text="Simulation Loading Please Wait", background="#414643", fg="White")
                loading_label.pack(pady=50)
                The_Simulation.run_simulation(race_name, init_sims, final_sims)
                root.after(0 ,lambda: show_main_window(root,race_name))
            except ValueError:
                error_label = Label(root, text="Please enter valid inputs", background="#414643", fg="red")
                error_label.pack(pady=(5,0))
        threading.Thread(target=simulation_thread, daemon=True).start()

    simulate_button = Button(root, text="Simulate Races", command=lambda: run_simulations(), bg="white")
    simulate_button.pack(pady=25)
    root.mainloop()





def generate_simulation_page_title(root, race_name):
    race_name = race_name.capitalize()
    title_frame = Frame(root, bg="#0e0033", pady=20)
    title_frame.pack(fill=X)

    title_label = tk.Label(title_frame, text=f"{race_name} Race Simulation Results", font=("Helvetica", 24, "bold"), fg="#ecf0f1", bg="#0e0033")
    title_label.pack()

def show_main_window(old_root, race_name):
    
    old_root.destroy()
    root = tk.Tk()
    root.geometry("1000x800")
    root.configure(background="#0e0033")
    root.title("Race Simulation Results")



    generate_simulation_page_title(root, race_name)
    generate_right_container_frame(root)
    generate_real_order_frame(root, race_name)
    simulated_results = generate_average_simulated_order(race_name)
    generate_simulated_order_frame(root, simulated_results)


root = run_intial_window()