#importing begins
import re
import os
import glob
import cgi
import cgitb; cgitb.enable()
import datetime
import math
from math import log
from math import floor
import webbrowser
import ConfigParser
import fileinput
#import ends

STATUSCODES = {
    200:'OK',                        
    201:'Created',
    202:'Request recorded, will be executed later',
    203:'Non-authoritative information',
    204:'Request executed',
    205:'Reset document',
    206:'Partial Content',
    
    300:'Multiple documents available',
    301:'Moved Permanently',
    302:'Found',
    303:'See other document',
    304:'Not Modified since last retrieval',
    305:'Use proxy', 
    306:'Switch proxy',
    307:'Document moved temporarily',
    
    400:'Bad Request',
    401:'Unauthorized',
    402:'Payment required',
    403:'Forbidden',
    404:'Document Not Found',
    405:'Method not allowed',
    406:'Document not acceptable to client',
    407:'Proxy authentication required',
    408:'Request Timeout',
    409:'Request conflicts with state of resource',
    410:'Document gone permanently',
    411:'Length required',
    412:'Precondition failed',
    413:'Request too long', 
    414:'Requested filename too long', 
    415:'Unsupported media type', 
    416:'Requested range not valid', 
    417:'Failed',
    500:'Internal server Error',
    501:'Not implemented',
    502:'Received bad response from real server',
    503:'Server busy',
    504:'Gateway timeout',
    505:'HTTP version not supported',
    506:'Redirection failed'
    }
#Regular Expression for log line
log_re=re.compile(r'(?P<Elapsed_Time>([^ ]*)) (?P<Client_IP>([^ ]*)) \"(?P<Username>([^\"]*))\" \"(?P<client_id>([^\"]*))\" \[(?P<Time>([^\ ]*))\] \"(?P<Connection_Method>([^\"]*)) (?P<Site>([^\"]*))\" (?P<Http_Status>([^ ]*)) (?P<Size>([^ ]*)) \"(?P<Siteref>([^\"]*))\" \"(?P<Browser>([^\"]*))\" (?P<Mime>([^ ]*)) \"(?P<Filter_Name>([^\"]*)) (?P<Filter_Reason>([^\ ]*))\" \"(?P<Profiles_Applied>([^\"]*))\" \"(?P<Proxy>([^\"]*))\"')
 datelist=[]
userlist=[]
dlist=[] #su use bane no ahiy
timelist=[]
usersizelist=[]

logfile=""
loc=""

def header_set(option,title):
	if option==1:
		set_back='"../../'
		set_back1='"'
	else:
		set_back='"../../../'	
		set_back1='"../'
	header = """ <!DOCTYPE html>
		<html>
		<head>
		<title>"""+title+"""</title>
		<link rel="stylesheet" type="text/css" href="""+set_back+"""css/combined.css" />
		<script src="""+set_back+"""js/combined.js"></script>
		<script src="""+set_back+"""js/paging.js"></script>
		</head>
		<body>
	    <div class="header">
		<div class="navigation-bar dark">
	    <div class="navigation-bar-content container">
			  <a class="element" href="""+set_back+"""index.html">
				  <img class="nav-img" src="""+set_back+"""images/left-icon.png"/>
				  </a>
			        <span class="element-divider"></span>
		 <a href="""+set_back1+"""index.html" class="element">HOMEPAGE</a>
	        <ul class="element-menu">
		
				<li>
	                <a class="element" href="""+set_back1+"""mime.html">Mime</a>
	            </li>
	            <li>
	                 <a class="element" href="""+set_back1+"""profiles.html">Profiles Applied</a>
	            </li>
	           
	            <li>
	                 <a class="element" href="""+set_back1+"""filters.html">Filters </a>
	            </li>
	          <li>
	                <a class="element" href="""+set_back1+"""topsite.html">Top Website</a>

	            </li>
				<li>
	                <a class="element" href="""+set_back1+"""topuser.html">Top User</a>

	            </li>
	            <li>
	                 <a class="element" href="""+set_back1+"""blacklist.html">Security breached</a>
	            </li>
	          
			   <ul class="element-menu place-right">
	            <li>
				<div class="dropdown12">
	                <a class="element" href="#" >View Report By</a>
	                <div class="hide">
					<ul class="dropdown-menu  place-right light dropdown" style="height: 292px; width: 422px; display: block;">
	                    <li> 
						<iframe src="""+set_back+"""Calender/calender.html" width="420px" height="290px" frameborder="0"> </iframe>
						</li>
					</ul>
					</div>
					</div>
				</li>
				<span class="element-divider"></span>
				<li>
				 <a class="element" href="""+set_back+"""settings.html">
				<img class="nav-img1" src="""+set_back+"""images/settings_icon.png"/> </a>
				</li>
				
			</ul>
			
			</ul>
				
			</div>
						
	    </div>
	</div>

	<div class="main">"""
	return header


#delete extra text file
def delete_files(directory):
	
	date_dire=os.listdir(directory)
	os.chdir(directory)
	for datedir in date_dire:
		os.chdir(datedir)
		files=glob.glob('*.TXT')
		for filename in files:
			os.unlink(filename)
		os.chdir('../')

	for datedir in date_dire:
		user_dire=os.listdir(datedir)
		os.chdir(datedir)
		for userdir in user_dire:
			if '.html' not in userdir:
				os.chdir(userdir)
				files=glob.glob('*.TXT')
				for filename in files:
					os.unlink(filename)
				os.chdir('../')	
		os.chdir('../')

#range selection
def selection(dateoption,fromdate,todate):
	global dlist
	if dateoption=='bydate':
		d1 = datetime.date(int(fromdate[6:]),int(fromdate[0:2]),int(fromdate[3:5]))
		d2 = datetime.date(int(todate[6:]),int(todate[0:2]),int(todate[3:5]))
		diff = d2 - d1
		
		for i in range(diff.days + 1):
			dlist.append((d1 + datetime.timedelta(i)).isoformat())
			
