#Archives Fullsite Crawler

[www.archives.com](http://www.archives.com/) is a website can search 4.3 billions National arichives and Federal census data. You can search birth record, death record, marriage record and divorce record. Additionally, the family history search engine may help you find your ancestor and family information.

##Information about this project

To get data from a website, basically there are only two ways:

1. Hack it, and clone the back-end database.
2. Simulating browse behavior, and go through the whole site to get all data.

Definitely, we use the second method.

The only way to get data from www.archives.com is through query. We have to properly design a system keep making query, and download the result. Of course we also need a strategy to find out which data query has made and which is not. Unlike other small crawler project, this one is huge. Approximately there are 4.3 billions records to crawl, which may needs TB-level database system to store that.

##Install and setup

	|---archives: a python library work with www.archives.com
	|---prerequisite: required library angora
	|---dev01_taskplan.py
	|---dev02_crawler.py


##Design

We use a master mongoDB + python script to handle multi-task scheduling. Because I don't have enough hardware resources (cluster, IP, database), the best things I can do is using a multi-task system.

**System diagram**

	+-----------------+                      +-----------------+                                 
	|task plan program+----------------------> master database |                                 
	+-----------------+                      +-^---------^---^-+                                 
	                                           |   |     |   |                                   
	                               +-----------+   |     |   +----------+                        
	                               |               |     |              |                        
	                  +----------------------------+     +----------------------------------+    
	                  |            |               |     |              |                   |    
	                  |            |               |     |              |                   |    
	                  |            |               |     |              |                   |    
	                  |            |               |     |              |                   |    
	          +-------v-------+    |         +-----v-----------+        |       +-----------v---+
	          |crawler program+----+         |crawler program  |        +-------+crawler program|
	          +---------------+              +-----------------+                +---------------+
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                           |                                    |        
	                   |                     +-----v-----------+                        |        
	                   +--------------------->storage database <------------------------+        
	                                         +-----------------+                                 

 
