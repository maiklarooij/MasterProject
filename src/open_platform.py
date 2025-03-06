import pickle
from Platform import Platform
import json

platform: Platform = pickle.load(open('../results/platform_10.pkl', 'rb'))

json.dump(platform.generate_log(), open('../results/log_10_b.json', 'w'), indent=4, default=str)