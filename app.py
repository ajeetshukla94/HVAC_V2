from flask import Flask, render_template, flash, url_for, request, make_response, jsonify, session,send_from_directory
from werkzeug.utils import secure_filename
import os, time
import io
import base64
import json
import datetime
import os, sys, glob
from flask import send_file
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from fnmatch import fnmatch
import time
import random
import pandas as pd
import flask
from db_dervices import DBO
from crypt_services import encrypt_sha256
import random
import string
from Report_Genration import Report_Genration
from pathlib import Path
#import win32com.client as win32
#import pythoncom

app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
print("MYDIR",MYDIR)
dbo = DBO()

app.config['UPLOAD_FOLDER']   = "static/inputData/"

ISO_guidlines_master          =  pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],"ISO_guidlines.xlsx"))
EUGMP_guidlines_master        =  pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],"EUGMP_guidlines.xlsx"))
guidlance_list                =  ISO_guidlines_master.Guidelines.unique().tolist()+EUGMP_guidlines_master.Guidelines.unique().tolist()


document_type_list            = ["CLASSIFIED A","CLASSIFIED B","CLASSIFIED C","CLASSIFIED D"]
visibility_list               = ["INTERNAL","EXTERNAL","PUBLIC"]
condition_list                = ['At Rest','In Operation']
grade_list                    = ['A','B','C','D','ISO 5','ISO 6','ISO 7','ISO 8']

sent_mail                     = False
server                        = 'smtp-mail.outlook.com'
port                          =  587
username                      = "pinpointengineers@hotmail.com"
password                      = "#############@12"
send_from                     = "pinpointengineers@hotmail.com"
send_to                       = "ashish@pinpointengineers.co.in"

def send_mail(subject,text,files,file_name,isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if file_name!="":
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}.xlsx'.format(file_name))
            msg.attach(part)
            
        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        
#################################### Start Login logout ######################################       
@app.route("/")
def render_default():
    session.pop('user', None)
    session.pop('selected_file', None)
    flash('Logout Successful')
    return make_response(render_template("LOGINPAGE/login.html",msg = True,err = False, warn = False,message='Logout Successful'),200)
    
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('selected_file', None)
    flash('Logout Successful')
    return make_response(render_template("LOGINPAGE/login.html",msg = True,err = False, warn = False,message='Logout Successful'),200)    
    
@app.route("/render_login", methods=["GET", "POST"])
def render_login(): 
    form_data    = request.form
    user_id      = form_data['login'].lower()
    password     = form_data['password']
    enc_pass     = encrypt_sha256(user_id+password)
    account      = dbo.get_cred(user_id)
    print(enc_pass)
    print(account["password"])
    #print(account["password"])
    if(enc_pass == account["password"]):        
      session_var = {"user": user_id, "role": account["role"],"username": account["username"]}
      session['user'] = session_var
      return make_response(render_template('LOGINPAGE/homepage.html',msg = True, err = False, warn = False, role = session_var["role"]),200)
    else:
      flash('Invalid Credentials')
      return make_response(render_template("LOGINPAGE/login.html", msg = False, err = True, warn = False),403)   

#################################### End Login logout ###################################### 



