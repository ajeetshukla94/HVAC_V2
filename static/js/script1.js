var frame_count = 1;  

$(document).ready(function(){
    $('body').append($('<script src="static/js/md5.min.js"></script>'));
	$('body').append($('<script type=module defer src="static/js/jquery-3.4.1.min.js"></script>'));
});

function add_row(elem)
{
	
	var row_index = elem.parentElement.parentElement.children[0].rows.length - 1;
	var row = elem.parentElement.parentElement.children[0].rows[row_index];
    var table = elem.parentElement.parentElement.children[0];
    var clone = row.cloneNode(true);
	var cells_length = clone.cells.length - 1;
	for(var i = 1; i<cells_length; i++)
	{
		clone.cells[i].children[0].value=""
	}
    table.appendChild(clone);
}

function delete_row(elem){
	if(elem.parentElement.parentElement.parentElement.rows.length > 2)
	{
		elem.parentElement.parentElement.remove();
	}
	else
	{
		alert("First row can not be deleted!")
	}
}



function thermal_submit(){
	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	$('#thermalsubmit').hide()
	if ($('#cycle_name').val()=="")
	{
		alert("Enter Cycle Name");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_name'] =$('#cycle_name').val();
	
	if ($('#started_on').val()=="")
	{
		alert("Cycle Start Time Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['started_on'] =$('#started_on').val();
	
	
	if ($('#cycle_start_time_duration').val()=="")
	{
		alert("Cycle start to Hold Duration Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_start_time_duration'] =$('#cycle_start_time_duration').val();
	
	if ($('#cycle_sterlization_duration').val()=="")
	{
		alert("Sterilization Hold Time Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_sterlization_duration'] =$('#cycle_sterlization_duration').val();
	
	if ($('#cycle_end_duration').val()=="")
	{
		alert("Hold End Time To Cycle End Time Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_end_duration'] =$('#cycle_end_duration').val();
	
	if ($('#interval_in_seconds').val()=="")
	{
		alert("Logging Interval Time Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['interval_in_seconds'] =$('#interval_in_seconds').val();
	
	if ($('#cycle_start_min').val()=="")
	{
		alert("Min. Temp At the Cycle Start Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_start_min'] =$('#cycle_start_min').val();
	
	if ($('#cycle_start_max').val()=="")
	{
		alert("Max. Temp At the Cycle Start Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_start_max'] =$('#cycle_start_max').val();
	
	
	
	if ($('#cycle_end_min').val()=="")
	{
		alert("Min. Temp At Cycle End Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_end_min'] =$('#cycle_end_min').val();
	
	if ($('#cycle_end_max').val()=="")
	{
		alert("Max. Temp At Cycle End Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['cycle_end_max'] =$('#cycle_end_max').val();
	
	if ($('#number_of_sensor').val()=="")
	{
		alert("Sensor Qty Required");$('#thermalsubmit').show()
		return;
	}
	basic_details['number_of_sensor'] =$('#number_of_sensor').val();
	
	
	if ($('#sterlization_min').val()=="")
	{
		alert("Min. Temp At the Hold Start Required");$('#thermalsubmit').show()
		return;
	}
	if ($('#sterlization_min').val()!="")
	{
		var myArray = $('#sterlization_min').val().split(",");
		if( myArray.length!=$('#number_of_sensor').val())
		{
			alert("Min. Temp At the Hold Start does not match with number of sensor quantity");$('#thermalsubmit').show()
			return;
		}
	}
	basic_details['sterlization_min'] =$('#sterlization_min').val();
	
	if ($('#sterlization_max').val()=="")
	{
		alert("Max. Temp At the Hold Start Required");$('#thermalsubmit').show()
		return;
	}
	if ($('#sterlization_max').val()!="")
	{
		var myArray1 = $('#sterlization_max').val().split(",");
		if( myArray1.length!=$('#number_of_sensor').val())
		{
			alert("Max. Temp At the Hold Start does not match with number of sensor quantity");$('#thermalsubmit').show()
			return;
		}
	}
	basic_details['sterlization_max'] =$('#sterlization_max').val();
		
	$.post('/submit_thermal_report', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		$('#thermalsubmit').show()
		

		
	});
	
}



function thermalsubmit_new(){
	
	$('#thermalsubmit_new').hide()
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	
	basic_details['report_name'] =$('#report_name').val();
	basic_details['number_of_sensor'] =$('#number_of_sensor').val();
	basic_details['interval_in_seconds'] =$('#interval_in_seconds').val();

	basic_details['stage1_start_time'] =$('#stage1_start_time').val();
	basic_details['stage1_end_time'] =$('#stage1_end_time').val();
	basic_details['stage1_start_temperature'] =$('#stage1_start_temperature').val();
	basic_details['stage1_end_temperature']   = $('#stage1_end_temperature').val();

	basic_details['number_of_left_side_pulse'] =$('#number_of_left_side_pulse').val();
	basic_details['left_side_pulse_start_time'] =$('#left_side_pulse_start_time').val();
	basic_details['left_side_pulse_end_time'] =$('#left_side_pulse_end_time').val();
	basic_details['left_side_pulse_start_temperature'] =$('#left_side_pulse_start_temperature').val();
	basic_details['left_side_pulse_end_temperature'] =$('#left_side_pulse_end_temperature').val();

	basic_details['pre_sterlization_start_time'] =$('#pre_sterlization_start_time').val();
	basic_details['pre_sterlization_end_time'] =$('#pre_sterlization_end_time').val();
	basic_details['pre_sterlization_start_temperature'] =$('#pre_sterlization_start_temperature').val();
	basic_details['pre_sterlization_end_temperature'] =$('#pre_sterlization_end_temperature').val();
	
	basic_details['sterlization_start_time'] =$('#sterlization_start_time').val();
	basic_details['sterlization_end_time'] =$('#sterlization_end_time').val();
	basic_details['sterlization_start_temperature'] =$('#sterlization_start_temperature').val();
	basic_details['sterlization_end_temperature'] =$('#sterlization_end_temperature').val();


	basic_details['post_sterlization_start_time'] =$('#post_sterlization_start_time').val();
	basic_details['post_sterlization_end_time'] =$('#post_sterlization_end_time').val();
	basic_details['post_sterlization_start_temperature'] =$('#post_sterlization_start_temperature').val();
	basic_details['post_sterlization_end_temperature'] =$('#post_sterlization_end_temperature').val();
		

	basic_details['number_of_right_side_pulse'] =$('#number_of_right_side_pulse').val();
	basic_details['right_side_pulse_start_time'] =$('#right_side_pulse_start_time').val();
	basic_details['right_side_pulse_end_time'] =$('#right_side_pulse_end_time').val();
	basic_details['right_side_pulse_start_temperature'] =$('#right_side_pulse_start_temperature').val();
	basic_details['right_side_pulse_end_temperature'] =$('#right_side_pulse_end_temperature').val();


	basic_details['final_stage_start_time'] =$('#final_stage_start_time').val();
	basic_details['final_stage_end_time'] =$('#final_stage_end_time').val();
	basic_details['final_stage_start_temperature'] =$('#final_stage_start_temperature').val();
	basic_details['final_stage_end_temperature'] =$('#final_stage_end_temperature').val();

	$.post('/submit_thermal_report_new', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		$('#thermalsubmit_new').show()
		

		
	});
	
}





function add_users()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Role cannot be blank in row : "+j);
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Company Name cannot be blank in row : "+j);
				return;
		}
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("First Name cannot be blank in row : "+j);
				return;
		}
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Last Name cannot be blank in row : "+j);
				return;
		}
		
		
		if (tds[4].firstElementChild.value=="")
		{	
				alert("Password cannot be blank in row : "+j);
				return;
		}	

		if (tds[5].firstElementChild.value=="")
		{	
				alert("Email cannot be blank in row : "+j);
				return;
		}	
	}
	var final_table_data = {};
    var full_data        = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Role']        = tds[0].firstElementChild.value 
		table_data['CompanyName'] = tds[1].firstElementChild.value 		
		table_data['fname']       = tds[2].firstElementChild.value 
		table_data['lname']       = tds[3].firstElementChild.value 
		salted_pass               = tds[4].firstElementChild.value
		table_data['email']       = tds[5].firstElementChild.value
		encrypted_pass            = md5(salted_pass)	
		table_data['Password']    = encrypted_pass		
		final_table_data[j]       = table_data
	}
	
	full_data['observation'] = final_table_data	
	$.getJSON('/submit_add_user', 
	{
		params_data : JSON.stringify(full_data)
	}
	, function(result) 
	{
		alert("Users Added kindly note down usernam-"+result.userID);		
	});
	
}


function view_user_details()
{
	USERNAME = $('#USERNAME').val();
	if ($('#USERNAME').val()=="")
	{
		alert("PLEASE SELECT USERNAME");
		return;
	}	
	basic_details={}
	basic_details['USERNAME'] = $('#USERNAME').val();
	$.getJSON('/get_user_detail_by_userID_sheet', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var record_list =  result['user_list'][0]
		$('#USERTABLE').empty();
		var header='<tr>\
				 <th>Role</th><th>COMPANY NAME</th><th>Username</th><th>First Name</th>\
				 <th>Last Name</th><th>Email ID</th><th>Status</th></tr>'
		$('#USERTABLE').append(header);
		
	
		var temp = '<tr id="myTableRow" name="myTableRow">\
		<td><select class="textfield" name="ROLE" id="ROLE" style="width:100%">'
		
		if (record_list.ROLE=="admin")
		{
			temp =temp +'<option value="admin" selected>Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp +'<option value="documentcell" >Documentation</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="analyst")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" selected >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp +'<option value="documentcell" >Documentation</option>'
			temp =temp +'<option value="companyPortal" >Company Portal</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="operation")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" selected>Operation</option>'
			temp =temp +'<option value="documentcell" >Documentation</option>'
			temp =temp +'<option value="companyPortal" >Company Portal</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="documentcell")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp +'<option value="documentcell"selected >Documentation</option>'
			temp =temp +'<option value="companyPortal" >Company Portal</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="companyPortal")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp +'<option value="documentcell" >Documentation</option>'
			temp =temp +'<option value="companyPortal"selected >Company Portal</option>'			
			temp =temp+'</select></td>'
		}
		var COMPANYNAME = record_list.COMPANYNAME.split(' ').join('\xa0');
		temp=temp+'<td><input type="text" name="compnayname" id="compnayname" value='+COMPANYNAME+' class="textfield" disabled ></td>\
		<td><input type="text" name="Username" id="Username" value='+record_list.USERNAME+' class="textfield" disabled></td>\
		<td><input type="text" name="FirstNAME" id="FirstNAME" value='+record_list.FNAME+' class="textfield" ></td>\
		<td><input type="text" name="LastNAME" id="LastNAME" value='+record_list.LNAME+' class="textfield" ></td>\
		<td><input type="text" name="emaild" id="emaild" value='+record_list.EMAILID+' class="textfield" ></td>\
		<td>\
		<select class="textfield" name="STATUS" id="STATUS" style="width:100%">\
		'	
		if (record_list.STATUS=="ACTIVE")
		{
			temp =temp +'<option value="ACTIVE" selected>ACTIVE</option>'
			temp =temp +'<option value="INACTIVE" >INACTIVE</option>'
		}
		else
		{
			temp =temp +'<option value="ACTIVE" >ACTIVE</option>'
			temp =temp +'<option value="INACTIVE" selected>INACTIVE</option>'
		}

		temp =temp+'</select></td></tr>'
		$('#USERTABLE tr:last').after(temp);		
				
		
		
	});
	
}

function delete_user_details()
{
	USERNAME = $('#USERNAME').val();
	if ($('#USERNAME').val()=="")
	{
		alert("PLEASE SELECT USERNAME");
		return;
	}	
	basic_details={}
	basic_details['USERNAME'] = $('#USERNAME').val();
	$.getJSON('/delete_user', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		alert(result.error)
		
	});	
}

function update_user_details()
{
	
	if ($('#USERNAME').val()=="")
	{
		alert("PLEASE SELECT USERNAME");
		return;
	}
	
	if ($('#FirstNAME').val()=="")
	{
		alert("Please Enter First Name");
		return;
	}	
	if ($('#LastNAME').val()=="")
	{
		alert("Please Enter Last Name");
		return;
	}	
	if ($('#emaild').val()=="")
	{
		alert("Please Enter Email id");
		return;
	}	
	basic_details={}
	basic_details['USERNAME']  = $('#USERNAME').val();
	basic_details['FirstNAME'] = $('#FirstNAME').val();
	basic_details['LastNAME']  = $('#LastNAME').val();
	basic_details['STATUS']    = $('#STATUS').val();
	basic_details['ROLE']      = $('#ROLE').val();
	basic_details['emaild']    = $('#emaild').val();
	basic_details['PASSWORD']  = "";
	$.getJSON('/submit_update_user_details', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		alert("User Details Updated");			
		
	});
	
}



function update_profile_details()
{
	if ($('#FNAME').val()=="")
	{
		alert("Please Enter First Name");
		return;
	}	
	if ($('#LNAME').val()=="")
	{
		alert("Please Enter Last Name");
		return;
	}	
	if ($('#emaild').val()=="")
	{
		alert("Please Enter Email id");
		return;
	}
	if ($('#PASSWORD').val()=="")
	{
		alert("Please Enter PASSWORD");
		return;
	}	
	basic_details={}
	basic_details['USERNAME']  = $('#USERNAME').val();
	basic_details['FirstNAME'] = $('#FNAME').val();
	basic_details['LastNAME']  = $('#LNAME').val();
	salted_pass                = $('#PASSWORD').val();
	encrypted_pass             = md5(salted_pass)
	basic_details['PASSWORD']  = encrypted_pass;
	basic_details['emaild']    = $('#EMAILID').val();
	$.getJSON('/submit_update_user_details', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		alert("User Details Updated");			
		
	});
	
}


function submit_request_expense()
{
	$("#submitexpensebutton").hide();
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Expense Type cannot be blank in row : "+j);$("#submitexpensebutton").show();
				return;
		}	

        if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter Company Name cannot be blank in row : "+j);$("#submitexpensebutton").show();
				return;
		}

		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter Description cannot be blank in row : "+j);$("#submitexpensebutton").show();
				return;
		}	
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter Amount cannot be blank in row : "+j);$("#submitexpensebutton").show();
				return;
		}	
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Expensetype']  = tds[0].firstElementChild.value 		
		table_data['company_name'] = tds[1].firstElementChild.value 
		table_data['Description']  = tds[2].firstElementChild.value	
		table_data['Amount']       = tds[3].firstElementChild.value		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data	
	$.getJSON('/submit_expense', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("Expense Request Raised");		
		window.location.reload();
		$("#submitexpensebutton").show();
	});	
}


function view_expense()
{
	USERNAME = $('#USERNAME').val();
	STATUS = $('#STATUS').val();
	if ($('#USERNAME').val()=="")
	{
		alert("Please select USERNAME");
		return;
	}
	if ($('#STATUS').val()=="")
	{
		alert("Please select STATUS");
		return ;
	}
	if ($('#startdate').val()=="")
	{
		alert("Please select Start Date");
		return ;
	}
	if ($('#enddate').val()=="")
	{
		alert("Please select End Date");
		return ;
	}
	
	basic_details={}
	basic_details['STATUS']        = $('#STATUS').val();
	basic_details['USERNAME']      = $('#USERNAME').val();
	basic_details['Expensetype']   = $('#Expensetype').val();
	basic_details['company_name']  = $('#company_name').val();
	basic_details['startdate']     = $('#startdate').val();
	basic_details['enddate']       = $('#enddate').val();
	
	$("#expense_submit_button").hide();	
	$.getJSON('/get_expense_sheet', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		record_list =  result['expense_list']
		var approvedamount  = 0	
		var deniedamount    = 0
		var amount_requested = 0
		$('#EXPENSETABLE').empty();
		if ( ($('#STATUS').val()=="APPROVED")  ||($('#STATUS').val()=="DENIED"))
		{
		var header='<tr>\
				 <th>Request ID</th><th>Expense Type</th><th>Company Name</th>\
				 <th>Description</th><th>User</th><th>Amount Requested</th><th>Amount Approved</th><th>Date</th>\
				  </tr>'
		}
		else
		{
		var header='<tr>\
				 <th>Request ID</th><th>Expense Type</th><th>Company Name</th>\
				 <th>Description</th><th>User</th><th>Amount Requested</th><th>Amount Approved</th><th>Date</th>\
				<th>Status</th></tr>'
		}
		$('#EXPENSETABLE').append(header);
		for(var j = 0; j<record_list.length; j++)
		{	var company_name=record_list[j].company_name;
			var Expensetype=record_list[j].Expensetype;
			var Description=record_list[j].Description;
			var userName=record_list[j].userName;
	        company_name = company_name.split(' ').join('\xa0');
			Expensetype  = Expensetype.split(' ').join('\xa0');
			Description  = Description.split(' ').join('\xa0');
			userName     = userName.split(' ').join('\xa0');
	        
			if ( ($('#STATUS').val()=="APPROVED")  ||($('#STATUS').val()=="DENIED"))
			{
			var temp = '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="request_id" value='+record_list[j].request_id+' class="textfield" disabled></td>\
			<td><input type="text" name="Expensetype" value='+Expensetype+' class="textfield" disabled></td>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="Description" value='+Description+' class="textfield" disabled></td>\
			<td><input type="text" name="userName" value='+userName+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_requested" value='+record_list[j].Amount_requested+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_approved" value='+record_list[j].Amount_approved+' class="textfield" disabled ></td>\
			<td><input type="text" name="date" value='+record_list[j].date+' class="textfield" disabled></td>\
			<td>\
			</td>\
			</tr>'
			amount_requested = parseFloat(amount_requested)+parseFloat(record_list[j].Amount_requested);
			approvedamount = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_approved);
			deniedamount   = parseFloat(deniedamount)+parseFloat(record_list[j].Amount_approved);
			}
			else
			{
			$("#expense_submit_button").show();
			var temp = '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="request_id" value='+record_list[j].request_id+' class="textfield" disabled></td>\
			<td><input type="text" name="Expensetype" value='+Expensetype+' class="textfield" disabled></td>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="Description" value='+Description+' class="textfield" disabled></td>\
			<td><input type="text" name="userName" value='+userName+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_requested" value='+record_list[j].Amount_requested+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_approved" value='+record_list[j].Amount_requested+' class="textfield" ></td>\
			<td><input type="text" name="date" value='+record_list[j].date+' class="textfield" disabled></td>\
			<td>\
			<select class="textfield" name="STATUS" id="STATUS" style="width:100%">\
			<option value="APPROVED">APPROVE</option>\
			<option value="REQUESTED">REQUESTED</option>\
			<option value="DENIED">DENIED</option>\
			</select>\
			</td>\
			</tr>'
			approvedamount = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_requested);
			deniedamount   = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_requested);
			}
			$('#EXPENSETABLE tr:last').after(temp);		
		}		

		if ($('#STATUS').val()=="REQUESTED")
		{
			$('#declined').val(0)
			$('#approved').val(approvedamount)
		}
		else
		{
		    $('#approved').val(approvedamount)
			$('#declined').val(parseFloat(amount_requested)-parseFloat(approvedamount))
		}
		
	});
	
}


