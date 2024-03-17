import math

class PARAMS:
    prev_speed = None
    prev_steering_angle = None 
    prev_steps = None
    prev_direction_diff = None

def angle_between_lines(x1, y1, x2, y2, x3, y3, x4, y4):
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3
    angle = math.atan2(dy2, dx2) - math.atan2(dy1, dx1)
    deg= math.degrees(angle)
    if deg>180:
        deg=deg-360
    if deg <-180:
        deg= deg+360
    return deg
def reward_function(params):
    steps=params['steps']
    speed=params['speed']
    steering_angle=params['steering_angle']
    progress= params['progress']

    if PARAMS.prev_steps is None or steps < PARAMS.prev_steps:
        PARAMS.prev_speed = None
        PARAMS.prev_steering_angle = None
        PARAMS.prev_direction_diff = None

    if params['is_offtrack'] or params['is_crashed']:
        return 1e-9
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    straight_waypoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169];
    left_waypoints=[93,94,95,96,97,98,99,100,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,117,118,119,120,121,132,133,134,135]
    right_waypoints=[77,78,79,80,81,82,83]
    not_very_right_waypoints=[67,68,69,70,71,72,73,74,75,76]
    not_very_left=[122, 123, 124, 125, 126, 127, 128, 129, 130, 131]
    basic_left=[18,19,20,21,22,23,53,54,55,56,57,58,59,60,89,90,91,92,101,102,103,104,105,106,107,1108,109,110,111,112,113,114,115,116,136,137,138,139,140,141,142,143]
    basic_right=[61,62,63,64,65,66,84,85,86,87,88]
    Total_time=14.0
    total_steps=211
# Calculate the direction of the center line based on the closest waypoints
    waypoints_length= len(waypoints)
    prev = int(closest_waypoints[0])
    next = int(closest_waypoints[1])
    next_point_1 = waypoints[next]
    next_point_2 = waypoints[(next+1)%waypoints_length]
    next_point_3 = waypoints[(next+2)%waypoints_length]
    next_point_4 = waypoints[(next+3)%waypoints_length]
    next_point_5 = waypoints[(next+4)%waypoints_length]
    next_point_6 = waypoints[(next+5)%waypoints_length]
    prev_point = waypoints[prev]
    prev_point_2 = waypoints[(prev-1+waypoints_length)%waypoints_length]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point_1[1] - params['y'], next_point_1[0] - params['x'])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    # straight_direction_diff = abs(track_direction - params['heading']-params['steering_angle'])
    direction_diff = abs(track_direction - params['heading'])
    dir_diff=track_direction - params['heading']
    if direction_diff > 180:
        direction_diff = 360 - direction_diff


    # Penalize the reward if the difference is too large
    angle_f= angle_between_lines(next_point_1[0],next_point_1[1],next_point_2[0],next_point_2[1],next_point_3[0],next_point_3[1],next_point_4[0],next_point_4[1])
    angle_f2= angle_between_lines(next_point_3[0],next_point_3[1],next_point_4[0],next_point_4[1],next_point_5[0],next_point_5[1],next_point_6[0],next_point_6[1])
    angle_b= angle_between_lines(prev_point_2[0],prev_point_2[1],prev_point[0],prev_point[1],next_point_1[0],next_point_1[1],next_point_2[0],next_point_2[1])
    reward = 1e-9
    total_angle = (angle_f+angle_b+angle_f2)/3
    if total_angle >90:
        total_angle-=180
    elif total_angle <-90:
        total_angle+=180
    if abs(total_angle)<=5:
        total_angle=0
    if next ==1 or prev==1 or (next+1)%waypoints_length ==1 or (next+2)%waypoints_length ==1 or (next+3)%waypoints_length ==1 or (next+4)%waypoints_length ==1 or (next+5)%waypoints_length ==1 or (next+6)%waypoints_length ==1 or (next+7)%waypoints_length ==1 or (prev -1 +waypoints_length)%waypoints_length ==1:
        total_angle =0


    opt_speed= 5*math.tanh(8/(1+abs(total_angle)))
    opt_speed=max(1.4,opt_speed)
    speed_reward=(5-abs(params['speed']-opt_speed))**3

# //////////////////
    speed_maintain_bonus=1.0
