import pprint as p
import pandas as pd
import requests
import json
from Geocoding import get_cord
from Socials_Extractor import Social_Exf



def searchParams():
	location = input('Location to search:')
	entity = input('Entity to search:')
	cordinates = get_cord(location)
	return [cordinates, entity, location]

def main():
	search = searchParams()
	num = 0
	page=''
	location = {
		'lng':search[0][1],
		'lat':search[0][0]
		}
	entity = search[1]
	data = []
	s = 1
	while s:
		url = f"https://www.google.com/search?tbm=map&authuser=0&hl=en&gl=us&pb=!4m12!1m3!1d67059.3029501303!2d{location['lng']}!3d{location['lat']}!2m3!1f0!2f0!3f0!3m2!1i1283!2i937!4f13.1!7i20{page}!10b1!12m8!1m1!18b1!2m3!5m1!6e2!20e3!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m50!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sz18KYLf-McOZ_QbJ-KS4Bw%3A2!2s1i%3A0%2Ct%3A11886%2Cp%3Az18KYLf-McOZ_QbJ-KS4Bw%3A2!7e81!12e5!17sz18KYLf-McOZ_QbJ-KS4Bw%3A432!18e15!24m56!1m16!13m7!2b1!3b1!4b1!6i1!8b1!9b1!20b0!18m7!3b1!4b1!5b1!6b1!9b1!13b0!14b0!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m4!1e3!1e6!1e14!1e15!24b1!25b1!26b1!29b1!30m1!2b1!36b1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!89b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i937!1m6!1m2!1i1233!2i0!2m2!1i1283!2i937!1m6!1m2!1i0!2i0!2m2!1i1283!2i20!1m6!1m2!1i0!2i917!2m2!1i1283!2i937!34m16!2b1!3b1!4b1!6b1!8m4!1b1!3b1!4b1!6b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!42b1!47m0!49m1!3b1!50m4!2e2!3m2!1b1!3b1!65m0!69i540&q={entity}"
		response = requests.get(url)




# Sterlizing Response
		obj = json.loads(response.text[5:])



# Parseing Json Response
		resturants = []
		for i in obj[0][1]:
			if len(i) == 15:
				resturant = {}
				try:
					resturant['Name'] = i[14][18].split(',', 1)[0]
					resturant['Address'] = i[14][18].split(',', 1)[1] 
					resturant['Website'] =  i[14][7][1]
					resturant['Phone'] = i[14][178][0][0]
					resturant['Rating'] = i[14][4][7]
					resturant['Reviews'] = i[14][4][8]
				except:
					pass
				resturants.append(resturant)
# Creating Dataframe 
		df = pd.DataFrame(resturants)
		try:
			df = df[df['Address'].str.contains(search[2].split(',')[0])]
		except:
			continue
		if df.empty:
			break
		data.append(df)
		num += 20
		page =f'!8i{num}'
	df = pd.concat(data)
	df.reset_index(drop = True, inplace=True)
	Social_Exf(df['Website'].tolist())
	df.to_csv(f'{entity}_in_{search[2]}.csv')
	print(df)

if __name__ == '__main__':
	main()