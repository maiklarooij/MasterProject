import json
import random

from pydantic import BaseModel

from openai import OpenAI
from openai.types.chat import ParsedChoice

class Action(BaseModel):
    option: int
    content: str
    explanation: str

class BooleanAction(BaseModel):
    choice: str
    explanation: str

class Agent():

    def __init__(self, model: str, persona: dict = None):
        
        self.persona = persona

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
        Not used anymore due to the persona being passed as an argument to enforce consistency.
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
    
    def json(self, include_persona: bool = False):
        """
        Return the agent's data in JSON format.
        """
        
        result = {
            "identifier": self.identifier,
            "followers": self.followers,
            "used_tokens_input": self.used_tokens_input,
            "used_tokens_output": self.used_tokens_output,
            "used_tokens_cached": self.used_tokens_cached
        }

        if include_persona:
            result['persona'] = self.persona

        return result
    
    def increase_followers(self):
        """
        Increase the number of followers by 1.
        """
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

        # Keep track of the tokens used for cost analysis
        self.used_tokens_input += response.usage.prompt_tokens
        self.used_tokens_output += response.usage.completion_tokens
        self.used_tokens_cached += response.usage.prompt_tokens_details.cached_tokens
        
        return response.choices[0]
    
    def link_with_user_on_bio(self, other_agent: 'Agent', post_content: str) -> str:
        """
        Supply the bio of another agent and let the user decide if they want to follow them.
        """

        msg = f"""
            You reposted this post:
            {post_content}

            You view the profile of the poster.
            Based on your beliefs, interests and personality, would you like to follow this user?
            User ID: {other_agent.identifier}
            Followers: {other_agent.followers}
            Bio: {other_agent.persona['biography']}

            Reply with 'yes' or 'no'. Also provide a short explanation for your choice.
        """

        response = self.get_response(msg, BooleanAction).message.parsed

        return True if response.choice.lower() == 'yes' else False, response.explanation
    
    def perform_action(self, news_data: list, timeline: list) -> Action:
        """
        The user is presented with a set of options to choose from based on their persona.
        - Repost a post from the timeline
        - Share a news headline with a comment
        - Do nothing
        """

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

