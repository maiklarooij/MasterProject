# Example
f = open('../results/other_partisan.txt', 'r')

data = f.readlines()

f.close()

curr_sim_accepts = 0
curr_sim_rejects = 0
curr_sim_links = []

all_sim_accepts = []
all_sim_rejects = []

for line in data:

    if line.startswith("Running simulation"):

        if curr_sim_accepts != 0 or curr_sim_rejects != 0:
            print(f"Simulation {len(all_sim_accepts) + 1} - Accepts: {curr_sim_accepts}, Rejects: {curr_sim_rejects}, Total Links: {len(curr_sim_links)}")
            all_sim_accepts.append(curr_sim_accepts)
            all_sim_rejects.append(curr_sim_rejects)

        curr_sim_accepts = 0
        curr_sim_rejects = 0
        curr_sim_links = []

    if 'chose not to link' in line:

        splitted_line = line.split()
        user1 = splitted_line[1]
        user2 = splitted_line[-1]

        if (user1, user2) not in curr_sim_links:
            curr_sim_rejects += 1
    
    elif 'linked to' in line:
        splitted_line = line.split()
        user1 = splitted_line[1]
        user2 = splitted_line[-1]
    
        if (user1, user2) not in curr_sim_links:
            curr_sim_links.append((user1, user2))
            curr_sim_accepts += 1

if curr_sim_accepts != 0 or curr_sim_rejects != 0:
    print(f"Simulation {len(all_sim_accepts) + 1} - Accepts: {curr_sim_accepts}, Rejects: {curr_sim_rejects}, Total Links: {len(curr_sim_links)}")
    all_sim_accepts.append(curr_sim_accepts)
    all_sim_rejects.append(curr_sim_rejects)
    print(f"Total Accepts: {sum(all_sim_accepts)}, Total Rejects: {sum(all_sim_rejects)}")

accept_percentages = []
reject_percentages = []

for i in range(len(all_sim_accepts)):
    print(f"Simulation {i + 1} - Accepts: {all_sim_accepts[i]}, Rejects: {all_sim_rejects[i]}, Total Links: {len(curr_sim_links)}")

    #percentages
    total_links = all_sim_accepts[i] + all_sim_rejects[i]
    if total_links > 0:
        accept_percentage = (all_sim_accepts[i] / total_links) * 100
        reject_percentage = (all_sim_rejects[i] / total_links) * 100
    else:
        accept_percentage = 0
        reject_percentage = 0
    print(f"Simulation {i + 1} - Accept Percentage: {accept_percentage:.2f}%, Reject Percentage: {reject_percentage:.2f}%")

    accept_percentages.append(accept_percentage)
    reject_percentages.append(reject_percentage)

print(f"Average Accept Percentage: {sum(accept_percentages) / len(accept_percentages):.2f}%")
print(f"Average Reject Percentage: {sum(reject_percentages) / len(reject_percentages):.2f}%")
