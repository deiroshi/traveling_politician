import json
import random
import math

# Load the state capitals data
with open ("us_state_capitals.json", "r") as f:
    all_capitals = json.load(f) ["state_capitals"]

# Get capital by state name
def get_capital(state_name):
    for capital in all_capitals:
        if capital["state"].lower() == state_name.lower(): # Not case sensitive
            return capital
    return None

# Fix route: start, 3 middle, end 
start = get_capital("Iowa")
end = get_capital("District of Columbia")
middle = [
    get_capital("Georgia"),
    get_capital("California"),
    get_capital("New York")
]

# Shuffle the middle?
random.shuffle(middle) 

initial_route = [start] + middle + [end] # [dict] + [dict, dict, dict] + [dict]

# Haversine formula
def haversine(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
# The math that figures out how far apart the points are on a sphere.
# It combines the latitude and longitude differences into one formula.
    a = math.sin(dlat / 2)**2 + math.cos(lat1) + math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    radius = 3959 # Radius of the Earth in miles
    return radius * c # Return distance in miles


# Total route distance
def total_distance(route):
    total_miles = 0
    for i in range(len(route) - 1):
        coords1 = (route[i]["coordinates"]["lat"], route[i]["coordinates"]["lon"])
        coords2 = (route[i + 1]["coordinates"]["lat"], route[i + 1]["coordinates"]["lon"])
        total_miles += haversine(coords1, coords2)
    return total_miles

# Simulated Annealing 
def s_a(route, temp=100, cooling_rate=0.95, max_iter=100): # How open to mistakes, max number of times the algorithm will try new routes
    current = route[1:-1] # Exclude start and end
    best = current[:] # Copy current to best to track the best version found so far

    current_distance = total_distance([route[0]] + current + [route[-1]]) # Calculate distance for the current route
    best_distance = current_distance

    for i in range(max_iter):
        # Create a new route by swapping two cities
        new_route = current[:] # Copy current route
        a, b = random.sample(range(len(new_route)), 2) # Pich 2 random
        new_route[a], new_route[b] = new_route[b], new_route[a] # Swap them

        new_distance = total_distance([route[0]] + new_route + [route[-1]]) 
        delta = new_distance - current_distance # How much the distance changed

        if delta < 0 or random.random() < math.exp(-delta / temp): # Formula that gives a chance to accept a worse route
            current = new_route
            current_distance = new_distance

            if current_distance < best_distance:
                best = new_route[:] 
                best_distance = new_distance
       
        temp *= cooling_rate

        if i % 50 == 0:
            print(f"Iteration {i}, Distance: {round(best_distance, 2)} miles")
        
    return [route[0]] + best + [route[-1]], best_distance 

# Optimize the route
optimized_route, best_distance = s_a(initial_route)

# Results
print("\nOptimized Route:")
for city in optimized_route:
    print(f"{city['state']} - {city['capital']}")

print(f"\nTotal Distance: {round(best_distance, 2)} miles")