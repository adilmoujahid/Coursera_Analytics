import pandas as pd
import ast
import urllib2
import json


def main():
	courses_df = pd.read_csv('coursera_with_sharedcount.tsv', sep='\t', encoding='utf-8')

	languages = {
				1: 'en',
				2: 'es',
				3: 'zh-cn',
				4: 'zh-tw',
				5: 'fr',
				6: 'de',
				7: 'ar',
				8: 'pt-br',
				9: 'ru',
				10: 'tr',
				11: 'it',
				12: 'he'
	}

	categories = {
				1: 'Computer Science: Theory',
				2: 'Computer Science: Software Engineering',
				3: 'Computer Science: Artificial Intelligence',
				4: 'Computer Science: Systems & Security',
				5: 'Information, Tech & Design',
				6: 'Engineering',
				7: 'Mathematics',
				8: 'Statistics and Data Analysis',
				9: 'Physics',
				10: 'Chemistry',
				11: 'Medicine',
				12: 'Economics & Finance',
				13: 'Social Sciences',
				11: 'Humanities',
				12: 'Law',
				13: 'Arts',
				14: 'Health & Society',
				15: 'Physical & Earth Sciences',
				16: 'Biology & Life Sciences',
				17: 'Business & Management',
				18: 'Education',
				19: 'Energy & Earth Sciences',
				20: 'Food and Nutrition',
				21: 'Music, Film, and Audio',
				22: 'Teacher Professional Development'
			}

	social_metrics = {
					1: 'twitter_count',
					2: 'facebook_count',
					3: 'linkedin_count'
			}


	print languages
	language = raw_input('Enter the language id: ')
	print '-------------\n'
	print categories
	category = raw_input('Enter the category id: ')
	print '-------------\n'
	print social_metrics
	social_metric = raw_input('Enter the social metric id: ')
	print '-------------\n'
	num_course = raw_input('Enter the number of courses you want to see: ')

	query = courses_df[courses_df['course_language'] == languages[int(language)]]
	query = query[query['categories_name'].map(lambda categories_name: categories[int(category)] in categories_name)]
	query = query.sort(social_metrics[int(social_metric)], ascending=0).head(int(num_course))


	print '---------------------------------------\n\n\n'
	print '************* The top %s %s Coursera courses in %s  ************* ' %(num_course, languages[int(language)], categories[int(category)])  
	print '\n'
	for row in query.iterrows():
		index, data = row
		print 'Course Name:     ' + data['course_name']
		print 'Course URL:      ' + data['course_url']
		print 'Course Language: ' + data['course_language']
		print 'Universities:    ' + data['universities_name']
		print 'Categories:      ' + data['categories_name']
		print 'Twitter Count:   ' + str(data['twitter_count'])
		print 'Linkedin Count:  ' + str(data['linkedin_count'])
		print 'Facebook Count:  ' + str(data['facebook_count'])
		print '------------------------\n'


if __name__ == "__main__":
	main()


