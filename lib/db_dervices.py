# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:22:11 2022


Default users password : P@ssw0rd
"""

#import sqlite3
import pandas as pd
import datetime
import time
import os
import pyodbc
import sqlalchemy as sa
from sqlalchemy import create_engine

driver = 'SQL Server'



def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()
    return binary

class DBO:
    def __init__(self):
        try:
#            self.conn = sqlite3.connect('static/db/test.db', check_same_thread=False)
            #self.cur = self.conn.cursor()  
#            self.conn = mysql.connector.connect(host="localhost",port=3306,user="root",password="root")
#            self.conn = self.conn.cursor()

            server="ppeddnserver.database.windows.net"
            port="1433"
            database="PPEHVACDB"
            username="arissdb"
            password='Ashijyoti@12'
            driver = 'SQL Server'

            sa_url = "mssql+pyodbc://{}:{}@{}:{}/{}?driver={}".format('arissdb','Ashijyoti@12',
            'ppeddnserver.database.windows.net',1433,"PPEHVACDB",driver)
            
            self.mydb  = create_engine(sa_url)
        except Exception as e:
            print("123")
            print(e)
           
            
        
        
    def create_user(self, username,fname,lname, role, password,emailid):
        try:             
            query = """INSERT INTO dbo.USERS ( USERNAME ,FNAME,LNAME ,ROLE, PASSWORD,EMAILID,STATUS)
                         VALUES ( '{}','{}','{}','{}','{}','{}','{}')""".format(username,fname,lname,role,password,emailid,'ACTIVE')
            self.mydb.execute(query)
            return 0
        except Exception as e:
            print(e)
            return e
        
    
    def delete_user(self, username):
        try:
            if username not in ('admin', 'analyst'):
               self.mydb.execute("DELETE from dbo.USERS where USERNAME = '" + username + "'")              

               print("Number of users deleted :", self.conn.total_changes)
            else:
                print("[-] Error : Cannot delete default users.")
            return 0
        except Exception as e:
            return e

        
    def get_cred(self, username):
        try:
            stmt = "SELECT ROLE, PASSWORD,FNAME,LNAME from dbo.USERS where status='ACTIVE' and USERNAME = '" + username + "'"
            cursor = self.mydb.execute(stmt)
            ret_obj = {"role": "", "password": ""}
            for row in cursor:
                print("inside cur loop")
                ret_obj["role"] = row[0]
                ret_obj["password"] = row[1]
                ret_obj["username"] = row[2]+" "+row[3]
                break
            print(ret_obj)
            return ret_obj
        except Exception as e:
            print(e)
            return e
        
    
    def update_user(self, username, role, password):
        try:
            self.mydb.execute("UPDATE dbo.USERS set PASSWORD = " + password + ", ROLE = " + role + " where USERNAME = '" + username + "'")
           
            print("[+] Password updated :", self.conn.total_changes)
            return 0
        except Exception as e:
            return e 
    def update_user_details(self,basic_details):
        try:
            print(basic_details)
            username  = basic_details['USERNAME']
            role      = basic_details['ROLE']
            FirstNAME = basic_details['FirstNAME']
            LastNAME  = basic_details['LastNAME']
            emaild    = basic_details['emaild']
            status    = basic_details['STATUS']
            print(role)
            query ="""UPDATE dbo.USERS set 
                    ROLE = '{}' ,FNAME = '{}' ,LNAME = '{}' ,EMAILID = '{}' ,STATUS = '{}' 
                    where USERNAME = '{}'""".format(role,FirstNAME,LastNAME,emaild,status,username)
            self.mydb.execute(query)
            
            return 0
        except Exception as e:
            print(e)
            return e 

    def get_username(self):
        try:
            cursor = self.mydb.execute("SELECT userName from dbo.USERS")
            username_list = []
            for row in cursor:
                username_list.append(row[0])
            return username_list
        except Exception as e:
            return e
      
    def get_user_detail_by_userID_sheet(self,userid):
            stmt = "SELECT * from dbo.USERS where USERNAME='{}'".format(userid)
            cursor=self.mydb.execute(stmt)
            user_list = []
            for row in cursor:
                user_list.append(list(row))
            user_frame = pd.DataFrame(user_list,columns = ['USERNAME','FNAME' ,'LNAME','ROLE' ,
                       'PASSWORD' , 'EMAILID' ,'STATUS'])
            return user_frame
            
    #################################### Start Of Euipment query #########################################################        
    def get_equipment(self):
        try:
            stmt = "SELECT * from dbo.equipment_master "
            cursor = self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            
            return equipment_frame
        except Exception as e:
            return e
            
    def get_equipment_by_id(self,SR_NO_ID):
        try:
            stmt = "SELECT * from dbo.equipment_master where SR_NO_ID='{}'".format(SR_NO_ID)
            cursor=self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list)
            equipment_frame.columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK']
            return equipment_frame
        except Exception as e:
            return e
            
    def get_logBook(self):
        try:
            stmt = "SELECT * from dbo.elogbook "
            cursor=self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['SR_NO_ID' ,'STATUS','ISSUED_TO' ,'COMPANY_NAME' , 'REMARK' ,'update_time'])
            return equipment_frame
        except Exception as e:
            return e
            
    def get_available_equipment(self):
        try:
            stmt = "SELECT * from dbo.equipment_master where status='AVAILABLE' OR status='CLOSED'"
            cursor = self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def get_penidng_for_approval_equipment(self):
        try:
            stmt = "SELECT * from dbo.equipment_master where status='REQUESTED'"
            cursor =self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def selected_instrument_dropdown(self,TYPE,ISSUED_TO,role):
        try:
            stmt = """SELECT * from dbo.equipment_master where
            status='APPROVED' and Type='{}' and ISSUED_TO='{}'""".format(TYPE,ISSUED_TO)
            if role=="documentcell" :
                stmt = """SELECT * from dbo.equipment_master where
                            Type='{}'""".format(TYPE)
            cursor = self.mydb.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
            
        except Exception as e:
            print(e)
            return e       

    def request_for_equipment(self,SR_NO_ID,company_name,REMARK,ISSUED_TO):
        try:
            stmt = """update dbo.equipment_master 
                      set STATUS= 'REQUESTED' , ISSUED_TO='{}' ,COMPANY_NAME='{}' ,REMARK='{}'
                      where SR_NO_ID='{}' """.format(ISSUED_TO,company_name,REMARK,SR_NO_ID)
            self.mydb.execute(stmt)
           

            ts = time.time()
            update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')       
            print(update_time)           
            query = """INSERT INTO dbo.elogbook 
                    (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,update_time) 
                    VALUES ( '{}','{}','{}','{}','{}','{}')""".format(SR_NO_ID,'REQUESTED',ISSUED_TO,company_name,REMARK,update_time)
            self.mydb.execute(query)
            

            
        except Exception as e:
            return e 
            
    def update_request_for_equipment(self,temp_Df,ISSUED_TO):
        try:
            for row in temp_Df.itertuples():
                STATUS = row[2]
                if STATUS=="APPROVED":
                    stmt = """update dbo.equipment_master 
                              set STATUS= '{}'  ,REMARK='{}' 
                              where SR_NO_ID='{}' """.format(row[2],row[3],row[1])
                    self.mydb.execute(stmt)
                    

                
                    ts = time.time()
                    update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')            
                    query = """INSERT INTO dbo.elogbook 
                            (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,update_time) 
                            VALUES ( '{}','{}','{}','{}','{}','{}')""".format(row[1],STATUS,ISSUED_TO,row[4],row[3],update_time)
                    self.mydb.execute(query)
                    

            
        except Exception as e:
            return e             
            
    def update_equipment(self,equipment_master):
        try:
            self.mydb.execute("""Truncate    dbo.equipment_master""")
            
            for row in equipment_master.itertuples():
                query = """INSERT INTO dbo.equipment_master 
                    (Type ,EQUIPMENT_NAME ,MAKE ,MODEL_NUMBER,SR_NO_ID ,
                    DONE_DATE ,DUE_DATE,STATUS,ISSUED_TO ,COMPANY_NAME,REMARK) 
                    VALUES ( '{}','{}','{}','{}','{}',
                   '{}','{}','{}','{}','{}','{}')""".format(row[1],row[2],row[3],row[4],
                                                  row[5],row[6],row[7],
                                                  row[8],row[9],row[10],row[11])
                self.mydb.execute(query)
            #self.mydb.commit()

                
        except Exception as e: 
            return e
    ################################# Start Company Details Query ####################################################        
    def get_company_details(self):
        try:
            stmt = "SELECT * from dbo.company_details "
            cursor = self.mydb.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            print(e)
            return e
            
    def get_company_details_by_company_name(self,COMPANY_NAME):
        try:
            stmt   = "SELECT * from dbo.company_details where COMPANY_NAME='{}'".format(COMPANY_NAME)
            cursor = self.mydb.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            print(e)
            return e
            
    def update_company_details(self,company_details):
        try:
            self.mydb.execute("""truncate dbo.company_details""")
            #self.mydb.commit()
            for row in company_details.itertuples():
                query = """INSERT INTO dbo.company_details 
                    (COMPANY_NAME ,ADDRESS ,REPORT_NUMBER) 
                    VALUES ( '{}','{}','{}')""".format(row[1],row[2],row[3])
                self.mydb.execute(query)
                #self.mydb.commit()

                
        except Exception as e: 
            return e            
    ################################# End Company Details Query ####################################################          
    
    def insert_file(self,file_name,file_path):
        try:
            table_name = "file_db"
            binary_file = convert_into_binary(file_path)
            sqlite_insert_blob_query = """INSERT INTO {} (name, data)
            VALUES ('{}', '{}')""".format(table_name,file_name,binary_file)
            print(sqlite_insert_blob_query)
            self.conn.execute(sqlite_insert_blob_query)
            self.conn.commit()
            print('File inserted successfully')
        except e:
            print("Failed to insert blob into the table")
            
            
    ############################# Expense############################################################################
    def raise_expense(self,temp_Df,userID,userName):
        try:
            for row in temp_Df.itertuples():
                             
                ts = time.time()
                update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')            
                query = """INSERT INTO dbo.ExpenseMaster 
                      (Expensetype ,company_name,Description ,
                       Amount_requested , Amount_approved ,userID,
                       userName,date,STATUS,updatedBY) 
                       VALUES ( '{}','{}','{}',
                               '{}','{}','{}',
                               '{}','{}','{}','{}')""".format(row[1],row[2],row[3],
                               row[4],"NA",userID,
                               userName,update_time,"REQUESTED","NA")
                self.mydb.execute(query)
                #self.mydb.commit()

            
        except Exception as e:
            print(e)
            return e 
            
    def get_expense_sheet(self,userid,status,Expensetype,company_name):
            stmt = "SELECT * from dbo.ExpenseMaster where STATUS='{}'".format(status)
            if userid!="ALL":
                stmt=stmt+" and userID='{}'".format(userid)    
                
            if status!="ALL":
                stmt=stmt+" and STATUS='{}'".format(status)
                
            if Expensetype!="ALL":
                stmt=stmt+" and Expensetype='{}'".format(Expensetype)
                
            if company_name!="ALL":
                stmt=stmt+" and company_name='{}'".format(company_name)
            cursor = self.mydb.execute(stmt)
            expense_list = []
            for row in cursor:
                expense_list.append(list(row))
            expense_frame = pd.DataFrame(expense_list,columns = ['request_id','Expensetype' ,'company_name','Description' ,
                       'Amount_requested' , 'Amount_approved' ,'userID',
                       'userName','date','STATUS','updatedBY'])
            expense_frame = expense_frame[['request_id','Expensetype' ,'company_name','Description' ,
                                          'Amount_requested','Amount_approved','date','STATUS','updatedBY']]
            return expense_frame
            
    def get_expense_sheet_by_user(self,userid):
            stmt = "SELECT * from dbo.ExpenseMaster where userid='{}' ORDER BY STATUS DESC ".format(userid)
            self.conn.execute(stmt)
            expense_list = []
            for row in self.conn:
                expense_list.append(list(row))
            expense_frame = pd.DataFrame(expense_list,columns = ['request_id','Expensetype' ,'company_name','Description' ,
                       'Amount_requested' , 'Amount_approved' ,'userID',
                       'userName','date','STATUS','updatedBY'])
            expense_frame = expense_frame[['request_id','Expensetype' ,'company_name','Description' ,
                                          'Amount_requested','Amount_approved','date','STATUS','updatedBY']]
            return expense_frame
            
            
    def update_expense(self,temp_Df,updatedBy):
        try:
            for row in temp_Df.itertuples():
                ts = time.time()
                update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')    
                stmt = """update dbo.ExpenseMaster 
                          set Amount_approved= '{}'  ,STATUS='{}' ,updatedBY='{}'
                          where request_id='{}' """.format(row[2],row[3],updatedBy,row[1])
                self.mydb.execute(stmt)
                #self.mydb.commit()

        except Exception as e:
            return e         
    
           
                