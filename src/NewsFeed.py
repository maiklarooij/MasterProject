import json
import random

class NewsFeed():

    def __init__(self, news_dataset_path: str):
        self.path = news_dataset_path

    def get_random_news(self, nr_of_items: int) -> list[dict]:
        """
        Get a list of news items from the dataset.
        """
        
        news_items = json.load(open(self.path, 'r'))
        return random.sample(news_items, nr_of_items)
    
    def get_random_news_str(self, nr_of_items: int) -> str:
        """
        Get a string representation of a list of news items.
        """
        
        news_items = self.get_random_news(nr_of_items)
        msg = ""

        for i, news_item in enumerate(news_items, start=1):

            msg += f"""
                ID: {i}
                Title: {news_item['headline']}
                Category: {news_item['category']}
                Description: {news_item['short_description']}\n\n
            """
        return msg

    