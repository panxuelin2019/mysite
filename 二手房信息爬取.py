#从www.szhome.com上抓取二手房信息

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import xlwt  #EXCEL
import time
from datetime import datetime

begin_time = time.time()

#style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
#style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
wb = xlwt.Workbook()
ws = wb.add_sheet('二手房信息')

#写入EXCEL标题行
n_column = 0
ws.write(0,n_column, '序号'); n_column += 1
ws.write(0,n_column, '房源'); n_column += 1
ws.write(0,n_column, '户型'); n_column += 1
ws.write(0,n_column, '面积(㎡)'); n_column += 1
ws.write(0,n_column, '朝向'); n_column += 1
ws.write(0,n_column, '装修/毛坯'); n_column += 1
ws.write(0,n_column, '楼层'); n_column += 1
ws.write(0,n_column, '单价(元/㎡)'); n_column += 1
ws.write(0,n_column, '总价(万元)'); n_column += 1
ws.write(0,n_column, '网址'); n_column += 1

#深圳市房地产信息网二手房信息
base_url = "http://zf.szhome.com/Search.html?sor=1&aom=1&kwd=&xzq=0&pq=0&price=0&prif=0&prit=0&barea=0&baf=0&bat=0&hx=0&ord=0&dtyx=0&dtst=0&scat=0&sx=0&schid=0&page="
page_num = 1

n_line = 1

while True:
    url = base_url + '%d'%page_num
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    houses = soup.find_all("div", {"class": "lpinfo"})
    
    if houses == []:
        break

    print('开始抓取第%d页数据...'%page_num)
        
    for house in houses:
        n_column = 0
        
        ws.write(n_line, n_column, n_line) #写入序号
        n_column += 1
    
        #写入房源名称
        ws.write(n_line, n_column, house.a['title'])
        n_column += 1

        #房源基础信息(几房、面积、南北通透、楼层等)
        for info in house.find_all("span", class_="mr10"):            
            text = info.get_text()
            text = text.replace('m²','') #去掉单位㎡
            ws.write(n_line, n_column, text)
            n_column += 1

        #房源价格（单价）   
        for info in house.find_all("p", class_="f14"):
            ws.write(n_line, n_column, info.get_text())
            n_column += 1
        
        #房源价格（总价）   
        for info in house.find_all("span", class_="red f20"):
            ws.write(n_line, n_column, info.get_text())
            n_column += 1

        
        #房源URL
        str_url = 'zf.szhome.com' + house.a['href']
#        ws.write(n_line, n_column, xlwt.Formula('HYPERLINK'+'("'+str_url+'";"'+"深圳房地产学信网" + '")')))
        ws.write(n_line, n_column, str_url)
        
        n_column += 1      
            
        n_line += 1
    
    page_num += 1
        
#爬取的网页信息写入EXCEL文件
#now = datetime.now()
filename = 'SZHOME.COM二手房源信息' + time.strftime("%Y-%m-%d", time.localtime()) + '.xls'
wb.save(filename)

#summary
print('')

print('网页数据抓取完毕，共抓取二手房源信息%d条，耗时：%.1f...'%(n_line, (time.time()-begin_time)))




"""
抓取信息格式如下：
<div class="lpinfo">
	<a class="imgbox" href="/sell/409436.html" target="_blank" title="德兴大厦">
		<div class="txtbox">
			<i></i>
			<p class="text white">
				<span class="esf-icon14"></span>6
			</p>
		</div>
		<img alt="德兴大厦" src="http://dongdong.szhomeimg.com/HouseImage/thumb/2019/08/08241940046714951.jpg"/>
	</a>
	
	<div class="mianbox">
		<a class="tit" href="/sell/409436.html" target="_blank" title="德兴大厦">8月25新上，装修保养好，9号线+1号线，月供7千不到</a>
		
		<div class="fix">
			<div class="left esf-info">
				<p>
					<a href="/community/detail/1274.html" style="color:#808080;" target="_blank">德兴大厦 - 罗湖区建设路1046号</a>
				</p>
				<p>
					<span class="mr10">二房</span>|
					<span class="mr10 ml10">38m²</span>|
					<span class="mr10 ml10">南</span>|
					<span class="mr10 ml10">精装修</span>|
					<span class="mr10 ml10">15/30层</span>
				</p>
				
				<p>
					<a class="mr10 blue-14" href="/userdetail/3070210.html" target="_blank">罗丽容</a>
					<span class="mr25">Q房网人民南加盟店</span>
					<span>1分钟前更新</span>
				</p>
			</div>
			
			<div class="right esf-pri">
				<p class="f16 red-fe">
					<strong class="f22">
						<span class="red f20">165</span>
					</strong>万
				</p>
				<p class="f14" name="sYuanM">43421 元/㎡</p>
			</div>
		</div>
		
		<div class="esfkeywords">
			<span>近地铁</span>
			<span>红本在手</span>
			<span>证满5年</span>		
		</div>
	</div>
</div>

"""