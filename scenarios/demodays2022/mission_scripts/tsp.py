import numpy as np
import ot
import matplotlib.pyplot as plt
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def solve_tsp(all_destinations, home):
    home = np.array([0., 0., 0.])
    num_destinations = 100
    all_destinations = [np.array(home)]
    for i in range(num_destinations):
        all_destinations += (np.random.uniform(np.array([-100, -100, 0]), np.array([100, 100, 0])),)

    print(f'Input: {all_destinations}')

    def create_data_model():
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = np.sqrt(ot.dist(np.array(all_destinations), np.array(all_destinations)))
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data

    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)


    def print_solution(manager, routing, solution):
        """Prints solution on console."""
        print('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        print(plan_output)
        plan_output += 'Route distance: {}miles\n'.format(route_distance)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution)

    def get_routes(solution, routing, manager):
        """Get vehicle routes from a solution and store them in an array."""
        # Get vehicle routes and store them in a two dimensional array whose
        # i,j entry is the jth location visited by vehicle i along its route.
        routes = []
        for route_nbr in range(routing.vehicles()):
            index = routing.Start(route_nbr)
            route = [manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))
            routes.append(route)
        return routes

    routes = get_routes(solution, routing, manager)
    print(routes)

    routes_in_coordinates = []
    for dest in routes[0]:
        routes_in_coordinates.append(all_destinations[dest])
    print(routes_in_coordinates)

    """ Plot """
    routes_in_coordinates = np.array(routes_in_coordinates)
    plt.style.use('ggplot')
    plt.close('all')
    plt.scatter(routes_in_coordinates[:1, 0], routes_in_coordinates[:1, 1], color='blue', linewidths=10)  # 2D case
    plt.scatter(routes_in_coordinates[1:, 0], routes_in_coordinates[1:, 1], color='red')  # 2D case
    x = routes_in_coordinates[:, 0]
    y = routes_in_coordinates[:, 1]
    plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1], scale_units='xy', angles='xy', scale=1)
    plt.show()
