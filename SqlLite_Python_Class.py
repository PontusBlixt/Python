import pandas as pd 
import sqlite3 as sqlite



#SKAPAT AV PONTUS BLIXT ÖNSKAT BETYG VG  
class datahantering(): 
    def __init__(self, db_name:str, csv:str,table_name,write_country_here): 
        """DETTA ÄR MIN KONSTRUKTOR HÄR NAMNGER VI DATABASEN LÄSER IN CSV FILEN MED PANDAS OCH SKAPAR EN TOM DATABAS
            OCH SKAPAR EN CURSOR TILL DENNA DATABAS"""

        self.db_name = db_name
        self.csv = csv
        self.table_name = table_name
        self.df = pd.read_csv(self.csv)
        self.db = sqlite.connect(self.db_name)
        self.cur = self.db.cursor() 
        self.write_country_here = write_country_here
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def seperate(self,column_name,seperator):
        """FUNKTIONEN SEPARERAR KOLUMN VACCIN TILL 7 KOLUMNER, 
        LEFT JOINAR DE 7 NYSKAPADE MED ORIGNAL, TAR BORT ORGINAL VACCIN KOLUMNEN 
        AVSLUTAR MED ATT GE DE NYA KOLUMNERNA NYA NAMN """
        self.column_name = column_name
        self.seperator = seperator
        splittad = self.df[self.column_name].str.split(self.seperator, expand=True)
        self.df = self.df.join(splittad)
        del self.df[self.column_name]
        self.df.rename(columns={0 : "vaccine_1", 1 : "vaccine_2", 2 : "vaccine_3", 3 : "vaccine_4", 4 : "vaccine_5", 5 : "vaccine_6", 6 : "vaccine_7"}, inplace = True)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def seed_database(self):
        "HÄR LÄSER VI IN VÅRT DATAFRAME I DEN TOMMA DATABASEN"
        self.df.to_sql(self.table_name, self.db)
        self.db.commit()
         

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def what_vacs_table(self,tab_name_vac):
        self.tab_name_vac = tab_name_vac # TABLE NAME SOM ANGES VID INITIERING AV DENNA FUNKTION
        # TAR BORT TABLE IFALL DET REDAN EXISTERAR
        self.cur.execute(f"DROP TABLE IF EXISTS {self.tab_name_vac}")
        # SKAPAR ETT TOMT TABLE MED COUNTRY SOM PK OCH DE KOLUMNER SOM SKA FYLLAS
        self.cur.execute(f"""CREATE TABLE {self.tab_name_vac} ( 
                        country TEXT PRIMARY KEY,
                        vaccine_1 TEXT,
                        vaccine_2 TEXT,
                        vaccine_3 TEXT,
                        vaccine_4 TEXT,
                        vaccine_5 TEXT,
                        vaccine_6 TEXT,
                        vaccine_7 TEXT,
                        source_name TEXT,
                        source_website TEXT
                        )""")
        # SKAPAR ETT TEMPORÄRT TABLE MED ETT QUERY DÄR JAG PLOCKAR UT DATA JAG VILL ANVÄNDA
        self.cur.execute("""CREATE TABLE temp AS
                        SELECT DISTINCT country, vaccine_1,vaccine_2,vaccine_3,vaccine_4,vaccine_5,vaccine_6,vaccine_7, source_name,source_website
                        FROM covid_table
                        GROUP BY country""")
       # TAR DATAN FRÅN TABLE OVAN OCH FYLLER PÅ DET I DEN TOMMA DATABASEN
        self.cur.execute(f"""INSERT INTO {self.tab_name_vac}
        (country,vaccine_1, vaccine_2, vaccine_3, vaccine_4, vaccine_5, vaccine_6, vaccine_7, source_name, source_website)
        SELECT * FROM temp""")
        # TAR BORT DET TEMPORÄRA TABLET MED DATA
        self.cur.execute("DROP TABLE temp")
        # GÖR EN COMMIT TILL DATABASEN FÖR ATT SE TILL ATT ALLT SPARAS SOM DE SKA 
        self.db.commit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def daily_table(self,tab_name,col_name,col_name1):
        self.tab_name = tab_name # TABLE NAME SOM ANGES VID INITIERING AV DENNA FUNKTION
        self.col_name = col_name # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        self.col_name1 = col_name1 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        # TAR BORT TABLE JAG SKAPAR NEDAN IFALL DET REDAN EXISTERAR 
        self.cur.execute(f"DROP TABLE IF EXISTS {self.tab_name}")
        # AKTIVERAR FOREIGN KEY
        self.cur.execute("PRAGMA FOREIGN_KEYS = ON")
        # SKAPAR ETT TOMT TABLE MED COUNTRY SOM PK OCH DE KOLUMNER SOM SKA FYLLAS
        self.cur.execute(f"""CREATE TABLE {self.tab_name} (
                        country TEXT PRIMARY KEY,
                        {self.col_name} REAL,
                        {self.col_name1} REAL,
                        FOREIGN KEY (country)
                            REFERENCES {self.tab_name_vac} (country))""")

        # SKAPAR ETT TEMPORÄRT TABLE MED ETT QUERY DÄR JAG PLOCKAR UT DATA JAG VILL ANVÄNDA
        self.cur.execute(f"""CREATE TABLE temp AS
                        SELECT DISTINCT country, ROUND(AVG(daily_vaccinations_raw),0),
                        ROUND(AVG(daily_vaccinations_per_million))
                        FROM covid_table
                        GROUP BY country """)
        # TAR DATAN FRÅN TABLE OVAN OCH FYLLER PÅ DET I DEN TOMMA DATABASEN
        self.cur.execute(f"""INSERT INTO {self.tab_name}
                        ({self.write_country_here},{self.col_name},{self.col_name1})
                        SELECT * FROM temp
                        """)
        # TAR BORT DET TEMPORÄRA TABLET MED DATA
        self.cur.execute("DROP TABLE temp")
        # GÖR EN COMMIT TILL DATABASEN FÖR ATT SE TILL ATT ALLT SPARAS SOM DE SKA 
        self.db.commit()
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def day_vac_prog(self,tab_name,col_name,col_name1):
        self.tab_name = tab_name # TABLE NAME SOM ANGES VID INITIERING AV DENNA FUNKTION
        self.col_name = col_name # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        self.col_name1 = col_name1 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        # TAR BORT TABLE JAG SKAPAR NEDAN IFALL DET REDAN EXISTERAR 
        self.cur.execute(f"DROP TABLE IF EXISTS {self.tab_name}")
        # AKTIVERAR FOREIGN KEY
        self.cur.execute("PRAGMA FOREIGN_KEYS = ON")
        # SKAPAR ETT TOMT TABLE MED COUNTRY OCH DATE SOM PK OCH DEN KOLUMN SOM SKA FYLLAS
        self.cur.execute(f"""CREATE TABLE {self.tab_name} (
                        {self.write_country_here} TEXT,
                        {self.col_name} TEXT,
                        {self.col_name1} REAL,
                        PRIMARY KEY ({self.write_country_here},{self.col_name})
                        FOREIGN KEY (country)
                            REFERENCES {self.tab_name_vac} (country))
                        """)
        # SKAPAR ETT TEMPORÄRT TABLE MED ETT QUERY DÄR JAG PLOCKAR UT DATA JAG VILL ANVÄNDA
        self.cur.execute("""CREATE TABLE temp AS 
                        SELECT country, date, daily_vaccinations FROM covid_table
                        WHERE daily_vaccinations NOT NULL""")
        # TAR DATAN FRÅN TABLE OVAN OCH FYLLER PÅ DET I DEN TOMMA DATABASEN
        self.cur.execute(f"""INSERT INTO {self.tab_name}
                        ({self.write_country_here},{self.col_name},{self.col_name1}) 
                        SELECT * FROM temp""")
        # TAR BORT DET TEMPORÄRA TABLET MED DATA
        self.cur.execute("DROP TABLE temp")
        # GÖR EN COMMIT TILL DATABASEN FÖR ATT SE TILL ATT ALLT SPARAS SOM DE SKA        
        self.db.commit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def tot_table(self,tab_name,tot_name,tot_name1,tot_name2,tot_name3,tot_name4):
        self.tab_name = tab_name # TABLE NAME SOM ANGES VID INITIERING AV DENNA FUNKTION
        self.tot_name = tot_name # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        self.tot_name1 = tot_name1 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        self.tot_name2 = tot_name2 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION
        self.tot_name3 = tot_name3 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION    
        self.tot_name4 = tot_name4 # KOLUMN NAMN SOM ANGES VID INITERING AV DENNA FUNKTION  
        # TAR BORT TABLE JAG SKAPAR NEDAN IFALL DET REDAN EXISTERAR 
        self.cur.execute(f"DROP TABLE IF EXISTS {self.tab_name}")
        # AKTIVERAR FOREIGN KEY
        self.cur.execute("PRAGMA FOREIGN_KEYS = ON")
        # SKAPAR ETT TOMT TABLE MED COUNTRY OCH DATE SOM PK OCH DEN KOLUMN SOM SKA FYLLAS
        self.cur.execute(f"""CREATE TABLE {self.tab_name} (
            {self.write_country_here} TEXT PRIMARY KEY,
            {self.tot_name} REAL,
            {self.tot_name1} REAL,
            {self.tot_name2} REAL,
            {self.tot_name3} REAL,
            {self.tot_name4} REAL,
            FOREIGN KEY (country)
                REFERENCES {self.tab_name_vac} (country))
            """)    
        # SKAPAR ETT TEMPORÄRT TABLE MED ETT QUERY DÄR JAG PLOCKAR UT DATA JAG VILL ANVÄNDA
        self.cur.execute(f"""CREATE TABLE temp AS
            SELECT DISTINCT country, 
            MAX(total_vaccinations),
            MAX(people_vaccinated),
            MAX(people_fully_vaccinated),
            MAX(total_vaccinations_per_hundred),
            MAX(people_fully_vaccinated_per_hundred) 
            FROM covid_table
            GROUP BY country """)
        # TAR DATAN FRÅN TABLE OVAN OCH FYLLER PÅ DET I DEN TOMMA DATABASEN
        self.cur.execute(f"""INSERT INTO {self.tab_name}
                        ({self.write_country_here},{self.tot_name},{self.tot_name1},{self.tot_name2},{self.tot_name3},{self.tot_name4}) 
                        SELECT DISTINCT country, 
                        MAX(total_vaccinations),
                        MAX(people_vaccinated),
                        MAX(people_fully_vaccinated),
                        MAX(total_vaccinations_per_hundred),
                        MAX(people_fully_vaccinated_per_hundred) 
                        FROM covid_table
                        GROUP BY country """)
        # TAR BORT DET TEMPORÄRA TABLET MED DATA
        self.cur.execute("DROP TABLE temp")
        # TAR BORT DET FÖRSTA TABLET MED CSV FILEN INLADDAD        
        self.cur.execute("DROP TABLE covid_table")
        # GÖR EN COMMIT TILL DATABASEN FÖR ATT SE TILL ATT ALLT SPARAS SOM DE SKA
        self.db.commit()
