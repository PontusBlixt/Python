from Pontus_Blixt_Class import datahantering
from Pontus_Blixt_Plot_Class import plot_class

#SKAPAT AV PONTUS BLIXT ÖNSKAT BETYG VG  

def main():
    cov = datahantering("covid.db","vaccin_covid.csv","covid_table","country") # CREATE DATABASE 
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    cov.seperate("vaccines",",") # SEPERATE COLUMN VACCINE AND LOAD DATAFRAME TO SQL
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    cov.seed_database() # LOAD CSV INTO DATABASE
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
     
    cov.what_vacs_table("vaccines_info") # CREATE TABLE REGARDING INFO ABOUT VACCINES 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
   
    cov.daily_table("avg_daily_info","vac_daily_raw_info","daily_vac_mil_info") # CREATES A TABLE WITH AVG ABOUT SOME DAILY VAC INFO 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    cov.day_vac_prog("vac_progress",'Date','daily_vaccinations_progress') # CREATES A TABLE THAT SHOWS EACH COUNTRIES PROGRESS IN VACCINATING THE POPULATION

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    cov.tot_table("tot_table",'tot_vacs','people_vacced','people_fully_vacced','tot_vac_per_100','tot_fully_vacced_100')
    # CREATES A TABLE THAT SHOW INFO REGARDING THE VACCINATION PROGRESS IN CURRENT TIME

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    plot_it = plot_class("vaccin_covid.csv") # LOAD CLASS PLOT_CLASS GIVE VACCIIN CSV ONCE AGIN FOR DUMMY DB
    plot_it.runner()
    # CREATES A CHART SHOWING WHICH NORDIC COUNTRY IS AHEAD IN FULLY VACCINATING THE POPULATION 
    

   
    
if __name__ == "__main__":
    main()

# OPEN DATABSE IN FOLDER MENU TO ANALYSE EACH TABLE INDIVIDUALLY 