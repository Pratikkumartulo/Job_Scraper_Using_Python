import requests
from bs4 import BeautifulSoup
import tkinter as tk

def search_job_area_timesjob(job_title, location,progress_box,fill_background_color,print_list):
    j_t_e = job_title.replace(" ", "+")
    loc = location.replace(" ", "+")
    base_url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={j_t_e}&txtLocation={loc}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_divs = soup.find_all("li", {"class": "clearfix job-bx wht-shd-bx"})
    total_jobs = len(job_divs)
    progress_box.insert(tk.END, f"Found {total_jobs} job(s) on Timesjob\n\n")
    job_posts=[]
    i = 0
    for job in job_divs:
        i += 1
        job_post = {}
        name_job = job.find_all("strong", {"class": "blkclor"})
        job_post['url'] = job.find("a").get('href')
        company_name = job.find("h3", {"class": "joblist-comp-name"})
        job_names = " ".join([nj.text for nj in name_job[0:len(name_job) - 1]])
        job_post['title'] = job_names
        job_post['company_name'] = (company_name.text).strip().replace("\n     (More Jobs)", "")
        time_posted = job.find("span", {"class": "sim-posted"})
        job_post['Time_posted'] = (time_posted.find("span").text)
        job_posts.append(job_post)
        progress_box.delete(1.0, tk.END)
        fill_background_color(start_line=0, start_char=0, width=int((i / total_jobs) * 100), height=5, color="lightblue")
        # progress_box.insert(tk.END, f"Processed {i}/{total_jobs} job(s)...\n")
    print_list(job_posts)