############################### Start Admin Panel   #####################################################################   
@app.route("/add_user_page")
def add_user_page():
    if 'user' in session:
        customer_details  = dbo.get_company_details()
        company_name_list = customer_details.COMPANY_NAME.unique().tolist()   
        session_var = session['user']
        return make_response(render_template('ADMIN/ADD_USER.html',company_list=company_name_list,role = session_var["role"]),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
    

@app.route("/submit_add_user" )    
def submit_add_user():
    if 'user' in session:
        data            = request.args.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Role','CompanyName','fname','lname','Password','email']]
        print(temp_df)  
        userlist =[]
        for row in temp_df.itertuples(): 
            CompanyName    = str(row[2]).strip()        
            fname    = str(row[3]).strip()
            lname    = str(row[4]).strip()
            role     = row[1]
            password = row[5]
            email    = row[6]
            fname    = fname.lower()
            lname    = lname.lower()
            username = fname+lname[:2]+str(random.randint(10,99))
            dbo.create_user(username,CompanyName,fname,lname, role, encrypt_sha256(username+password),email)
            userlist.append(username)
            subject   = "NEW USER REGISTERED TYPE -{} ID: {} ".format(role,username)
            text      = """Hi PinPoint Team \n\n
                           {} {} has been reigistered into HVAC system with  {} role \n\n
                           Kindly note done Login ID for Reference - {}
                           Regards \n
                           Ajeet Shukla :) :) :)""".format(fname,lname,role,username)
            #send_mail(subject,text,"","") 
            d = {"error":"none","userID":userlist}   
            return json.dumps(d)
    return make_response(render_template('LOGINPAGE/login.html'),200)   

@app.route("/update_user_details_page")  
def update_user_details ():
    if 'user' in session:
        usernameList  = dbo.get_username()
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('ADMIN/UPDATE_USER_DETAILS.html',usernameList=usernameList,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)     
 

    
@app.route("/get_user_detail_by_userID_sheet")  
def get_user_detail_by_userID_sheet ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        user_detail   = dbo.get_user_detail_by_userID_sheet(basic_details['USERNAME']).to_dict('records') 
        d = {"error":"none","user_list":user_detail}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/delete_user")  
def delete_user ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        ret_msg       = dbo.delete_user(basic_details['USERNAME'])
        d = {"error":ret_msg}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/submit_update_user_details")  
def submit_update_user_details ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        dbo.update_user_details(basic_details) 
        d = {"error":"none"}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/update_self_profile_page")  
def update_self_profile_page ():
    if 'user' in session:
        usernameList  = dbo.get_username()
        session_var = session['user']
        role = session_var["role"]
        user_id = session_var["user"]
        user_detail   = dbo.get_user_detail_by_userID_sheet(user_id).to_dict('records') 
        print(user_id)
        print(user_detail)
        return make_response(render_template('ADMIN/SELF_PROFILE.html',user_detail = user_detail,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)  
    
    
@app.route("/UpdateCompanyDetails")
def UpdateCompanyDetails():
    if 'user' in session:
        session_var       = session['user']
        role              = session_var["role"]
        customer_details  = dbo.get_company_details()
        customer_list     = customer_details.to_dict('records')
        return make_response(render_template('ADMIN/UpdateCompanyDetails.html',customer_list  = customer_list, role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)  
    
@app.route("/UpdateinstrumentDetails")
def UpdateinstrumentDetails():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        equipment_details   = dbo.get_equipment("ALL")
        equipment_list      = equipment_details.to_dict('records')
        tmptype             = pd.read_excel(os.path.join("static/inputData/",'eqp.xlsx'))
        type                = tmptype.Type.unique().tolist()
        Equipment_Name      = tmptype.Equipment_Name.unique().tolist()
        return make_response(render_template('ADMIN/UpdateinstrumentDetails.html',Equipment_Namelst=Equipment_Name,eqtype=type,equipment_list  = equipment_list, role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
      
############################### END Admin Panel   #####################################################################  










############################### START EXPENSE MANAGMENT  ##################################################################### 
@app.route("/request_expense")
def request_expense():
    if 'user' in session:
        session_var     = session['user']
        customer_details  = dbo.get_company_details()
        company_name_list = customer_details.COMPANY_NAME.unique().tolist()
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('EXPENSE_MANAGMNET/REQUEST_EXPENSE.html',company_list=company_name_list,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)  
            
@app.route("/submit_expense")
def submit_expense():
    if 'user' in session:
        session_var     = session['user']
        role            = session_var["role"]         
        data            = request.args.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Expensetype','company_name','Description','Amount']]
        dbo.submit_expense(temp_df,session_var['user'],session_var['username'])       
        d = {"error":"none"}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 

@app.route("/expense_status")
def expense_status():
    if 'user' in session:
        session_var     = session['user']
        expense_frame     = dbo.get_expense_sheet_by_user(session_var['user'])
        expense_frame['Description'] = expense_frame['Description'].apply(lambda x : str(x).replace(' ','-'))
        expense_frame['company_name'] = expense_frame['company_name'].apply(lambda x : str(x).replace(' ','-'))
        expense_frame     = expense_frame.to_dict('records')
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('EXPENSE_MANAGMNET/EXPENSE_STATUS.html',expense_record = expense_frame,role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200) 
    
@app.route("/UPDATE_EXPENSE_STATUS")  
def UPDATE_EXPENSE_STATUS ():
    if 'user' in session:
        usernameList  = dbo.get_username()
        customer_details  = dbo.get_company_details()
        company_name_list = customer_details.COMPANY_NAME.unique().tolist()
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('EXPENSE_MANAGMNET/UPDATE_EXPENSE_STATUS.html',company_list=company_name_list,usernameList=usernameList,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
@app.route("/get_expense_sheet")  
def get_expense_sheet ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        expense_list  = dbo.get_expense_sheet(basic_details['USERNAME'],basic_details['STATUS'],
                                    basic_details['Expensetype'],basic_details['company_name'],
                                    basic_details['startdate'],
                                    basic_details['enddate']
                                ).to_dict('records')
     
        d = {"error":"none","expense_list":expense_list}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
 
@app.route("/submit_update_expense",methods=['GET', 'POST'])  
def submit_update_expense():
    if 'user' in session:   
        session_var = session['user']
        role = session_var["role"]    
        data            = request.form.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['request_id','Amount_approved','STATUS']]
        err_msg         = dbo.update_expense(temp_df,session_var['username'])        
        d = {"error":err_msg}
        return flask.jsonify(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
############################### END EXPENSE MANAGMENT  ##################################################################### 

############################### START INSTRUMENT MODULE  ##################################################################### 
@app.route("/request_instrument")
def request_instrument():
    if 'user' in session:
        customer_details    = dbo.get_company_details()
        company_name_list   = customer_details.COMPANY_NAME.unique().tolist()
        session_var         = session['user']
        role                = session_var["role"]
        equipment_details   = dbo.get_available_equipment()
        equipment_list      = equipment_details.to_dict('records')
        return make_response(render_template('INVENTORY/REQUEST_INSTRUMENT.html',
                             equipment_list=equipment_list,company_list=company_name_list, role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
@app.route("/push_instrument_request")
def push_instrument_request():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]         
        data            = request.args.get('params_data')
        observation     = json.loads(data)   
        for equipment in observation['selected_eq']:
                        dbo.request_for_equipment(str(equipment),observation['company_name'],observation['REMARK'],session_var['user'])
        d = {"error":"none"}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 

@app.route("/close_instrument_request")
def close_instrument_request():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        equipment_details   = dbo.get_requested_instrument(session_var['user'])
        equipment_list      = equipment_details.to_dict('records')
        return make_response(render_template('INVENTORY/CLOSE_INSTRUMENT_REQUEST.html',equipment_list  = equipment_list, role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
@app.route("/update_close_request" )    
def update_close_request():
    if 'user' in session:
        session_var = session['user']
        data            = request.args.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['SR_NO_ID','APPROVE/DENY','REMARK','COMPANY_NAME']]
        dbo.close_request_for_equipment(temp_df,session_var['user'])
        d = {"error":"none",}   
        return json.dumps(d) 
        
@app.route("/render_elogbook")
def render_elogbook():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        
        
        serial_id_list      = dbo.get_equipment("ALL").SR_NO_ID.unique().tolist()   
        tmptype             = pd.read_excel(os.path.join("static/inputData/",'eqp.xlsx'))
        type                = tmptype.Type.unique().tolist()
        Equipment_Name_list      = tmptype.Equipment_Name.unique().tolist()      
        customer_details    = dbo.get_company_details()        
        company_name_list   = customer_details.COMPANY_NAME.unique().tolist()
        
        usernameList  = dbo.get_username()
        
        return make_response(render_template('INVENTORY/ELOGBOOK.html', 
        serial_id_list=serial_id_list,type=type,usernameList=usernameList,company_name_list=company_name_list,
        role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
    
@app.route("/get_elogbook")  
def get_elogbook ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        elog_list     = dbo.get_filtered_elogbook(basic_details['serial_id'],basic_details['user_id'],
                                    basic_details['company_name'],basic_details['STATUS'],
                                    basic_details['startdate'],basic_details['enddate']
                                ).to_dict('records')
     
        d = {"error":"none","elog_list":elog_list}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
@app.route("/export_logbook")
def export_logbook():
    if 'user' in session:   
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        logbook       = dbo.get_filtered_elogbook(basic_details['serial_id'],basic_details['user_id'],
                                    basic_details['company_name'],basic_details['STATUS'],
                                    basic_details['startdate'],basic_details['enddate']
                                )  
        logbook.to_excel("static/Report/THERMAL_REPORT/logbook.xlsx",index=False)
        file_name = "logbook.xlsx"
        file_path = "static/Report/THERMAL_REPORT/logbook.xlsx"
        d = {"error":"none",
             "file_name":file_name,
             "file_path":file_path}
             
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
    
############################### END INSTRUMENT MODULE  ##################################################################### 



############################### START HVAC MODULE  ##################################################################### 
@app.route("/get_instument_details")
def get_instument_details():
    if 'user' in session:
        data          = request.args.get('params_data')
        SR_NO_val     = json.loads(data)
        INSTRUMENT_NAME = ""
        MAKE            = ""
        MODEL_NUMBER    = "" 
        done_date       = ""
        due_date        = ""
        VALIDITY        = ""
    
        if SR_NO_val is not None :
            temp_df         = dbo.get_equipment(SR_NO_val)       
            INSTRUMENT_NAME = str(temp_df.EQUIPMENT_NAME.values[0])
            MAKE            = str(temp_df.MAKE.values[0])
            MODEL_NUMBER    = str(temp_df.MODEL_NUMBER.values[0])
            done_date       = str(temp_df.DONE_DATE.values[0]).split()[0]
            due_date        = str(temp_df.DUE_DATE.values[0]).split()[0]
            VALIDITY        = str(temp_df.DUE_DATE.values[0]).replace("-","/").split()[0]  
           
        d = {"error":"none",
            "INSTRUMENT_NAME" : INSTRUMENT_NAME,
            "MAKE"           :  MAKE,
            "MODEL_NUMBER"   :  MODEL_NUMBER,
            "done_date"      :  done_date,
            "due_date"       :  due_date,
            "VALIDITY"        : VALIDITY}
        print(d)
        return json.dumps(d)
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
 
@app.route("/get_company_details", methods=['POST', 'GET'])
def get_company_details():
    if 'user' in session:
        data              = request.args.get('params_data')
        company_name_val  = json.loads(data)
        company_address   = ""   
        Department          = ""
        test_taken        = datetime.datetime.today().strftime('%d/%m/%Y')
        if company_name_val is not None :
            temp_df = dbo.get_company_details_by_company_name(company_name_val)
            company_address =str(temp_df.ADDRESS.values[0])          
        d = {
            "error":"none",
            "company_address":company_address,
            "test_taken":test_taken,
            "Department":Department,
        }
        return json.dumps(d)
    return make_response(render_template('LOGINPAGE/login.html'),200)


@app.route("/render_Air_velocity")
def render_Air_velocity():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"] 
              
        temp_df     = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user'],role)
        company_name_list             = temp_df.COMPANY_NAME.unique().tolist()
        if role =="documentcell":
            customer_details = dbo.get_company_details() 
            company_name_list             = customer_details.COMPANY_NAME.unique().tolist()            
        equipment_list                = temp_df.SR_NO_ID.unique().tolist()
        return make_response(render_template('HVAC_SOLUTION/AIR_VELOCITY.html',
                            company_list=company_name_list,equipment_list =equipment_list,
                            grade_list=grade_list,role = role),200)
    return make_response(render_template('LOGINPAGE/login.html'),200)

@app.route("/submit_air_velocity",methods=['GET', 'POST'])
def submit_air_velocity():
    if 'user' in session:
        data          = request.form.get('params_data')

        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']    
        company_name  = basic_details['company_name']
        temp_df       = pd.DataFrame.from_dict(observation,orient ='index')
        session_var   = session['user']		
        file_name,file_path = Report_Genration.generate_report_air_velocity(temp_df ,basic_details,session_var['username'],session_var['user'])
        subject       = "HVAC-Air Velocity Automated Genrated Report - {}".format(company_name)
        text          = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \n{} :) :) :)".format(file_name,company_name,session_var['username'])
  
        
        if sent_mail:
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path}       
        return flask.jsonify(d)  
        
        
        
@app.route("/render_paotest")
def render_paotest():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        temp_df     = dbo.selected_instrument_dropdown("PAO_TEST",session_var['user'],role)
        company_name_list             = temp_df.COMPANY_NAME.unique().tolist()
        if role =="documentcell":
            customer_details = dbo.get_company_details() 
            company_name_list             = customer_details.COMPANY_NAME.unique().tolist()
        equipment_list                = temp_df.SR_NO_ID.unique().tolist()

        return make_response(render_template('HVAC_SOLUTION/PAO.html',company_list=company_name_list,
                                            equipment_list = equipment_list, role = role),200)
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
@app.route("/submit_data_pao",methods=['GET', 'POST'])
def submit_data_pao():
    if 'user' in session:
        data          = request.form.get('params_data')
        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']
        company_name  = basic_details['company_name']
        temp_df = pd.DataFrame.from_dict(observation,orient ='index')
        session_var = session['user']
        file_name,file_path=Report_Genration.generate_report_pao(temp_df,basic_details,session_var['username'],session_var['user'])
        subject   = "HVAC-PAO Automated Genrated Report - {}".format(company_name)
        text      = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \n{}  :) :) :)".format(file_name,company_name,session_var['username'])
    
        if sent_mail :
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path} 
       
        return flask.jsonify(d)
      
@app.route("/render_particle_count")
def render_particle_count():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        #customer_details              = dbo.get_company_details()
        company_name_list             = dbo.selected_instrument_dropdown("PARTICLE_COUNT",session_var['user'],role).COMPANY_NAME.unique().tolist()
        equipment_list                = dbo.selected_instrument_dropdown("PARTICLE_COUNT",session_var['user'],role).SR_NO_ID.unique().tolist()
        if role =="documentcell": 
            customer_details = dbo.get_company_details()
            company_name_list = customer_details.COMPANY_NAME.unique().tolist()
        print(guidlance_list)
        return make_response(render_template('HVAC_SOLUTION/particle_count.html',company_list=company_name_list,
    					     guidlance_list = guidlance_list  ,
    					     equipment_list = equipment_list,
                             condition_list = condition_list, role = role),200)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
    
@app.route("/update_grade", methods=['POST', 'GET'])
def update_grade(): 
    if 'user' in session:
        data          = request.args.get('params_data')
        gl_value      = json.loads(data)  
        print(gl_value)
        if "ISO" in gl_value :    
            grade_list    = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)]['Grade'].tolist()      
        if "EU" in gl_value  :
            grade_list    = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)]['Grade'].unique().tolist()      
          
        dict_list=[]
        for x in grade_list:
            thisdict ={"id":x,"name":x}
            dict_list.append(thisdict)
        d = {"dict_list":dict_list,"error":"none"}
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)

