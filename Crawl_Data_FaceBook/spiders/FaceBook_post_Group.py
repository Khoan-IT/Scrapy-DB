from operator import pos
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json
from Crawl_Data_FaceBook.items import CrawlData

Customer_Id = ['100056799280787']
Group_Id = ['606213853219261', '149680169049858', '1183923128403731', '244049526220617']

class FacebookPostGroupSpider(scrapy.Spider):
    name = 'FaceBook_post_Group'
    def __init__(self, scrolls='', the_uuid='', user_id='', **kwargs):
        self.scrolls = scrolls
        self.user_id = user_id
        self.the_uuid = the_uuid
        super().__init__(**kwargs)

    # This will setup settings variable to get constant from settings.py

    settings = get_project_settings()

    xpath_view_more_info = "text_exposed_hide"
    # Lua script to interact with js in the website while crawling

    
    def start_requests(self):

        script_link = """
                function main(splash, args)
                    splash:init_cookies(splash.args.cookies)
                    assert(splash:go{
                        splash.args.url,
                        headers=splash.args.headers
                    })
                    assert(splash:wait(5))
                    splash:set_viewport_full()
                    local scroll_to = splash:jsfunc("window.scrollTo")
                    local get_body_height = splash:jsfunc(
                        "function() {return document.body.scrollHeight;}"
                    )
                    for _ = 1, 2 do
                        scroll_to(0, get_body_height())
                        assert(splash:wait(1))
                    end 
                    
                    assert(splash:wait(5))

                    local divs = splash:select_all("div[class='""" + self.xpath_view_more_info + """']")
                    for _, _ in ipairs(divs) do
                        local _div = splash:select("div[class='""" + self.xpath_view_more_info + """']")
                        if _div ~= nil then
                            assert(_div:mouse_click())
                        end
                    end
                    
                    local entries = splash:history()
                    local last_response = entries[#entries].response

                    return {
                        cookies = splash:get_cookies(),
                        headers = last_response.headers,
                        html = splash:html(),
                        url = splash.url()
                    }
                end
            """


        # Send splash request with facebook cookie and lua script to check if cookie is logged in or not
        with open('./cookies/cookie_1.json', 'r') as jsonfile:
            cookies = json.load(jsonfile)["cookies"]
               
        with open('./homepage/html/homepage_BDS.html', 'w+') as out:
            out.write('')
            #Lấy list id 
        for g_id in Group_Id:
            yield SplashRequest(
                url="https://m.facebook.com/profile.php?id={}&groupid={}".format(Customer_Id[0], g_id),
                callback=self.parse,
                session_id="test",
                meta={
                    "splash": {
                        "endpoint": "execute", 
                        "args": {
                            "lua_source": script_link,
                            "cookies": cookies,
                            "timeout":3600,
                        }
                    }
                }
            )

    def parse(self, response):

        
        # If login is fail, delete cookie and ask for new one
        # client = MongoClient(CONNECTION_STRING)
        # db_name = client["Posts"]
        # collection_name = db_name["Post"]

        with open('./homepage/html/PostInGroup.html', 'w+') as out:
            out.write(response.text)

        h = scrapy.Selector(response)
        post_info = h.css("div._4gur._5t8z")
        item = CrawlData()
        for product in post_info:
            item["post"] = " ".join(product.css("div._il ::text").extract())
            yield item