#Check if the speed has dropped
    is_turn_upcoming= next in right_waypoints or next in left_waypoints or next in not_very_left or next in not_very_right_waypoints
    has_speed_dropped = False
    is_heading_in_right_direction=False
    if next in left_waypoints or next in not_very_left and dir_diff>=0:
        is_heading_in_right_direction=True
    if next in right_waypoints or next in not_very_right_waypoints and dir_diff<=0:
        is_heading_in_right_direction=True
    if PARAMS.prev_speed is not None:
        if PARAMS.prev_speed > speed:
            has_speed_dropped = True
    #Penalize slowing down without good reason on straight portions
    if has_speed_dropped and not is_turn_upcoming: 
        speed_maintain_bonus = min( speed / PARAMS.prev_speed, 1 )
    #Penalize making the heading direction worse
    heading_decrease_bonus = 0
    if PARAMS.prev_direction_diff is not None:
        if is_heading_in_right_direction:
            if abs( PARAMS.prev_direction_diff / direction_diff ) > 1:
                heading_decrease_bonus = min(10, abs( PARAMS.prev_direction_diff / direction_diff ))
    #has the steering angle changed
    has_steering_angle_changed = False
    if PARAMS.prev_steering_angle is not None:
        if not(math.isclose(PARAMS.prev_steering_angle,steering_angle)):
            has_steering_angle_changed = True
    steering_angle_maintain_bonus = 1 
    #Not changing the steering angle is a good thing if heading in the right direction
    if is_heading_in_right_direction and not has_steering_angle_changed:
        if abs(direction_diff) < 10:
            steering_angle_maintain_bonus *= 2
        if abs(direction_diff) < 5:
            steering_angle_maintain_bonus *= 2
        if PARAMS.prev_direction_diff is not None and abs(PARAMS.prev_direction_diff) > abs(direction_diff):
            steering_angle_maintain_bonus *= 2
# Reward for making steady progress
    progress_reward = 10 * progress / (steps+1)
    if steps <= 5:
        progress_reward = 1 #ignore progress in the first 5 steps
# Bonus that the agent gets for completing every 10 percent of track
# Is exponential in the progress / steps. 
# exponent increases with an increase in fraction of lap completed
    intermediate_progress_bonus = 0
    pi = int(progress//10)
    if pi > 0 :
        intermediate_progress_bonus = progress_reward ** (3+0.25*pi)

# ////////
    #Then compute the heading reward
    heading_reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 10
    if abs(direction_diff) <= 20:
        heading_reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 4

    reward=reward+steering_angle_maintain_bonus*heading_reward*25

    Total_time=14.0
    total_steps=211

    # if progress == 100 and steps > 250:
    #     return 0.5*reward
    
    # if (steps % 10) == 0 and progress >= (steps / total_steps) * 100 :
    #     reward += 1000
    # elif (steps %10) == 0 and progress <=(steps/total_steps)*100:
    #     reward -=500
    
    if next in straight_waypoints:
        reward += 200/(1+abs(track_direction - params['heading']-params['steering_angle']))

    if next in left_waypoints and params['is_left_of_center']:
        reward+=30.0
        if  params['distance_from_center']>=0.1*params['track_width']:
            reward+=20
        if params['distance_from_center']>=0.2*params['track_width']:
           reward+=30
        if params['distance_from_center']>=0.3*params['track_width']:
           reward+=50
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20

    if next in right_waypoints and not params['is_left_of_center']:
        reward+=30.0
        if params['distance_from_center']>=0.1*params['track_width']:
            reward+=20
        if params['distance_from_center']>=0.2*params['track_width']:
            reward+=30
        if params['distance_from_center']>=0.3*params['track_width']:
            reward+=50
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20
    if next in not_very_right_waypoints and not params['is_left_of_center']:
        reward+=60.0
        if params['distance_from_center']>=0.1*params['track_width']:
           reward+=20
        if params['distance_from_center']>=0.2*params['track_width']:
           reward+=40
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20
    if next in not_very_left and params['is_left_of_center']:
        reward+=60.0
        if params['distance_from_center']>=0.1*params['track_width']:
           reward+=20
        if params['distance_from_center']>=0.2*params['track_width']:
           reward+=40
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20
    if next in basic_left:
        if params['is_left_of_center'] or params['distance_from_center']==0:
            reward+=100
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20
    if next in basic_right:
        if not params['is_left_of_center'] or params['distance_from_center']==0:
            reward+=100
        if params['distance_from_center']>=0.47*params['track_width']:
            reward-=20
    speed_reward= speed_reward*speed_maintain_bonus
# Before returning reward, update the variables
    PARAMS.prev_speed = speed
    PARAMS.prev_steering_angle = steering_angle
    PARAMS.prev_direction_diff = direction_diff
    PARAMS.prev_steps = steps
    
    return float(reward+speed_reward+intermediate_progress_bonus)