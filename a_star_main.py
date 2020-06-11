
import numpy as np
import scipy.signal as signal
import scipy.stats as stats
import time

import matplotlib.pyplot as plt


# Structure:
#
# You have a starting point, and an endpoint
#
# You have the points on the grid around the starting point
# Starting point is a known coordinate. We don't really care about the
# distance (set as zero) or the heuristic score (set high)
#
# Find the point around the start that works well
# Add the points to an array
# Sort the points by their score
# Expand the lowest score point, find the points around that
# Add the expanded points to the array, remove the point we expanded from, and
# repeat until we get to the end and there are no other shorter paths to the end
#


# Global definition, obstacles

obstacles = [[5, 5],
             [5, 6],
             [5, 7],
             [7, 7],
             [8, 7],
             [9, 7],
             [3, 4],
             [3, 5],
             [2, 3],
             [4, 3],
             [4, 4],
             [2, 4],
             [12, 8],
             [11, 8],
             [13, 8]]

# obstacles = []







class Coord:

    def __init__(self, y, x, name, prev_coords):     #, old_y, old_x
        self.location = [y, x]
        self.name = name
        self.score = 100000000
        self.dist = 0
        self.combined_score = 100000000
        self.available = 1

        self.coord_array = prev_coords.copy()
        self.coord_array.append(self.location)

        # coord_array.append(self.location)

        # self.old_location = [old_y, old_x]





