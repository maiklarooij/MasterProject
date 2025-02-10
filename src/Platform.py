from datetime import datetime

from Agent import Agent, Action
import random

from openai import OpenAI

class Post():
    def __init__(self, post_id: int, author: Agent, timestamp: datetime, content: str):
        self.post_id = post_id
        self.author = author
        self.timestamp = timestamp
        self.content = content
        
        self.reposts = 0
        self.reposters = []

    def __str__(self):
        return f"""Post ID: {self.post_id}\nPosted by: user with {self.author.followers} followers\nReposts: {self.reposts}\nContent: {self.content}"""
    
    def __repr__(self):
        return f"User {self.author} posted: {self.content}"
    
    def json(self):
        return {
            "post_id": self.post_id,
            "author": self.author.identifier,
            "timestamp": self.timestamp,
            "content": self.content,
            "reposts": self.reposts,
            "reposters": self.reposters
        }
    
    def count_repost(self, reposter_id: int):
        self.reposters.append(reposter_id)
        self.reposts += 1

    def reposted_by(self, reposter_id: int):
        return reposter_id in self.reposters

class Platform():

    def __init__(self):
        self.users: list[Agent] = []

        # Of the form {"user_id": int, "time": int, "content": str, "repost": bool, "repost_user_id": int}
        self.posts: list[dict] = []

        self.raw_posts: list[Post] = []

        # Of the form (user_id_link_from, user_id_link_to)
        self.user_links: list[(int, int)] = []

        self.actions: list[dict] = []

    def set_client(self, client: OpenAI | None):
        for user in self.users:
            user.llm = client

    def initialize_random_links(self, nr_links: int):
        """
        Cold-start: randomly link users to each other.
        The fraction determines the fraction of users to link to.
        """

        for user in self.users:
            
            # Randomly select a fraction of the users to link to
            linked_users = random.sample(self.users, nr_links)
            for linked_user in linked_users:
                if linked_user != user:
                    self.link_users(linked_user, user)

    def sample_user(self) -> Agent:
        return random.choice(self.users)
    
    def generate_posts_json(self):

        final_json = []

        for post in self.posts:

            final_json.append({
                "post_id": post["post_id"],
                "user_id": post["user_id"],
                "time": post["time"],
                "post_content": post["post_content"].json()
            })

        return final_json

    def generate_users_json(self):

        return [user.json() for user in self.users]
    
    def generate_log(self):

        total_input_tokens = sum([user.used_tokens_input for user in self.users])
        total_output_tokens = sum([user.used_tokens_output for user in self.users])
        total_cached_tokens = sum([user.used_tokens_cached for user in self.users])

        predicted_cost = ((0.6 / 1000000) * total_output_tokens) + \
                            ((0.15 / 1000000) * (total_input_tokens - total_cached_tokens) + \
                            ((0.075 / 1000000) * total_cached_tokens))

        return {
            "total_tokens_input": total_input_tokens,
            "total_tokens_output": total_output_tokens,
            "total_tokens_cached": total_cached_tokens,
            "predicted_cost": predicted_cost,
            "users": self.generate_users_json(),
            "posts": self.generate_posts_json(),
            "raw_posts": [post.json() for post in self.raw_posts],
            "user_links": self.user_links,
            "actions": self.actions
        }

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

        # Link already exists
        if self.has_link(user_link_from.identifier, user_link_to.identifier):
            return
        
        # Don't allow self links
        if user_link_from == user_link_to:
            return

        self.user_links.append((user_link_from.identifier, user_link_to.identifier))
        user_link_to.increase_followers()

    def has_link(self, user_id_1: int, user_id_2: int) -> bool:
        return (user_id_1, user_id_2) in self.user_links

    def get_follower_count(self, user_id: int) -> int:
        """
        Get the number of followers of the user.
        """

        user = self.get_user(user_id)
        return user.followers

    def get_timeline(self, user_id: int, size: int) -> list[dict]:
        """
        Gets the timeline -> all posts and reposts of users linked to the user.
        """

        # Get the id's of the users linked to the user
        linked_users = [link[1] for link in self.user_links if link[0] == user_id]

        # Only show posts and reposts by linked users
        # Exclude posts that are already reposted by the user
        timeline = [post for post in self.posts if post["user_id"] in linked_users and not post["post_content"].reposted_by(user_id)
                    and not post['post_content'].author.identifier == user_id]

        # Sort timelime by time
        timeline.sort(key=lambda x: x["time"], reverse=True)

        return timeline[:size]
    
    def post(self, user: Agent, content: str):
        """
        User posts a message.
        """

        timestamp = datetime.now()
        post = Post(len(self.posts)+1, user, timestamp, content)

        self.raw_posts.append(post)

        self.posts.append({
            "post_id": post.post_id,
            "user_id": user.identifier,
            "time": timestamp,
            "post_content": post
        })

    def repost(self, user: Agent, post_id: int, link_users: bool = True):
        """
        User reposts a message.
        """

        timestamp = datetime.now()
        post = self.get_post(post_id)

        if post.author.identifier == user.identifier:
            raise Exception(f"User {user.identifier} tries to repost its own post {post_id}!")

        if post.reposted_by(user.identifier):
            raise Exception(f"User {user.identifier} has already reposted post {post_id}!")

        post.count_repost(user.identifier)

        if link_users:
            self.link_users(user, post.author)

        self.posts.append({
            "post_id": len(self.posts)+1,
            "user_id": user.identifier,
            "time": timestamp,
            "post_content": post
        })

    def add_action(self, user_id: int, action: Action, success: bool, prompt: str):
        """
        Adds action to the platform for logging purposes.
        """
        self.actions.append({
            "user_id": user_id,
            "action": action.option,
            "content": action.content,
            'success': success,
            'explanation': action.explanation,
            "prompt": prompt
        })

    def parse_and_do_action(self, user_id: int, action: Action, prompt: str) -> None:

        agent = self.get_user(user_id)

        if not agent:
            print("User not found")
            self.add_action(user_id, action, False, prompt)
            return
        
        if action.option == 2:
            self.post(agent, action.content)
        elif action.option == 1:

            try:
                self.repost(agent, int(action.content), link_users=True)
            except Exception as e:
                print("Invalid post ID: ", e)
                self.add_action(user_id, action, False, prompt)
                return
        elif action.option == 3:
            pass
        else:
            print("Invalid action")
            self.add_action(user_id, action, False, prompt)

        self.add_action(user_id, action, True, prompt)

    