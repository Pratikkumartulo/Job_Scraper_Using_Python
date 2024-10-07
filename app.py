import tkinter as tk
from bs4 import BeautifulSoup
import threading
import linkedIn
import timeJobs
import fresherWorld
import pandas as pd
from datetime import datetime

local_job_list = []
root = tk.Tk()
root.title("Job Hunter")
progress_box = tk.Text(root,height=1, width=100,state=tk.DISABLED)
progress_box.grid(row=4, column=0, columnspan=2)

def fill_background_color(start_line, start_char, width, height, color):
    for i in range(height):
        progress_box.configure(state=tk.NORMAL)
        progress_box.insert(f"{start_line + i}.{start_char}", " " * width)
        end_char = start_char + width
        progress_box.tag_add("highlight", f"{start_line + i}.{start_char}", f"{start_line + i}.{end_char}")
    progress_box.tag_configure("highlight", background=color)

def search_jobs():
    job_title = job_title_entry.get()
    location = job_location_entry.get()
    selected_website = website_var.get()
    if(selected_website == "LinkedIn"):
        linkedIn.search_job_area_linkedin(job_title, location,progress_box,fill_background_color,print_list)
        threading.Thread(target=linkedIn.search_job_area_linkedin, args=(job_title, location,progress_box,fill_background_color,print_list)).start()
    if(selected_website == "Timesjob"):
        timeJobs.search_job_area_timesjob(job_title, location,progress_box,fill_background_color,print_list)
        threading.Thread(target=timeJobs.search_job_area_timesjob, args=(job_title, location,progress_box,fill_background_color,print_list)).start()
    if(selected_website == "Freshersworld"):
        fresherWorld.search_job_area_timesjob(job_title, location,progress_box,fill_background_color,print_list)
        threading.Thread(target=fresherWorld.search_job_area_timesjob, args=(job_title, location,progress_box,fill_background_color,print_list)).start()
    job_results_box.delete(1.0, tk.END) 
    progress_box.delete(1.0, tk.END)

def print_list(job_list):
    global local_job_list
    local_job_list = job_list
    for job in job_list:
        job_info = f"Title: {job['title']}\nCompany: {job['company_name']}\nPosted: {job['Time_posted']}\nLink: {job['url']}\n\n"
        job_results_box.insert(tk.END, job_info)

def export_excel():
    global local_job_list
    if not local_job_list:
        progress_box.configure(state=tk.NORMAL)
        progress_box.insert(tk.END, "No jobs to export.\n")
        progress_box.configure(state=tk.DISABLED)
        return
    local_job_list_pd = pd.DataFrame(local_job_list)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{website_var.get()}-{now}.xlsx"
    local_job_list_pd.to_excel(filename)
    progress_box.configure(state=tk.NORMAL)
    progress_box.delete(1.0, tk.END)
    progress_box.insert(tk.END, f"Exported to {filename}\n")
    progress_box.configure(state=tk.DISABLED)



job_input_frame = tk.Frame(root)
job_input_frame.grid(row=0, column=0, padx=20, pady=20)

# Center the input boxes within the frame using grid
job_title_label = tk.Label(job_input_frame, text="Job Title:")
job_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # Align to the right

job_title_entry = tk.Entry(job_input_frame, width=30)
job_title_entry.grid(row=0, column=1, padx=10, pady=10)

job_location_label = tk.Label(job_input_frame, text="Job Location:")
job_location_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")  # Align to the right

job_location_entry = tk.Entry(job_input_frame, width=30)
job_location_entry.grid(row=1, column=1, padx=10, pady=10)

# Make sure the columns and frame expand and stay centered
job_input_frame.grid_columnconfigure(0, weight=1)
job_input_frame.grid_columnconfigure(1, weight=1)

root.grid_columnconfigure(0, weight=1)


website_frame = tk.Frame(root)
website_frame.grid(row=2, column=0, padx=10, pady=10)

website_label = tk.Label(website_frame, text="Select Website:")
website_label.grid(row=2, column=0, padx=10, pady=10)



website_var = tk.StringVar(value="LinkedIn")
websites = ["LinkedIn", "Timesjob", "Freshersworld"]
website_menu = tk.OptionMenu(website_frame, website_var, *websites)
website_menu.grid(row=2, column=1, padx=10, pady=10)



search_button = tk.Button(root, text="Search Jobs", command=search_jobs)
search_button.grid(row=3, column=0, columnspan=2, pady=20)

results_frame = tk.Frame(root)
results_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

job_results_box = tk.Text(results_frame, height=20, width=100, wrap=tk.NONE)
job_results_box.grid(row=0, column=0, sticky="nsew")

vertical_scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=job_results_box.yview)
vertical_scrollbar.grid(row=0, column=1, sticky="ns")

horizontal_scrollbar = tk.Scrollbar(results_frame, orient="horizontal", command=job_results_box.xview)
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

job_results_box.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)


export_btn = tk.Button(root,text="Export Excel",command=export_excel)
export_btn.grid(row=8,column=0)


results_frame.grid_rowconfigure(0, weight=1)
results_frame.grid_columnconfigure(0, weight=1)

root.mainloop()