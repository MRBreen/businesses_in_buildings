
Objective:
To find find businesses in a local area which may not be readily be apparent to the those in the area.  Finding these businesses in buildings would facilitate networking opportunities for careers in addition to feeding curiosity as to what businesses are in the area.

Data Understanding:
Data was sourced from the Washington Business License Service one scrape at a time by street name and city of Seattle.  Business licenses are issued to different types of businesses, and the ones of interest are corporations, llc, and join ventures.  The company name, registered business address and Seattle were put into a bing search.  Subsequent data scraping into three main categories: ten links, ten accompanying text for those links and the number of search results.

Data:
Web Scraped BLS -> S3 -> MongoDB -> Search query and web scrape -> S3 -> MongoDB -> Python

Modeling:
TFID was performed and follow on nmf clustering

Evaluation:
This exercise was successful in identifying business that are likely to be in the local area that are not necessarily on yelp or google places.  The model does have a high false positive as some companies have gone out of business, sometimes this is caught by the model which identifies bankrupt companies by collector agencies and credit related services.

Deployment:
This will be rolled out and it will be awesome.