$('#EXPENSETABLE').on('change', 'input', function () 
{
    var req  = 0
    var appr  = 0
    var requested  =0
	var approvedamount =0
    code_tbl = document.getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
        req  = tds[5].firstElementChild.value	
		appr = tds[6].firstElementChild.value
		requested = parseFloat(requested)+parseFloat(req);
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Expense Type cannot be blank in row : "+j);
				return;
		}	
		else
		{
			approvedamount   = parseFloat(approvedamount)+parseFloat(appr);
		}
	}	
	
	$('#approved').val(approvedamount)
	$('#declined').val(parseFloat(requested)-parseFloat(approvedamount))
	
	
	
});


function submit_update_expense()
{
	code_tbl = document.getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[6].firstElementChild.value=="")
		{	
				alert("Filter Amount Approved cannot be blank in row : "+j);
				return;
		}	

        if (tds[8].firstElementChild.value=="")
		{	
				alert("Filter Status cannot be blank in row : "+j);
				return;
		}	
	}	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['request_id']  = tds[0].firstElementChild.value 		
		table_data['Amount_approved'] = tds[6].firstElementChild.value 
		table_data['STATUS']  = tds[8].firstElementChild.value	
		final_table_data[j] = table_data
	}	
	full_data['observation']=final_table_data	
	$.post('/submit_update_expense', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("Expense Request Updated");		
		window.location.reload();
	});
}


