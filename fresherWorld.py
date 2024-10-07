import requests
from bs4 import BeautifulSoup
import tkinter as tk

def search_job_area_timesjob(job_title, location,progress_box,fill_background_color,print_list):
    j_t_e = job_title.replace(" ","-")
    j_l_e = location.replace(" ","-")
    base_url = f"https://www.freshersworld.com/jobs/jobsearch/{j_t_e}-jobs-in-{j_l_e}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text,"html.parser")
    page_jobs = soup.find_all("div",{"class":"col-md-12 col-lg-12 col-xs-12 padding-none job-container jobs-on-hover top_space"})
    total_jobs = len(page_jobs)
    progress_box.insert(tk.END, f"Found {total_jobs} job(s) on Timesjob\n\n")
    job_posts=[]
    j=0
    for i in page_jobs:
        j+=1
        job_list={}
        job_list["title"] = i.find("span",{"class":"wrap-title seo_title"}).text
        job_list['company_name'] = i.find("h3",{"class":"latest-jobs-title font-16 margin-none inline-block company-name"}).text
        job_list['Time_posted'] = i.find("div",{"class":"text-ago"}).text
        job_list['url'] = i.get('job_display_url')
        job_posts.append(job_list)
        progress_box.delete(1.0, tk.END)
        fill_background_color(start_line=0, start_char=0, width=j*10, height=5, color="lightblue")
    print_list(job_posts)