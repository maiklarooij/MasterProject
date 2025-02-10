import json
import random

from pydantic import BaseModel

from openai import OpenAI
from openai.types.chat import ParsedChoice

class Action(BaseModel):
    option: int
    content: str
    explanation: str

class Agent():

    def __init__(self, model: str, persona_path: str):
        
        self.persona = self._generate_persona(persona_path)

        self.llm = None
        self.model = model

        self.identifier = 0
        self.followers = 0

        self.used_tokens_input = 0
        self.used_tokens_output = 0
        self.used_tokens_cached = 0

    def __repr__(self):
        return f"User {self.identifier} with {self.followers} followers"
    
    def __str__(self):
        return f"User {self.identifier} with {self.followers} followers"

    def _generate_persona(self, persona_path: str) -> str:
        """
        From a list of personas, randomly select one to use as the agent's persona.
        """
        
        persona_list = json.load(open(persona_path, 'r'))
        return random.choice(persona_list)
    
    def _generate_sys_msg(self) -> str:
        """
        Generate a system message to introduce the agent to the system and its persona.
        """

        sys_msg = f"""You are a user of the X social media platform. 
                    This is a platform where users share opinions and thoughts on topics of interest in the form of posts.
                    You main goal is to repost others' posts and you are also able to share your own posts.

                    Here is a description of your persona:
                    {self.persona['persona']}
        """

        return sys_msg
    
    def json(self):
        return {
            "identifier": self.identifier,
            "followers": self.followers,
            "used_tokens_input": self.used_tokens_input,
            "used_tokens_output": self.used_tokens_output,
            "used_tokens_cached": self.used_tokens_cached,
            "persona": self.persona
        }
    
    def increase_followers(self):
        self.followers += 1
    
    def get_response(self, message: str, response_format = None) -> ParsedChoice:
        """
        Get the response from the agent to the given message.
        """

        response = self.llm.beta.chat.completions.parse(
            model=self.model,
            messages = [
                {"role": "system", "content": self._generate_sys_msg()},
                {"role": "user", "content": message}
            ],
            response_format=response_format

        )


        self.used_tokens_input += response.usage.prompt_tokens
        self.used_tokens_output += response.usage.completion_tokens
        self.used_tokens_cached += response.usage.prompt_tokens_details.cached_tokens
        
        return response.choices[0]
    
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
        
        return self.get_response(msg).content
    
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

        return self.get_response(msg).content


    def perform_action(self, news_data: list, timeline: list) -> Action:

        msg = """You are presented with the following options. You have to choose exactly one option based on your persona.
1. Choose exactly one of the posts from the timeline to repost on your social media feed that relates to your persona. [You can't repost if there are no posts on the timeline. Only write down the message ID as content!]
2. Choose exactly one of the headlines to share on your social media feed based on your persona, and write a comment of 10-50 words about that one headline in the style of your personality. [Write only the message you want to share as content. Don't repeat the title of the headline, but introduce the topic briefly. You may choose news you agree or do not agree with and share this vision. Do not use quotation marks. Do not introduce yourself. Use informal language. You may write a positive message, but you may also use sarcasm or irony, swear, criticize, threat, lie, and engage in personal attacks. You can also bring up a related topic that the post made you think of. Do not start your message by describing your persona. Don't use hashtags.]
3. Do nothing. [You can choose this option if you don't feel like sharing anything at the moment, or if you want to observe the platform for a while.]
Also provide an explanation of one sentence about your choice.
Reply in JSON format.\n\n"""

        msg += """Here are the messages on the timeline for option 1:\n"""

        for post in timeline:

            msg += str(post['post_content'])
            msg += "\n\n"

        msg += """Here are the news headlines for option 2:\n"""

        for i, news_item in enumerate(news_data, start=1):

            msg += f"""ID: {i}\nTitle: {news_item['headline']}\nCategory: {news_item['category']}\nDescription: {news_item['short_description']}\n\n"""

        # Get response and handle the action
        response = self.get_response(msg, response_format=Action)

        return response.message.parsed, msg
