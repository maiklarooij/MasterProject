from datetime import datetime

from Agent import Agent

class Post():
    def __init__(self, post_id: int, author: int, timestamp: datetime, content: str):
        self.post_id = post_id
        self.author = author
        self.timestamp = timestamp
        self.content = content
        
        self.reposts = 0

    # TODO
    def __str__(self):
        return f"User {self.author} posted: {self.content}"
    
    def __repr__(self):
        return f"User {self.author} posted: {self.content}"
    
    def count_repost(self):
        self.reposts += 1

class Platform():

    def __init__(self):
        self.users: list[Agent] = []

        # Of the form {"user_id": int, "time": int, "content": str, "repost": bool, "repost_user_id": int}
        self.posts: list[dict] = []

        # Of the form (user_id_link_from, user_id_link_to)
        self.user_links: list[(int, int)] = []

    def register_user(self, agent: Agent):

        # TODO: ID should be unique
        agent.identifier = len(self.users)+1
        self.users.append(agent)

    def get_user(self, user_id: int) -> Agent:
        for user in self.users:
            if user.identifier == user_id:
                return user
        return None
    
    def get_post(self, post_id: int) -> Post:
        for post in self.posts:
            if post["post_id"] == post_id:
                return post["post_content"]

        return None

    
    def link_users(self, user_link_from: Agent, user_link_to: Agent):
        self.user_links.append((user_link_from.identifier, user_link_to.identifier))
        user_link_to.increase_followers()

    def get_timeline(self, user_id: int) -> list[dict]:
        """
        Gets the timeline -> all posts and reposts of users linked to the user.
        """

        # Get the id's of the users linked to the user
        linked_users = [link[1] for link in self.user_links if link[0] == user_id]

        return [post for post in self.posts if post["user_id"] in linked_users]
    
    def post(self, user: Agent, content: str):
        """
        User posts a message.
        """

        timestamp = datetime.now()
        post = Post(len(self.posts)+1, user.identifier, timestamp, content)

        # TODO: Time?
        # TODO: Keep track of reposts
        self.posts.append({
            "post_id": post.post_id,
            "user_id": user.identifier,
            "time": timestamp,
            "post_content": post
        })

    def repost(self, user: Agent, post_id: int):
        """
        User reposts a message.
        """

        timestamp = datetime.now()
        post = self.get_post(post_id)
        post.count_repost()

        self.posts.append({
            "post_id": len(self.posts)+1,
            "user_id": user.identifier,
            "time": timestamp,
            "post_content": post
        })

    