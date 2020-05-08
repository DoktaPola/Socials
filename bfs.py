import vk_api
import json
import time
code = '2f44f3122f44f3122f44f312422f34e2f922f442f44f312711a582d5fc2a27b99d64bf4'
app = 7344619
secret = 'GJdQphxS7yjBShLWemze'
vk_session = vk_api.VkApi(app_id=app, client_secret=secret, token=code)
vk = vk_session.get_api()


def BFS (friends, q, used, id, count, current):
    info = vk.users.get(user_ids=id, fields='is_closed')
    if not('deactivated' in info[0]) and not(info[0]['is_closed']):
        response = vk.friends.get(user_id=id, fields='bdate, sex')
        k = response['count']
        for i in range(0, min(count - current, response['count'])):
            resp = response['items'][i]
            person = dict()
            if resp['first_name'] != 'DELETED' and not(resp['id'] in used):
                person['id'] = resp['id']
                person['last_name'] = resp['last_name']
                person['first_name'] = resp['first_name']
                if resp['sex'] == 2:
                    person['sex'] = 'male'
                elif resp['sex'] == 1:
                    person['sex'] = 'female'
                else:
                    person['sex'] = 'unknown'
                if 'bdate' in resp:
                    person['bdate'] = resp['bdate']
                else:
                    person['bdate'] = 'unknown'
                person_info = vk.users.get(user_ids=person['id'], fields='is_closed')
                if not('deactivated' in person_info[0]) and not (person_info[0]['is_closed']):
                    person_friends = vk.friends.get(user_id=person['id'])
                    person['friends'] = person_friends['items']
                else:
                    person['friends'] = 'unknown'
                friends.append(person)
                used.add(person['id'])
                q.append(resp['id'])
            else:
                k -= 1
        current += min(count - current, k)
        if current < count:
            BFS(friends, q, used, q.pop(0), count, current)
        else:
            exit
    else:
        BFS(friends, q, used, q.pop(0), count, current)


start_time = time.time()
user_id = input()
count = int(input())
used = set()
q = []
q.append(user_id)
friends = []
start_info = vk.users.get(user_ids=user_id, fields='bdate, sex')
start = dict()
start['id'] = start_info[0]['id']
start['last_name'] = start_info[0]['last_name']
start['first_name'] = start_info[0]['first_name']
if start_info[0]['sex'] == 2:
    start['sex'] = 'male'
elif start_info[0]['sex'] == 1:
    start['sex'] = 'female'
else:
    start['sex'] = 'unknown'
if 'bdate' in start_info[0]:
    start['bdate'] = start_info[0]['bdate']
else:
    start['bdate'] = 'unknown'
if not ('deactivated' in start_info[0]) and not (start_info[0]['is_closed']):
    start_friends = vk.friends.get(user_id=start['id'])
    start['friends'] = start_friends['items']
else:
    start['friends'] = 'unknown'
    print('Closed account')
friends.append(start)
used.add(start['id'])
BFS(friends, q, used, q.pop(0), count, 0)
f = open('friends.json', 'w')
f.write(json.dumps(friends, indent=4))
f.close()
# print("--- %s seconds ---" % (time.time() - start_time))
