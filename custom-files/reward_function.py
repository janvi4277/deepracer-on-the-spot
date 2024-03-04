def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    closest_point=params['closest_waypoints']
    waypoints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169];
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    next_point= closest_point[1]
    
    if next_point in waypoints:
        if distance_from_center>marker_1:
            return 1e-7
    
    return float(speed)
    