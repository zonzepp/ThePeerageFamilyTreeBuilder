# ThePeerageFamilyTreeBuilder
A Script that builds a family tree from an entry on ThePeerage.com
For example. Take the entry for Duke of Edinburgh http://www.thepeerage.com/p10071.htm#i100704
Take the end of his page.  p10071.htm#i100704 and run the script from a command line "./PeerageExtractionVersion1.py p10071.htm#i100704 > YourTxtFileToSaveTree.txt"
This will save the tree to the text file. 
Depending on the size of the tree the time for the script to ru will vary. I have added a 1 second delay between calls to the website to reduce demand on it. For more detailed trees this number may need to be reduced
Script was written by @simontuohy and @EamonnOToole