@app.route("/submit_particle_report",methods=['GET', 'POST'])
def submit_particle_report():
    if 'user' in session:
        data          = request.form.get('params_data')
        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']	
        company_name  = basic_details['company_name']
        temp_df       = pd.DataFrame.from_dict(observation,orient ='index')
        session_var = session['user']
        file_name,file_path=Report_Genration.generate_report_particle_count(temp_df,basic_details,session_var['username'],session_var['user'],
                                                    EUGMP_guidlines_master,ISO_guidlines_master)
        subject   = "Particle Count Automated Genrated Report - {}".format(company_name)
        text      = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \nAjeet Shukla :) :) :)".format(file_name,company_name)
        if sent_mail:
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path}        
        return flask.jsonify(d) 
    
    
    
    
@app.route("/get_limits", methods=['POST', 'GET'])
def get_limits():
    if 'user' in session:    
        data          = request.args.get('params_data')
        full_data     = json.loads(data)   
        gl_value      = full_data['gl_value']
        grade         = full_data['grade']
        condition     = full_data['condition']
        print(gl_value)
        if "EU" not in gl_value :
            value1        = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (ISO_guidlines_master.Grade==grade)
                                                 ]['point_five_percent'].values[0]
            value2        = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (ISO_guidlines_master.Grade==grade)
                                                 ]['five_percent'].values[0]   
        if "EU" in gl_value  : 
        
            value1        = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (EUGMP_guidlines_master.Grade==grade)
                                                        &
                                                (EUGMP_guidlines_master.Condition==condition)
                                                 ]['point_five_percent'].values[0]
                                                 
                                                 
            value2        = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (EUGMP_guidlines_master.Grade==grade)
                                                        &
                                                (EUGMP_guidlines_master.Condition==condition)
                                                 ]['point_five_percent'].values[0]
        
            
            
        
        d = {"value1":str(value1),
             "value2":str(value2),
             "error":"none"}
        print(d)
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)    


