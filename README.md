# U.S. State Capitals Route Optimization with Simulated Annealing

This project uses **Simulated Annealing**, a probabilistic optimization algorithm, to solve a version of the **Traveling Salesman Problem (TSP)** over all 50 U.S. state capitals. The goal is to find a near-optimal route that visits every state capital **exactly once**, starting in **Iowa** and ending in **Washington, D.C.**, while minimizing the total travel distance (in miles).


## Features

- Reads full capital data from a structured JSON file (`us_state_capitals.json`)
- Calculates geodesic distance using the **Haversine formula**
- Clusters states into 5 regional groups to reduce computation time
- Applies **Simulated Annealing** to optimize both clusters and the full route
- Outputs the final optimized route with total distance


## Output Example

Optimized Full Route Through All States:

Iowa - Des Moines -> 
Alaska - Juneau -> 
Washington - Olympia -> 
Oregon - Salem -> 
Idaho - Boise -> 
Montana - Helena -> 
Utah - Salt Lake City -> 
Arizona - Phoenix -> 
Nevada - Carson City -> 
California - Sacramento -> 
Hawaii - Honolulu -> 
New Mexico - Santa Fe -> 
Colorado - Denver -> 
South Dakota - Pierre -> 
North Dakota - Bismarck -> 
Minnesota - Saint Paul -> 
Nebraska - Lincoln -> 
Kansas - Topeka -> 
Oklahoma - Oklahoma City -> 
Texas - Austin -> 
Louisiana - Baton Rouge -> 
Mississippi - Jackson -> 
Arkansas - Little Rock -> 
Missouri - Jefferson City -> 
Illinois - Springfield -> 
Wisconsin - Madison -> 
Indiana - Indianapolis -> 
Kentucky - Frankfort -> 
Tennessee - Nashville -> 
Alabama - Montgomery -> 
Florida - Tallahassee -> 
Georgia - Atlanta -> 
South Carolina - Columbia -> 
North Carolina - Raleigh -> 
Virginia - Richmond -> 
Maryland - Annapolis -> 
West Virginia - Charleston -> 
Ohio - Columbus -> 
Michigan - Lansing -> 
Pennsylvania - Harrisburg -> 
Delaware - Dover -> 
New Jersey - Trenton -> 
Connecticut - Hartford -> 
Rhode Island - Providence -> 
Massachusetts - Boston -> 
New Hampshire - Concord -> 
New York - Albany -> 
Vermont - Montpelier -> 
Maine - Augusta -> 
District of Columbia - Washington, D.C.

Total Distance: 19190.29 miles


## How It Works

1. **Capitals Data**  
   Loaded from a JSON file containing name, coordinates, and capital info.

2. **Preprocessing**  
   Capitals are sorted by longitude and divided into 5 clusters (10 states each).

3. **Local Optimization**  
   Each cluster is optimized with Simulated Annealing to reduce subroute lengths.

4. **Global Optimization**  
   Clusters are merged and the full route is re-optimized (excluding fixed start/end).

5. **Final Output**  
   Optimized list of capitals and total distance printed to the console.


## Files

`main_tpp.py` - The main script that solves the full Traveling Salesman Problem (TSP) for all 50 U.S. state capitals.  
- Starts in Iowa and ends in Washington, D.C.  
- Uses Simulated Annealing to find an efficient route.  
- Divides capitals into 5 clusters for faster optimization.

`us_state_capitals.json` - A structured JSON file containing all 50 state capitals, including:  
- State name  
- Capital name  
- Latitude and longitude

`georgia_california_newyork.py` - A small test script that finds the shortest route from Iowa through Georgia, California, and New York, ending in Washington, D.C.  
- First test to understand TSP logic.

`random_3_s.p` - A practice script that solves TSP through 3 randomly chosen capitals (plus Iowa -> DC).  
- Second test to experiment with random subsets and route calculation.

`m_states.py` - A focused script that optimizes a route through the 8 U.S. state capitals starting with the letter “M”.  
- Last practice test before building the full solution.
