from customtkinter import *


from PIL import Image,ImageTk
from selenium.webdriver import Chrome,Edge
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import csv

import os

import logging



class Scraper(CTk):
    def __init__(self):
        super().__init__()
        # Interface:
        
        self._set_appearance_mode('dark')
        self.iconbitmap(r'C:\Users\7seas\Downloads\scrapericon.ico')
        self.title('Jobs')
        self.geometry('800x700')
       
       
        self.resizable()
        self.normal=CTkFont('aerial',11,'normal')
        font_search_label=CTkFont('Courier',12,'bold')
        self.font_welcome_label=CTkFont('Candara',15,'bold')
        # Excel Path:
        self.jobfile=r'E:\PYTHON\MyJobsData.xlsx'
        # Labels:
        CTkLabel(self,text='Search jobs by Skills, Company, Postion :',font=font_search_label,bg_color='grey',height=25).grid(row=0,column=0)
        CTkLabel(self,text='Type location or \"Remote\" :',font=font_search_label,bg_color='grey',anchor='w',width=295,height=25).grid(row=1,column=0,sticky='W')
        # Entries:
        self.search_entry=CTkEntry(self,text_color='black',font=self.normal,width=250,border_width=0,height=25)
        self.search_entry.grid(row=0,column=1,padx=5)
        self.search_entry.insert(0,'Python')
        self.location_entry=CTkEntry(self,text_color='black',font=self.normal,width=250,border_width=0,height=25)
        self.location_entry.grid(row=1,column=1,padx=5)
        self.location_entry.insert(0,'karachi')
        # Buttons:
        self.search_button=CTkButton(self,text='Search',text_color='white',fg_color='red',bg_color='black',command=self.SEARCH)
        self.search_button.grid(row=0,column=2)
        self.clear_records=CTkButton(self,text='Clear Records',text_color='white',fg_color='red',bg_color='black',command=self.CLEAR)
        self.clear_records.grid(row=1,column=2)
        self.show_button=CTkButton(self,text='Show',text_color='white',fg_color='red',bg_color='black',command=self.SHOW)
        self.show_button.grid(row=3,column=1,columnspan=2)
        
    
        




    def SEARCH(self):
        global wb
        self.loading=CTkLabel(self,text='Error Click Search....',bg_color='grey',height=25)
        self.loading.grid(row=3,column=0)
        # Config for logs:
        logging.basicConfig(filename='jobs.logs',filemode='a',format='%(name)s-%(asctime)s-%(message)s',datefmt='%H:%M:%S %m/%d/%Y',level=logging.INFO)
        logging.info('Search was Instantiated! ') 
      
        # All the links from which data will be used:
        indeed=r'https://pk.indeed.com/'
        glassdoor=r'https://www.glassdoor.com/Job/index.htm'
        upwork=r'https://www.upwork.com/nx/search/jobs/?sort=recency'
        
        


        """                    This block of code will Scrap data and will do automation from indeed site:         """
        
        
        
        chromedriver=r'C:\Program Files\Python312\Scripts\chromedriver-win64\chromedriver.exe'    
        
        options=Options()
       
       
        
        server=Service(executable_path=chromedriver)
        indeed_driver=Chrome(options=options,service=server)
        
        indeed_driver.get(indeed)
        WebDriverWait(indeed_driver,25).until(EC.url_contains(indeed))
        
        WebDriverWait(indeed_driver,25).until(EC.presence_of_element_located((By.XPATH,'//input[@name="q"]')))

        indeed_driver.find_element('xpath','//input[@name="q"]').send_keys(self.search_entry.get())
      

        indeed_driver.find_element('xpath','//input[@name="l"]').send_keys(self.location_entry.get())
        
        indeed_driver.find_element('xpath','//button[@class="yosegi-InlineWhatWhere-primaryButton"]').click()
        WebDriverWait(indeed_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//span[@title]')))

        title=indeed_driver.find_elements('xpath','//span[@title]')
        WebDriverWait(indeed_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//span[@data-testid="company-name"]')))
        company=indeed_driver.find_elements('xpath','//span[@data-testid="company-name"]')
       
        WebDriverWait(indeed_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]')))
        jobs_link=indeed_driver.find_elements('xpath','//a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]')# <-- Direct links for jobs
        print('Indeed Data Retrieve Successfully')
        logging.info('Indeed Data was retrieved')
        ''''''

        
        # Creating Dataframe:
        data_list=[]
        for titles,companys,jobs_links in zip(title,company,jobs_link):
            dic={
                'title':titles.text,
                'company':companys.text,
                'link':jobs_links.get_attribute('href')
            }
            data_list.append(dic)
                  
        indeed_driver.close()
        
        '''                           This  block of code will scrap data from glassdoor site:                        '''
        glassdoor_driver=Chrome(service=server)   
        
        glassdoor_driver.get(glassdoor)
        # Search:
        WebDriverWait(glassdoor_driver,25).until(EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Search keyword"]')))  
        glassdoor_driver.find_element('xpath','//input[@aria-label="Search keyword"]').send_keys(self.search_entry.get())
        time.sleep(0.5)
        # Location:
        WebDriverWait(glassdoor_driver,25).until(EC.presence_of_element_located((By.XPATH,'//input[@aria-label="Search location"]')))  
        glassdoor_driver.find_element('xpath','//input[@aria-label="Search location"]').send_keys((self.location_entry.get(),Keys.ENTER))    
        # Title of the job:
        WebDriverWait(glassdoor_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="JobCard_jobTitle__rbjTE"]')))
        title2=glassdoor_driver.find_elements('xpath','//a[@class="JobCard_jobTitle__rbjTE"]')
        # Company:
        WebDriverWait(glassdoor_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="JobCard_location__N_iYE"]')))
        company2=glassdoor_driver.find_elements('xpath','//div[@class="JobCard_location__N_iYE"]')
        # Link:
        WebDriverWait(glassdoor_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="JobCard_trackingLink__zUSOo"]')))
        link2=glassdoor_driver.find_elements('xpath','//a[@class="JobCard_trackingLink__zUSOo"]')
        # Converting Glassdoor data into a df:
        print('glassdoor Data Retrive Successfully')
        logging.info('GlassDoor data was Retrived')
        for title,company,link in zip(title2,company2,link2):
            dic2={
                'title':title.text,
                'company':company.text,
                'link':link.get_attribute('href')
            }
            data_list.append(dic2)
        glassdoor_driver.close()    
        
        
        '''                      This block of code will scrap data from upwork site                     '''
        
        upwork_driver=Chrome(service=server)
        
        upwork_driver.get(upwork)
        # Search
        

        upwork_driver.find_element('xpath','//div[@class="search-bar flex-1"]').click()
        
        WebDriverWait(upwork_driver,25).until(EC.presence_of_element_located((By.XPATH,'//input[@role]')))
        upwork_driver.find_element('xpath','//input[@role]').send_keys((self.search_entry.get(),Keys.ENTER))
        
        
            # Title:
        WebDriverWait(upwork_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="up-n-link"]')))
        title3=upwork_driver.find_elements('xpath','//a[@class="up-n-link"]')
            # Link:
        WebDriverWait(upwork_driver,25).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="up-n-link"]')))
        link3=upwork_driver.find_elements('xpath','//a[@class="up-n-link"]')
        print('Upwork data was Retrieved')
        logging.info('Upwork data was Retrived')
        for title,link in zip(title3,link3):
            dic3={
                'title':title.text,
                'link':link.get_attribute('href')
            }
            data_list.append(dic3)
            
               
                             
        df=pd.DataFrame(data_list)
        
        df.to_excel(self.jobfile)        
        time.sleep(0.5)
        self.loading.destroy()
        self.loading=CTkLabel(self,text='DONE..',bg_color='grey',fg_color='grey',text_color='black')
        self.loading.grid(row=3,column=0)
        logging.info('Program run succesfully')
        upwork_driver.close()
        
        
    
# This clear function will clear all the job records store in a file:        
    def CLEAR(self):
          
          with open(self.jobfile,'w') as file:
              csv.writer(file)  
                  
    def SHOW(self): 
        
                 
        print('Button was clicked')
        if os.path.exists(self.jobfile):
            print('File located')
            os.startfile(self.jobfile)
        else:
            print('File was not found')    
       
scrap=Scraper()
scrap.mainloop()