class Neighbours:

    def __init__(self, oy, ox, name, prev_coord):
        self.a = Coord(oy-1, ox-1, name+'->a', prev_coord)
        self.b = Coord(oy-1, ox, name+'->b', prev_coord)
        self.c = Coord(oy-1, ox+1, name+'->c', prev_coord)
        self.d = Coord(oy, ox-1, name+'->d', prev_coord)
        self.e = Coord(oy, ox+1, name+'->e', prev_coord)
        self.f = Coord(oy+1, ox-1, name+'->f', prev_coord)
        self.g = Coord(oy+1, ox, name+'->g', prev_coord)
        self.h = Coord(oy+1, ox+1, name+'->h', prev_coord)

        self.neighbours = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        self.neighbours_dist = []
        self.neighbours_scores = []
        self.neighbours_combined_scores = []


    def calculate_heuristic_score(self, end_point):

        for ele in self.neighbours:
            ele.score = np.sqrt(pow((end_point.location[0]-ele.location[0]), 2) + pow((end_point.location[1]-ele.location[1]), 2))
        #
        # self.a.score = np.sqrt(pow((end_point.location[0]-self.a.location[0]), 2) + pow((end_point.location[1]-self.a.location[1]), 2))
        # self.b.score = np.sqrt(pow((end_point.location[0] - self.b.location[0]), 2) + pow((end_point.location[1] - self.b.location[1]), 2))
        # self.c.score = np.sqrt(pow((end_point.location[0] - self.c.location[0]), 2) + pow((end_point.location[1] - self.c.location[1]), 2))
        # self.d.score = np.sqrt(pow((end_point.location[0] - self.d.location[0]), 2) + pow((end_point.location[1] - self.d.location[1]), 2))
        # self.e.score = np.sqrt(pow((end_point.location[0] - self.e.location[0]), 2) + pow((end_point.location[1] - self.e.location[1]), 2))
        # self.f.score = np.sqrt(pow((end_point.location[0] - self.f.location[0]), 2) + pow((end_point.location[1] - self.f.location[1]), 2))
        # self.g.score = np.sqrt(pow((end_point.location[0] - self.g.location[0]), 2) + pow((end_point.location[1] - self.g.location[1]), 2))
        # self.h.score = np.sqrt(pow((end_point.location[0] - self.h.location[0]), 2) + pow((end_point.location[1] - self.h.location[1]), 2))



        #
        # self.neighbours_scores = [self.a.score, self.b.score, self.c.score, self.d.score, self.e.score,
        #                           self.f.score, self.g.score, self.h.score]


    def calculate_dist(self, origin_coord):

        for ele in self.neighbours:
            ele.dist = np.sqrt(pow((origin_coord.location[0]-ele.location[0]), 2) + pow((origin_coord.location[1]-ele.location[1]), 2))

            ele.dist += origin_coord.dist

        # self.a.dist = np.sqrt(pow((origin_coord.location[0]-self.a.location[0]), 2) + pow((origin_coord.location[1]-self.a.location[1]), 2))
        # self.b.dist = np.sqrt(pow((origin_coord.location[0] - self.b.location[0]), 2) + pow((origin_coord.location[1] - self.b.location[1]), 2))
        # self.c.dist = np.sqrt(pow((origin_coord.location[0] - self.c.location[0]), 2) + pow((origin_coord.location[1] - self.c.location[1]), 2))
        # self.d.dist = np.sqrt(pow((origin_coord.location[0] - self.d.location[0]), 2) + pow((origin_coord.location[1] - self.d.location[1]), 2))
        # self.e.dist = np.sqrt(pow((origin_coord.location[0] - self.e.location[0]), 2) + pow((origin_coord.location[1] - self.e.location[1]), 2))
        # self.f.dist = np.sqrt(pow((origin_coord.location[0] - self.f.location[0]), 2) + pow((origin_coord.location[1] - self.f.location[1]), 2))
        # self.g.dist = np.sqrt(pow((origin_coord.location[0] - self.g.location[0]), 2) + pow((origin_coord.location[1] - self.g.location[1]), 2))
        # self.h.dist = np.sqrt(pow((origin_coord.location[0] - self.h.location[0]), 2) + pow((origin_coord.location[1] - self.h.location[1]), 2))

        # # When calculating the distance to travel to get to the point, it must accumulate from the startpoint onwards
        # self.a.dist += origin_coord.dist
        # self.b.dist += origin_coord.dist
        # self.c.dist += origin_coord.dist
        # self.d.dist += origin_coord.dist
        # self.e.dist += origin_coord.dist
        # self.f.dist += origin_coord.dist
        # self.g.dist += origin_coord.dist
        # self.h.dist += origin_coord.dist
        #
        # self.neighbours_dist = [self.a.dist, self.b.dist, self.c.dist, self.d.dist, self.e.dist,
        #                           self.f.dist, self.g.dist, self.h.dist]



    def check_if_point_is_available(self):
        for ele in self.neighbours:
            if ele.location in obstacles:
                ele.available = 0
            else:
                ele.available = 1




    def calculate_combined_score(self):

        # check none of the points are blocked (unavailable)
        for ele in self.neighbours:
            if (ele.available == 0) or (ele.location[0] <= 0) or (ele.location[1] <= 0):
                ele.combined_score = 1000000
            else:
                ele.combined_score = ele.dist + ele.score

            self.neighbours_combined_scores.append(ele.combined_score)




        # for ele in self:
        #     if (ele.available == 0) or (ele.location[0] <= 0) or (ele.location[1] <= 0):
        #         ele.dist = 1000000
        #         ele.score = 1000000
        #
        #     ele.combined_score = ele.dist + ele.score






class Point:

    def __init__(self):
        self.location = [0, 0]
        self.x = 0
        self.y = 0
        self.neighbours = []

        # self.a = Coord()
        # self.b = Coord()
        # self.c = Coord()
        # self.d = Coord()
        # self.e = Coord()
        # self.f = Coord()
        # self.g = Coord()
        # self.h = Coord()






def get_score(data):
    return data.combined_score



def create_grid(x, y):
    max_coord = [y, x]
    return max_coord


# def create_obstacles(buffer):