months={'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}

# function for bandwidth size conversion
def convertSize(size):
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	if size==0:
		return '0B'
	else:
		i = int(math.floor(math.log(size,1024)))
		p = math.pow(1024,i)
		s = round(size/p,2)
		if (s > 0):
			return '%s %s' % (s,size_name[i])
		else:
			return '0B'
#------------------------------------------------

#generate calender html file
def calender_file(datelist1,loc):
	linklist=[]
	for i in datelist1:
		linklist.append('../'+loc+'/'+i+'/index.html')
	calhtml = open("Calender/calender.html",'wb')
	calhtml.write("""<html>
    <head>
    <link href="jquery-ui.css" rel="stylesheet" type="text/css" />
    <script src="jquery/jquery.min.js"></script>
    <script src="jquery/jquery-ui.min.js"></script>    
		 
    <style type="text/css">
    	body
		{
    		font-family:Arial;
    		font-size : 10pt;
    		padding:0px;
		}

		.Highlight a{
		   background-color : #00aba9 !important;
		   background-image :none !important;
		   color: White !important;
		   font-weight:bold !important;
		   font-size: 15px;
		}
        .nohighlight a{
           background-color : #004050 !important;
           background-image :none !important;
           color: White !important;
           font-weight:bold !important;
           font-size: 15px;
        }



		.ui-datepicker{
			font-size:15px;
            width: 372px;
            height: 240px;
		}

    </style>    
    
	<script>
		$(document).ready(function() {
        var disabledDays ="""+str(datelist1)+""";
        var tips = ['some description1', 'some other description2'];
        var hrefs ="""+str(linklist)+""";
$("#txtDate").datepicker({
    dateFormat: 'yyyy-mm-dd',
    beforeShowDay: function (date) {
        var m = date.getMonth(),
            d = date.getDate(),
            y = date.getFullYear();
        for (var i = 0; i < disabledDays.length; i++) {
            if ($.inArray(y + '-' + (m + 1) + '-' + d, disabledDays) != -1) {
                return [true, 'highlight', "Report"];
            }
            else{
             return [true, 'nohighlight', "No Report"];   
            }
        }
        return [true];
    },
    onSelect: function(dateText, inst) {        
        var date = new Date(dateText.slice(4)),
            m = date.getMonth(),
            d = date.getDate(),
            y = date.getFullYear();        
        if ($.inArray(y + '-' + (m + 1) + '-' + d, disabledDays) != -1) {
            window.parent.location = hrefs[disabledDays.indexOf((y + '-' + (m + 1) + '-' + d))];
        }
    }
});
		});
	</script>
    </head>
    <body>
		<div id='txtDate' /></div>
    </body>
</html>""")

#Funtion to get unique websites as per bandwidth and hits
def get_site(list_sites,list_size, option):
	websitenamesize={}
	websitenamehit={}	
	websitenamesize1=[]
	websitenamehit1=[]
	websiteunique=[]
	websitesize=[]
	webpagehit=[]
	for i,j in enumerate(list_sites):
		if list_sites[i] not in websiteunique:
			websiteunique.append(list_sites[i])
			websitesize.append(int(list_size[i]))
			webpagehit.append(1)
		else:
			b=websiteunique.index(j)
			c=webpagehit[b]
			d=int(c)+1
			webpagehit[b]=d

			bb=websiteunique.index(j)
			cc=websitesize[b]
			dd=int(cc)+int(list_size[i])
			websitesize[bb]=dd
	if option==1 or option==3:
		for i in range(len(websiteunique)):
			websitenamehit[websiteunique[i]]=webpagehit[i]
			websitenamesize[websiteunique[i]]=websitesize[i]
		sort_web=sorted( ((v,k) for k,v in websitenamesize.iteritems()), reverse=True)
		sort_web_hit=sorted( ((v,k) for k,v in websitenamehit.iteritems()), reverse=True)
		if option==1:
			if sort_web:
				return sort_web[0],sort_web_hit[0]
			else:
				return 0
		else:
			return sort_web,sort_web_hit
	
	elif option==2:
		for i in range(len(websiteunique)):
			websitenamehit1.append((websiteunique[i],webpagehit[i]))
			websitenamesize1.append((websiteunique[i],websitesize[i]))	
		return websitenamesize1,websitenamehit1
#-----------------------------------------------

#function to give unique values
def get_unique(list_data):
    dataunique=[]
    datano=[]
    datalist={}
    for i,j in enumerate(list_data):
        if list_data[i] not in dataunique:
            dataunique.append(list_data[i])
            datano.append(1)
        else:
            b=dataunique.index(j)
            c=datano[b]
            d=int(c)+1
            datano[b]=d

    for i in range(len(dataunique)):
        datalist[dataunique[i]]=datano[i]
    sort_data=sorted( ((v,k) for k,v in datalist.iteritems()), reverse=True)
    return sort_data
	
#--------------------------------------
#02-mar-2014 -->2014-3-2
def date_format(date):
	months={'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
	mon=months[date[3:6]]
	day=date[0:2]
	if day[0]=='0':
		day=day[1]
	fordate=date[7:11]+'-'+mon+'-'+day
	return fordate
#----------------------------------------
#2014-09-07 -->07-Sep-2014  
def dlist_format(date):
	months={'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
	mon=months[date[5:7]]
	day=date[8:10]
	fordate=day+'-'+mon+'-'+date[0:4]
	return fordate

#make chart
def pass_to_chart(list_data,list_hits,id,wid,hei,x,y,z):
	chart="""
	<style> 

.wrapper1, .wrapper2, .wrapper3, .wrapper4, .wrapper5, .wrapper6, .wrapper7, .wrapper8
{
	width:461px;
	height:380px;
	background-color:#b9c9fe;
	box-shadow: 10px 10px 5px #888888;
	margin-left: 40%;
	padding-left: 10px;
	padding-bottom: 10px;
}

.legend_chart {
    width: 19em;
    display: block;
    border: 1px solid black;
	position: relative;
	right: -140px;
	color: black;
	overflow: hidden;
}

.legend_chart .title_chart {
    display: block;
    margin: 0.5em;
    border-style: solid;
    border-width: 0em 0em 0em 1em;
	padding: 0 1.3em;
	height: 0.9em;
    font-size:89%;
	overflow: hidden;
}
.buttons_chart {
	margin-left: -10px;
	margin-top: 126px;
	position:relative;
	top:-60px;
}
</style>
<script src="../../js/Chart.js"></script>


</head>
<body onload="pie1();pie2();pie3();pie4();pie5();pie6();">

<div class="wrapper"""+id+"""">
	
	<canvas id="myChart"""+id+""""  style="width: 400px; height: 400px;margin-top:25px;margin-left: 45px;"></canvas>
	<div id="Legend"""+id+""""></div>
	<div class="buttons_chart" id="buttons"""+id+"""">
		<button onclick="pie"""+id+"""()"><img src="../../images/chart.png" height="25px" width="25px"/></button>
    	<button onclick="bar"""+id+"""()"><img src="../../images/chart_bar.png" height="25px" width="25px"/></button>
	</div>
</div>


<script type="text/javascript">
	var ctx"""+id+""" = document.getElementById("myChart"""+id+"""").getContext("2d");
	
	var sites"""+id+""" ="""+str(list_data)+"""; 
	var hits"""+id+""" = """+str(list_hits)+""";
	var color"""+id+""" = ['#5D8AA8','#E32636','#FFBF00','#8DB600','#FBCEB1','#7FFFD4','#98777B','#DE5D83','#FFEF00','#36454F'];

	

	function pie"""+id+"""() {
		
		var x= document.getElementById("myChart"""+id+"""");
		x.setAttribute("width",320);
		x.setAttribute("height",320);

		document.getElementById('myChart"""+id+"""').style.marginLeft = '60px';
		document.getElementById('buttons"""+id+"""').style.marginLeft = '474px';
		document.getElementById('buttons"""+id+"""').style.marginTop = '20px';
		

		var data = [];
        for (i = 0; i < """+str(len(list_data))+"""; i++) {
            var obj = {
                label: sites"""+id+"""[i],
                value : hits"""+id+"""[i],
                color: color"""+id+"""[i],
                title: sites"""+id+"""[i]
            };
            data.push(obj);
        }

		defaults = {
			animation : false
		}
		var myNewChart"""+id+""" = new Chart(ctx"""+id+""").Pie(data,defaults);
		
		document.getElementById("Legend"""+id+"""").innerHTML = "";
	    

	}
	
 	function bar"""+id+"""(){
		var x= document.getElementById("myChart"""+id+"""");
		x.setAttribute("width","""+wid+""");
		x.setAttribute("height","""+hei+""");
		
		document.getElementById('myChart"""+id+"""').style.marginLeft = '"""+x+"""';
		document.getElementById('buttons"""+id+"""').style.marginLeft = '"""+y+"""';
		document.getElementById('buttons"""+id+"""').style.marginTop = '"""+z+"""';
		
		

        var data = {
            labels : [],
            datasets : [
            {
                fillColor : [],
                strokeColor : ["black"],
                data : [],
                title: []
            }
            ]
        }

        
        for (i = 0; i < """+str(len(list_data))+"""; i++) {
            data.labels[i]=sites"""+id+"""[i];
            data.datasets[0].data[i]=hits"""+id+"""[i];
            data.datasets[0].fillColor[i]=color"""+id+"""[i];
            data.datasets[0].title[i]=sites"""+id+"""[i];
        }    

        defaults = {
			animation : false
		} 
        

        var myNewChart = new Chart(ctx"""+id+""").Bar(data,defaults);
	}
</script>
	"""
	return chart

#setting for top 10
def top10_set(list_data):

	count=0
	if len(list_data)<10:
		lent=len(list_data)
	else:
		lent=10
	return lent

#class for report generate
class ReportGenerate:
	def __init__(self,info,logs):
		self.info=info
		self.logs=logs

	def make_folder(self,loc,dateoption,datelist,bydate_datelist):
		if dateoption=="complete":
			for line in self.logs:
				m=log_re.search(line)
				if m:
					username=m.group('Username')
					logdate=m.group('Time')
				if logdate:
					dir1=loc+date_format(logdate)
					if not os.path.exists(dir1):
						os.mkdir(dir1)
					if username and username!='-':
						dir=loc+date_format(logdate)+'/'+username
						if not os.path.exists(dir):
							os.mkdir(dir)
		elif dateoption=="bydate":
			for line in self.logs:
				m=log_re.search(line)
				if m:
					username=m.group('Username')
					logdate=m.group('Time')
				
				if logdate:
					dire1=loc+date_format(logdate)
					if date_format(logdate) in bydate_datelist:
						if not os.path.exists(dire1):
							os.mkdir(dire1)
					if username and username!='-' and date_format(logdate) in bydate_datelist:
						dir=loc+date_format(logdate)+'/'+username
						if not os.path.exists(dir):
							os.mkdir(dir)
	
	def split_file(self,date_queue, user_queue,loc,bydate_datelist,dateoption):
		for date in date_queue:
			dire=date_format(date)
			for line in self.logs:
				if dateoption == "complete":
					if date[0:11] in line:
						datetxt = open(loc+dire+"/"+dire+".txt",'ab')
						datetxt.write(line)
						datetxt.write('\r\n')
						datetxt.close()
					if date[0:11] in line and date[0:11] in date_queue:
						for user in user_queue:
							if user in line:
								usertxt = open(loc+dire+"/"+user+"/"+user+".txt",'ab')
								usertxt.write(line)
								usertxt.write('\r\n')
								usertxt.close()
				if dateoption == "bydate":
					if date[0:11] in line and dire in bydate_datelist:
						datetxt = open(loc+dire+"/"+dire+".txt",'ab')
						datetxt.write(line)
						datetxt.write('\r\n')
						datetxt.close()
					if date[0:11] in line and dire in bydate_datelist:
						for user in user_queue:
							if user in line:
								usertxt = open(loc+dire+"/"+user+"/"+user+".txt",'ab')
								usertxt.write(line)
								usertxt.write('\r\n')
								usertxt.close()
				

	def homepage(self,datelist1,loc):
		color_code=['#5D8AA8','#E32636','#FFBF00','#8DB600','#FBCEB1','#7FFFD4','#98777B','#DE5D83','#FFEF00','#36454F']
		for date in datelist1:
			list_mime=[]
			list_http=[]
			list_prof=[]
			list_fap=[]
			list_user = []
			list_website =[]
			list_size=[]
			
			dire=date
			fn=loc+'/'+dire+"/"+dire+".txt"
			ofile=open(fn,'r')
			try:
				while 1:
					line = ofile.readline()
					if not line:
						break
					m=log_re.search(line)
					if m:
						username=m.group('Username')
						mimelist=m.group('Mime')
						httpstlist=m.group('Http_Status')
						profileapp=m.group('Profiles_Applied')
						filterapp=m.group('Filter_Name')
						weblist=m.group('Site')
						if weblist:
							list_website.append(weblist)
						if profileapp:
							list_prof.append(profileapp)
						if httpstlist:
							list_http.append(httpstlist)
						if mimelist and mimelist!='-':
							list_mime.append(mimelist)
						if filterapp and filterapp!='-':
							list_fap.append(filterapp)			  
						if username and username!='-':
							list_user.append(username)
			except Exception, e:
				print e

			indexhtml = open(loc+"/"+dire+"/index.html",'wb')
			header=header_set(1,'Homepage')
			indexhtml.write(header)
			#top 10 websites
			list_website_domain=[]
			for webs in list_website:
				index=webs.find(':')
				index_last=webs.find('/',index+3)
				list_website_domain.append(webs[0:index_last])
			
			websites=get_unique(list_website_domain)
			list_website_top10=[]
			count=0
			for i in websites:
				if count==top10_set(websites):
					break
				else:
					list_website_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example19:before {
		content:"Top 10 Websites";
		margin: 50px -10px;
		}
		</style>
		<div class="example19">
		<div class="message">""")
			list_web_pass=[] #websites
			list_web_hits_pass=[] # website's hits
			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>Website</th><th>Hits</th></tr>""")
			for j in range(len(list_website_top10)):
				list_web_pass.append(list_website_top10[j][1])
				list_web_hits_pass.append(list_website_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td><a href="""+str(list_website_top10[j][1])+""" target="_blank">"""+str(list_website_top10[j][1])+"""</a></td><td class='mintd'>"""+str(list_website_top10[j][0])+"""</td></tr>""")

			indexhtml.write("</table></div>")
			chart_print_web=pass_to_chart(list_web_pass,list_web_hits_pass,'6','650','600','-114px','474px','-258px')
			indexhtml.write(chart_print_web)

			indexhtml.write("</div></div>")
			indexhtml.write("<br>")
			#top 10 Users

			users=get_unique(list_user)
			list_user_top10=[]
			count=0
			for i in users:
				if count==top10_set(users):
					break
				else:
					list_user_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example20:before {
		content:"Top 10 Users";
		margin: 40px 0px;
		}
		</style>
		<div class="example20">
		<div class="message">""")
			list_user_pass=[]
			list_user_hits_pass=[]
			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>User</th><th>Hits</th></tr>""")
			for j in range(len(list_user_top10)):
				list_user_pass.append(list_user_top10[j][1])
				list_user_hits_pass.append(list_user_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td><a href=../../"""+loc+"/"+dire+"/"+list_user_top10[j][1]+"/"+list_user_top10[j][1]+".html"">"""+list_user_top10[j][1]+"""</a></td><td class='mintd'>"""+str(list_user_top10[j][0])+"""</td></tr>""")
			indexhtml.write("</table></div>")		
			chart_print=pass_to_chart(list_user_pass,list_user_hits_pass,'1','550','525','-80px','474px','-187px')
			indexhtml.write(chart_print)
			indexhtml.write("</div></div>")

			indexhtml.write("<br><br>")
				
			#top 10 Mime
			mimes=get_unique(list_mime)
			list_mime_top10=[]
			count=0
			for i in mimes:
				if count==top10_set(mimes):
					break
				else:
					list_mime_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example21:before {
		content:"Top 10 Mime";
		margin: 40px 0px;
		}
		</style>
		<div class="example21">
		<div class="message">""")
			list_mime_pass=[]
			list_mime_hits_pass=[]
			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>Mime</th><th>Hits</th></tr>""")
			for j in range(len(list_mime_top10)):
				list_mime_pass.append(list_mime_top10[j][1])
				list_mime_hits_pass.append(list_mime_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td>"""+list_mime_top10[j][1]+"""</td><td class='mintd'>"""+str(list_mime_top10[j][0])+"""</td></tr>""")
			indexhtml.write("""</table></div>""")
			chart_print_mime=pass_to_chart(list_mime_pass,list_mime_hits_pass,'2','500','475','-50px','474px','-135px')
			indexhtml.write(chart_print_mime)
			
			indexhtml.write("</div></div>")
			indexhtml.write("<br><br>")
			
			
			#top 10 Profiles
			list_prof1=[]
			for i in list_prof:
				list_pr=i.split(',')
				for j in list_pr:
					list_prof1.append(j)
						
			profiles=get_unique(list_prof1)
			list_prof_top10=[]
			count=0
			for i in profiles:
				if count==top10_set(profiles):
					break
				else:
					list_prof_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example22:before {
		content:"Top 10 Profiles";
		margin: 40px 0px;
		}
		</style>
		<div class="example22">
		<div class="message">""")
			list_prof_pass=[]
			list_prof_hits_pass=[]
			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>Profiles</th><th>Hits</th></tr>""")
							
			for j in range(len(list_prof_top10)):
				list_prof_pass.append(list_prof_top10[j][1])
				list_prof_hits_pass.append(list_prof_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td>"""+list_prof_top10[j][1]+"""</td><td class='mintd'>"""+str(list_prof_top10[j][0])+"""</td></tr>""")
			indexhtml.write("</table></div>")
			chart_print_prof=pass_to_chart(list_prof_pass,list_prof_hits_pass,'4','525','450','-54px','474px','-111px')
			indexhtml.write(chart_print_prof)
			indexhtml.write("</div></div>")
			indexhtml.write("<br><br>")
			
				
			#top 10 Filters
			list_filter=list_fap
			faps=get_unique(list_filter)
			list_fap_top10=[]
			count=0

			for i in faps:
				if count==top10_set(faps):
					break
				else:
					list_fap_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example23:before {
		content:"Top 10 Filters";
		margin: 40px 0px;
		}
		</style>
		<div class="example23">
		<div class="message">""")
			list_fap_pass=[]
			list_fap_hits_pass=[]
			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>Filters</th><th>Hits</th></tr>""")
			for j in range(len(list_fap_top10)):
				list_fap_pass.append(list_fap_top10[j][1])
				list_fap_hits_pass.append(list_fap_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td>"""+list_fap_top10[j][1]+"""</td><td class='mintd'>"""+str(list_fap_top10[j][0])+"""</td></tr>""")
			indexhtml.write("</table></div>")
			chart_print_fap=pass_to_chart(list_fap_pass,list_fap_hits_pass,'5','475','550','-100px','474px','-211px')
			indexhtml.write(chart_print_fap)
			indexhtml.write("</div></div>")
			indexhtml.write("<br><br>")
			
			#top 10 http status
			https=get_unique(list_http)
			list_http_top10=[]

			count=0
			for i in https:
				if count==top10_set(https):
					break
				else:
					list_http_top10.append(i)
				count = count +1
			indexhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example24:before {
		content:"Top 10 Staus";
		margin: 40px 0px;
		}
		</style>
		<div class="example24">
		<div class="message">""")
			list_http_pass=[]
			list_http_hits_pass=[]

			indexhtml.write("""<table class="box-table-a" style="width: 35%;"  border=2 id='rounded-corner'>
	                        <tr><th>Legend</th><th>Http Status</th><th>Name</th><th>Hits</th></tr>""")
			for j in range(len(list_http_top10)):
				list_http_pass.append(list_http_top10[j][1])
				list_http_hits_pass.append(list_http_top10[j][0])
				indexhtml.write("""<tr><td><span class="color_code" style="border-color:"""+str(color_code[j])+"""; border-style: solid;"></span></td><td>"""+list_http_top10[j][1]+"""</td><td>"""+STATUSCODES.get(int(list_http_top10[j][1]))+"""</td><td class='mintd'>"""+str(list_http_top10[j][0])+"""</td></tr>""")
			indexhtml.write("</table></div>")
			chart_print_http=pass_to_chart(list_http_pass,list_http_hits_pass,'3','400','350','0px','474px','-18px')
			indexhtml.write(chart_print_http)
			indexhtml.write("</div></div>")
			indexhtml.write("<br><br>")
			
			
	#-----------------------------------------------------------
	def top_website(self,datelist1):
		for date in datelist1:
			websiteslist = []
			websiteslist1 = []
			websitesize1= []
			websites = []
			websites1 = []
			
			dire=date
			fn=loc+'/'+dire+"/"+dire+".txt"
			ofile=open(fn,'r')
			try:
				while 1:
					line = ofile.readline()
					if not line:
						break
					m=log_re.search(line)
					if m:
						websites=m.group('Siteref')
						websites1=m.group('Site')
						if websites1:
							if websites:
								if websites!='-':
									websiteslist.append(websites)
								else:
									websiteslist1.append(websites1)
								websitesize=m.group('Size')
								websitesize1.append(websitesize)
			except Exception, e:
				print e					

			topwebhtml = open(loc+"/"+dire+"/topsite.html",'wb')
			
			top_web,top_web_hit=get_site(websiteslist,websitesize1,3)
			top_web_url,top_web_hit_url=get_site(websiteslist1,websitesize1,3)
			header=header_set(1,'Top Website')
			topwebhtml.write(header)
			topwebhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example2:before {
		content:"Top Web (By Bandwidth)";
		margin: 80px -50px;
		}
		</style>
		<div class="example2">
		<div class="message">""")
			topwebhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'>
	                        <tr><th>Website</th><th>Bandwidth</th></tr>""")
			for i in top_web:
				topwebhtml.write("""<tr><td><a href="""+i[1]+""" target="_blank">"""+i[1]+"""</a></td><td class='mintd'>"""+str(convertSize(i[0]))+"""</td></tr>""")
			topwebhtml.write("""</table><div id="pageNavPosition"></div></div>
					</div></div>""")
			topwebhtml.write("<br><br>")
			topwebhtml.write("""<div class="tab-container"><br> <br> <style>
			.example1:before {
			content:"Top Web (By Hits)";
			margin: 65px -25px;
			}
			</style>
			<div class="example1">
			<div class="message">""")
		
			topwebhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner1'><tr><th>Website</th><th>Hits</th></tr>""")
			
			top_web_hit_count=0
			for i in top_web_hit:
				topwebhtml.write("""<tr><td><a href="""+i[1]+""" target="_blank">"""+i[1]+"""</a></td><td>"""+str(i[0])+"""</td></tr>""")
			topwebhtml.write("""</table><div id="pageNavPosition1"></div></div></div></div>""")
			
			topwebhtml.write("""<div class="tab-container">
	        <br> <br>  
			<style>
		.example:before {
		content:"Top Web (By Hits)";
		margin: 110px -30px;
		}
		</style>
		<div class="example">
		<div class="message">""")
			topwebhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner2'><tr><th>Website</th><th>Hits</th></tr>""")
			for i in top_web_hit_url:
				topwebhtml.write("""<tr><td><a href="""+i[1]+""" target="_blank">"""+i[1]+"""</a></td><td>"""+str(i[0])+"""</td></tr>""")
				
			topwebhtml.write("""</table><div id="pageNavPosition2"></div></div></div></div>""")
			topwebhtml.write("""<script type="text/javascript"><!--
        var pager1 = new Pager('rounded-corner', 30); 
        pager1.init(); 
        pager1.showPageNav('pager1', 'pageNavPosition'); 
        pager1.showPage(1);

        var pager2 = new Pager('rounded-corner1', 30); 
        pager2.init(); 
        pager2.showPageNav('pager2', 'pageNavPosition1'); 
        pager2.showPage(1);

        var pager3 = new Pager('rounded-corner2', 30); 
        pager3.init(); 
        pager3.showPageNav('pager3', 'pageNavPosition2'); 
        pager3.showPage(1);
    //--></script>""")
			topwebhtml.write("""</body> </html>""")
	#-------------------------------------------------	
	#Top User

	def top_user(self,datelist1):

		for date in datelist1:
			userlist1=[]
			timelist=[]
			usersizelist=[]
			siteslist =[]
			profilelist=[]
			faplist=[]
			datelist1=[]
			
			dire=date
			fn=loc+'/'+dire+"/"+dire+".txt"
			ofile=open(fn,'r')
			try:
				while 1:
					line = ofile.readline()
					if not line:
						break
					m=log_re.search(line)
					if m:
						username=m.group('Username')
						usersize=m.group('Size')
						usertime=m.group('Elapsed_Time')
						if usertime:
							timelist.append(usertime)
						if usersize:
							usersizelist.append(usersize)
						if username:
							userlist1.append(username)
					else:
						pass
			except Exception, e:
				print e

			top_user,top_user_hit=get_site(userlist1,usersizelist,2)
			top_time,top_time_hit=get_site(userlist1,timelist,2)
			top_hits=get_unique(userlist1)

			topuserhtml = open(loc+"/"+dire+"/topuser.html",'wb')
			header=header_set(1, 'Top User')
			topuserhtml.write(header)

			topuserhtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example3:before {
		content:"Userlist(By Bandwidth)";
		margin: 70px -40px;
		}
		</style>
		<div class="example3">
		<div class="message">""")
			topuserhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'><tr><th>Username</th><th>Bandwidth</th><th>Hits</th><th>Total Time(hh:mm:ss)</th></tr>""")
			for i in range(len(top_user)):
				ss = (top_time[i][1]/1000) % 60
				mm = (top_time[i][1]/(1000 * 60)) % 60
				hh = (top_time[i][1]/(1000 * 60 * 60)) % 24
				bandwidthuser=convertSize(top_user[i][1])
				if top_user[i][0]!='-':
					topuserhtml.write("<tr><td><a href='"+str(top_user[i][0])+"/"+str(top_user[i][0])+".html'>"+str(top_user[i][0])+"</a></td><td>"+str(bandwidthuser)+"</td><td>"+str(top_hits[i][0])+"</td><td>"+str(str(hh)+":"+str(mm)+":"+str(ss))+"</td></tr>")
			topuserhtml.write("""<br> <br></table><div id="pageNavPosition"></div>""")
			topuserhtml.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				        		    //--></script>""")
			topuserhtml.close()
		
	#user html page
	def user_html(self,datelist1):
		
		for date in datelist1:
			dire=date
			fn=loc+'/'+dire+"/"+dire+".txt"
			ofile=open(fn,'r')
			userlist = []
			try:
				while 1:
					line = ofile.readline()
					if not line:
						break
					m=log_re.search(line)
					if m:			
						username=m.group('Username')
						if username:
							if username!='-' and username not in userlist:
								userlist.append(username)
					else:
						pass
			except Exception, e:
				print e					
			for user1 in userlist: 
				timelist=[]
				usersizelist=[]
				siteslist =[]
				profilelist=[]
				faplist=[]
				datelist1=[]
				mimelist = []
				ufile=open(loc+'/'+dire+'/'+user1+'/'+user1+'.txt','r')
				try:
					while 1:
						line = ufile.readline()
						if not line:
							break
						m=log_re.search(line)
						if m:
							usersize=m.group('Size')
							usertime=m.group('Elapsed_Time')
							websites=m.group('Siteref')
							websites1=m.group('Site')
							filterapp=m.group('Filter_Name')
							profileap=m.group('Profiles_Applied')
							datere=m.group('Time')
							mimere=m.group('Mime')
							if datere:
								datelist1.append(datere)
							if websites:
								if websites!='-':
									siteslist.append(websites)
								else:
									if websites1:
										siteslist.append(websites1)
										
							if profileap:
								profilelist.append(profileap)
					
							if filterapp and filterapp!='-':
								faplist.append(filterapp)
									
							if usertime:
								timelist.append(usertime)

							if usersize:
								usersizelist.append(usersize)
								
							if mimere and mimere!='-':
								mimelist.append(mimere)
						else:
							pass

				except Exception, e:
					print e
				
				
				total1=0
				for i in usersizelist:
					total1=total1+int(i)
				
				timetotal=0
				for i in timelist:
					timetotal=timetotal+int(i)
				
				list_prof=[]
				for i in profilelist:
					list_pr=i.split(',')
					for j in list_pr:
						if j!='-':
							list_prof.append(j)
				
				timehit=[]
				sort_filter=get_unique(faplist)
				sort_site=get_unique(siteslist)
				sort_profile=get_unique(list_prof)
				
				for i in datelist1:
					timehit.append(i[-8:-6])
				
				dataunique=[]
				depth = [[]]
				for i in range(24):
					depth.append([])
				depth1=[]
				for i,j in enumerate(siteslist):
					if siteslist[i] not in dataunique:
						dataunique.append(siteslist[i])
				for i in range(len(dataunique)):
					for j in range(24):
						depth[j].append(0)
						
				for i,j in enumerate(siteslist):
					if siteslist[i] in dataunique:
						b=dataunique.index(j)
						c=int(timehit[i])
						depth[c][b]=depth[c][b]+1

				ss1 = (timetotal/1000) % 60
				mm1 = (timetotal/(1000 * 60)) % 60
				hh1 = (timetotal/(1000 * 60 * 60)) % 24
				bandwidthuser1=convertSize(total1)
				
				userhtml = open(loc+"/"+dire+"/"+user1+"/"+user1+".html",'wb')
				header1=header_set(2, user1)
				userhtml.write(header1)
				userhtml.write("""<div class="tab-container" style= "width: 30%; margin-left: 35%;">
					        <br> <br>  
						<style>
						.example4:before {
						content:"UserDetails";
						margin: 25px 0px;
						}
						</style>
						<div class="example4">
						<div class="message" style= "color:black;">""")
				
				userhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'> <th>
						<b>Username : </b>"""+user1+"""<br>
						<b>Total Bandwidth :</b> """+str(bandwidthuser1)+"""<br>
						<b>Total time :</b> """+str(str(hh1)+":"+str(mm1)+":"+str(ss1))+"""<br></th></table>
						</div></div></div><br></center>""")
				userhtml.write("""<div class="tab-container">
					        <br> <br>  
						<style>
						.example5 {
						min-height: 250px;
						}
						.example5:before {
						content:"Website Hourly Details";
						margin: 85px -40px;
						}
						</style>
						<div class="example5">
						<div class="message">""")	
				userhtml.write("""
						<table border=2 class='box-table-a' id='rounded-corner'>
						<caption><font size='4'><b>"""+dire+"""</b></font></caption>
						<tr><th>Website</th>
						""")
				for i in range(24):
					if len(str(i))==1:
						userhtml.write("<th style='width:20px;text-align:center;'>0"+str(i)+"</th>")
					else:
						userhtml.write("<th style='width:20px;text-align:center;'>"+str(i)+"</th>")
				userhtml.write("</tr>")

				for i in range(len(dataunique)):
					userhtml.write("""<tr><td><a href="""+str(dataunique[i])+""" target="_blank">&nbsp;&nbsp;"""+str(dataunique[i])+"""&nbsp;&nbsp;""</a></td>""")
					for j in range(24):
						userhtml.write("<td style='text-align:center; overflow: hidden; white-space: nowrap;'>"+str(depth[j][i])+"</td>")
						if j==23:
							userhtml.write("</tr>")
					userhtml.write("</tr>")
				userhtml.write("</table></div></div></div>")
				userhtml.write("<br><br>")
				
				if sort_profile:
					userhtml.write("""<div class="tab-container">
						        <br> <br>  
							<style>
							.example6 {
							min-height: 250px;
							}
							.example6:before {
							content:"Profile by Hits";
							margin: 50px -10px;
							}
							</style>
							<div class="example6">
							<div class="message">""")
					userhtml.write("""
						<table border=2 class='box-table-a' id='rounded-corner'>
						<tr><th>Profile</th><th>Hits</th></tr>
						""")
					for i in sort_profile:
						userhtml.write("<tr><td>"+str(i[1])+"</td><td>"+str(i[0])+"</td></tr>")
					userhtml.write("</table></div></div></div>")
				else:
					userhtml.write("<b>No Profiles</b>")
				userhtml.write("<br><br>")

				test=get_site(siteslist,usersizelist,1)
				if test!=0:
					userhtml.write("""<div class="tab-container">
						        <br> <br>  
							<style>
							
							.example7:before {
							content:" Top Web BW";
							margin: 30px 0px;
							}
							</style>
							<div class="example7">
							<div class="message">""")
					userhtml.write("""
						<table border=2 class='box-table-a' id='rounded-corner'>
					<tr><th>Website</th><th>Bandwidth</th></tr>
					<tr><td><a href="""+test[0][1]+""" target="_blank">"""+test[0][1]+"""</a></td><td>"""+str(convertSize(test[0][0]))+"""</td></tr>
					</table></div></div></div>
					<br><br>""")
					
					userhtml.write("""<div class="tab-container">
					        <br> <br>  
						<style>
						
						.example8:before {
						content:" Top Web hits";
						margin: 30px 0px;
						}
						</style>
						<div class="example8">
						<div class="message">
						<table border=2 class='box-table-a' id='rounded-corner'><tr><th>Website</th><th>Hits</th></tr>
					<tr><td><a href="""+test[1][1]+""" target="_blank">"""+test[1][1]+"""</a></td><td>"""+str(test[1][0])+"""</td></tr>
					</table></div></div></div>""")
						
				userhtml.write("<br><br>")
				
				sort_filter=get_unique(faplist)
				if sort_filter:
					userhtml.write("""<div class="tab-container">
					        <br> <br>  
						<style>
						.example9:before {
						content:"Filters by Hits";
						margin: 50px -10px;
						}
						</style>
						<div class="example9">
						<div class="message">""")
					userhtml.write("""
							<br><br>
						<table border=2 class='box-table-a' id='rounded-corner'><tr><th>Filters</th><th>Hits</th></tr>""")
					for i in sort_filter:
						userhtml.write("<tr><td>"+i[1]+"</td><td>"+str(i[0])+"</td></tr>")
					userhtml.write("</table> </div></div></div>")
				else:
					userhtml.write("<b>No Filters</b>")

				userhtml.write("<br><br>")
				sort_mime=get_unique(mimelist)
				if sort_mime:
					userhtml.write("""<div class="tab-container">
					        <br> <br>  
						<style>
						.example10:before {
						content:"Mime by Hits";
						margin: 30px 0px;
						}
						</style>
						<div class="example10">
						<div class="message">""")
					userhtml.write("""<table border=2 class='box-table-a' id='rounded-corner'>
							<tr><th>Mime</th><th>Hits</th></tr>""")
					for i in sort_mime:
						userhtml.write("<tr><td>"+i[1]+"</td><td>"+str(i[0])+"</td></tr>")
					userhtml.write("</table> </div> </div> </div>")
				else:
					userhtml.write("<b>No Mime</b>")
				userhtml.write('<br> <br> <//div> </body></html>')
				userhtml.close()
	#-------------------------------------------------		
	#mime html
	def mime_info(self,datelist1):
		
		for date in datelist1:
			list_mime=[]
			size_mime=[]
			mimesizelist=[]
			dire=date
			fn=loc+'/'+dire+'/'+dire+'.txt'
			ofile=open(fn,'r')
			ab=[]
			try:
				while 1:
					line = ofile.readline()
					ab.append(line)
					if not line:
						break
					m=log_re.search(line)
					if m:
						mimelist=m.group('Mime')
						userlist1=m.group('Username')
						if mimelist and userlist1:
							if mimelist!='-' and userlist1!='-':
								list_mime.append(mimelist)
							usersize=m.group('Size')
							if usersize:
								mimesizelist.append(usersize)
					else:
						pass
			except Exception, e:
				print e
			
			mimehtml = open(loc+"/"+dire+"/mime.html",'wb')
			header=header_set(1,'Mime')
			mimehtml.write(header)
			mimehtml.write("""<div class="tab-container">
				        <br> <br>  
					<style>
					.example11:before {
					content:"Mime By Bandwidth";
					margin: 65px -30px;
					}
					</style>
					<div class="example11">
					<div class="message">""")
			mimehtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'>
	                        <tr><th>Mime</th><th>No of times</th><th>Bandwidth</th></tr>""")
							
			mime_band,mime_hit=get_site(list_mime,mimesizelist,3)
			for i in range(len(mime_band)):
				mimehtml.write("<tr><td><a href=../../"+loc+"/"+dire+"/Mime/"+mime_band[i][1].replace("/", "-")+".html>"+mime_band[i][1]+"</a></td><td>"+str(mime_hit[i][0])+"</td><td>"+str(convertSize(mime_band[i][0]))+"</td></tr>")
			mimehtml.write("</table></div></div>")
			mimehtml.close()
			
			
			if not os.path.exists(loc+"/"+dire+"/Mime"):
				os.mkdir(loc+"/"+dire+"/Mime")
				
			for mime_type in list_mime:
				usernamelist = []
				mime_typehtml= open(loc+"/"+dire+"/Mime/"+mime_type.replace("/", "-")+".html",'wb')
				header1=header_set(2, mime_type.replace("/", "-"))
				mime_typehtml.write(header1)
				mime_typehtml.write("""<div class="tab-container">
				        <br> <br>  
					<style>
					.example12:before {
					content:"User-Site MIME";
					margin: 55px -20px;
					}
					</style>
					<div class="example12">
					<div class="message">""")
				
				mime_typehtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'><tr><th>Username</th><th>Websites</th></tr>""")
				for line1 in ab:
					if mime_type in line1:
						m=log_re.search(line1)
						if m:
							username=m.group('Username')
							if username:
								if username!='-':
									if username not in usernamelist:
										usernamelist.append(username)
				mimedict={}
				for user1 in usernamelist:
					websiteslist=[]
					ufile=open(loc+'/'+dire+'/'+user1+'/'+user1+'.txt','r')
					try:
						while 1:
							line2 = ufile.readline()
							if not line2:
								break
							m=log_re.search(line2)
							if m:
								if mime_type in line2:
									websites=m.group('Siteref')
									websites1=m.group('Site')
									if websites1:
										if websites:
											if websites!='-':
												if websites not in websiteslist:
													websiteslist.append(websites)
											else:
												if websites1 not in websiteslist:
													websiteslist.append(websites1)
								mimedict[user1]=websiteslist
							else:
								pass
					except Exception, e:
						print e
				a=0
				
				for i,j in mimedict.iteritems():
					mime_typehtml.write("""<tr><td><a href="../"""+i+"""/"""+i+""".html">"""+i+"""</a></td><td>""")
					for web in j:
						if a==len(j)-1:
							mime_typehtml.write(web+"<br>")
						else:
							mime_typehtml.write(web+"<br><hr>")
						a=a+1
					mime_typehtml.write("""</td></tr>""")
				mime_typehtml.write("""</table></div></div></div>""")
				mime_typehtml.close()
				


	def filter_applied(self,datelist1):
		
		for date in datelist1:
			faplist=[]
			faplist1=[]
			dire=date
			fn=loc+'/'+dire+'/'+dire+'.txt'
			if not os.path.exists(loc+"/"+dire+"/Filter"):
				os.mkdir(loc+"/"+dire+"/Filter")
			ofile=open(fn,'r')
			ad=[]
			try:
				while 1:
					line = ofile.readline()
					ad.append(line)
					if not line:
						break
					m=log_re.search(line)
					if m:
						filterre=m.group('Filter_Name')
						ulist=m.group('Username')
						slist=m.group('Siteref')
						if filterre and ulist and slist:
							if filterre!='-' and ulist!='-' and slist!='-':
								if filterre not in faplist:
									faplist.append(filterre)
			except Exception, e:
				print e						
			list_filter=faplist
			filterhtml = open(loc+"/"+dire+"/filters.html",'wb')
			header=header_set(1, 'Filters Applied')
			filterhtml.write(header)
			filterhtml.write("""<div class="tab-container">
				        <br> <br>  
					<style>
					.example13:before {
					content:"Filters";
					margin: 20px 20px;
					}
					</style>
					<div class="example13">
					<div class="message">""")
			filterhtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'>
	                        <tr><th>Filter Name</th><th>Filter Reason</th></tr>""")
			filterhtml.write("<tr>")
			for i in range(len(list_filter)):
				list_reason=[]				
				filterhtml.write("<td>"+list_filter[i]+"</td><td>")				
				for line in ad:
					if list_filter[i] in line:
						m=log_re.search(line)
						if m:
							reason=m.group('Filter_Reason')
							ulist=m.group('Username')
							slist=m.group('Siteref')
							if reason and ulist and slist:
								if reason not in list_reason:
									list_reason.append(reason)
				for j in list_reason:
					fi=list_filter[i]+"-"+j
					fi1=list_filter[i]+" "+j
					faplist1.append(fi1)
					filterhtml.write("<a href=../../"+loc+"/"+dire+"/Filter/"+fi.replace("/", "-").replace(" ", "-")+".html>"+str(j)+"</a><br><hr>")
				filterhtml.write("</td></tr>")
			filterhtml.write("""</table><div id="pageNavPosition"></div></div>""")
			filterhtml.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				        		    //--></script>""")
			filterhtml.close()
			
			
			for fil in faplist1:
				usernamelist = []
				fil1=fil
				filter_html= open(loc+"/"+dire+"/Filter/"+fil.replace("/", "-").replace(" ", "-")+".html",'wb')
				header1=header_set(2, fil.replace("/", "-").replace(" ", "-"))
				filter_html.write(header1)
				filter_html.write("""<div class="tab-container">
				        <br> <br>  
					<style>
					.example14:before {
					content:"User by Website";
					margin: 50px -20px;
					}
					</style>
					<div class="example14">
					<div class="message">""")
				filter_html.write("""<table class="box-table-a"  border=2 id='rounded-corner'><tr><th>username</th><th>websites</th></tr>""")
				
				for line1 in ad:
					
					if fil1 in line1:
						m=log_re.search(line1)
						if m:
							username=m.group('Username')
							websites=m.group('Siteref')
							websites1=m.group('Site')
							if username and websites and websites1:
								if username!='-':
									if username not in usernamelist:
										usernamelist.append(username)
				
				filter_html.write("""<tr>""")
				for user1 in usernamelist:
					filter_html.write("""<td><a href="../"""+user1+"""/"""+user1+""".html">"""+user1+"""</a></td> """)
					websiteslist=[]
					ufile=open(loc+'/'+dire+'/'+user1+'/'+user1+'.txt','r')
					try:
						while 1:
							line = ufile.readline()
							if not line:
								break
							if fil1 in line:
								m=log_re.search(line)
								if m:
									websites=m.group('Siteref')
									websites1=m.group('Site')
									if websites1:
										if websites:
											if websites!='-':
												if websites not in websiteslist:
													websiteslist.append(websites)
											else:
												if websites1 not in websiteslist:
													websiteslist.append(websites1)
					except Exception, e:
						print e		
					filter_html.write("""<td>""")
					a=0
					for website in websiteslist:
						if a==len(websiteslist)-1:
							filter_html.write(website+"<br>")
						else:
							filter_html.write(website+"<br><hr>")
						a=a+1
					filter_html.write("""</td></tr>""")
				filter_html.write("""</table><div id="pageNavPosition">""")
				filter_html.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				        		    //--></script>""")
				filter_html.close()


	def security_breach(self,datelist1):

		for date in datelist1:
			statuscode=[]
			dire=date
			fn=loc+'/'+dire+"/"+dire+".txt"
			ofile=open(fn,'r')
			ab=[]
			try:
				while 1:
					line = ofile.readline()
					ab.append(line)
					if not line:
						break
					m=log_re.search(line)
					if m:
						stucode=m.group('Http_Status')
						if stucode:
							if stucode=='403' or stucode=='407':
								if stucode not in statuscode:
									statuscode.append(stucode)
			except Exception, e:
				print e
			testuser=[]
			blackhtml = open(loc+"/"+dire+"/blacklist.html",'wb')
			header=header_set(1, 'Security Breach')
			blackhtml.write(header)
				
			for i in statuscode:
				if i=='403':
					id1="rounded-corner"
					id2="pageNavPosition"
					blackhtml.write("""<div class="tab-container">
				<br> <br>  <style type="text/css">
						.example15:before{
						content: "Forbidden";
						margin: 40px 0px; 
						}</style><br><br><div class= "example15"> <div class="message">""")
						
				elif i=='407':
					id1="rounded-corner1"
					id2="pageNavPosition1"
					blackhtml.write("""<div class="tab-container">
				<br> <br>  <style type="text/css">
						.example18:before{
						content: "Proxy Authentication";
						margin: 60px -35px; 
						}
						.example18{
						min-height: 200px;
						}
						.box-table-a
						{margin: 20px 10px;
						}
						</style><br><br><div class= "example18"> <div class="message">""")
				blackhtml.write("<table class='box-table-a'  border=2 id="+id1+">")
				blackhtml.write("<tr><th valign='top'>Username</th><th valign='top' style='word-wrap:break-word;'>Websites</th></tr>")
				#print statuscode[i]
				user_list_b=[]
				for line in ab:
					if " "+i+" " in line:
						m=log_re.search(line)
						if m:
							username=m.group('Username')
							if username and username!='-' and username not in user_list_b :
								user_list_b.append(username)
							
				blackhtml.write("<tr>")
				for u in user_list_b:
					blackhtml.write("""<td word-wrap: style='normal;word-break: normal;'><a href="""+str(u)+"""/"""+str(u)+""".html>"""+str(u)+"""</a></td>""")
					websiteslist=[]
					ufile=open(loc+'/'+dire+'/'+u+'/'+u+'.txt','r')
					try:
						while 1:
							line1 = ufile.readline()
							if not line1:
								break
							m=log_re.search(line1)
							if m:
								x=" "+i+" "
								if x in line1:
									websites=m.group('Siteref')
									websites1=m.group('Site')
									if websites1:
										if websites:
											if websites!='-':
												if websites not in websiteslist:
													websiteslist.append(websites)
											else:
												if websites1 not in websiteslist:
													websiteslist.append(websites1)
					except Exception, e:
						print e
					blackhtml.write("<td valign='top' style='word-wrap:break-word;'>")
					a=0
					for web in websiteslist:
						if a==len(websiteslist)-1:
							blackhtml.write(web+"<br>")
						else:
							blackhtml.write(web+"<br><hr>")
						a=a+1
					blackhtml.write("</td></tr>")
				blackhtml.write("""</table> <div id="""+id2+"""></div></div></div></div>""")
				blackhtml.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				        var pager2 = new Pager('rounded-corner1', 30); 
				        pager2.init(); 
				        pager2.showPageNav('pager2', 'pageNavPosition1'); 
				        pager2.showPage(1);
								    //--></script>""")
			blackhtml.close()
			
	def profile_applied(self,datelist1):

		for date in datelist1:
			profilelist=[]
			dire=date
			fn=loc+'/'+dire+'/'+dire+'.txt'
			if not os.path.exists(loc+"/"+dire+"/Profile"):
				os.mkdir(loc+"/"+dire+"/Profile")
			ofile=open(fn,'r')
			prohtml = open(loc+"/"+dire+"/profiles.html",'wb')
			header=header_set(1, 'Profiles')
			prohtml.write(header)
			prohtml.write("""<div class="tab-container">
	        <br> <br>  
		<style>
		.example17:before {
		content:"Profiles";
		margin: 20px 15px;
		}
		</style>
		<div class="example17">
		<div class="message"> """)
			prohtml.write("""<table class="box-table-a"  border=2 id='rounded-corner'>
	                        <tr><th>Profiles</th></tr>""")
			ab=[]
			try:
				while 1:
					line = ofile.readline()
					ab.append(line)
					if not line:
						break
					m=log_re.search(line)
					if m:			
						paplist=m.group('Profiles_Applied')
						ulist=m.group('Username')
						if paplist and ulist:
							if ulist!='-'and paplist!='- -':
								if paplist not in profilelist:
									profilelist.append(paplist)
			except Exception, e:
				print e
			list_prof=[]
			for i in profilelist:
				list_pr=i.split(',')
				for j in list_pr:
					if j not in list_prof:
						list_prof.append(j)
		 				
			for i in list_prof:
				prohtml.write("<tr><td><a href='../../"+loc+"/"+dire+"/profile/"+i+".html'>"+ str(i) +"</a></td></tr>")
			prohtml.write("""</table> <div id="pageNavPosition"></div></div> </div> </div>""")
			prohtml.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				    //--></script>""")
			prohtml.close()
										
			for profile in list_prof:
				userlist=[]
				pap_html= open(loc+"/"+dire+"/Profile/"+profile+".html",'wb')
				header1=header_set(2, profile)
				pap_html.write(header1)
				pap_html.write("""<div class="tab-container">
				        <br> <br>  
					<style>
					.example16:before {
					content:"User for Profile";
					margin: 55px -15px;
					}
					</style>
					<div class="example16">
					<div class="message"> """)
				pap_html.write("""<table class="box-table-a"  border=2 id='rounded-corner'><tr><th>Username</th><th>Websites</th></tr>""")
				for line in ab:
					if profile in line:
						m=log_re.search(line)
						if m:
							ulist=m.group('Username')
							if ulist:
								if ulist not in userlist and ulist!='-':
									userlist.append(ulist)
				
				for user1 in userlist:
					pap_html.write("""<tr><td style= 'overflow: hidden; white-space: nowrap;'><a href="../"""+user1+"""/"""+user1+""".html">"""+user1+"""</a></td> """)
					user_web=[]
					ufile=open(loc+'/'+dire+'/'+user1+'/'+user1+'.txt','r')
					try:
						while 1:
							line1 = ufile.readline()
							if not line1:
								break
							m=log_re.search(line1)
							if m:
								if profile in line1:
									websites=m.group('Siteref')
									websites1=m.group('Site')
									if websites1:
										if websites:
											if websites!='-':
												if websites not in user_web:
													user_web.append(websites)
											else:
												if websites1 not in user_web:
													user_web.append(websites1)
					except Exception, e:
						print e
					pap_html.write("""<td>""")
					a=0
					for website in user_web:
						if a==len(user_web)-1:
							pap_html.write(website+"<br>")
						else:
							pap_html.write(website+"<br><hr>")
						a=a+1
					pap_html.write("""</td></tr>""")
				pap_html.write("""</table><div id="pageNavPosition"></div></div></div>""")
				pap_html.write("""<script type="text/javascript"><!--
				        var pager1 = new Pager('rounded-corner', 30); 
				        pager1.init(); 
				        pager1.showPageNav('pager1', 'pageNavPosition'); 
				        pager1.showPage(1);
				    //--></script>""")
				pap_html.close()
			

					
