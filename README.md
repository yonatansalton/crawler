Web Crawler
--

This code implements a simple web crawler that gets a URL <br>
and saves the parsed data into ./Data directory
In order to start crawling:
python main.py [URL] [CONCCURENCY]

Some notes:
1) I didn't managed to connect to the url you provided, they blocked me
right away, So the content i'm parsing is just the title. If i was able to login
I would look for the right headers in the web page to parse as you asked.
2) If I had to implement such a system in reality, I would have use microsevices architecture as follows: 
- First component is the crawler, get the input (main url) from a kafka topic.
- One crawler pod working on one url, and send back more links to the input topic.
- The crawler pod interacts with redis db that keep tracking of the visited urls using key(main url) and list of values (visited urls)
- The crawlers send the parsed json to another topic consumed by the data handler pod
- The second component would be the data handler that consumes this topic, and saves the data to the desired location (DB, FileSystem, etc..)


Thats it, <br>
Thank you !