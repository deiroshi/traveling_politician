import json
import random
import math

# Load the state capitals
with open("us_state_capitals.json", "r") as f:
    all_capitals = json.load(f)["state_capitals"]

# Get capital by state name
def get_capital(state_name):
    for capital in all_capitals:
        if capital["state"].lower() == state_name.lower():
            return capital
    return None

# Define start and end
start = get_capital("Iowa")
end = get_capital("District of Columbia")

# Get 3 random middle states, excluding Iowa and DC
middle = [
    capital for capital in all_capitals
    if capital["state"].lower() not in ("iowa", "district of columbia")
]
middle = random.sample(middle, 3)

initial_route = [start] + middle + [end]

# Haversine formula
def haversine(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 3959 * c  # Earth radius in miles

# Total route distance
def total_distance(route):
    total_miles = 0
    for i in range(len(route) - 1):
        coords1 = (route[i]["coordinates"]["lat"], route[i]["coordinates"]["lon"])
        coords2 = (route[i + 1]["coordinates"]["lat"], route[i + 1]["coordinates"]["lon"])
        total_miles += haversine(coords1, coords2)
    return total_miles

# Simulated Annealing
def s_a(route, temp=1000, cooling_rate=0.995, max_iter=3000):
    current = route[1:-1]
    best = current[:]
    current_distance = total_distance([route[0]] + current + [route[-1]])
    best_distance = current_distance

    for i in range(max_iter):
        new_route = current[:]
        a, b = random.sample(range(len(new_route)), 2)
        new_route[a], new_route[b] = new_route[b], new_route[a]
        new_distance = total_distance([route[0]] + new_route + [route[-1]])
        delta = new_distance - current_distance

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = new_route[:]
            current_distance = new_distance
            if current_distance < best_distance:
                best = new_route[:]
                best_distance = new_distance

        temp *= cooling_rate
        if i % 250 == 0:
            print(f"Iteration {i}, Distance: {round(best_distance, 2)} mi")

    return [route[0]] + best + [route[-1]], best_distance

# Optimize the route
optimized_route, best_distance = s_a(initial_route)

# Results
print("\nOptimized Route:")
for city in optimized_route:
    print(f"{city['state']} - {city['capital']}")

print(f"\nTotal Distance: {round(best_distance, 2)} miles")