#Main---------------								
def main():
	global datelist
	global userlist
	global logfile
	global loc
	global timelist
	global usersizelist

	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "</head>"
	print "<body>"

	bydate_datelist=[]
	form = cgi.FieldStorage() 
	config = ConfigParser.ConfigParser()
	
	filename="conf.ini"
	
	if os.path.exists(filename):
		config.read("conf.ini")
		logfile=config.get("report", "log_file_location")
		loc=config.get("report", "output_location")

		dirRep=loc
		if not os.path.exists(dirRep):
			os.mkdir(dirRep)

		ofile=open(logfile,'r')
		logs=[]
		try:
			while 1:
				line = ofile.readline()
				logs.append(line)
				if not line:
					break
				m=log_re.search(line)
				if m:
					date=m.group('Time')
					
					if date[0:11] not in datelist:
						datelist.append(date[0:11])
					username=m.group('Username')
					if username not in userlist and username!='-':
						userlist.append(username)
				else:
					pass
		except Exception, e:
			print e

		dateoption = form.getvalue('select')

		if dateoption=="bydate":
			fromdate=form.getvalue('from')
			todate=form.getvalue('to')
			selection(dateoption,fromdate,todate)
			temp=[]
			temp1=[]
			for i in dlist:
				date_temp=dlist_format(i)
				temp.append(date_temp)
				date_temp1=date_format(dlist_format(i))
				temp1.append(date_temp1)
			datelist_test=temp
			bydate_datelist=temp1

		reportobj=ReportGenerate('ReportGenerate',logs)

		reportobj.make_folder(loc+'/',dateoption,datelist,bydate_datelist)
		reportobj.split_file(datelist,userlist,loc+'/',bydate_datelist,dateoption)
		datelist1=os.listdir(loc+'/')
		
		reportobj.homepage(datelist1,loc)
		reportobj.top_website(datelist1)
		reportobj.top_user(datelist1)
		reportobj.user_html(datelist1)
		reportobj.mime_info(datelist1)
		reportobj.filter_applied(datelist1)
		reportobj.security_breach(datelist1)
		reportobj.profile_applied(datelist1)

		calender_file(datelist1,loc) 
		delete_files(loc+'/')
		print "Successfully generated reports....Visit <a href='http://localhost:8000/cgi-bin/view.py'> View </a> to see reports..."
		
	else:
		print "Please visit  <a href='http://localhost:8000/settings.html'>Settings</a> Page as you have not saved settings :) <br> Come back after saving settings"
	
#----------------------------------------------------------------

			
main()
	

