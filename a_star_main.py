
import numpy as np
import scipy.signal as signal
import scipy.stats as stats
import time


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
#
#



class Coord:

    def __init__(self, y, x, name):
        self.location = [y, x]
        self.name = name
        self.score = 100000000
        self.dist = 0
        self.combined_score = 100000000
        self.available = 1





class Neighbours:

    def __init__(self, oy, ox, name):
        self.a = Coord(oy-1, ox-1, name+'->a')
        self.b = Coord(oy-1, ox, name+'->b')
        self.c = Coord(oy-1, ox+1, name+'->c')
        self.d = Coord(oy, ox-1, name+'->d')
        self.e = Coord(oy, ox+1, name+'->e')
        self.f = Coord(oy+1, ox-1, name+'->f')
        self.g = Coord(oy+1, ox, name+'->g')
        self.h = Coord(oy+1, ox+1, name+'->h')

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


    # def check_if_point_is_unavailable(self):


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



# def determine_neighbour_positions(curr_point, end_point):

    # curr_point.neighbours = []
    #
    # curr_point.neighbours.append([curr_point.location[0]-1, curr_point.location[1]-1])
    #
    # curr_point.a.location = [curr_point.location[0]-1, curr_point.location[1]-1]



    # for i in range(8):                  #8 possible neighbours for grid
    #     curr_point.neighbours.append(Coord(curr_point.x, curr_point.y))
    #     curr_point.neigbours[i].dist = np.sqrt(pow())





def get_score(data):
    return data.combined_score



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

    start_point = Coord(start_coord_row, start_coord_column, 'start')
    end_point = Coord(end_coord_row, end_coord_column, 'end')


    reached_end = 0
    iteration_count = 0
    max_iterations = 5000

    recorded_points = []
    recorded_paths = []

    recorded_points.append(start_point)


    while (reached_end == 0) and (iteration_count < max_iterations):


        if recorded_points[-1].location == end_point.location:
            reached_end = 1

        else:

            current_neighbours = Neighbours(recorded_points[-1].location[0], recorded_points[-1].location[1],
                                            recorded_points[-1].name)

            current_neighbours.calculate_dist(recorded_points[-1])
            current_neighbours.calculate_heuristic_score(end_point)
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

    if iteration_count >= max_iterations:
        print("Maximum iterations reached")
    else:
        print("Reached the end")







if __name__ == '__main__':
    main()

