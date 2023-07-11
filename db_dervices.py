# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:22:11 2022


Default users password : P@ssw0rd
"""
import pandas as pd
import datetime
import time
import os
import mysql.connector
from mysql.connector import errorcode
from dateutil.tz import gettz
import os 
import io
from crypt_services import encrypt_sha256
import base64
from base64 import b64encode
from pathlib import Path
MYDIR        = os.path.dirname(__file__)

   
config = {
  'host':"pinpointserver.mysql.database.azure.com",
  'port':"3306",
  'user':"arissdb",
  'password':"ppedbpass@12",
  'db':'PPEHVACDB'
}

def get_equipment_property(SR_NO_ID):
    try:
        stmt = "SELECT MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME  from ppehvacdb.equipment_master where SR_NO_ID='{}' ".format(SR_NO_ID)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        MODEL_NUMBER   = ""
        Type           = "" 
        EQUIPMENT_NAME = ""
        MAKE           = ""
        for row in cursor:
            print(row)
            MODEL_NUMBER = row[0]
            Type = row[1]
            EQUIPMENT_NAME = row[2]
            MAKE = row[3]
        print(MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME)
        return MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME
    except Exception as e:
        return e

def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary=file.read()
    return binary

class DBO:
    def __init__(self):
        try:           
            pass                
        except Exception as e:
            pass
           
            
        
        
    def create_user(self, username,CompanyName,fname,lname, role, password,emailid):
        try:             
            query = """INSERT INTO ppehvacdb.USERS ( USERNAME ,COMPANYNAME,FNAME,LNAME ,ROLE, PASSWORD,EMAILID,STATUS,photo_blob)
                         VALUES ( '{}','{}','{}','{}','{}','{}','{}','{}','')""".format(username,CompanyName,fname,lname,role,password,emailid,'ACTIVE')
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception as e:
            print(e)
            return e
        
    
    def delete_user(self, username):
        try:
            if username not in ('admin'):
                stmt = "DELETE from ppehvacdb.USERS where USERNAME = '" + username + "'"  
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute(stmt)    
                conn.commit()
                return "User Deleted Successfully"
            else:
                return "Error : Cannot delete default users."
            
        except Exception as e:
            return e

        
    def get_cred(self, username):
        try:
            stmt = "SELECT ROLE, PASSWORD,FNAME,LNAME ,COMPANYNAME from ppehvacdb.USERS where status='ACTIVE' and USERNAME = '" + username + "'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            ret_obj = {"role": "", "password": ""}
            for row in cursor:
                ret_obj["role"] = row[0]
                ret_obj["password"] = row[1]
                ret_obj["username"] = row[2]+" "+row[3]
                ret_obj["COMPANYNAME"] = row[4]
                break
            return ret_obj
        except Exception as e:
            return e
        
    
    def update_user(self, username, role, password):
        try:
            query="UPDATE ppehvacdb.USERS set PASSWORD = " + password + ", ROLE = " + role + " where USERNAME = '" + username + "'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("[+] Password updated :", self.conn.total_changes)
            return 0
        except Exception as e:
            return e 
    def update_user_details(self,basic_details):
        try:
            username  = basic_details['USERNAME']            
            FirstNAME = basic_details['FirstNAME']
            LastNAME  = basic_details['LastNAME']
            emaild    = basic_details['emaild']
            PASSWORD  = basic_details['PASSWORD']
            
            if PASSWORD=="":
                role      = basic_details['ROLE']
                status    = basic_details['STATUS']
                query ="""UPDATE ppehvacdb.USERS set 
                        ROLE = '{}' ,FNAME = '{}' ,LNAME = '{}' ,EMAILID = '{}' ,STATUS = '{}' 
                        where USERNAME = '{}'""".format(role,FirstNAME,LastNAME,emaild,status,username)
            else:
                temp_password = encrypt_sha256(username+PASSWORD)
                query ="""UPDATE ppehvacdb.USERS set 
                        FNAME = '{}' ,LNAME = '{}' ,EMAILID = '{}' ,PASSWORD ='{}'
                        where USERNAME = '{}'""".format(FirstNAME,LastNAME,emaild,temp_password,username)   
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit() 
            return 0
        except Exception as e:
            return e 

    def get_username(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT userName from ppehvacdb.USERS")
            username_list = []
            for row in cursor:
                username_list.append(row[0])
            return username_list
        except Exception as e:
            print(e)
            return e
      
    def get_user_detail_by_userID_sheet(self,userid):
            stmt = "SELECT * from ppehvacdb.USERS where USERNAME='{}'".format(userid)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            user_list = []
            for row in cursor:
                user_list.append(list(row))
            user_frame = pd.DataFrame(user_list,columns = ['USERNAME' ,  'COMPANYNAME' , 'FNAME' ,
                                            'LNAME' , 'ROLE' , 'PASSWORD' , 'EMAILID' ,
                                            'STATUS'  , 'photo_blob' ])
            return user_frame[['USERNAME','COMPANYNAME','FNAME','LNAME','ROLE','PASSWORD','EMAILID','STATUS']]
###########################################################End of user query ##################################################################
            
            
    def get_company_details(self):
        try:
            stmt = "SELECT * from ppehvacdb.company_details "
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            return e
    def update_company_details(self,company_details):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("""truncate ppehvacdb.company_details""")
            conn.commit()
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            for row in company_details.itertuples():
                query = """INSERT INTO ppehvacdb.company_details 
                    (COMPANY_NAME ,ADDRESS ,REPORT_NUMBER) 
                    VALUES ( '{}','{}','{}')""".format(row[1],row[2],row[3])
                
               
                cursor.execute(query)
            conn.commit()

                
        except Exception as e: 
            return e  

            
    def get_company_details_by_company_name(self,COMPANY_NAME):
        try:
            stmt   = "SELECT * from ppehvacdb.company_details where COMPANY_NAME='{}'".format(COMPANY_NAME)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            print(e)
            return e
            
            
    def get_equipment(self,SR_NO_ID):
        try:
            stmt = "SELECT * from ppehvacdb.equipment_master "
            if SR_NO_ID!="ALL":
                stmt = "SELECT * from ppehvacdb.equipment_master where SR_NO_ID='{}'".format(SR_NO_ID)
            
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            
            return equipment_frame
        except Exception as e:
            return e
            
    
            
    




    ############################################################ START EXPENSE MANGMENT #######################################################################
    def submit_expense(self,temp_Df,userID,userName):
        try:
            for row in temp_Df.itertuples():
                             
                ts = time.time()
                update_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
                update_time = str(update_time.strftime('%d/%m/%Y %H:%M:%S')).split(".")[0]               
                query = """INSERT INTO ppehvacdb.ExpenseMaster 
                      (Expensetype ,company_name,Description ,
                       Amount_requested , Amount_approved ,userID,
                       userName,date,STATUS,updatedBY) 
                       VALUES ( '{}','{}','{}',
                               '{}','{}','{}',
                               '{}','{}','{}','{}')""".format(row[1],row[2],row[3],
                               row[4],"NA",userID,
                               userName,update_time,"REQUESTED","NA")
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()

            
        except Exception as e:
            print(e)
            return e 
            
    def get_expense_sheet_by_user(self,userid):
        stmt = "SELECT * from ppehvacdb.ExpenseMaster where userid='{}' ORDER BY STATUS DESC ".format(userid)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        expense_list = []
        for row in cursor:
            expense_list.append(list(row))
        expense_frame = pd.DataFrame(expense_list,columns = ['request_id','Expensetype' ,'company_name','Description' ,
                   'Amount_requested' , 'Amount_approved' ,'userID',
                   'userName','date','STATUS','updatedBY'])
        expense_frame = expense_frame[['request_id','Expensetype' ,'company_name','Description' ,
                                      'Amount_requested','Amount_approved','date','STATUS','updatedBY']]
        return expense_frame
    

    def get_expense_sheet(self,userid,status,Expensetype,company_name,startDate,endDate):
         
            startDate  =  datetime.datetime.strptime(startDate, "%Y-%m-%d").strftime("%d/%m/%Y")
            endDate    =  datetime.datetime.strptime(endDate, "%Y-%m-%d").strftime("%d/%m/%Y")
            stmt = "SELECT * from ppehvacdb.ExpenseMaster where STATUS='{}'".format(status)
            if userid!="ALL":
                stmt=stmt+" and userID='{}'".format(userid)    
                
            if status!="ALL":
                stmt=stmt+" and STATUS='{}'".format(status)
                
            if Expensetype!="ALL":
                stmt=stmt+" and Expensetype='{}'".format(Expensetype)
                
            if company_name!="ALL":
                stmt=stmt+" and company_name='{}'".format(company_name)
                            
            stmt=stmt+"""and str_to_date(date,'%d/%m/%Y') >=str_to_date('{}','%d/%m/%Y') 
            and str_to_date(date,'%d/%m/%Y') <=str_to_date('{}','%d/%m/%Y') """.format(startDate,endDate)

            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            expense_list = []
            for row in cursor:
                expense_list.append(list(row))
            expense_frame = pd.DataFrame(expense_list,columns = ['request_id','Expensetype' ,'company_name','Description' ,
                       'Amount_requested' , 'Amount_approved' ,'userID',
                       'userName','date','STATUS','updatedBY'])
            expense_frame = expense_frame[['request_id','Expensetype' ,'company_name','Description' ,
                                          'Amount_requested','Amount_approved','date','userName','STATUS','updatedBY']]
            return expense_frame
    
    def update_expense(self,temp_Df,updatedBy):
        try:
            for row in temp_Df.itertuples():
                ts = time.time()
                update_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
                update_time = str(update_time.strftime('%d/%m/%Y %H:%M:%S')).split(".")[0]      
                stmt = """update ppehvacdb.ExpenseMaster 
                          set Amount_approved= '{}'  ,STATUS='{}' ,updatedBY='{}'
                          where request_id='{}' """.format(row[2],row[3],updatedBy,row[1])
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute(stmt)
                conn.commit()

        except Exception as e:
            return e     
    ############################################################ END EXPENSE MANGMENT #######################################################################
  
    ############################### START INSTRUMENT MODULE  #####################################################################   
    def get_available_equipment(self):
        try:
            stmt = "SELECT * from ppehvacdb.equipment_master where status='AVAILABLE'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def update_equipment(self,equipment_master):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("""Truncate ppehvacdb.equipment_master""")
            conn.commit()
            
            for row in equipment_master.itertuples():
                query = """INSERT INTO ppehvacdb.equipment_master 
                    (Type ,EQUIPMENT_NAME ,MAKE ,MODEL_NUMBER,SR_NO_ID ,
                    DONE_DATE ,DUE_DATE,STATUS,ISSUED_TO ,COMPANY_NAME,REMARK) 
                    VALUES ( '{}','{}','{}','{}','{}',
                   '{}','{}','{}','{}','{}','{}')""".format(row[1],row[2],row[3],row[4],
                                                  row[5],row[6],row[7],
                                                  row[8],row[9],row[10],row[11])
                
                cursor.execute(query)
            conn.commit()
            
                
        except Exception as e: 
            return e
            

            
            
    def request_for_equipment(self,SR_NO_ID,company_name,REMARK,ISSUED_TO):
        try:
            query = """update ppehvacdb.equipment_master 
                      set STATUS= 'REQUESTED' , ISSUED_TO='{}' ,COMPANY_NAME='{}' ,REMARK='{}'
                      where SR_NO_ID='{}' """.format(ISSUED_TO,company_name,REMARK,SR_NO_ID)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
           

            ts = time.time()
              
            update_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
            update_time = str(update_time.strftime('%d/%m/%Y %H:%M:%S')).split(".")[0]            
         
            MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME = get_equipment_property(SR_NO_ID)

  
            query = """INSERT INTO ppehvacdb.elogbook 
                    (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,
                    model_number ,make ,type ,equipment_type,update_time) 
                    VALUES ( '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(SR_NO_ID,'REQUESTED',ISSUED_TO,company_name,REMARK,
                    MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME,update_time)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()            
        except Exception as e:
            return e 
            
            
    def close_request_for_equipment(self,temp_Df,ISSUED_TO):
        try:
            for row in temp_Df.itertuples():
                STATUS = row[2]
                if STATUS=="CLOSED":
                    query = """update ppehvacdb.equipment_master 
                              set STATUS= '{}'  ,REMARK='{}' 
                              where SR_NO_ID='{}' """.format("AVAILABLE",row[3],row[1])
                    conn = mysql.connector.connect(**config)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()
                    

                
                    ts = time.time()
                  
                    update_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
                    update_time = str(update_time.strftime('%d/%m/%Y %H:%M:%S')).split(".")[0]
                    
                    
                    MODEL_NUMBER ,MAKE ,Type, EQUIPMENT_NAME = get_equipment_property(row[1])
                    
            
                    query = """INSERT INTO ppehvacdb.elogbook 
                    (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,
                    model_number ,make ,type ,equipment_type,update_time) 
                    VALUES ( '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(row[1],STATUS,ISSUED_TO,row[4],row[3],MODEL_NUMBER ,MAKE ,Type,
                    EQUIPMENT_NAME,update_time)
                    conn = mysql.connector.connect(**config)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()           
        except Exception as e:
            print(e)
            return e        
            
    def get_requested_instrument(self,ISSUED_TO):
        try:
            stmt = "SELECT * from ppehvacdb.equipment_master where status='REQUESTED' and ISSUED_TO='{}' ".format(ISSUED_TO)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def get_filtered_elogbook(self,serial_id,user_id,STATUS,COMPANY_NAME,startDate,endDate):
         
            startDate  =  datetime.datetime.strptime(startDate, "%Y-%m-%d").strftime("%d/%m/%Y")
            endDate    =  datetime.datetime.strptime(endDate, "%Y-%m-%d").strftime("%d/%m/%Y")
            
            
            
            stmt= """SELECT SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,update_time from ppehvacdb.elogbook where str_to_date(update_time,'%d/%m/%Y') >=str_to_date('{}','%d/%m/%Y') 
            and str_to_date(update_time,'%d/%m/%Y') <=str_to_date('{}','%d/%m/%Y') """.format(startDate,endDate)
            
            if user_id!="ALL":
                stmt=stmt+" and ISSUED_TO='{}'".format(user_id)    
                
            if serial_id!="ALL":
                stmt=stmt+" and SR_NO_ID='{}'".format(serial_id)    
                
            if STATUS!="ALL":
                stmt=stmt+" and STATUS='{}'".format(STATUS)
                
            if COMPANY_NAME!="ALL":
                stmt=stmt+" and COMPANY_NAME='{}'".format(COMPANY_NAME)        

            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            expense_list = []
            for row in cursor:
                expense_list.append(list(row))
            elog_frame = pd.DataFrame(expense_list,columns = ['SR_NO_ID' ,'STATUS','ISSUED_TO' ,'COMPANY_NAME' , 'REMARK' ,'update_time'])
            return elog_frame
   
    def selected_instrument_dropdown(self,TYPE,ISSUED_TO,role):
        try:
            stmt = """SELECT * from ppehvacdb.equipment_master where
            status='REQUESTED' and Type='{}' and ISSUED_TO='{}'""".format(TYPE,ISSUED_TO)
            if role=="documentcell" :
                stmt = """SELECT * from ppehvacdb.equipment_master where
                            Type='{}'""".format(TYPE)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
            
        except Exception as e:
            return e      
            
    ############################### END INSTRUMENT MODULE  ##################################################################### 
    def get_report_number(self,report_type,date,company_name):
        try:   
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()        
            query ="""select count(*) from ppehvacdb.file_repo where
                           company_name='{}' and date ='{}' and report_type = '{}'""".format(company_name,date,report_type)
            cursor.execute(query)
            counter_val  = cursor.fetchall()[0][0]
            return counter_val            
        except Exception as e:
            print(e)
    def insert_file(self,report_type,report_number,prepared_by,date,timestamp,company_name,room_name,file_path):
        try:   
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            
            table_name = "file_repo"
            binary_file = convert_into_binary(file_path)            
            sql_insert_blob_query = """ INSERT INTO file_repo (report_type, report_number,
             prepared_by,date,timestamp,
             company_name,room_name,file_blob) VALUES (%s,%s,
             %s,%s,%s,
             %s,%s,%s)"""

            insert_blob_tuple = (report_type,report_number,
                                            prepared_by,date,timestamp,company_name,room_name,binary_file)
  
            cursor.execute(sql_insert_blob_query, insert_blob_tuple)

            conn.commit()
            print('File inserted successfully')
        except Exception as e:
            print(e)
            print("Failed to insert blob into the table")
           
    def get_report_log(self,basic_details,write_to_directory=False):
        
        companyname  = basic_details['companyname']
        USERNAME     = basic_details['USERNAME']
        reportnumber = basic_details['reportnumber']
        reporttype   = basic_details['reporttype']
        room_name    = basic_details['room_name']
        startDate    = basic_details['startdate']
        endDate      = basic_details['enddate']
        
       
        startDate  =  datetime.datetime.strptime(startDate, "%Y-%m-%d").strftime("%d/%m/%Y")
        endDate    =  datetime.datetime.strptime(endDate, "%Y-%m-%d").strftime("%d/%m/%Y")
        stmt= """SELECT * from ppehvacdb.file_repo where (str_to_date(date,'%d/%m/%Y') >=str_to_date('{}','%d/%m/%Y') 
            and str_to_date(date,'%d/%m/%Y') <=str_to_date('{}','%d/%m/%Y') )""".format(startDate,endDate)
            
        if companyname!="ALL":
            stmt = stmt+" and company_name='{}'".format(companyname)
                
        if USERNAME!="ALL":
            stmt=stmt+" and prepared_by='{}'".format(USERNAME)
            
        if reporttype!="ALL":
            stmt=stmt+" and report_type='{}'".format(reporttype)            
        if reportnumber!="":
            stmt=stmt+" and lower(report_number) like '%{}%'".format(reportnumber.lower())
        if room_name!="":
            stmt=stmt+" and lower(room_name) like '%{}%'".format(room_name.lower())
        
        
        print(stmt)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        report_list = []
        if write_to_directory:
            [f.unlink() for f in Path("static/Report/TEMP_DIR/").glob("*") if f.is_file()] 
        for row in cursor:
            temp_row=[]
            temp_row.append(row[0])
            temp_row.append(row[1])
            temp_row.append(row[2])
            temp_row.append(row[3])
            temp_row.append(row[4])
            temp_row.append(row[5])
            temp_row.append(row[6])
            file_name ="{}.xlsx".format(row[1])
            temp_row.append(file_name)
            temp_row.append(base64.b64encode(row[7]).decode('ascii'))
            if write_to_directory:                  
                    final_working_directory = "static/Report/TEMP_DIR/{}"       
                    store_location = final_working_directory.format(file_name)
                    final_working_directory = MYDIR + "/"+final_working_directory.format(file_name)         
                    with open(final_working_directory, 'wb') as file:
                        file.write(row[7])
        
                      
            report_list.append(temp_row)
        report_frame = pd.DataFrame(report_list,columns = ['report_type', 'report_number',
                                        'prepared_by','date','timestamp',
                                        'company_name','room_name','file_name','data'])
        
         
        return report_frame     
