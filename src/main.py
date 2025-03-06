import dotenv
import os
import json
import pickle
import random

from openai import OpenAI

from Agent import Agent
from Platform import Platform
from NewsFeed import NewsFeed

dotenv.load_dotenv()

def log_action(user, action):
    """
    Log the action taken by the user to the console.
    """

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

def select_users(persona_path, n):
    """
    Create a sample of users for the simulation from the persona file.
    """

    # According to Gallup, 45% of Americans identify as Democrats, 46% as Republicans, and 9% as other (2025)
    fraction_democrat = 0.45
    fraction_republican = 0.46
    fraction_non_partisan = 0.09

    users = json.load(open(persona_path, 'r'))

    democrat_users = [user for user in users if user['party'] == 'Democrat']
    republican_users = [user for user in users if user['party'] == 'Republican']
    non_partisan_users = [user for user in users if user['party'] == 'Non-partisan']

    # Randomly sample users from each group
    democrat_sample = random.sample(democrat_users, int(n * fraction_democrat))
    republican_sample = random.sample(republican_users, int(n * fraction_republican))
    non_partisan_sample = random.sample(non_partisan_users, int(n * fraction_non_partisan))

    return democrat_sample + republican_sample + non_partisan_sample


if __name__ == "__main__":

    # Define the path to the persona file
    persona_path = os.path.join(os.getcwd(), 'personas_with_bio.json')
    news_feed = NewsFeed('../News/News_Category_Dataset_v3.json')

    # Set parameters for the simulation
    simulation_size = 100
    simulation_steps = 1500
    run_id = 12

    # Set strategies for the platform
    user_link_strategy = "on_repost_bio"
    timeline_select_strategy = "random_weighted"

    platform = Platform(user_link_strategy=user_link_strategy, timeline_select_strategy=timeline_select_strategy)
    
    # Ensure the right fraction of Democrats, Republicans, and non-partisans
    selected_users = select_users(persona_path, n=simulation_size)

    # Register users
    [platform.register_user(Agent(model, user)) for user in selected_users]

    # Set client for platform to OpenAI gpt-4o-mini
    model = "gpt-4o-mini"
    client = OpenAI()
    platform.set_client(client)

    for _ in range(simulation_steps):

        print(f"Simulation step {_ + 1}")

        # Select a random user
        user = platform.sample_user()

        # Perform an action
        action, prompt = user.perform_action(news_feed.get_random_news(10), platform.get_timeline(user.identifier, 10))
        platform.parse_and_do_action(user.identifier, action, prompt)

        print(log_action(user, action))

        # Add snapshot of the platform for analysis
        platform.add_snapshot()

    json.dump(platform.generate_log(), open(f'../results/log_{run_id}.json', 'w'), indent=4, default=str)

    # Set reuse of platform
    platform.set_client(None)
    client.close()

    pickle.dump(platform, open(f'../results/platform_{run_id}.pkl', 'wb'))
