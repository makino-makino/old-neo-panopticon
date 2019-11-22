import requests as rq

class Test:
    def __init__(self):
        self.root = 'http://localhost:3000/'
        self.headers = {'access-token':'',
                        'uid':'',
                        'client':'' }
        self.succeeded = 0
        self.failed = 0

    def url(self, access_point):
        return self.root + access_point

    def ok(self, r, check=True):
        success = 200 <= r.status_code < 300
        if success and check:
            self.succeeded += 1
            print('ok.', end=" ")
        else:
            self.failed += 1
            print(f"failed. {self.failed}", end=" ")

        print(r.status_code)
        print(r.json())
        return success



    """ ==== test about users ==== """

    # creating users

    def create_user(self, name, email, phone, password):

        print(f"""name = {name}
        email: {email}
        phone: {phone}
        password: {password}
        """)

        payloads = {'name': name, 'email': email, 'phone': phone, 'password': password}
        r = rq.post(self.url('auth/'), data=payloads)

        if self.ok(r) and all([x == '' for x in self.headers.values()]):
            headers = r.headers
            self.headers = {'access-token': headers['access-token'],
                            'uid': headers['uid'],
                            'client': headers['client'] }
        else:
            headers = r.headers
            self.headers_sub = {'access-token': headers['access-token'],
                                'uid': headers['uid'],
                                'client': headers['client'] }


        return r.json()

    # showing users

    def users_index(self):

        print("users index")
        r = rq.get(self.url('users/'), self.headers)
        self.ok(r)

        return r.json()

    def get_a_user(self, id=1):

        print(f"id = {id}: ", end="")
        r = rq.get(self.url(f'users/{id}'), self.headers)
        self.ok(r)

        return r.json()


    
    """  ==== tests about followings ==== """

    # creating follow

    def follow(self, from_id, to_id, sub=False, dup=False):
        headers = self.headers if not sub else self.headers_sub        

        print(f"follow from {from_id} to {to_id}: ", end="")
        payload = {'from_id': from_id, 'to_id': to_id}
        r = rq.post(self.url("followings/"), headers=headers, data=payload)

        if not dup:
            self.ok(r)
        else:
            if r.status_code == 400:
                print(f"refused. {r.status_code}")
                self.succeeded += 1
            else:
                self.failed += 1
                print("didn't work.:", self.failed)

            print(r.json())

        return r.json()

    # showing followings

    def followings(self, user_id=1):

        print(f"followers of user {user_id}: ", end="")
        r1 = rq.get(self.url(f"users?follower={user_id}"), headers=self.headers)
        self.ok(r1, check=(len(r1.json()) == 1))

        print(f"followees of user {user_id}: ", end="")
        r2 = rq.get(self.url(f"users?followee={user_id}"), headers=self.headers)
        self.ok(r2, check=(len(r2.json()) == 1))

        return r1.json(), r2.json()



    """ ==== tests about posts ==== """

    # creating posts

    def new_post(self, content="hogehoge"):

        print(f"content={content}: ", end="")

        payload = {'content': content}
        r = rq.post(self.url('posts/'), headers=self.headers, data=payload)

        self.ok(r)

        return r.json()

    def new_rt(self, content="", source_id=1):

        print(f"source id={source_id}: ", end="")

        payload = {'content': content, 'source_id': source_id}
        r = rq.post(self.url('posts/'), headers=self.headers, data=payload)
        self.ok(r)

        return r.json()

    # showing posts

    def posts_index(self, numbers=2):

        print("index: ", end="")
        r1 = rq.get(self.url('posts/'), self.headers)
        self.ok(r1)

        print(f"index(numbers = {numbers}): ", end="")
        r2 = rq.get(self.url(f'posts?numbers={numbers}'), self.headers)
        self.ok(r2, check=(len(r2.json()) == numbers))

        return r1.json(), r2.json()
    
    def get_a_post(self, id=1):

        print(f"id = {id}: ", end="")
        r = rq.get(self.url('posts/1'), self.headers)
        self.ok(r)

        return r.json()



    """ ==== tests about evaluations ==== """

    # creating evaluations

    def create_new_evaluation(self, post_id=1, is_positive="true", dup=False):

        print(f"evaluate post {post_id}: ", end="")
        payload = {'post_id': post_id, 'is_positive': is_positive}
        r = rq.post(self.url(f"evaluations/"), headers=self.headers, data=payload)

        if not dup:
            self.ok(r)
        else:
            print(r.status_code)
            if r.status_code == 400:
                self.succeeded += 1
            else:
                self.failed += 1
                print("failed.:", self.failed)
            print(r.json())

        return r.json()



    """ ==== tests about notifications ==== """

    def get_notifications(self):

        r = rq.get(self.url("notifications/"), self.headers)
        self.ok(r, check=(len(r.json()) == 3))

        return r.json()



    def put_result(self):
        print(f"secceeded: {self.succeeded}")
        print(f"failed:    {self.failed}")




def nl(text):
    print("\n\n========= " + text + " =========\n")


def main():
    test = Test()

    nl("create a new user test")
    user1 = test.create_user(name="makino", email="makino@example.com", phone="0123456789", password="password")['data']
    user2 = test.create_user(name="akama",  email="akama@example.com",  phone="9876543210", password="password")['data']
    nl("users index test")
    test.users_index()
    nl("a user test")
    test.get_a_user(user1['id'])

    nl("new follow test")
    test.follow(from_id=user1['id'], to_id=user2['id'])
    test.follow(from_id=user2['id'], to_id=user1['id'], sub=True)
    nl("duplicated follow test")
    test.follow(from_id=user1['id'], to_id=user2['id'], dup=True)
    nl("followings test")
    test.followings(user_id=user1['id'])

    nl("create a new post test")
    post1 = test.new_post(content="hogehoge")
    post2 = test.new_post(content="fugafuga")
    print("~~ this is reply ~~")
    post3 = test.new_post(content="@makino @akama fugifugi")
    nl("create a new retweet")
    test.new_rt(source_id=post1['id'])
    nl("posts index test")
    test.posts_index(numbers=2)
    nl("a post test")
    test.get_a_post(post1['id'])

    nl("create new evaluation test")
    test.create_new_evaluation(post1['id'], "true")
    test.create_new_evaluation(post2['id'], "false")
    nl("duplicated evaluation test")
    test.create_new_evaluation(post1['id'], "true", dup=True)

    nl("notifications test")
    test.get_notifications()

    nl("--- finished ---")

    test.put_result()


if __name__ == "__main__":
    main()