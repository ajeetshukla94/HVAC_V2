class MyHeader extends HTMLElement{
	
	connectedCallback()	{
		this.innerHTML ='<div id="header"> \
		<img src="static/images/ppe.png" id="header-img"> \
		<h2 id="header-text">PIN POINT ENGINEERS</h2> \
		</div> \
		<div class="navbar"> \
		<a id = "request_instrumnet_link" href="/request_instrument">REQUEST INSTRUMENT</a> \
		<a id = "approve_instrumnet_link" href="/approve_instrument_request">UPDATE INSTRUMENT REQUEST</a> \
		<a id = "close_instrumnet_link" href="/close_instrument_request">CLOSE INSTRUMENT REQUEST</a> \
		<a id = "log_book_link" href="/elogbook">E-LOGBOOK</a> \
		<a id = "air_velicty_link" href="/render_Air_velocity">AIR VELOCITY REPORT</a> \
		<a id = "paotest_link" href="/render_paotest">PAO TEST</a> \
		<a id = "particle_count_link" href="/render_particle_count">PARTICLE COUNT TEST</a> \
		<a id = "add_user_page_link" href="/add_user_page">ADD NEW USER</a>   \
		<a id = "update_company_details_link" href="/UpdateCompanyDetails">UPDATE COMPANY DETAILS</a>   \
		<a id = "update_instrument_link" href="/UpdateinstrumentDetails">UPDATE INSTRUMENT DETAILS</a>   \
		<a id = "thermal_link" href="/thermal_report">THERMAL REPORT</a>   \
		<a id = "request_expense_link" href="/request_expense">REQUEST EXPENSE</a>   \
		<a id = "approve_expense_link" href="/approve_expense">APPROVE EXPENSE</a>   \
		<a id = "update_user_link" href="/update_user_details">UPDATE USER DETAILS</a>   \
		<a id = "download_report_link" href="/download_report">DOWNLOAD REPORT</a>   \
		<a href="/logout">LOGOUT</a>  \
		</div>\
		'
		
	}
}
customElements.define('my-header',MyHeader)


class MyFooter extends HTMLElement{
	
	connectedCallback()	{
		this.innerHTML ='<div id="footer">\
			<h6 id="footer-text">Developed By &#169; Pin Point Engineers</h6>\
		</div>\
		'
	}
}
customElements.define('my-footer',MyFooter)