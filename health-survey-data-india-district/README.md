As the front page says, this data was scraped off the website of National Family Health Survey, India at http://rchiips.org/nfhs/

The folder *rawfiles* contains pdf files for each district. For this one instance, I clicked on each district to download its pdf. However, for future work, I plan to write a scraper to do this job, which as you can guess, was not the most fun part of this exercise.
The folder *scripts* contains the python script used to generate tables from the pdfs. I can not thank the guys at <a href="http://tabula.technology/"> Tabula </a> enough for the amazing tool they developed to extract pdf tables.
I also used the helpful wrapper <a href="https://github.com/chezou/tabula-py"> Tabula-py </a> for data munging.
I have left comments in the code, but still, feel free to drop me an email should you have any questions.

The chief data file is mp-data.csv. Again, as I said, I might either generate one file for each state or merge it all in a single giant file, in which case I will replace this with an updated version. 
The main features of the data are the health indicators, which are under a conveniently named column *Indicators*. They were scraped straight off the pdfs.
A tricky part while data transformation was the DistrictType feature. Intially, I pulled a random file which only had two columns, one for "Urban" and another named Total.
My script was hardcoded for "Urban" which failed for the Rural districts. Just when I thought I had covered my bases, out came Gwalior, with BOTH Rural and Urban district type.
This not only messed with data split but also the table structure. So, in the future should you want to parse your own pdfs, do take these caveats into account.

Well, thank you for reading this. I hope you find the data file useful.
Shoot me an email or a tweet if you found bugs in data processing or just to sa

y Hi! Would love to see how you used this data
Ciao
