# HKEX-web-scraping
HKEX.py is a Python script that helps the users to scrape stock trading data from the official website of Hong Kong Stock Exchange(HKEX) using beautiful soup (bs4) and request package. The data is scrapped from the dynamic web pages of the following three url using the technique of form data:

http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk
http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz
http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh.

The script allows users to download stock trading data no earlier than one year before the date of usage. (e.g. If a user ran the script on 31st December 2018, he or she could not downlaod data earlier than 1st January 2018)

Users should beware that if they attempt to download data that is earlier, the script will error out because HKEX forbids access to earlier data.

The .csv files are sample files showing the results retrived from HKEX should you use the script properly.