function filterInstrument(column_number,input_name) 
{
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById(input_name);
  filter = input.value.toUpperCase();
  table = document.getElementById("eqp_table");
  tr = table.getElementsByTagName("tr")
  
  for (i = 0; i < tr.length; i++) 
  {
    
    td = tr[i].getElementsByTagName("td")[column_number];
    if (td) 
	{
      txtValue = td.children[0].value
      if (txtValue.toUpperCase().indexOf(filter) > -1) {tr[i].style.display = "";} 
	  else {tr[i].style.display = "none";}
    }
  }
}

function request_instrument()
{
	var selected_eq = new Array();	
	$("input:checkbox[name=selected_eq]:checked").each(function() {
       selected_eq.push($(this).val());
	});
	
	if (selected_eq==""  || selected_eq==undefined)
	{	
		alert("Please select Instrument");
		return;
	}	
	
	company_name = $('#company_name').val();
	if (company_name=="")
	{	
		alert("Please enter company name");
		return;
	}	
	
	REMARK = $('#remark').val();
	if (REMARK=="")
	{	
		alert("Please enter REMARK");
		return;
	}	
	
	var table_data = {};
	table_data['selected_eq']  = selected_eq
	table_data['company_name'] = company_name		
	table_data['REMARK'] = REMARK 
	
	$.getJSON('/push_instrument_request', 
	{
		params_data : JSON.stringify(table_data)
	}, function(result) 
	{
		alert("INSTRUMENT : "+selected_eq+" : HAS BEEN REQUESTED");	
		window.location.reload();
	});
	
}



