# MasterProject

Code for thesis titled "Testing Prosocial Interventions on Social Media Through Generative Simulation" by Maik Larooij.

## How to run?

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Fill in the necessary API keys in a `.env` file:
   ```plaintext
   OPENAI_API_KEY=YOUR_KEY
   PERSPECTIVE_API_KEY=YOUR_KEY
   ```
3. Edit the main script to set the size of the simulation, the number of steps and strategies in the call to the function `run_simulation` in `main.py`:
   ```python
   run_simulation(simulation_size=500, simulation_steps=10000, 
                       user_link_strategy="on_repost_bio", 
                       timeline_select_strategy="other_partisan",
                       show_info=True, run_nr=i)
   ```
4. Run the main script:
   ```bash
   python main.py > output.txt
   ```

Outputs will be saved in results folder - a Pickle file with the whole platform state and a JSON file with results.