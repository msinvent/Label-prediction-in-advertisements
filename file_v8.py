#Programmer : Manish Sharma
#Email : msinvent@gmail.com
#Description : Program derives a feature vector which in this case is dictionary
# 				of words contained in the training data. The training data is 
#				trained in a sense that closely matches how we compute bayes
#				probability. To do the testing the testing vector is initialized
#				with values 1 on the indexes where the words of the title are found
#				in the dictionary.
#Some Assumptions : I am not using the data of city at all because I think it will
#not give any useful information and may be its use will train the system to follow
#some wrong bias. Example : suppose a city dont have a data of a certain category,
#now the system will think that given this particular city a specific category is
#not what I should look for. I agree that this data may be used to derive some useful
#information though and may improve the performance of the prediction system.
#
#Expected Accuracy : 75% - 85% (but please verify with your testing set)
#
#How to use :
# 1- In line 144 change the name of 'testing.json' with your training file
# 2- The program will generate a file named result.text in the specified format

import json
import unicodedata
import fileinput
import re
import collections
import operator
import string
import numpy

file = open('training.json','r');
x =  int(file.readline());

all_category = [];
all_section = [];
hierarchy1 = [];

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

for i in range(0,x):
	data = file.readline();
	j = json.loads(data);
	hierarchy1_section = j['section'];
	category = j['category'];
	if (category in all_category)== False: #new category encountered
		all_category.append(category);
		if (hierarchy1_section in all_section)== False: #section is also new
			all_section.append(hierarchy1_section);
			localvar = [];
			localvar.append(category);
			hierarchy1.append(localvar);
						
		else:
			index = all_section.index(hierarchy1_section)
			hierarchy1[index].append(category)
	
print "\nAll Section : "
print all_section
print "\nAll Categories : " 
print all_category
print "\nFirst level Hierarchy : " 
print hierarchy1
file.close()

## section 2 
#creating different dictionary for each section

dictionary = collections.Counter()
	
filehandle = open('training.json','r');
x =  int(filehandle.readline());

for i in range(0,x):
	head_lower_nonnum=[];
	data = filehandle.readline();
	j =json.loads(data);
	head_split = re.findall(r"[\w']+", j['heading'])
	head_lower = [item.lower() for item in head_split];
	for item in head_lower:
		if(is_number(item) == False):
			head_lower_nonnum.append(item)
			
	#print head_split
	dictionary.update(head_lower_nonnum)
	
filehandle.close();
sorted_words = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)

#for word, count in sorted_words:
#    print word, count

	
## section 3
#Initializing the weights
trained_vec = [];

#initializing weights with 0
for i in range(0,len(hierarchy1)):
	trained_vec.append([]);
	for j in range(0,len(hierarchy1[i])):
		trained_vec[i].append([0]*len(dictionary));
dict_copy = []; # very important vector

for word in dictionary:
    dict_copy.append(word)
	
		
filehandle = open('training.json','r');
x =  int(filehandle.readline());
#training
for i in range(0,x):
	data = filehandle.readline();
	j =json.loads(data);
	index1 = all_section.index(j['section'])
	index2 = hierarchy1[index1].index(j['category'])
	
	head_lower_nonnum = [];
	head_split = re.findall(r"[\w']+", j['heading'])
	head_lower = [item.lower() for item in head_split];
	for item in head_lower:
		if(is_number(item) == False):
			head_lower_nonnum.append(item)
	
	length = len(head_lower_nonnum)
	for item in head_lower_nonnum:	
		#search the item in the dictionary and adjust weight
		index3 = dict_copy.index(item)
		if length is not 0 and trained_vec[index1][index2][index3]<=1:
		#if length is not 0:
			trained_vec[index1][index2][index3] += 1.00/length;	
		

filehandle.close();

		
##testing
dict_len = len(dictionary);
#put name of test file in place of training.json
filehandle = open('testing.json','r');
outputfile = open('result.txt','w');
x =  int(filehandle.readline());
#correct = 0;

for i in range(0,x):
	test_vector = [0]*len(dictionary);
	data = filehandle.readline();
	j =json.loads(data);
	index1 = all_section.index(j['section']) #section of object
		
	head_lower_nonnum = [];
	head_split = re.findall(r"[\w']+", j['heading'])
	head_lower = [item.lower() for item in head_split];
	for item in head_lower:
		if(is_number(item) == False):
			head_lower_nonnum.append(item)
	
	length = len(head_lower_nonnum)
	#computing test vector
	for item in head_lower_nonnum:	
			#search the item in the dictionary and adjust weight
			index3 = dict_copy.index(item)
			if length is not 0:
				test_vector[index3] = 1.00/length;
			
	distances = [];
	
	for k in range (0,len(hierarchy1[index1])):
		dd = 0.00;
		# computing distance with each possible category
		v1 = numpy.asarray(test_vector);
		v2 = numpy.asarray(trained_vec[index1][k])
		dd = numpy.dot(v1,v2);
		distances.append(dd);
	
	label_i= distances.index(max(distances))
	#print hierarchy1[index1][label_i]
	#print j['category']
	
	#creating outputfile for testing
	outputfile.write(hierarchy1[index1][label_i]+"\n")
	
	#if j['category'] == hierarchy1[index1][label_i]:
	#	correct+=1;
	
#print correct
	
filehandle.close();
outputfile.close();

#print "Accuracy : "
#print (correct*100.00)/x;