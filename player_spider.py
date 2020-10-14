import scrapy


class PlayerSpider(scrapy.Spider):
    name = "Player"
    baseurl = 'https://fbref.com'
    # start_urls= ['https://fbref.com/en/players/6025fab1/all_comps']

    # Comment this function and uncomment start_urls to test for one player
    def start_requests(self):
        yield scrapy.Request(url = self.baseurl+'/en/comps', callback=self.getleagueurl)

    def getleagueurl(self , response):
        url=self.scrapeurl('La Liga',response)
        yield scrapy.Request(url=self.baseurl+url , callback=self.getseasonurl)

    def getseasonurl(self , response ):
        url=self.scrapeurl('2020-2021',response)
        yield scrapy.Request(url=self.baseurl+url , callback=self.getteamurls)

    def scrapeurl(self ,s,response):
        comps_tables = response.css('table')
        for a in comps_tables:
            for b in a.css('a'):
                if b.css('a::text').get()==s:
                    return b.css('a::attr(href)').get()

    def getteamurls(self , response):
        self.log("Reached team urls")
        self.log(response.url)
        td = response.css('table')[0].css('td[data-stat="squad"]')
        for i in td:
            a=i.css('a::attr(href)')
            yield response.follow(a.get(), callback=self.getplayerurl)

    def getplayerurl(self , response):
        
        self.log(response.url)
        th = response.css('table')[0].css('th[data-stat="player"][scope="row"]')
        for i in th:
            a = i.css('a::attr(href)')
            url=a.get()
            if(url=="" or url==None):
                continue
            x=url.split('/')
            url='/'+x[1]+'/'+x[2]+'/'+x[3]
            # self.log("url="+url)
            yield response.follow(url+'/all_comps/', callback=self.parse)
    


    
    # This is the main function that scrapes the player data
    def parse(self , response):
        playerdata={}

        playerdata['name']=response.css('h1[itemprop="name"] span').css('span::text').get()


        # Get standard stat table using its identifier
        standard_stats=self.getlast3seasonrows(response , '#div_stats_standard_ks_collapsed tbody' )

        features=['goals_per90','assists_per90','goals_assists_pens_per90']

        # Puts the feature and their value in player data object
        self.getfeaturevals( standard_stats , features ,playerdata)
        


        yield playerdata

    
    # Helper functions for parse function
    def getfeaturevals(self,table , features , playerdata):
        for feature in features:
            playerdata[feature]=[]
            for row in table:
                
                val=row.css('td[data-stat="{0}"]'.format(feature)).css('td::text').get()
                # val=float(val)
                playerdata[feature].append(val)


    def getlast3seasonrows(self,response , id):
        # Get  stat table using its identifier
        stat_table=response.css(id)
        # self.log(stat_table.get())
        # self.log(response.css('body').get())
        rows=stat_table.css('tr')

        #Getting last 3 rows
        return rows[-3:]
