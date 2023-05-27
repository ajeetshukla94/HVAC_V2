
class MyHeader extends HTMLElement{
	
	connectedCallback()	{						   
		var menu = '<nav class="animated bounceInDown bg-dark">\
						<ul>\
							<li><img src="static/images/logo.png" id="header-img"></li>\
							<li id="admin_grp" class="sub-menu"><a href="#profile">ADMIN PANEL<div class="fa fa-caret-down right"></div></a>\
								<ul>\
									<li><a href="/add_user_page">ADD USER</a></li>\
									<li><a href="/update_user_details_page">UPDATE USER DETAILS</a></li>\
									<li><a href="/UpdateCompanyDetails">UPDATE COMPANY DETAILS</a></li>\
									<li><a href="/UpdateinstrumentDetails">UPDATE INSTRUMENT DETAILS</a></li>\
									<li><a href="/UPDATE_EXPENSE_STATUS">UPDATE EXPENSE STATUS</a></li>\
									<li><a href="/render_elogbook">E-LOGBOOK</a></li>\
								</ul>\
							</li>\
							<li id="expense_grp" class="sub-menu"><a href="#expense">EXPENSE PANEL<div class="fa fa-caret-down right"></div></a>\
								<ul>\
									<li><a href="/request_expense">REQUEST EXPENSE</a></li>\
									<li><a href="/expense_status">EXPENSE STATUS</a></li>\
								</ul>\
							</li>\
							<li id="INSTRUMENT_grp" class="sub-menu"><a href="#expense">INSTRUMENT PANEL<div class="fa fa-caret-down right"></div></a>\
								<ul>\
									<li><a href="/request_instrument">RAISE INSTRUMENT REQUEST</a></li>\
									<li><a href="/close_instrument_request">CLOSE INSTRUMENT REQUEST</a></li>\
								</ul>\
							</li>\
							<li id="HVAC_grp" class="sub-menu"><a href="#expense">HVAC REPORTING<div class="fa fa-caret-down right"></div></a>\
								<ul>\
									<li><a href="/render_Air_velocity">AIR VELOCITY</a></li>\
									<li><a href="/render_paotest">PAO TEST</a></li>\
									<li><a href="/render_particle_count">PARTICLE COUNT</a></li>\
									<li><a href="/thermal_report">THERMAL REPORT</a></li>\
									<li><a href="/download_report">DOWNLOAD REPORT</a></li>\
								</ul>\
							</li>\
							<li id="profile_grp" class="sub-menu"><a href="#Profile">Profile<div class="fa fa-caret-down right"></div></a>\
							<ul>\
									<li><a href="/update_self_profile_page">PROFILE</a></li>\
									<li><a href="/logout">LOGOUT</a></li>\
						    </ul>\
							</li>\
						</ul>\
					</nav>'
		
		this.innerHTML = menu
		
	}
}
customElements.define('my-header',MyHeader)


class MyFooter extends HTMLElement
{	
	connectedCallback()
	{
		this.innerHTML ='<div id="footer"><h6 id="footer-text">Developed By &#169; Document Manager</h6></div>'
	}
}
customElements.define('my-footer',MyFooter)

