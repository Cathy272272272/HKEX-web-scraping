# HKEX-web-scraping
HKEX.py is a piece of code which helps to scrape data from the official website of Hong Kong Stock Exchange(HKEX)from the following 3 urls. 
http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk
http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz
http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh.

The technique I used for the 3 dynamic web pages is using form data to scrape.

Users could use the code to download data within one year from the day you use it.

Caution: If you try to download data that is earlier, the code will go wrong because HKEX forbids the access of those earlier data.

The .csv files are sample files you could get from HKEX if you try to use HKEX.py to download.