function close_instrument()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[8].firstElementChild.value=="")
		{	
				alert("Filter APPROVE/CLOSE cannot be blank in row : "+j);
				return;
		}	

        if (tds[7].firstElementChild.value=="")
		{	
				alert("Filter REMARK cannot be blank in row : "+j);
				return;
		}			
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['APPROVE/DENY']  = tds[8].firstElementChild.value 		
		table_data['SR_NO_ID']       = tds[4].firstElementChild.value 
		table_data['REMARK']       = tds[7].firstElementChild.value	
		table_data['COMPANY_NAME']       = tds[6].firstElementChild.value		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/update_close_request', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("EQUIPMENT DETAILS UPDATED");		
		window.location.reload();
	});	
}

function view_logbook()
{
	if ($('#startdate').val()=="")
	{
		alert("Please select Start Date");
		return ;
	}
	if ($('#enddate').val()=="")
	{
		alert("Please select End Date");
		return ;
	}
	
	basic_details={}	
	basic_details['serial_id']        = $('#serial_id').val();
	basic_details['user_id']   = $('#user_id').val();
	basic_details['company_name']  = $('#company_name').val();	
	basic_details['STATUS']        = $('#STATUS').val();
	basic_details['startdate']     = $('#startdate').val();
	basic_details['enddate']       = $('#enddate').val();
	
	$.getJSON('/get_elogbook', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		record_list =  result['elog_list']

		$('#LOGTABLE').empty();
		
		var header='<tr>\
				 <th>Serial ID</th><th>Company Name</th><th>STATUS</th>\
				 <th>ISSUED TO</th><th>REMARK</th><th>Update timestamp</th>\
				  </tr>'
		
		$('#LOGTABLE').append(header);
		for(var j = 0; j<record_list.length; j++)
		{	
			var SR_NO_ID     = record_list[j].SR_NO_ID;
			var company_name = record_list[j].COMPANY_NAME;
			
			var STATUS       = record_list[j].STATUS;
			var ISSUED_TO    = record_list[j].ISSUED_TO;
			
			var REMARK       = record_list[j].REMARK;
			var update_time  = record_list[j].update_time;
			
	        // SR_NO_ID        = SR_NO_ID.split(' ').join('\xa0');
			company_name    = company_name.split(' ').join('\xa0');
			// STATUS          = STATUS.split(' ').join('\xa0');
			// ISSUED_TO       = ISSUED_TO.split(' ').join('\xa0');
			// REMARK          = REMARK.split(' ').join('\xa0');
			// update_time     = update_time.split(' ').join('\xa0');
	        
			
			var temp = '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="SR_NO_ID" value='+SR_NO_ID+' class="textfield" disabled></td>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="STATUS" value='+STATUS+' class="textfield" disabled></td>\
			<td><input type="text" name="ISSUED_TO" value='+ISSUED_TO+' class="textfield" disabled></td>\
			<td><input type="text" name="REMARK" value='+REMARK+' class="textfield" disabled></td>\
			<td><input type="text" name="update_time" value='+update_time+' class="textfield" disabled></td>\
			<td>\
			</td>\
			</tr>'
			
			
			$('#LOGTABLE tr:last').after(temp);		
		}		

		
		
	});
	
}


