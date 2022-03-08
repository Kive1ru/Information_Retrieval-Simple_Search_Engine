# Information_Retrieval-Simple_Search_Engine
## UCI CS 121 Information Retrieval Project(Assignment3)

### Required library:

	NLTK - pip install nltk
	BeautifulSoup4 - pip install beautifulsoup4
	Simhash - pip install simhash
	Flask - pip install Flask
  
### How to run the code that creates the index?

	1. Open Indexer.py
	2. Change the root(the address of the DEV folder) and storeRoot(the address of where you want your index files be placed)  under "if __name__ == '__main__':"
	3. Run the program
	4. Wait until the program ends to see the index files (a folder named "TEST" containing all the indexes classified according to their first initial character)

### How to start the search interface (text interface)?

	1. Open Searcher.py
	2. Change the root (the address of where your index files be placed) under "if __name__ == '__main__':"
	3. Run the program
	4. After you start Searcher.py, each time you want to search, type in the query and hit enter
	5. To exit the program, simply hit enter
	
### 20 Test Queries:
	1. cristina lopes
	2. machine learning
	3. ACM
	4. master of software engineering
	5. aux
	6. of
	7. to be or not to be
	8. computer science
	9. CS 121
	10. 2016 Summer
	11. uci 
	12. Women in Computer Science
	13. Artificial Intelligence
	14. informatics
	15. department
	16. the
	17. Programming Languages and Software Engineering
	18. ICS Student Life
	19. Donald Bren School of Information & Computer Sciences
	20. Information Retrieval

For query 1 & 2 & 4 & 7 & 8 & 9 & 10 & 12 & 13 & 17 & 18 & 19 & 20, the searching time was very slow because each time we had to load the whole index dictionary, including all the postings for all the terms, again. We improve the searching time by storing index files according to their first initial character, which reduce the searching time.

For query 2, the first time we found that the top result url was not solid because it contains many "machine" but few "learning". We improve it by weighing terms differently according to the tag type of the string. For example, normal text and bold text have different weights.

For query 4, at first, it did poorly because there are many useless pages including large amount of "of"s. Those pages are large files with low content. We alter the Indexer.py to only index pages with text content smaller than the threshold we define.

For query 5 'aux', when we created the index file for the first time, we found that on Windows we cannot create a file called 'aux.json', so we store the file as 'aux_.json'. When we search queries include 'aux', it would directly find the 'aux_json' file. 
