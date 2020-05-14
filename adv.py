from room import Room
from player import Player
from world import World
from util import Stack, Queue  # These may come in handy

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
my_key_graph = {
    "all_rooms": [],
    "path_to_go": []#make this a list of node order to follow and then convert to directions based on room.direction keys
}
traversal_path = []

### Get all the rooms
#can I get the rooms use DFT?
s = Stack()
s.push(player.current_room) #difrent paramiter
all_rooms = set() # Keep track of visited nodes

while s.size() > 0:# Repeat until queue is empty
    here = s.pop() # Dequeue first vert
    if here.id not in all_rooms: # If it's not visited:
        #print(v)
        all_rooms.add(here.id) # Mark visited
        my_key_graph[ str(here.id) ] = {
            "visited": False,
            "n": None,
            "s": None,
            "e": None,
            "w": None
        }
        my_key_graph["all_rooms"].append(here.id)
        for x in here.get_exits():
            my_key_graph[ str(here.id) ][x] = here.get_room_in_direction(x).id
            s.push(here.get_room_in_direction(x))
#for room in all_rooms:
#    print(room)
#print(my_key_graph)

### Path fo go from room[0] to next taget not visted to do that...
#can I use DFS to get legs of roomX to roomY?
def dfs(starting_vertex, destination_vertex):
    s = Stack()
    s.push([starting_vertex])
    visited = set()

    while s.size() > 0:
        path = s.pop()
        vertex = path[-1] #the room
        if vertex not in visited:
            visited.add(vertex) # Mark it as visited...
            if vertex == destination_vertex:
                return path # IF SO, RETURN PATH
            else:# Then add A PATH TO its neighbors to the back of the queue
                for x in world.rooms[vertex].get_exits():
                    s.push([*path, world.rooms[vertex].get_room_in_direction(x).id])

    return visited

### Need a loop recurshiuon that will re run this for each leg
first_start = player.current_room.id
my_key_graph[ str(player.current_room.id) ]["visited"] = True
my_key_graph["path_to_go"].append(player.current_room.id)
#print(my_key_graph[ str(player.current_room.id) ]["visited"])
go_to_room = "no Room Yet"#my_key_graph["all_rooms"][1]
for index in range( 0, len(my_key_graph["all_rooms"]) ):
#for index in range( 0, 500 ):
#for x in my_key_graph["all_rooms"]:
    if my_key_graph[ str(my_key_graph["all_rooms"][index]) ]["visited"] == True:
        pass
    else: #triggers on next not visted room
        #pass
        #print(my_key_graph[ str(my_key_graph["all_rooms"][index]) ])
        go_to_room = my_key_graph["all_rooms"][index]
        path_leg = dfs(first_start, go_to_room)
        first_start = path_leg[len(path_leg)-1]
        #print(path_leg)
        #print(path_leg[len(path_leg)-1])
        for room in path_leg:
            my_key_graph[ str(room) ]["visited"] = True
            if room != my_key_graph["path_to_go"][len(my_key_graph["path_to_go"])-1]:
                my_key_graph["path_to_go"].append(room)
print(my_key_graph["path_to_go"])

### translate to directions



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