function export_logbook()
{
	
	if ($('#startdate').val()=="")
	{
		alert("Please select Start Date");
		return ;
	}
	if ($('#enddate').val()=="")
	{
		alert("Please select End Date");
		return ;
	}
	
	basic_details={}	
	basic_details['serial_id']        = $('#serial_id').val();
	basic_details['user_id']   = $('#user_id').val();
	basic_details['company_name']  = $('#company_name').val();	
	basic_details['STATUS']        = $('#STATUS').val();
	basic_details['startdate']     = $('#startdate').val();
	basic_details['enddate']       = $('#enddate').val();
	
	$.getJSON('/export_logbook', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));		
	});
	
}


$(function() 
{
	$("#SR_NO").change(function()
	{        
	SR_NO = $('option:selected',this).text();
	
	$.getJSON('/get_instument_details', 
	{
		params_data : JSON.stringify(SR_NO)
	}, function(data) 
	{			
		
		$('#INSTRUMENT_NAME').val(data.INSTRUMENT_NAME);
      	$('#MAKE_MODEL').val(data.MAKE);
        $('#VALIDITY').val(data.VALIDITY);							
	
	});
  });
});


$(function() 
{
    $("#company_name").change(function() 
    {
	company_name = $('option:selected',this).text();
	$.getJSON('/get_company_details', 
	{
		params_data : JSON.stringify(company_name)
	}, function(data) 
	{
		$('#company_address').val(data.company_address);
      	$('#Test_taken').val(data.test_taken);		
		$('#Department').val(data.Department);							
	});
 });
});


var val_1;
var val_2;
$("#airvelocitygrade").change(function()
{ 
	grade = $('option:selected',this).text();
	var full_data = {};
	full_data['grade'] = grade   	
	if (grade=="A" || grade=="ISO 5")
	{
		$("#acph_thresold").hide();
		$("#acph_thresold_label").hide();
        $("#room_volume_label").hide();
        $("#room_volume").hide();
        $("#Inlet_size_label").hide();
        $("#Inlet_sizetd").hide();
		$("#CALCACPHVALUELABEL").hide();	
		$("#CALCACPHVALUE").hide();
		$("#ahu_number_label").text("Equipment ID");
		$("#room_name_label").text("Equipment Name");
	}
	else
	{
		$("#acph_thresold").show();
		$("#acph_thresold_label").show();		
		$("#CALCACPHVALUELABEL").show();	
		$("#CALCACPHVALUE").show();
        $("#room_volume_label").show();
        $("#room_volume").show();
		$("#Inlet_size_label").show();
        $("#Inlet_sizetd").show();
		$("#ahu_number_label").text("AHU Number");
		$("#room_name_label").text("ROOM NAME");	
	}
});