def main():

    print("Please enter the row position for the start")
    start_coord_row = input()
    while not isinstance(start_coord_row, int):
        try:
            start_coord_row = int(start_coord_row)
        except:
            print("Please enter an integer")
            start_coord_row = input()


    print("Please enter the column position for the start")
    start_coord_column = input()
    while not isinstance(start_coord_column, int):
        try:
            start_coord_column = int(start_coord_column)
        except:
            print("Please enter an integer")
            start_coord_column = input()


    print("Please enter the row position for the end")
    end_coord_row = input()
    while not isinstance(end_coord_row, int):
        try:
            end_coord_row = int(end_coord_row)
        except:
            print("Please enter an integer")
            end_coord_row = input()


    print("Please enter the column position for the end")
    end_coord_column = input()
    while not isinstance(end_coord_column, int):
        try:
            end_coord_column = int(end_coord_column)
        except:
            print("Please enter an integer")
            end_coord_column = input()


    # start_point = Point(start_coord_row, start_coord_column)
    # end_point = Point(end_coord_row, end_coord_column)

    start_point = Coord(start_coord_row, start_coord_column, 'start', [])
    end_point = Coord(end_coord_row, end_coord_column, 'end', [])


    if (start_point.location in obstacles) or (end_point.location in obstacles):
        print("Your start or end point is actually an obstacle!")

    else:


        reached_end = 0
        iteration_count = 0
        max_iterations = 5000

        recorded_points = []
        recorded_paths = []

        recorded_points.append(start_point)

        # coord_array = [start_point.location]

        prev_coords = [start_point.location]


        # while (reached_end == 0) and (iteration_count < max_iterations):
        while reached_end == 0:

            if recorded_points[-1].location == end_point.location:
                reached_end = 1

            else:

                current_neighbours = Neighbours(recorded_points[-1].location[0], recorded_points[-1].location[1],
                                                recorded_points[-1].name, recorded_points[-1].coord_array)

                current_neighbours.calculate_dist(recorded_points[-1])
                current_neighbours.calculate_heuristic_score(end_point)
                current_neighbours.check_if_point_is_available()
                current_neighbours.calculate_combined_score()

                # for ele in current_neighbours.neighbours:
                #     print(ele.name, ele.combined_score)


                # We have fully expanded the latest point, so remove it from the queue
                recorded_points.pop()
                for ele in current_neighbours.neighbours:
                    recorded_points.append(ele)

                recorded_points.sort(key=get_score, reverse=True)   # Last in array is the top of the queue

                # print("\n")
                # print("Iteration count", iteration_count)
                #
                # for ele in recorded_points:
                #     print(ele.name, ele.location, ele.combined_score)


                iteration_count += 1


                if iteration_count % 100 == 0:
                    print("Still going")
                    print(iteration_count)
                    print("\n")

                # Get the neighbour points around the current point being looked at
                # first iteration, this is the start point

        print("\n")
        print("iteration count", iteration_count)

        print("\n")
        print("last point")
        print(recorded_points[-1].name, recorded_points[-1].location, recorded_points[-1].combined_score)
        print("\n")
        print("number of paths still in queue:", len(recorded_points))
        print("\n")

        print(recorded_points[-1].coord_array)

        shortest_path = recorded_points[-1].coord_array

        if iteration_count >= max_iterations:
            print("Maximum iterations reached")
        else:
            print("Reached the end")


        x_coords = []
        y_coords = []
        for ele in shortest_path:
            x_coords.append(ele[1])
            y_coords.append(ele[0])

        obs_x_coords = []
        obs_y_coords = []
        for ele in obstacles:
            obs_x_coords.append(ele[1])
            obs_y_coords.append(ele[0])

        axis_lim = 16
        ticks_array = []
        for i in range(axis_lim + 1):
            ticks_array.append(i)

        plt.figure()
        plt.plot(x_coords, y_coords, 'r', marker='x')
        plt.scatter(obs_x_coords, obs_y_coords)
        plt.xlim([0, axis_lim])
        plt.ylim([0, axis_lim])
        plt.xticks(ticks_array)
        plt.yticks(ticks_array)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid('minor')
        plt.show()




if __name__ == '__main__':
    main()

