import urllib2
import json
import pandas as pd


SHAREDCOUNT_API_KEY = 'XXXXXXXXXXXX'

def map_ids_names(ids_array, df, object_name):
	names_array = []
	for object_id in ids_array:
		try:
			names_array.append(df.loc[object_id][object_name])
		except:
			continue
	return names_array

def get_social_metrics(url, api_key):
	sharedcount_response = urllib2.urlopen('https://free.sharedcount.com/?url=' + url + '&apikey=' + api_key)
	return json.load(sharedcount_response)

def main():

	print 'Getting Courses Data'

	courses_response = urllib2.urlopen('https://api.coursera.org/api/catalog.v1/courses?fields=shortName,name,language&includes=universities,categories')
	courses_data = json.load(courses_response)
	courses_data = courses_data['elements']

	universities_response = urllib2.urlopen('https://api.coursera.org/api/catalog.v1/universities?fields=name,locationCountry')
	universities_data = json.load(universities_response)
	universities_data = universities_data['elements']

	categories_response = urllib2.urlopen('https://api.coursera.org/api/catalog.v1/categories')
	categories_data = json.load(categories_response)
	categories_data = categories_data['elements']

	#2. Structuring the Data
	print 'Structuring the Data'

	courses_df = pd.DataFrame()

	courses_df['course_name'] = map(lambda course_data: course_data['name'], courses_data)
	courses_df['course_language'] = map(lambda course_data: course_data['language'], courses_data)
	courses_df['course_short_name'] = map(lambda course_data: course_data['shortName'], courses_data)
	courses_df['categories'] = map(lambda course_data: course_data['links']['categories'] if 'categories' in course_data['links'] else [], courses_data)
	courses_df['universities'] = map(lambda course_data: course_data['links']['universities'] if 'universities' in course_data['links'] else [], courses_data)

	universities_df = pd.DataFrame()
	universities_df['university_id'] = map(lambda university_data: university_data['id'], universities_data)
	universities_df['university_name'] = map(lambda university_data: university_data['name'], universities_data)
	universities_df['university_location_country'] = map(lambda university_data: university_data['locationCountry'], universities_data)
	universities_df = universities_df.set_index('university_id')

	categories_df = pd.DataFrame()
	categories_df['category_id'] = map(lambda category_data: category_data['id'], categories_data)
	categories_df['category_name'] = map(lambda category_data: category_data['name'], categories_data)
	categories_df = categories_df.set_index('category_id')

	courses_df['categories_name'] = courses_df.apply(lambda row: map_ids_names(row['categories'], categories_df, 'category_name'), axis=1)
	courses_df['universities_name'] = courses_df.apply(lambda row: map_ids_names(row['universities'], universities_df, 'university_name'), axis=1)

	#Getting Social Shares Data
	print 'Getting Social Shares Data'
	courses_df['course_url'] = 'https://www.coursera.org/course/' + courses_df['course_short_name']
	courses_df['sharedcount_metrics'] = map(lambda course_url: get_social_metrics(course_url, SHAREDCOUNT_API_KEY), courses_df['course_url'])

	courses_df['twitter_count'] = map(lambda sharedcount: sharedcount['Twitter'], courses_df['sharedcount_metrics'])
	courses_df['linkedin_count'] = map(lambda sharedcount: sharedcount['LinkedIn'], courses_df['sharedcount_metrics'])
	courses_df['facebook_count'] = map(lambda sharedcount: sharedcount['Facebook']['total_count'], courses_df['sharedcount_metrics'])

	#Saving the Data to a tsv File
	print 'Saving the Data'
	courses_df.to_csv('coursera_with_sharedcount.tsv', sep='\t', encoding='utf-8')

if __name__ == "__main__":
	main()

