import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3 as sqlite

class plot_class():
        def __init__(self,csv):
                # SKAPAR EN DUMMY DATABAS OCH FYLLER DEN MED DATA
               
                self.csv = csv
                self.db_name = 'db_for_plot.db'
                
       
                df = pd.read_csv(self.csv)
                self.db = sqlite.connect(self.db_name)
                self.cur = self.db.cursor() 
        
                df.to_sql('covid_table', self.db)
                self.db.commit()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        def _plot(self):
            #SKAPAR EN BARPLOT MED MITT DATAFRAME
                ax = sns.barplot(x = 'country', y = 'MAX(people_fully_vaccinated_per_hundred)', data = self.plot_df, hue ='country', )
                ax.set_ylabel('Procent people fully vaccinated')
                ax = plt.show()

        def _read_df(self):
                """ANVÄNDER MIN DUMMY DATABAS FÖR ATT TA UT VÄRDEN TILL NYA TABELLEER SOM JAG SEDAN FÖR ÖVER TILL EN DATAFRAME
                TAR OCKSÅ BORT ALLA TABELLER JAG SKAPAR 
                """
                self.cur.execute("""CREATE TABLE swe AS 
                                SELECT country, MAX(people_fully_vaccinated_per_hundred) FROM covid_table
                                WHERE country = 'Sweden' """)
                self.cur.execute("""CREATE TABLE nor AS 
                                SELECT country, MAX(people_fully_vaccinated_per_hundred) FROM covid_table
                                WHERE country = 'Norway' """)
                self.cur.execute("""CREATE TABLE den AS 
                                SELECT country, MAX(people_fully_vaccinated_per_hundred) FROM covid_table
                                WHERE country = 'Denmark' """)
                self.cur.execute("""CREATE TABLE fin AS 
                        SELECT country, MAX(people_fully_vaccinated_per_hundred) FROM covid_table
                        WHERE country = 'Finland' """)
                self.cur.execute("""CREATE TABLE ice AS 
                        SELECT country, MAX(people_fully_vaccinated_per_hundred) FROM covid_table
                        WHERE country = 'Iceland' """)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
                """TAR ALLA TABLE SOM SKAPATS ÖVER OCH GÖR OM DE TILL DATAFRAME OCH JOINAR IHOP ALLT TILL ETT DATAFRAME
                   TAR SEDAN BORT ALLA TABLES"""

                den_q = self.cur.execute("SELECT * FROM den")
                cols_den = [column[0] for column in den_q.description]
                den_df = pd.DataFrame.from_records(data = den_q.fetchall(), columns= cols_den)

                swe_q = self.cur.execute("SELECT * FROM swe")
                cols_swe = [column[0] for column in swe_q.description]
                swe_df = pd.DataFrame.from_records(data = swe_q.fetchall(), columns= cols_swe)

                nor_q = self.cur.execute("SELECT * FROM nor")
                cols_nor = [column[0] for column in nor_q.description]
                nor_df = pd.DataFrame.from_records(data = nor_q.fetchall(), columns= cols_nor)

                ice_q = self.cur.execute("SELECT * FROM ice")
                cols_ice = [column[0] for column in ice_q.description]
                ice_df = pd.DataFrame.from_records(data = ice_q.fetchall(), columns= cols_ice)

                fin_q = self.cur.execute("SELECT * FROM fin")
                cols_fin = [column[0] for column in fin_q.description]
                fin_df = pd.DataFrame.from_records(data = fin_q.fetchall(), columns= cols_fin)

                self.plot_df = pd.concat([den_df, swe_df,nor_df,ice_df,fin_df], axis=0)
        
                self.cur.execute("DROP TABLE den")
                self.cur.execute("DROP TABLE swe")
                self.cur.execute("DROP TABLE nor")
                self.cur.execute("DROP TABLE ice")
                self.cur.execute("DROP TABLE fin")
                self.cur.execute("DROP TABLE covid_table")
        
        def runner(self):
        # DEF RUNNER ÄR DEN PUBLIKA METODEN SOM INITIERAR METODERNA OVAN
                self._read_df()
                self._plot()
        



        

    
  