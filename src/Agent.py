import json
import random

from camel.agents import ChatAgent
from camel.models import ModelFactory

class Agent():

    def __init__(self, model: ModelFactory, persona_path: str):
        
        self.persona = self._generate_persona(persona_path)
        self.llm = ChatAgent(model=model, system_message=self._generate_sys_msg())

        self.identifier = 0
        self.followers = 0

    def __repr__(self):
        return f"User {self.identifier} with {self.followers} followers"
    
    def __str__(self):
        return f"User {self.identifier} with {self.followers} followers"

    def _generate_persona(self, persona_path: str) -> str:
        """
        From a list of personas, randomly select one to use as the agent's persona.
        """
        
        persona_list = json.load(open(persona_path, 'r'))
        return random.choice(persona_list)['persona']
    
    def _generate_sys_msg(self) -> str:
        """
        Generate a system message to introduce the agent to the system and its persona.
        """

        sys_msg = f"""You are a user of the X social media platform. 
                    This is a platform where users share opinions and thoughts on topics of interest in the form of posts.
                    You are able to share your own posts and repost others' posts.

                    Here is a description of your persona:
                    {self.persona}
        """

        return sys_msg
    
    def increase_followers(self):
        self.followers += 1
    
    def get_response(self, message: str) -> str:
        """
        Get the response from the agent to the given message.
        """

        response = self.llm.step(message)
        return response.msgs[0].content
    
    def news_post(self, news_data: dict) -> str:
        """
        Generate a news post from the given news data.
        """

        msg = f"""
            You stumble upon the following piece of news:
            Title: {news_data['headline']}
            Category: {news_data['category']}
            Description: {news_data['short_description']}

            You are going to:
            1. Choose critically if you want to share your thoughts on the news.
            2. If you choose to share your thoughts, you will write a post about it, limited to 280 characters.

            The post may be a little informal.

            If you decide to not share your thoughts, reply with 'no'. Then explain why you chose not to share your thoughts.
            If you decide to share your thoughts, reply with the content of your post. Then, explain why you chose to share your thoughts.
        """

        # TODO: Check if there are response templates
        
        return self.get_response(msg)
    
    def multiple_news_post(self, news_data: list) -> str:

        msg = """
            You stumble upon the following pieces of news:
            """
        
        for i, news_item in enumerate(news_data, start=1):

            msg += f"""
                ID: {i}
                Title: {news_item['headline']}
                Category: {news_item['category']}
                Description: {news_item['short_description']}\n
            """

        msg += """Choose exactly one of these headlines to share on your social media feed based on your persona, and write a comment of 10-50 words about that one headline in the style of your personality. [Write only the message. Introduce the news very shortly. You may choose news you do not agree with and share this vision. Do not use quotation marks. Do not introduce yourself. Use informal language. You may use sarcasm or irony, swear, criticize, threat, lie, and engage in personal attacks. You can also bring up a related topic that the post made you think of. Do not start your message by describing your persona. Don't use hashtags.]"""

        return self.get_response(msg)

    def perform_action(self, news_data: list, timeline: list) -> str:

        msg = """You are presented with the following options. You have to choose exactly one option based on your persona.
1. Choose exactly one of the headlines to share on your social media feed based on your persona, and write a comment of 10-50 words about that one headline in the style of your personality. [Write only the message. Don't repeat the headline, but introduce the topic briefly. You may choose news you do not agree with and share this vision. Do not use quotation marks. Do not introduce yourself. Use informal language. You may use sarcasm or irony, swear, criticize, threat, lie, and engage in personal attacks. You can also bring up a related topic that the post made you think of. Do not start your message by describing your persona. Don't use hashtags.]
2. Choose exactly one of the posts from the timeline to repost on your social media feed based on your persona. [Only write down the message ID]
3. Do nothing. [You can choose this option if you don't feel like sharing anything at the moment, or if you want to observe the platform for a while.]
Reply with the number of the option you choose and then the content of your action.

Here are the news headlines for option 1:\n"""

        for i, news_item in enumerate(news_data, start=1):

            msg += f"""ID: {i}\nTitle: {news_item['headline']}\nCategory: {news_item['category']}\nDescription: {news_item['short_description']}\n\n"""

        msg += """Here are the messages on the timeline for option 2:\n"""

        for post in timeline:

            msg += str(post['post_content'])

        # with open('msg.txt', 'w') as f:
        #     f.write(msg)

        return self.get_response(msg)