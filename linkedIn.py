import requests
from bs4 import BeautifulSoup
import tkinter as tk

def search_job_area_linkedin(job_title, location,progress_box,fill_background_color,print_list):
    job_title_encoded = job_title.replace(" ", "%20")
    location_encoded = location.replace(",", "%2C%20")
    list_url = f"https://www.linkedin.com/jobs/search?keywords={job_title_encoded}&location={location_encoded}"
    response = requests.get(list_url)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")
    id_list = []
    for job in page_jobs:
        base_div = job.find("div", {"class": "base-card"})
        try:
            job_id = base_div.get("data-entity-urn").split(":")[3]
        except:
            continue
        id_list.append(job_id)
    search_no = f"{len(id_list)} job(s) found\n\n"
    progress_box.insert(tk.END, search_no)
    search_id(id_list,progress_box,fill_background_color,print_list)

def search_id(id_list,progress_box,fill_background_color,print_list):
    i=0
    job_list=[]
    for job_id in id_list:
        if i == 10:
            break
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = requests.get(job_url)
        if job_response.status_code == 200:
            job_soup = BeautifulSoup(job_response.text,"html.parser")
            job_post={}
            try:
                job_post["title"]=job_soup.find("h2",{"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
            except:
                job_post["title"]=None
            try:
                job_post["company_name"]=job_soup.find("a",{"class":"topcard__org-name-link topcard__flavor--black-link"}).text.strip()
            except:
                job_post["company_name"]=None
            try:
                job_post["Time_posted"]=job_soup.find("span",{"class":"posted-time-ago__text topcard__flavor--metadata"}).text.strip()
            except:
                job_post["Time_posted"]=None
            try:
                job_post["url"]=job_soup.find("a",{"class":"topcard__link"}).get('href')
            except:
                job_post["url"]=None
            job_list.append(job_post)
            i+=1
            progress_box.delete(1.0, tk.END)
            fill_background_color(start_line=0, start_char=0, width=i*10, height=5, color="lightblue")
    print_list(job_list)