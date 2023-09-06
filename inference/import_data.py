import pyodbc
import pandas as pd
import os
import cred
import datetime
import csv


class extract_data:
    def __init__(self):
        self.cnxn = pyodbc.connect(Driver='{driver}',
                              Server='server_address',
                              # Trusted_Connection='no',
                              TrustServerCertificate='yes',
                              UID=cred.user,
                              PWD=cred.password) 

        self.cursor = self.cnxn.cursor()
        print(f'connection established at {datetime.datetime.now()}')       
        
        self.path = os.path.join(os.getcwd(), 'data')        

    def fetchall(self, query, filename):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(f'fetchall done at {datetime.datetime.now()}')
        
        columns = [column[0] for column in self.cursor.description]
        df = pd.DataFrame((tuple(t) for t in data), columns=columns)
        print(f'df created at {datetime.datetime.now()}')
        
        df.to_csv(f'{self.path}/{filename}.csv', index=False)
        print(f'df written to file at {datetime.datetime.now()}')
        
        del data
        del df

        self.cursor.close()
        self.cnxn.close()
        
        print('')
        print(f'job finished at {datetime.datetime.now()}')


    def fetchmany(self, query, filename, chunk_size=100000):
        self.cursor.execute(query)
        
        with open(f'{self.path}/{filename}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([column[0] for column in self.cursor.description]) 
            print(f'file created at {datetime.datetime.now()}')
            
            i=1
            
            while True:
                data = self.cursor.fetchmany(chunk_size)
                if not data:
                    break
                print('')
                print(i)
                print(f'fetchmany chunk completed at {datetime.datetime.now()}')
                
                writer.writerows(data)
                print(f'file chunk written at {datetime.datetime.now()}')
                i+=1
            
            del data
            
            self.cursor.close()
            self.cnxn.close()
            
            print('')
            print(f'job finished at {datetime.datetime.now()}')