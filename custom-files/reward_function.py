def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_point=params['closest_waypoints']
    straight_waypoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169];
    left_waypoints=[93,94,95,96,97,98,99,100,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]
    right_waypoints=[67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]
    not_very_left=[120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135]
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    next_point= closest_point[1]
    if distance_from_center >= 0.4* track_width:
        distance_from_center = 0.8* track_width - distance_from_center
    if params['is_crashed'] or params['is_offtrack']:
        return 1e-10

    if next_point in straight_waypoints:
        return speed**3
    if next_point in left_waypoints or next_point in not_very_left:
        if not params['is_left_of_center']:
            return 1e-7
        else:
            return 64*(distance_from_center/(0.4*track_width))
    if next_point in right_waypoints:
        if params['is_left_of_center']:
            return 1e-7
        else:
            return 64*(distance_from_center/(0.4*track_width))
        
    return float(speed)