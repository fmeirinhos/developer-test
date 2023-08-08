import sqlite3
import json
from functools import lru_cache
import os
import networkx as nx

def get_routes_from_db(db_path):
    """ Fetch routes from the database """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT origin, destination, travel_time FROM routes"
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error querying the database: {e}")
        return None

def create_graph(routes):
    """ Create an undirected graph from the given routes """
    G = nx.Graph()
    for origin, destination, travel_time in routes:
        G.add_edge(origin, destination, travel_time=travel_time, label=str(travel_time))
    return G

def parse_json(json_path):
    try:
        with open(json_path, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Error reading the file {json_path}: {e}")
        return None
    
def solve(mf_path, e_path):
    """ Loads Millenium Falcon and Empire configs and solves the problem """
    mf = parse_json(mf_path)
    e = parse_json(e_path)
    
    # Create universe graph, assuming only RELATIVE paths to the universe
    # g_path = os.path.join(os.path.dirname(mf_path), mf['routes_db'])
    g_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "databases/universe.db")

    g = create_graph(get_routes_from_db(g_path))
    
    return _solve(g, mf['departure'], mf['arrival'], mf['autonomy'], e['countdown'], e['bounty_hunters'])
    
def _solve(graph, departure, arrival, autonomy, countdown, bounty_hunters, prob_capture = 1 / 10, max_autonomy = 6):
    """ Algorithm to calculate the probability of success using dynamic programming and memoization """

    @lru_cache(maxsize=None)
    def func(planet, autonomy, day):
        # Could not reach the destination before the countdown
        if day > countdown:
            return 0.0
        
        success_factor = 1.0
        
        # Account for bounty hunters
        for bh in bounty_hunters:
            if bh['planet'] == planet and bh['day'] == day:
                success_factor *= 1.0 - prob_capture
        
        if planet == arrival:
            return success_factor
        
        # We either stay to refuel
        rest = func(planet, max_autonomy, day + 1)

        # Or exlplore the neighbors of the planet within reach
        for neighbor in graph.neighbors(planet):
            travel_time = graph[planet][neighbor]['travel_time']
            if autonomy >= travel_time:
                rest = max(rest, func(neighbor, autonomy - travel_time, day + travel_time))
        
        return success_factor * rest

    return func(departure, autonomy, 0)
