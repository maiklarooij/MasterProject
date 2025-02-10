import dotenv
import os
import json
import pickle

from openai import OpenAI

from Agent import Agent
from Platform import Platform
from NewsFeed import NewsFeed

dotenv.load_dotenv()

def log_action(user, action):

    log_msg = f"User {user.identifier} chose action "

    if action.option == 1:
        log_msg += "1, repost."
        log_msg += f"User reposted message with ID {action.content}\n"
    elif action.option == 2:
        log_msg += "2, post.\n"
        log_msg += f"User wrote: {action.content}\n"
    elif action.option == 3:
        log_msg += "3, do nothing.\n"
    else:
        log_msg += f"{action.option}, which is invalid.\n"

    return log_msg

if __name__ == "__main__":

    # Define the model, gpt-4o-mini
    # model = ModelFactory.create(
    #     model_platform=ModelPlatformType.OPENAI,
    #     model_type=ModelType.GPT_4O_MINI,
    #     model_config_dict=ChatGPTConfig().as_dict()
    # )

    # Define the path to the persona file
    persona_path = os.path.join(os.getcwd(), 'personas.json')

    platform = Platform()

    # Create an instance of the Agent class
    # agent1 = Agent(model, persona_path)
    # agent2 = Agent(model, persona_path)
    # agent3 = Agent(model, persona_path)

    # # Register the agents with the platform
    # platform.register_user(agent1)
    # platform.register_user(agent2)
    # platform.register_user(agent3)

    # print(platform.users)

    news_feed = NewsFeed('../News/News_Category_Dataset_v3.json')

    # news_items = news_feed.get_random_news(10)
    
    # # Agent 1 posts about a news item
    # post1 = agent1.multiple_news_post(news_items)
    # print(agent1)
    # print(post1)
    # print()

    # platform.post(agent1, post1)

    # # Agent 2 reposts and forms a link to Agent 1
    # platform.repost(agent2, 1)
    # platform.link_users(agent2, agent1)

    # # Show all posts
    # print(platform.posts)

    # # Show the timeline of Agent 2
    # print(platform.get_timeline(2))

    # # Show the links of the platform
    # print(platform.user_links)

    # # Agent 3 forms a link with Agent 2 and sees post of Agent 1
    # platform.link_users(agent3, agent2)
    # timeline = platform.get_timeline(3)

    # # Agent 3 performs an action -> post, repost or do nothing
    # print(agent3.perform_action(news_feed.get_random_news(10), timeline))

    # Register 10 users for simulation
    simulation_size = 25
    simulation_steps = 250
    run_id = 6
    model = "gpt-4o-mini"
    client = OpenAI()

    [platform.register_user(Agent(model, persona_path)) for _ in range(simulation_size)]
    platform.set_client(client)
    platform.initialize_random_links(2)

    print(platform.users)

    for _ in range(simulation_steps):

        print(f"Simulation step {_ + 1}")

        # Select a random user
        user = platform.sample_user()

        # Perform an action
        action, prompt = user.perform_action(news_feed.get_random_news(10), platform.get_timeline(user.identifier, 10))
        platform.parse_and_do_action(user.identifier, action, prompt)

        print(log_action(user, action))

    json.dump(platform.generate_log(), open(f'../results/log_{run_id}.json', 'w'), indent=4, default=str)

    # Set reuse of platform
    platform.set_client(None)
    client.close()

    pickle.dump(platform, open(f'../results/platform_{run_id}.pkl', 'wb'))