@app.route("/thermal_report")
def thermal_report():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('HVAC_SOLUTION/Thermal.html',role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)   

@app.route("/Thermal_new")
def Thermal_new():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('HVAC_SOLUTION/Thermal_new.html',role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)  

@app.route("/submit_thermal_report",methods=['GET', 'POST'])
def submit_thermal_report():
    if 'user' in session:
        data          = request.form.get('params_data')
        basic_details = json.loads(data)        
        session_var   = session['user']		
        file_name,file_path = Report_Genration.generate_thermal_report(basic_details)           
        d = {"error":"none","file_name":file_name,"file_path":file_path}
       
        return flask.jsonify(d)    

@app.route("/submit_thermal_report_new",methods=['GET', 'POST'])
def submit_thermal_report_new():
    if 'user' in session:
        data          = request.form.get('params_data')
        basic_details = json.loads(data)        
        session_var   = session['user']		
        file_name,file_path = Report_Genration.generate_thermal_report_new(basic_details)           
        d = {"error":"none","file_name":file_name,"file_path":file_path}
       
        return flask.jsonify(d)    
    
@app.route("/download_report")  
def download_report ():
    if 'user' in session:
        account = session["user"]
        userid  = account['user']
        usernameList = [userid]
        role         =  account['role']
        print(account)
        if role == "admin":
            usernameList  = dbo.get_username() 
        customer_details  = dbo.get_company_details()
        company_name_list = customer_details.COMPANY_NAME.unique().tolist() 
        if role == "companyPortal":
            account      = dbo.get_cred(account['user'])
            company_name_list = [account['COMPANYNAME']]
              
        return make_response(render_template('DOCUMENTCELL/DOWNLOAD_REPORT.html',company_list=company_name_list,usernameList=usernameList,role = role,userid=userid),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 

@app.route("/edit_report")  
def edit_report ():
    if 'user' in session:
        account       = session["user"]
        usernameList  = [account['user']]
        role          = account['role']
        data          = request.args.get('params_data')
        basic_details = json.loads(data) 
        
        
        basic_details['companyname']  = "ALL"
        basic_details['USERNAME']     = "ALL"
        basic_details['room_name']    = ""
        basic_details['startdate']    = ""
        basic_details['enddate']      = ""
        basic_details['reportnumber']    = str(basic_details['reportnumber'] ).split('.xlsx')[0]
        report_log      = dbo.get_report_log(basic_details).to_dict('records')
       
        data      = report_log[0]['data']
        
        file_name ="{}.xlsx".format(report_log[0]['report_number'])
        print(data)
        print(file_name)
        final_working_directory = "static/Report/EDIT_REPORT/{}"       
        store_location = final_working_directory.format(file_name)
        final_working_directory = MYDIR + "/"+final_working_directory.format(file_name)         
        with open(final_working_directory, 'wb') as file:
            file.write(data)
            
        if report_type=="AIR VELOCITY'":
            session_var = session['user']
            role        = session_var["role"]    
            temp_df     = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user'],role)
            company_name_list             = temp_df.COMPANY_NAME.unique().tolist()
            equipment_list                = temp_df.SR_NO_ID.unique().tolist()
            return make_response(render_template('HVAC_SOLUTION/AIR_VELOCITY_EDIT.html',
                                company_list=company_name_list,equipment_list =equipment_list,
                                grade_list=grade_list,role = role),200)
    return make_response(render_template('LOGINPAGE/login.html'),200) 
 
@app.route("/view_reportlog")  
def view_reportlog():
    if 'user' in session:   
        data            = request.args.get('params_data')
        basic_details   = json.loads(data)    
        report_log      = dbo.get_report_log(basic_details).to_dict('records')
        d = {"error":"none","report_log":report_log}  
        return flask.jsonify(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
@app.route("/consolidate_report")  
def consolidate_report():
    if 'user' in session:   
        data            = request.args.get('params_data')
        basic_details   = json.loads(data)    
        report_log      = dbo.get_report_log(basic_details,write_to_directory=True)
        # win32c =  win32.constants
        # excel = win32.gencache.EnsureDispatch('Excel.Application',pythoncom.CoInitialize())
        # excel.Visible = False  # False
        # wb1  = ""    
        # path = MYDIR + "\\"+"static\\Report\\TEMP_DIR"
        # file_list = glob.glob(path+"\\*.xlsx")
        # for file_name in file_list:
            # print(file_name)
            # if wb1 == "":
                # wb1 = excel.Workbooks.Open(file_name)        
            # else:
                # wb2 = excel.Workbooks.Open(file_name)
                # wb2.Sheets(1).Copy(Before=wb1.Sheets(1))
                # wb2.Close(True)
        # save_path = path+"\\Combined_Report.xlsx"
        # wb1.SaveAs(Filename = save_path) 
        # wb1.Close(True)
        # excel.Quit()
        
        file_name="Combined_Report.xlsx"
        file_path = "static\\Report\\TEMP_DIR\\Combined_Report.xlsx"
        d = {"error":"none","file_name":file_name,"file_path":file_path}  
        
        return flask.jsonify(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/submit_updateCompanyDetails" ,methods=['GET', 'POST'])    
def submit_updateCompanyDetails():
    if 'user' in session:
        data            = request.form.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['COMPANY_NAME','ADDRESS','REPORT_NUMBER']]
        temp_df['COMPANY_NAME'] = temp_df['COMPANY_NAME'].apply(lambda x : str(x).strip())
        temp_df['ADDRESS'] = temp_df['ADDRESS'].apply(lambda x : str(x).strip())
        dbo.update_company_details(temp_df)
        d = {"error":"none",}   
        return flask.jsonify(d)
        
@app.route("/submit_updateinstrumentDetails",methods=['GET', 'POST'] )    
def submit_updateinstrumentDetails():
    if 'user' in session:
        data            = request.form.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Type','EQUIPMENT_NAME','MAKE','MODEL_NUMBER','SR_NO_ID','DONE_DATE','DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK']]
        dbo.update_equipment(temp_df)
        d = {"error":"none",}   
        return json.dumps(d)

############################### END HVAC MODULE  ##################################################################### 

if __name__ == '__main__':
    app.debug = True
    app.run()

