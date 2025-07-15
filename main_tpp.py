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

# Haversine formula
def haversine(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    radius = 3959
    return radius * c

# Total route distance
def total_distance(route):
    total_miles = 0
    for i in range(len(route) - 1):
        coords1 = (route[i]["coordinates"]["lat"], route[i]["coordinates"]["lon"])
        coords2 = (route[i + 1]["coordinates"]["lat"], route[i + 1]["coordinates"]["lon"])
        total_miles += haversine(coords1, coords2)
    return total_miles

# Simulated Annealing
def s_a(route, temp=10000, cooling_rate=0.9995, max_iter=10000):
    current = route[:]
    best = route[:]

    current_distance = total_distance(current)
    best_distance = current_distance

    for i in range(max_iter):
        new_route = current[:]
        a, b = random.sample(range(len(new_route)), 2)
        new_route[a], new_route[b] = new_route[b], new_route[a]
        
        new_distance = total_distance(new_route)
        delta = new_distance - current_distance

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = new_route
            current_distance = new_distance

            if current_distance < best_distance:
                best = new_route[:]
                best_distance = new_distance
        
        temp *= cooling_rate
    
    return best


# Divide all capitals into 5 clusters of 10 (sorted roughly by longitude)
def get_longitude(city):
    return city["coordinates"]["lon"]

sorted_caps = sorted(all_capitals, key=get_longitude) # Key= tells py how to sort
clusters = []
i = 0
while i < 50:
    cluster = sorted_caps[i:i+10]
    clusters.append(cluster)
    i += 10

# Optimize each cluster
optimized_clusters = []
for cluster in clusters:
    optimized = s_a(cluster)
    optimized_clusters.append(optimized)

# Combine clusters into one full route
combined_route = []
for cluster in optimized_clusters:
    for city in cluster:
        combined_route.append(city)

# Find start and end
start = get_capital("Iowa")
end = get_capital("District of Columbia")

# Remove start and end from the middle if they are there already
filtered_route = []
for city in combined_route:
    if city["state"] != "Iowa" and city["state"] != "District of Columbia":
        filtered_route.append(city)

# Final route: start + optimized middle + end
optimized_middle = s_a(filtered_route)

final_route = [start]
for city in optimized_middle:
    final_route.append(city)
final_route.append(end)

total = total_distance(final_route)

# Results
print("\nOptimized Full Route Through All States:")
for city in final_route:
    print(f"{city['state']} - {city['capital']}")

print(f"\nTotal Distance: {round(total, 2)} miles")