$('#AIRVELOCITYTABLE').on('change', 'input', function () {
	if ($('#airvelocitygrade').val()=="")
	{
		alert("Please select Grade");
		return ;
	}
	if($('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5" )
	{
		if ($('#room_volume').val()=="" )
		{
				alert("Please enter Room Volume");
				return ;
		}
		var room_volume =$('#room_volume').val();
		var frame_list = document.getElementsByClassName("frame");
		code_tbl = frame_list[0].getElementsByClassName("code_tbl")[1]
		code_rows = code_tbl.rows	
		
		var Total_cfm  = 0;
		for(var j = 1; j<code_rows.length; j++)
		{
			tds = code_rows[j].children		
			for(var l = 2; l<7; l++)
			{
				var velocity = 0;
				var cfm    = 0;
				
				if (tds[l].firstElementChild.value!="")
				{	
					velocity = velocity+parseInt(tds[l].firstElementChild.value);
					
				}
				if (tds[1].firstElementChild.value!="")
				{	
					var inlet_size = parseFloat(tds[1].firstElementChild.value);
					cfm =((velocity/5)*parseFloat(inlet_size));						
				}
				
				Total_cfm = Total_cfm+cfm					
			}					
			var ACPH_VALUE  = parseFloat((Total_cfm * 60)) / parseFloat(room_volume)
			$('#CALCACPHVALUE').val(parseFloat(ACPH_VALUE).toFixed(2));			
		}
	}
	
	
});

function submit_air_velocity(){	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	$("#airvelocitysubmit").hide();
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");
		$("#airvelocitysubmit").show();
		return;
	}
	if ($('#airvelocitygrade').val()=="")
	{
		alert("Please select Grade");$("#airvelocitysubmit").show();
		return ;
	}


	if ($('#ahu_number').val()=="" && $('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5" )
	{
		alert("Please Enter AHU Number");$("#airvelocitysubmit").show();
		return ;
	}
	if ($('#room_name').val()=="" && $('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5" )
	{
		alert("Please Room Name");$("#airvelocitysubmit").show();
		return ;
	}
	
	if ($('#ahu_number').val()=="" && $('#airvelocitygrade').val()=="A" && $('#airvelocitygrade').val()=="ISO 5" )
	{
		alert("Please Enter Equipment ID");$("#airvelocitysubmit").show();
		return ;
	}
	if ($('#room_name').val()=="" && $('#airvelocitygrade').val()=="A" && $('#airvelocitygrade').val()=="ISO 5" )
	{
		alert("Please Equipment Name");$("#airvelocitysubmit").show();
		return ;
	}





	if ($('#room_volume').val()=="" && $('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5")
	{
		alert("Please enter Room Volume");$("#airvelocitysubmit").show();
		return ;
	}	
		
	if ($('#acph_thresold').val()=="" && $('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5" )
	{
		alert("Please enter ACPH Thresold");$("#airvelocitysubmit").show();
		return ;
	}	
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");$("#airvelocitysubmit").show();
		return ;
	}
	if ($('#Department').val()=="")
	{
		alert("Please enter Department ");$("#airvelocitysubmit").show();
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");$("#airvelocitysubmit").show();
		return ;
	}
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no'] =$('#SR_NO').val();
	basic_details['company_name'] =$('#company_name').val();
	basic_details['room_volume'] =$('#room_volume').val();
	basic_details['room_name'] =$('#room_name').val();
	basic_details['ahu_number'] =$('#ahu_number').val();	
	basic_details['Department'] =$('#Department').val();
	basic_details['Test_taken'] =$('#Test_taken').val();
	basic_details['grade'] =$('#airvelocitygrade').val();
	basic_details['acph_thresold'] =$('#acph_thresold').val();
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter ID number cannot be blank in row : "+j);$("#airvelocitysubmit").show();
				return;
		}
		if (tds[1].firstElementChild.value=="" && $('#airvelocitygrade').val()!="A" && $('#airvelocitygrade').val()!="ISO 5" )
		{	
				alert("Inlet Size cannot be blank in row : "+j);$("#airvelocitysubmit").show();
				return;
		}
		
		for(var l = 2; l<7; l++)
		{
			temp=l-1
			if (tds[l].firstElementChild.value=="")
			{	
				alert("Please enter correct value for V"+temp+" in row : "+j);$("#airvelocitysubmit").show();
				return;
			}
			
		}		
	}
	
	for(var j = 1; j<code_rows.length; j++){
		
		tds = code_rows[j].children
		Label_number = tds[0].firstElementChild.value
		V1 = tds[2].firstElementChild.value
		V2 = tds[3].firstElementChild.value
		V3 = tds[4].firstElementChild.value
		V4 = tds[5].firstElementChild.value
		V5 = tds[6].firstElementChild.value
		
		
		var table_data = {};
		table_data['Label_number'] =Label_number 
		table_data['V1'] =V1
		table_data['V2'] =V2
		table_data['V3'] =V3
		table_data['V4'] =V4
		table_data['V5'] =V5
        if ($('#airvelocitygrade').val()=="A" && $('#airvelocitygrade').val()=="ISO 5" )
		{
			inlet_size = ""
		}
		else
	    { 
			inlet_size = tds[1].firstElementChild.value
		}
		table_data['Inlet_size'] =inlet_size
		final_table_data[j] = table_data
	}
	
	
		
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.post('/submit_air_velocity', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		$("#airvelocitysubmit").show();	
	});
}

$('#paotable').on('change', 'input', function () {
    var row = $(this).closest('tr');
   	var check_val = $('#check_val').val();
    var upstream  = $('#Upstream', row).val();
	var Leakage   = $('#Leakage', row).val();	
	
	if ((upstream!="") && (upstream<=100 &&  upstream>=1) && (Leakage!="" )&& (Leakage<=check_val))
	{
		$('#Remark', row).val("Pass");
	}	
	else 
	{
		$('#Remark', row).val("Fail");
	}
});


function submit_pao()
{
	test_type = $('input[name="test_type"]:checked').val();
	$("#paosubmit_button").hide();
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");$("#paosubmit_button").show();
		return;
	}
	
	if ($('#ahu_number').val()=="")
	{
		alert("Please Enter AHU Number");$("#paosubmit_button").show();
		return ;
	}
	if ($('#room_name').val()=="")
	{
		alert("Please Room Name");$("#paosubmit_button").show();
		return ;
	}
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");$("#paosubmit_button").show();
		return ;
	}
	if ($('#location').val()=="")
	{
		alert("Please enter Department ");$("#paosubmit_button").show();
		return ;
	}	
	if ($('#compresed_value').val()=="")
	{
		alert("Please Enter Compressed Air Value");$("#paosubmit_button").show();
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");$("#airvelocitysubmit").show();
		return ;
	}
	
	if ($('#regent_used').val()=="")
	{
		alert("Please Enter Regent Used ");$("#airvelocitysubmit").show();
		return ;
	}
	
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no']        = $('#SR_NO').val();
	basic_details['company_name'] = $('#company_name').val();
	basic_details['room_name']    = $('#room_name').val();
	basic_details['ahu_number']   = $('#ahu_number').val();	
	basic_details['location']     = $('#location').val();
	basic_details['Test_taken']   = $('#Test_taken').val();
	basic_details['regent_used']  = $('#regent_used').val();
	
	basic_details['compresed_value'] = $('#compresed_value').val();
	basic_details['check_val']       = $('#check_val').val();
	basic_details['test_type']       = test_type;
	
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter ID number cannot be blank in row : "+j);$("#paosubmit_button").show();
				return;
		}
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter INLET NUMBER cannot be blank in row : "+j);$("#paosubmit_button").show();
				return;
		}
		
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter Upstream cannot be blank in row : "+j);$("#paosubmit_button").show();
				return;
		}
		
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter Leakage cannot be blank in row : "+j);$("#paosubmit_button").show();
				return;
		}
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter Remark cannot be blank in row : "+j);$("#paosubmit_button").show();
				return;
		}		
		
	}
	for(var j = 1; j<code_rows.length; j++)
	{		
		tds = code_rows[j].children
		INLET_NUMBER = tds[0].firstElementChild.value
		Upstream = tds[1].firstElementChild.value
		Leakage = tds[2].firstElementChild.value
		Remark = tds[3].firstElementChild.value
		
		var table_data = {};
		table_data['INLET_NUMBER'] =INLET_NUMBER 
		table_data['Upstream'] =Upstream
		table_data['Leakage'] =Leakage
		table_data['Remark'] =Remark
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.post('/submit_data_pao', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		$("#paosubmit_button").show();
	});
	
}






