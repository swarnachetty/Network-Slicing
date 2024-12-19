#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 2024

@author: vxn523
"""

"""
!!!! have it so remote surgery it kicks out the other users!! a lot more important

per basestation arrange them in the order
and then check available space overall, arrange it in a dictionary so that 
keys per slice and users 

we look at the keys for urllc, 
if we have space, use it up, if we have  space for urlcc, use it up
elseif no space, take up unused mMTC and embb space, all for urlcc
elseif get a new percentage off

# make a graph of how many users were added each time - in 10, 20, 30, 40, 50 
iterations and make a graph of the og version vs my version of network slicing

so i have all the standby users, i have the basetation object and try to connect in order


to do: 
    - check each of the logistics of functions 
    - fix all the errors
    - get this file looking better
    
    - get graphs of the amount of users saved

"""

from Heurictic_model_03_12_2024 import Network


def connect_most_important_user():
    bs_ls = network.base_stations
    for bs in bs_ls:
        # check if each basestation has any standby users and arrange them 
        # as a dictionary for easier access
        if any(bs.standby_users):
            standby_users_dict_slices = {}
            for usr in bs.standby_users:
                if usr[1] not in standby_users_dict_slices.keys():
                    standby_users_dict_slices[usr[1]] = [usr[0]]
                else:
                    standby_users_dict_slices[usr[1]].append(usr[0])
            # first check if there is unused prbs and reasign them
            # starts with URLLC as a priority
            for slice_name in ['URLLC', 'eMBB', 'mMTC']:
                if slice_name in standby_users_dict_slices.keys():
                    total_avail_prbs = sum(bs.available_prb_slices.values())
                    total_prbs_requested = calculate_sum_slice_prbs(slice_name, standby_users_dict_slices)
                    print(total_avail_prbs, total_prbs_requested)
                    if (total_avail_prbs - total_prbs_requested) > 0:
                        print("We have prb's available and user is now added", slice_name)
                        reshuffle_slice_prbs(bs, slice_name, total_prbs_requested)
                        bs.can_connect_standby_user(standby_users_dict_slices[slice_name][0], slice_name)
                        # call a fct to update the list
                    elif slice_name == 'URLLC':
                        print("old users", bs.connected_users)
                        if replace_users_for_urlcc(bs, total_prbs_requested, total_avail_prbs):
                            print("SUCCESSSSSS!!!!")
                            print("updated users", bs.connected_users)
                            bs.can_connect_standby_user(standby_users_dict_slices[slice_name][0], 'URLLC')
                        
            print(bs.available_prb_slices)
            # calculate_sum_slice_prbs('URLLC', standby_users_dict_slices)
            # check_available_prbs(bs, standby_users_dict_slices)
            
        
"""         
first have a look if there is enough leftover prb's?? 
we take 273 - leftover prbs == requested prb
add as much as we can -- return the new prbs available
(keep a counter of the percentage prbs)


then, if more in the list, we create a list of next up slices available
so we have a dictionary of values that need changing
-- get rid of urlcc at a time


-- update the slice values at the end ----
"""

def check_users_that_fit(bs, total_avail_prbs, slice_name, user_ls):
    # check how many users can we connect to the base station at a time
    for user in user_ls:
        if (total_avail_prbs - user.prb_requested) > 0:
            reshuffle_slice_prbs(bs, slice_name, user.prb_requested)
            bs.can_connect_standby_user(user, slice_name)
            print("We have prb's available and user is now added", slice_name, user.id)
    

def calculate_sum_slice_prbs(slice_name, ls_prbs_standby_users):
    standby_users = ls_prbs_standby_users[slice_name] 
    total_sum_request = 0
    for user in standby_users:
        total_sum_request += user.prb_requested
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ", total_sum_request)
    return total_sum_request


def reshuffle_slice_prbs(bs, slice_name, total_prbs_requested):
    # this is assumiming the prbs have enough space and wants to give a new
    # netowrk slicing percentage, work on resetting it
    """
    given a slice, we take away from the rest to make space for this 
    so if 15:3:4, but we need 17 in the middle
    T = 15+3+4 = 22
    22-3 = 19 -- need to borrow this much from the other slices
    15 - 19 = -4
    0:22:0
    """
    temp = total_prbs_requested - bs.available_prb_slices[slice_name]
    bs.available_prb_slices[slice_name] = total_prbs_requested
    total_prbs_requested = temp
    all_slices = ['URLLC', 'eMBB', 'mMTC']
    idx = all_slices.index(slice_name)
    all_slices.pop(idx)
    for slice_x in all_slices:
        if bs.available_prb_slices[slice_x] - total_prbs_requested < 0:
            bs.available_prb_slices[slice_x] = 0
            total_prbs_requested -= bs.available_prb_slices[slice_x]
        else:
            bs.available_prb_slices[slice_x] = bs.available_prb_slices[slice_x] - total_prbs_requested
    print("The slice prbs have been successfuly updated")


def replace_users_for_urlcc(bs, total_prbs_requested, total_avail_prbs):
    """
    have a look at the accepted ls for embb and take out as much as needed
    for urlcc that has priority
    
    needed 60, have 5 available
    need to steal 60 - 5 from embb
    """
    additional_prbs_needed = total_prbs_requested - total_avail_prbs
    print(bs.connected_users)
    replaceable_users = []
    for user,slice_n in bs.connected_users:
        if slice_n == 'eMBB' and additional_prbs_needed > 0:
            # result = bs.can_disconnect_user_to_standby(user, 'eMBB')
            replaceable_users.append(user)
            additional_prbs_needed -= user.prb_requested
    
    if additional_prbs_needed < 0:
        # make sure to uodate the percentages for the network slicing
        for user in replaceable_users:
            bs.can_disconnect_user_to_standby(user, 'eMBB')
        
        bs.available_prb_slices['eMBB'] = abs(additional_prbs_needed)
        bs.available_prb_slices['URLLC'] = 0
        bs.available_prb_slices['mMTC'] = 0
        
        print(bs.connected_users)
        return True
    else:
        print("Failed :(")
        return False
    ##### see what connexted users do


# this function looks at the less priority slices given any slice
# it can automatically remove users from those slices
def free_space_for_slice(net_slice):
    if net_slice != 'mMTC':
        slice_order_priority = ['URLLC', 'eMBB', 'mMTC']
        indx = slice_order_priority.index(net_slice)
        slice_ordered = slice_order_priority[indx+1:]
        print(slice_ordered)
    else:
        print("Not much space we can find for IoT")
        return None



if __name__ == "__main__":
    # Running the simulation
    network = Network()
    network.simulate_network_operation()
    connect_most_important_user()











