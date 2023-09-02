from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
import selenium
import csv
import os
import multiprocessing
import re

def convert_string_to_integer(string, default_value):
  if not string:
    return default_value
  else:
    return int(string)

def get_requirements():
    global JOB_title,experience_input,location_input,pages_input,csv_file_name
    print("======================================\nNAUKRI WEB SCRAPER\n======================================")
    JOB_title=input("Enter skills/ designations/ companies \n---------------------------------------\n-> ")
    experience_input=input("======================================\nSelect Experience (Press Enter to skip) \n1.Fresher\n2.1 Year\n3.2 Years\n4.3 Years\n5.4 Years\n6.5 Years\n======================================\n-> ")
    location_input=input("======================================\nEnter Location (Press Enter to skip)\n---------------------------------------\n-> ")
    pages_input=input("======================================\nEnter number of pages to scrape (Press Enter to skip)\n---------------------------------------\n-> ")
    csv_file_name=input("======================================\nEnter CSV file name (Press Enter to skip)\n---------------------------------------\n-> ")

def start(url):
    global driver
   # Get the path to the Chrome profile directory.
    chrome_profile_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")

    # Create a ChromeOptions object and set the user data directory to the logged-in profile directory.
    options = selenium.webdriver.ChromeOptions() 
    options.add_argument("--start-maximized" )
    options.add_argument(f"user-data-dir={chrome_profile_dir}")
    print("======================================\nStarting ChromeDriver\n======================================")

    # Create a ChromeWebDriver object and pass in the ChromeOptions object.
    driver = selenium.webdriver.Chrome(options=options)
    driver.get(url)
    

   
def set_csv():
    
    # cwd = os.getcwd()
    global csv_path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    csv_path = os.path.join(dir_path, csv_file_name+".csv")
    if(csv_file_name==""):
        csv_path=os.path.join(dir_path, JOB_title+" Data"+".csv")

    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = ["Job", "Company", "Experience", "Salary", "Location", "Description", "Skill 1","Skill 2","Skill 3","Skill 4","Skill 5", "Posted", "Date Recorded"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def land_first_page():
    # Load the initial page
    driver.get("https://www.naukri.com")
    driver.implicitly_wait(3)
    search_element = driver.find_element(By.CLASS_NAME, "suggestor-input")
    search_element.send_keys(JOB_title)
    
    
    DropDownMenu=driver.find_element(By.CSS_SELECTOR,"span.dropArrowDD")
    DropDownMenu.click()
    if(experience_input=="1"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[1]").click()
    elif(experience_input=="2"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[2]").click()
    elif(experience_input=="3"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[3]").click()
    elif(experience_input=="4"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[4]").click()
    elif(experience_input=="5"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[5]").click()
    elif(experience_input=="6"):
        driver.find_element(By.XPATH,"//*[@id=\"sa-dd-scrollexpereinceDD\"]/div[1]/ul/li[6]").click()
    else:
        pass

    if(location_input!=""):
        location_field=driver.find_element(by="xpath", value="//input[@placeholder='Enter location']")
        location_field.send_keys(location_input)

    search_btn = driver.find_element(By.CLASS_NAME, "qsbSubmit")
    search_btn.click()
        

def collect_details():

    with open(csv_path, "a", newline="") as csvfile:
        fieldnames = ["Job", "Company", "Experience", "Salary", "Location", "Description", "Skill 1","Skill 2","Skill 3","Skill 4","Skill 5", "Posted", "Date Recorded"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


        divs = driver.find_element(By.CLASS_NAME,"list")
        total_count_inside_page=len(divs.find_elements(By.CSS_SELECTOR,"article"))

        for i in range(0,total_count_inside_page):
            job_titles = driver.find_elements(By.XPATH, f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[1]/div[1]/a")
            company_names=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[1]/div[1]/div/a[1]")
            experiences=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[1]/ul/li[1]/span[1]")
            salaries=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[1]/ul/li[2]/span[1]")
            locations=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[1]/ul/li[3]/span")
            descriptions=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[2]")
            skills=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/ul")
            posted_new=driver.find_elements(By.XPATH,f"/html/body/div/div[5]/div[2]/div/section[2]/div[2]/article[{i+1}]/div[3]/div[1]/div/span")
            
            for i in range(0,len(job_titles)):
                job_title = job_titles[i].text                
                company_name = company_names[i].text                
                experience = experiences[i].text 
                if(experience[-3:]!="Yrs"):
                    experience=""             
                salary = salaries[i].text                
                if len(skills) > i:
                    skills_list = skills[i].text.splitlines()[:5]
                else:
                    skills_list = []         
                location = locations[i].text               
                description = descriptions[i].text
                if len(posted_new)>i:              
                    posted_data = posted_new[i].text
                else:
                    posted_data = "Check"
                match = re.search(r'\d+', posted_data)
                if match:
                    days_ago = int(match.group())
                    posted = (datetime.now() - timedelta(days=days_ago)).date()
                else:
                    posted = ""

                if job_title == "" or company_name == "" or location == "" or description == "" or posted == "Check" or skills_list == []:
                    break
    # Create a dictionary with the column names and values
                row_dict = {
        "Job": job_title,
        "Company": company_name,
        "Experience": experience,
        "Salary": salary,
        "Location": location,
        "Description": description,
        "Posted": posted,
        "Date Recorded": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

    # Add the skills to the dictionary as separate columns
            for j in range(5):
                if j < len(skills_list):
                    row_dict[f"Skill {j+1}"] = skills_list[j]
                else:
                    row_dict[f"Skill {j+1}"] = ""

            writer.writerow(row_dict)


def land_next_page(pages_input):
    global total_count , pages
    total_pages = driver.find_element(By.CSS_SELECTOR, "span.fleft.count-string.mr-5.fs12")
    total_count = int(total_pages.text.split()[-1])
    per_page=20
    pages = total_count // per_page
    if total_count % per_page > 0:
        pages += 1
    pages_input=convert_string_to_integer(pages_input,pages)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    for i in range(0, min(pages,pages_input)):
        next_button = driver.find_element(By.CSS_SELECTOR, "a.fright.fs14.btn-secondary.br2")
        collect_details()
        if i == pages-1:
            print("======================================\nAll pages scraped successfully\n======================================")
            break
        next_button.click()
    pool.close()
    pool.join()
        
      

if __name__ == "__main__":
    get_requirements()
    start("https://www.naukri.com")
    set_csv()
    land_first_page()
    land_next_page(pages_input)
    driver.quit()