function s2ab(s)
 {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
  return buf;
}


function edit_report(reportnumber,reporttype)
{
	basic_details={}
	basic_details['reporttype']    = reporttype;
	basic_details['reportnumber']  = reportnumber;
	$.getJSON('/edit_report', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
			
	});
	
}






function view_report_log()
{
	basic_details={}
	basic_details['companyname']   = $('#companyname').val();
	basic_details['USERNAME']      = $('#USERNAME').val();
	basic_details['reporttype']    = $('#reporttype').val();
	basic_details['reportnumber']  = $('#reportnumber').val();
	basic_details['room_name']     = $('#room_name').val();
	basic_details['startdate']     = $('#startdate').val();
	basic_details['enddate']       = $('#enddate').val();
	
	if ($('#startdate').val()=="")
	{
		alert("Please select Start Date");
		return ;
	}
	if ($('#enddate').val()=="")
	{
		alert("Please select End Date");
		return ;
	}
	
	$('#ReportTable').empty();
	$('#DownlodReportbtn').hide();
	$('#DownlodaggReportbtn').hide();
	$.getJSON('/view_reportlog', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		report_list =  result['report_log']
		var header='<th>Company Name</th>\
		<th>User Name</th><th>Report Type</th>\
		<th>Room Name</th><th>DATETIME</th><th>DOWNLOAD</th>'
		$('#ReportTable').append(header);
		for(var j = 0; j<report_list.length; j++)
		{	var company_name  = report_list[j].company_name;
			var prepared_by   = report_list[j].prepared_by;
			var report_type   = report_list[j].report_type;
			var room_name     = report_list[j].room_name;
			var timestamp     = report_list[j].timestamp;
			
			var blob      = new Blob([s2ab(atob(report_list[j].data))], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,'});
			var link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);

	        
			company_name  = company_name.split(' ').join('\xa0');
			prepared_by   = prepared_by.split(' ').join('\xa0');
			report_type   = report_type.split(' ').join('\xa0');
			room_name = room_name.split(' ').join('\xa0');
			timestamp     = timestamp.split(' ').join('\xa0');	   			
			var temp = '<tr>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="prepared_by" value='+prepared_by+' class="textfield" disabled></td>\
			<td><input type="text" name="report_type" value='+report_type+' class="textfield" disabled></td>\
			<td><input type="text" name="report_number" value='+room_name+' class="textfield" disabled></td>\
			<td><input type="text" name="timestamp" value='+timestamp+' class="textfield" disabled></td>\
			<td><a href='+link+' download='+report_list[j].file_name+'>'+report_list[j].file_name+'</a><td>\
			</tr>'		
			$('#ReportTable').append(temp);	
			$('#DownlodReportbtn').show();
			$('#DownlodaggReportbtn').hide();
						
		}	
	});
	
}


function consolidate_report()
{
	basic_details={}
	basic_details['companyname']   = $('#companyname').val();
	basic_details['USERNAME']      = $('#USERNAME').val();
	basic_details['reporttype']    = $('#reporttype').val();
	basic_details['reportnumber']  = $('#reportnumber').val();
	basic_details['room_name']     = $('#room_name').val();
	basic_details['startdate']     = $('#startdate').val();
	basic_details['enddate']       = $('#enddate').val();
	
	if ($('#startdate').val()=="")
	{
		alert("Please select Start Date");
		return ;
	}
	if ($('#enddate').val()=="")
	{
		alert("Please select End Date");
		return ;
	}
	
	$.getJSON('/consolidate_report', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
	});
	
}




function DownlodReport()
{
	var table = document.getElementById("ReportTable");
	for (var i = 0; i<table.rows.length+1; i++) 
	{
        table.rows[i].cells[5].children[0].click()
	}	
}

var val_1;
var val_2;
$("#pa_grade").change(function()
	{
        
	grade = $('option:selected',this).text();
	var full_data = {};
	full_data['grade'] = grade
	full_data['gl_value'] = $('#gl_value').val()
	full_data['condition'] = $('#condition').val()	
	$.getJSON('/get_limits', 
	{
		params_data : JSON.stringify(full_data)
	}, function(data) 
	{		
			val_1 = data.value1 
			val_2 = data.value2
										
	});
    });
	
$('#particleCountTable').on('change', 'input', function () 
{
    var row = $(this).closest('tr');
	if (typeof(val_1)=="undefined" ||typeof(val_2)=="undefined")
	{
		alert("Please select Guildline and Grade");
		$('#five_point_zero', row).val("");
		$('#zeor_point_five', row).val("");
		$('#remark', row).val("");
		
		return ;
	}	
    var zeor_point_five  = $('#zeor_point_five', row).val();
	var five_point_zero   = $('#five_point_zero', row).val();	
	
	if (zeor_point_five<=parseInt(val_1) && five_point_zero <= parseInt(val_2))
	{
			$('#remark', row).val("Pass");
	}	
	else {$('#remark', row).val("Fail");}	
});


