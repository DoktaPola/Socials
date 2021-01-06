import vk_api
import json
import time

vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()


def makeWay(way, current, ancestor):
    while current:
        info = vk.users.get(user_ids=str(current), fields='is_closed')
        person = dict()
        person['id'] = str(current)
        person['last_name'] = info[0]['last_name']
        person['first_name'] = info[0]['first_name']
        if not ('deactivated' in info[0]) and not (info[0]['is_closed']):
            person['friends'] = vk.friends.get(user_id=person['id'])['items']
        else:
            person['friends'] = 'unknown'
        way.insert(0, person)
        current = ancestor[current]
    return


def findWay(way, queue, used, ancestor, idFinale, finalFriends, time_limit):
    start_time = time.time()
    while queue:
        if time.time() - start_time > time_limit:
            current = queue.pop(0)[1]
            makeWay(way, current, ancestor)
            return
        person = queue.pop(0)
        if person[0] in used:
            continue
        used.add(person[0])
        info = vk.users.get(user_ids=person[0], fields='is_closed')
        if not ('deactivated' in info[0]) and not (info[0]['is_closed']):
            response = vk.friends.get(user_id=person[0])
            if person[0] in ancestor:
                continue
            else:
                ancestor[person[0]] = person[1]
            intersection = set(response['items']).intersection(finalFriends)
            if intersection:
                intersection = str(list(set(response['items']).intersection(finalFriends))[0])
                test_info = vk.users.get(user_ids=intersection, fields='is_closed')
                if not ('deactivated' in test_info[0]):
                    ancestor[person[0]] = person[1]
                    ancestor[intersection] = person[0]
                    ancestor[idFinale] = intersection
                    current = idFinale
                    makeWay(way, current, ancestor)
                    return
            for id in response['items']:
                if not(str(id) in used):
                    queue.append((str(id), person[0]))


def BFS (friends, q, used, id, count, current, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return
    info = vk.users.get(user_ids=id, fields='is_closed')
    if not('deactivated' in info[0]) and not(info[0]['is_closed']):
        response = vk.friends.get(user_id=id, fields='bdate, sex')
        if response['count'] != 0:
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
            current = len(friends) - 1
        if (current < count) and (current > 0):
            BFS(friends, q, used, q.pop(0), count, current, start_time, time_limit)
        else:
            return
    else:
        BFS(friends, q, used, q.pop(0), count, current, start_time, time_limit)


def findGroups(id, people, time_limit):
    used = set()
    queue = []
    start_time = time.time()
    info = vk.users.get(user_ids=id, fields='is_closed')
    temp = dict()
    temp['id'] = id
    temp['last_name'] = info[0]['last_name']
    temp['first_name'] = info[0]['first_name']
    temp['groups'] = vk.groups.get(user_id=id, extended=1, count=200)['items']
    people.append(temp)
    used.add(id)
    if not ('deactivated' in info[0]) and not (info[0]['is_closed']):
        response = vk.friends.get(user_id=id, fields='sex')
        for resp in response['items']:
            if time.time() - start_time < time_limit and len(people) < 200:
                person_info = vk.users.get(user_ids=resp['id'], fields='is_closed')
                if not (resp['id'] in used) and not (resp['first_name'] == 'DELETED') and not(person_info[0]['is_closed']):
                    person = dict()
                    person['id'] = resp['id']
                    person['last_name'] = resp['last_name']
                    person['first_name'] = resp['first_name']
                    person['groups'] = vk.groups.get(user_id=resp['id'], extended=1, count=200)['items']
                    people.append(person)
                    used.add(str(resp['id']))
                    friends = vk.friends.get(user_id=resp['id'])
                    queue.extend(friends['items'])
            else:
                return
        while time.time() - start_time < time_limit and len(people) < 200:
            current = str(queue.pop(0))
            current_info = vk.users.get(user_ids=current, fields='is_closed')
            if not (current in used) and not ('deactivated' in current_info[0]) and not(current_info[0]['is_closed']):
                current_person = dict()
                current_person['id'] = current
                current_person['last_name'] = current_info[0]['last_name']
                current_person['first_name'] = current_info[0]['first_name']
                current_person['groups'] = vk.groups.get(user_id=current, extended=1, count=200)['items']
                people.append(current_person)
                used.add(current)
        return
    else:
        return


def main(type, user_id, count, time_limit, idStart, idFinale, id):

    if type == 1:
        # user_id = input()
        # count = int(input())
        # time_limit = int(input())
        used = set()
        q = [user_id]
        friends = []
        start_info = vk.users.get(user_ids=user_id, fields='bdate, sex')
        start = dict()
        if not ('deactivated' in start_info[0]) and not (start_info[0]['is_closed']):
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
            start_friends = vk.friends.get(user_id=start['id'])
            start['friends'] = start_friends['items']
            friends.append(start)
            used.add(start['id'])
            start_time = time.time()
            BFS(friends, q, used, q.pop(0), count, 0, start_time, time_limit)
        f = open('friends.json', 'w', encoding="utf-8")
        f.write(json.dumps(friends, indent=4, ensure_ascii=False))
        f.close()
    elif type == 2:
        # idStart = input()
        # idFinale = input()
        # time_limit = int(input())
        used = set()
        ancestor = dict()
        way = []
        finalFriends = []
        queue = [(idStart, None)]
        info = vk.users.get(user_ids=idFinale, fields='is_closed')
        if not ('deactivated' in info[0]) and not (info[0]['is_closed']):
            response = vk.friends.get(user_id=idFinale)
            for resp in response['items']:
                finalFriends.append(resp)
            findWay(way, queue, used, ancestor, idFinale, finalFriends, time_limit)
            f = open('way.json', 'w', encoding="utf-8")
            f.write(json.dumps(way, indent=4, ensure_ascii=False))
            f.close()
    elif type == 3:
        # id = input()
        # time_limit = int(input())
        people = []
        findGroups(id, people, time_limit)
        f = open('groups.json', 'w', encoding="utf-8")
        f.write(json.dumps(people, indent=4, ensure_ascii=False))
        f.close()


if __name__ == '__main__':
    main()

