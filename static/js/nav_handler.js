function handle_nav_bar(role)
{
	if (role == "admin")
	{			
		document.getElementById("admin_grp").style.display = "block";
		document.getElementById("expense_grp").style.display = "none";
		document.getElementById("INSTRUMENT_grp").style.display = "none";
		document.getElementById("HVAC_grp").style.display = "none";
		document.getElementById("HVAC_REPORT_DWN").style.display = "none";		
				
	}	
	else if(role == "analyst")
	{
		document.getElementById("admin_grp").style.display = "none";
		document.getElementById("expense_grp").style.display = "block";
		document.getElementById("INSTRUMENT_grp").style.display = "block";
		document.getElementById("HVAC_grp").style.display = "block";
		document.getElementById("HVAC_REPORT_DWN").style.display = "block";
	}
	else if(role == "operation")
	{
		document.getElementById("admin_grp").style.display = "none";
		document.getElementById("expense_grp").style.display = "block";
		document.getElementById("INSTRUMENT_grp").style.display = "block";
		document.getElementById("HVAC_grp").style.display = "block";
		document.getElementById("HVAC_REPORT_DWN").style.display = "block";
	}
	else if(role == "documentcell")
	{
		document.getElementById("admin_grp").style.display = "none";
		document.getElementById("expense_grp").style.display = "block";
		document.getElementById("INSTRUMENT_grp").style.display = "none";
		document.getElementById("HVAC_grp").style.display = "block";
		document.getElementById("HVAC_REPORT_DWN").style.display = "block";
	}
	else if(role == "companyPortal")
	{
		document.getElementById("admin_grp").style.display = "none";
		document.getElementById("expense_grp").style.display = "none";
		document.getElementById("INSTRUMENT_grp").style.display = "none";
		document.getElementById("HVAC_grp").style.display = "none";
		document.getElementById("HVAC_REPORT_DWN").style.display = "block";
	}
}

