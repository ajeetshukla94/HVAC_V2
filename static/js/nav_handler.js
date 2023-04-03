function handle_nav_bar(role){
	if (role == "admin")
	{
			document.getElementById("request_instrumnet_link").style.display = "none";
			document.getElementById("approve_instrumnet_link").style.display = "block";
			document.getElementById("log_book_link").style.display = "block";
			document.getElementById("air_velicty_link").style.display = "none";
			document.getElementById("paotest_link").style.display = "none";			
			document.getElementById("particle_count_link").style.display = "none";
			document.getElementById("add_user_page_link").style.display = "block";
			document.getElementById("update_company_details_link").style.display = "block";
			document.getElementById("update_instrument_link").style.display = "block";
			document.getElementById("thermal_link").style.display = "none";
			document.getElementById("request_expense_link").style.display = "none";	
			document.getElementById("approve_expense_link").style.display = "block";	
			document.getElementById("update_user_link").style.display = "block";	
			document.getElementById("close_instrumnet_link").style.display = "block";
			document.getElementById("download_report_link").style.display = "block";

			
			
	}
	else if(role == "analyst")
	{
			document.getElementById("request_instrumnet_link").style.display = "block";
			document.getElementById("approve_instrumnet_link").style.display = "none";
			document.getElementById("log_book_link").style.display = "none";
			document.getElementById("air_velicty_link").style.display = "block";
			document.getElementById("paotest_link").style.display = "block";			
			document.getElementById("particle_count_link").style.display = "block";
			document.getElementById("add_user_page_link").style.display = "none";
			document.getElementById("update_company_details_link").style.display = "none";
			document.getElementById("update_instrument_link").style.display = "none";		
            document.getElementById("thermal_link").style.display = "none";		
			document.getElementById("request_expense_link").style.display = "block";
		    document.getElementById("approve_expense_link").style.display = "none";
			document.getElementById("update_user_link").style.display = "none";
			document.getElementById("close_instrumnet_link").style.display = "block";
			document.getElementById("download_report_link").style.display = "block";
	}
	else if(role == "documentcell")
	{
			document.getElementById("request_instrumnet_link").style.display = "none";
			document.getElementById("download_report_link").style.display = "block";
			document.getElementById("approve_instrumnet_link").style.display = "none";
			document.getElementById("log_book_link").style.display = "none";
			document.getElementById("air_velicty_link").style.display = "block";
			document.getElementById("paotest_link").style.display = "block";
			document.getElementById("particle_count_link").style.display = "block";
			document.getElementById("add_user_page_link").style.display = "none";
			document.getElementById("update_company_details_link").style.display = "none";
			document.getElementById("update_instrument_link").style.display = "none";
            document.getElementById("thermal_link").style.display = "block";
			document.getElementById("request_expense_link").style.display = "block";
		    document.getElementById("approve_expense_link").style.display = "none";
			document.getElementById("update_user_link").style.display = "none";
			document.getElementById("close_instrumnet_link").style.display = "none";
	}
	else if(role == "operation")
	{
			document.getElementById("request_instrumnet_link").style.display = "none";
			document.getElementById("download_report_link").style.display = "none";
			document.getElementById("approve_instrumnet_link").style.display = "block";
			document.getElementById("log_book_link").style.display = "block";
			document.getElementById("air_velicty_link").style.display = "none";
			document.getElementById("paotest_link").style.display = "none";			
			document.getElementById("particle_count_link").style.display = "none";
			document.getElementById("add_user_page_link").style.display = "none";
			document.getElementById("update_company_details_link").style.display = "none";
			document.getElementById("update_instrument_link").style.display = "none";	
            document.getElementById("thermal_link").style.display = "block";	
			document.getElementById("request_expense_link").style.display = "block";
			document.getElementById("approve_expense_link").style.display = "none";
			document.getElementById("update_user_link").style.display = "none";
			document.getElementById("close_instrumnet_link").style.display = "block";
	}
}