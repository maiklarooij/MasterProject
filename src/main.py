import dotenv
import os

from camel.models import ModelFactory
from camel.configs import ChatGPTConfig
from camel.types import ModelPlatformType, ModelType

from Agent import Agent
from Platform import Platform
from NewsFeed import NewsFeed

dotenv.load_dotenv()

if __name__ == "__main__":

    # Define the model, gpt-4o-mini
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
        model_config_dict=ChatGPTConfig().as_dict()
    )

    # Define the path to the persona file
    persona_path = os.path.join(os.getcwd(), 'personas.json')

    platform = Platform()

    # Create an instance of the Agent class
    agent1 = Agent(model, persona_path)
    agent2 = Agent(model, persona_path)

    # Register the agents with the platform
    platform.register_user(agent1)
    platform.register_user(agent2)

    print(platform.users)

    news_feed = NewsFeed('../News/News_Category_Dataset_v3.json')

    news_items = news_feed.get_random_news(10)
    
    # Agent 1 posts about a news item
    post1 = agent1.multiple_news_post(news_items)
    if post1 != 'no':
        print(agent1)
        print(post1)
        print()

        platform.post(agent1, post1)

    # Agent 2 reposts and forms a link to Agent 1
    platform.repost(agent2, 1)
    platform.link_users(agent2, agent1)

    # Show all posts
    print(platform.posts)

    # Show the timeline of Agent 2
    print(platform.get_timeline(2))

    # Show the links of the platform
    print(platform.user_links)