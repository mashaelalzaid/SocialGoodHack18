import sys, subprocess, ipaddress, time, datetime, json,  os, csv, copy
from watson_developer_cloud import DiscoveryV1
from utils3 import *




def get_natural_language_query(discovery, query):
	my_query = discovery.query(environment_id=EnvID, collection_id=ColID, query=query, passages='true', passages_count='1', count=1, highlight='true')
	print('completing natural_laguage_query')
	return my_query


## get all document ID
def get_all_documentid(discovery):
	my_query = discovery.query(environment_id=EnvID, collection_id=ColID, count='5')
	docid_dict={}
	for i in range(len(my_query["results"])):
		docid_dict[my_query["results"][i]["id"]]=my_query["results"][i]["id"]
	print(json.dumps(docid_dict,indent=2))

	return docid_dict

#read questions
def readQuestion():
	Q_list=[]
	with open('/home/osboxes/Desktop/culture/questions.csv', 'r') as csvfile:
		csv_iterator= csv.reader(csvfile, delimiter=',')
		for row in csv_iterator:
			Q_list.append(row[0])
	print(Q_list)
	print('completing reading question')
	return Q_list

#main method

def main():
	print("cutlture")

	#to create discovery object
	discovery = DiscoveryV1(
 	url= "https://gateway.watsonplatform.net/discovery/api",
	version='2018-03-05',
	username="9e523dc4-1206-4898-a30f-faf75cd8526b",
	password="tQFEkjWAz6hr"
	)
	print(discovery)
	docs =['sa.pdf','us.pdf','eg.pdf','in.pdf','ch.pdf']
#	for doc in docs:
	#add docs
#		with open(os.path.join(os.getcwd(), '/home/osboxes/Desktop/culture/pdffiles', doc)) as fileinfo:
#			add_doc = discovery.add_document(EnvID, ColID, file=fileinfo)
#			print(json.dumps(add_doc, indent=2))
#			#get collection details
#			collection = discovery.get_collection(EnvID, ColID)
#			print(json.dumps(collection, indent=2))

	#query natural language
#	dict_id = get_all_documentid(discovery)
	#reads question
	query=readQuestion()

	with open('/home/osboxes/Desktop/culture/result.csv', 'w') as csvfile:
		fieldnames = ['query', 'top1','document_id1']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
	    
	for q in query:
		query_response=get_natural_language_query(discovery, q)
		print(json.dumps(query_response,indent=2))
#		writetocsv(query_response,q)
		#    with open('/home/osboxes/Desktop/data.json','w') as outfile:
		#	    json.dump(query_response, outfile)
	
	
def writetocsv(query_response,q):    
	with open('/home/osboxes/Desktop/culture/result.csv', 'a') as csvfile:
		fieldnames = ['query', 'top1', 'document_id1']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		row_dict ={}
		row_dict['query']=q
		row_dict['top1']=query_response['passages'][0]['passage_text']
		row_dict['document_id1']=query_response['passages'][0]['document_id']
		
		writer.writerow(row_dict)	
	print("Conmplete file writing")

if __name__ == "__main__":
	main()
