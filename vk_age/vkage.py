import requests
from datetime import date

#function for returning age in years 
def calc_age(birthday):
    birthday = date(int(birthday[-1]), int(birthday[-2]), int(birthday[-3]))
    today = date.today()
    return (today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))) 


class Counter(dict):
	def __missing__(self, key):
		return 0

if __name__ == '__main__':

	unknown_age_counter = 0
	result_dict = Counter()

	#poluchenie ID usera, esli byl vveden nickname
	#getting User_ID if the nickname is passed
	api_url = 'https://api.vk.com/method/users.get?v=5.87&access_token=3d044f423d044f423d044f42033d62b1c933d043d044f4266edd604bde25a0f05f8eeb1&user_ids='
	user_name = input("Enter user ID or nickname: ")
	r = requests.get(api_url + user_name)
	user_id = r.text.split(':')[2]

	api_url = 'https://api.vk.com/method/friends.get?v=5.87&access_token=3d044f423d044f423d044f42033d62b1c933d043d044f4266edd604bde25a0f05f8eeb1&user_id='

	r = requests.get(api_url + user_id[:-13] + '&fields=bdate')
	data = r.json()
	try:
		friend_list = data['response']['items']
	except KeyError:
		print('This user limited access to his friend list')
		exit(0)
	for friends in friend_list:
		try:
			friends['bdate']
			birthday = friends['bdate'].split('.')
			if (len(birthday) == 3): ##all three fields of age are filled DD.MM.YYYY
				result_dict[calc_age(birthday)] += 1
		except KeyError:
			unknown_age_counter += 1 #the quantity of friends without filled age row
	
	intermediate_sort = sorted(result_dict.items(), key = lambda x : x[0]) #sorting by age increasing
	sorted_dict = sorted(intermediate_sort, key = lambda x : x[1], reverse = True)  #sorting by quantity decreasing


	print(sorted_dict)