function submit_particle_report(){
	
	$("#particleCountsubmit").hide();
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");$("#particleCountsubmit").show();
		return;
	}
	
	if ($('#ahu_number').val()=="")
	{
		alert("Please Enter AHU Number");$("#particleCountsubmit").show();
		return ;
	}
	if ($('#room_name').val()=="")
	{
		alert("Please Room Name");$("#particleCountsubmit").show();
		return ;
	}	
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");$("#particleCountsubmit").show();
		return ;
	}
	if ($('#location').val()=="")
	{
		alert("Please enter Department ");$("#particleCountsubmit").show();
		return ;
	}
	if ($('#pa_grade').val()=="")
	{
		alert("Please Select Grade ");$("#particleCountsubmit").show();
		return ;
	}
	if ($('#condition').val()=="")
	{
		alert("Please Select condition");$("#particleCountsubmit").show();
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");$("#particleCountsubmit").show();
		return ;
	}
	
	if ($('#gl_value').val()=="")
	{
		alert("Please Select Guidelines");$("#particleCountsubmit").show();
		return ;
	}
	
	
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no'] =$('#SR_NO').val();
	basic_details['company_name'] =$('#company_name').val();
	basic_details['room_name'] =$('#room_name').val();
	basic_details['ahu_number'] =$('#ahu_number').val();	
	basic_details['location'] =$('#location').val();
	basic_details['Test_taken'] =$('#Test_taken').val();
	basic_details['condition'] =$('#condition').val();
	basic_details['grade'] =$('#pa_grade').val();
	basic_details['gl_value'] =$('#gl_value').val();
	
	
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Location cannot be blank in row : "+j);$("#particleCountsubmit").show();
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter ≥ 0.5 μm cannot be blank in row : "+j);$("#particleCountsubmit").show();
				return;
		}
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter ≥ 5.0 μm cannot be blank in row : "+j);$("#particleCountsubmit").show();
				return;
		}
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Remark cannot be blank in row : "+j);$("#particleCountsubmit").show();
				return;
		}
		
		
		
		
	}
	for(var j = 1; j<code_rows.length; j++){
		
		tds = code_rows[j].children
		Location = tds[0].firstElementChild.value
		zeor_point_five = tds[1].firstElementChild.value
		five_point_zero = tds[2].firstElementChild.value
		remark = tds[3].firstElementChild.value
		
		
		var table_data = {};
		table_data['Location'] =Location 
		table_data['zeor_point_five'] =zeor_point_five
		table_data['five_point_zero'] =five_point_zero
		table_data['remark'] =remark
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.post('/submit_particle_report', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		$("#particleCountsubmit").show();
		

		
	});
	
}

function updateCompanyDetails()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	$("#updatecompnaybutton").hide();	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter COMPANY NAME cannot be blank in row : "+j);$("#updatecompnaybutton").show();	
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter ADDRESS cannot be blank in row : "+j);$("#updatecompnaybutton").show();	
				return;
		}
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter REPORT NUMBER  cannot be blank in row : "+j);$("#updatecompnaybutton").show();	
				return;
		}		
	}
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['COMPANY_NAME'] =tds[0].firstElementChild.value 	
		table_data['ADDRESS'] =tds[1].firstElementChild.value 	
		table_data['REPORT_NUMBER'] =tds[2].firstElementChild.value 		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.post('/submit_updateCompanyDetails', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("COMPANY DETAILS UPDATED");	
		$("#updatecompnaybutton").show();			
	});
	
}

function updateinstrumentDetails()
{
	code_tbl = document.getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows	
	$("#instrumnetupdtbtn").hide();	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Type cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter EQUIPMENT NAME cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}	
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter MAKE cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}			
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter MODEL NUMBER cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}			
		if (tds[4].firstElementChild.value=="")
		{	
				alert("Filter SR NO ID cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}			
		if (tds[5].firstElementChild.value=="")
		{	
				alert("Filter DONE DATE cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}			
		if (tds[6].firstElementChild.value=="")
		{	
				alert("Filter DUE DATE cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}
		if (tds[7].firstElementChild.value=="")
		{	
				alert("Filter STATUS  cannot be blank in row : "+j);$("#instrumnetupdtbtn").show();	
				return;
		}			
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Type']  = tds[0].firstElementChild.value 	
		table_data['EQUIPMENT_NAME']       = tds[1].firstElementChild.value 	
		table_data['MAKE'] = tds[2].firstElementChild.value 
		table_data['MODEL_NUMBER']  = tds[3].firstElementChild.value 	
		table_data['SR_NO_ID']       = tds[4].firstElementChild.value 	
		table_data['DONE_DATE'] = tds[5].firstElementChild.value 	
		table_data['DUE_DATE']  = tds[6].firstElementChild.value 		
		table_data['STATUS']    = tds[7].firstElementChild.value 	
		table_data['ISSUED_TO'] = tds[8].firstElementChild.value 
		table_data['COMPANY_NAME']    = tds[9].firstElementChild.value 	
		table_data['REMARK'] = tds[10].firstElementChild.value 
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.post('/submit_updateinstrumentDetails', 
	{
		params_data : JSON.stringify(full_data)
	}, function() 
	{
		alert("EQUIPMENT DETAILS UPDATED");	
        window.location.reload();	
		$("#instrumnetupdtbtn").show();	
	});
}
	


$('input[type=radio][name=test_type]').change(function() 
{
    if (this.value == 'AHU') 
	{
        $("#test_for_name_lbl").text("AHU Number");
		$("#test_for_id_lbl").text("ROOM Name");
    }
    else if (this.value == 'EQUIPMENT')
	{
        $("#test_for_name_lbl").text("Equipment ID");
		$("#test_for_id_lbl").text("Equipment Name");
    }
});


var val_1;
var val_2;
$("#pa_grade").change(function()
{ 
	grade = $('option:selected',this).text();
	var full_data = {};
	full_data['grade'] = grade   	
	if (grade=="A" || grade=="ISO 5")
	{
		 $("#test_for_name_lbl").text("Equipment ID");
		$("#test_for_id_lbl").text("Equipment Name");
	}
	else
	{
		$("#test_for_name_lbl").text("AHU Number");
		$("#test_for_id_lbl").text("ROOM Name");
	}
});

