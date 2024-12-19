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
"""
#
# a = [(<__main__.User object at 0x75de0c3abc70>, 'eMBB'), (<__main__.User object at 0x75de0c3abc10>, 'URLLC'), (<__main__.User object at 0x75de0c3ab670>, 'eMBB'), (<__main__.User object at 0x75de0c3ab910>, 'URLLC'), (<__main__.User object at 0x75de0c3ab460>, 'eMBB'), (<__main__.User object at 0x75de0c3ab130>, 'eMBB')]
# standby_users_ls = [(1,'mMTC'), (3,'eMBB'), (5,'URLLC'), (2,'mMTC'), (4,'eMBB'), (6,'URLLC')]

from Heurictic_model_03_12_2024 import Network
import numpy as np
import pandas as pd
from operator import itemgetter 
from itertools import groupby 

def connect_most_important_user():
    bs_ls = network.base_stations
    for bs in bs_ls:
        # check if each basestation has any standby users and arrange them 
        # per slice
        if any(bs.standby_users):
            ordered_standby_ls = {}
            for usr in bs.standby_users:
                if usr[1] not in ordered_standby_ls.keys():
                    ordered_standby_ls[usr[1]] = [usr[0]]
                else:
                    ordered_standby_ls[usr[1]].append(usr[0])
            # first check if there is unused prbs and reasign them
            # starts with URLLC as a priority
            for slice_name in ['URLLC', 'eMBB', 'mMTC']:
                if slice_name in ordered_standby_ls.keys():
                    total_avail_prbs = sum(bs.available_prb_slices.values())
                    total_prbs_requested = calculate_sum_slice_prbs(slice_name, ordered_standby_ls)
                    if total_avail_prbs - total_prbs_requested > 0:
                        print("We have prb's available", slice_name)
                        reset_slice_prbs(bs, slice_name, total_prbs_requested)
                    if slice_name is 'URLLC':
                        
                        
            
            # calculate_sum_slice_prbs('URLLC', ordered_standby_ls)
            # check_available_prbs(bs, ordered_standby_ls)
            
        # in order of importance, first looking at URLLC, oif there is free
        # space rearrange slice %tages, else kick out some eMBB users
        
"""

            for slice_name in ['URLLC', 'eMBB', 'mMTC']:
                if slice_name in ordered_standby_ls.keys():
                    total_avail_prbs = sum(bs.available_prb_slices.values())
                    total_prbs_requested = calculate_sum_slice_prbs(slice_name, ordered_standby_ls)
                    if total_avail_prbs - total_prbs_requested > 0:
                        print("We have prb's available")
            print(ordered_standby_ls)
            
            
first have a look if there is enough leftover prb's?? 
we take 273 - leftover prbs == requested prb
add as much as we can -- return the new prbs available
(keep a counter of the percentage prbs)


then, if more in the list, we create a list of next up slices available
so we have a dictionary of values that need changing
-- get rid of urlcc at a time


-- update the slice values at the end ----
"""

def calculate_sum_slice_prbs(slice_name, ls_prbs_standby_users):
    standby_users = ls_prbs_standby_users[slice_name] 
    total_sum_request = 0
    for user in standby_users:
        total_sum_request += user.prb_requested
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ", total_sum_request)
    return total_sum_request


def reset_slice_prbs(bs, slice_name, total_prbs_requested):
    # this is assumiming the prbs have enough space and wants to give a new
    # netowrk slicing percentage, work on resetting it
    """
    given a slice, we take away from the rest to make space for this 
    so if 15:3:4, but we need 17 in the middle
    T = 15+3+4 = 22
    22-3 = 19 -- need to borrow this much from the other slices
    15 - 19
    21 - 19 
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
    


def free_space_for_clice(net_slice):
    if net_slice != 'mMTC':
        slice_order_priority = ['URLLC', 'eMBB', 'mMTC']
        indx = slice_order_priority.index(net_slice)
        slice_ordered = slice_order_priority[indx+1:]
        print(slice_ordered)
    else:
        print("Not much space we can find for IoT")
        return None

    # if there is space, use it
    # if no space, take it from mtc and then emb

"""
   
"""

if __name__ == "__main__":
    # Running the simulation
    network = Network()
    network.simulate_network_operation()
    # check_available_prbs(network)
    connect_most_important_user()
    # free_space_for_clice('URLLC')
    # free_space_for_clice('eMBB')
    # free_space_for_clice('mMTC')











