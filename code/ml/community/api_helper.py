import functools

def get_top_friends(twitter_api, user_name, friends_at_depths=[4, 3]):
    connections = dict()
    queue = [user_name]
    found_names = set(queue)
    for num_friends in friends_at_depths:
        get_top_friends_next_level(twitter_api, num_friends, queue, connections, found_names)
    return connections

def get_top_friends_next_level(twitter_api,
    num_friends,
    queue,
    connections,
    found_names):
    
    names = queue.copy()
    l = len(queue)
    found_names.update(queue)

    while names:

        user_name = names.pop(0)
        friends = twitter_api.friends.list(screen_name = user_name, count=200)
        friends = friends['users']
        
        friends.sort(key=lambda fr: fr['followers_count'], reverse=True)
        friends = list(filter(lambda fr: fr['screen_name'] not in found_names, friends))
        # print(friends)
        connections[user_name] = {
            'friends' : [ {
                            'name': friends[i]['screen_name'],
                            'followers_count': friends[i]['followers_count'],
                            'follower': user_name,
                            'details':  friends[i],
                            } for i in range(num_friends)
                        ],
        }
        
        queue.extend([ friends[i]['screen_name'] for i in range(num_friends)])

    del queue[:l]
    