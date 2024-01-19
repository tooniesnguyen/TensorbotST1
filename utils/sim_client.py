import time
from .conn_db import *




def PathFollowing2(path_moving: list):
    '''
    Input: [[1,2],[2,3],...[3,5]]
    Output: [[1,2]] 

    '''
    for num, i in enumerate(path_moving):
        time.sleep(0.2)
        update_target_coordinates("Tensorbot",list(i))
        # print("Breakkk", num)

        # if (num+1) % 10 == 0:
        #     sim_block = [i,[4,8]] # 2D [[2,3],[3,5]]
        #     return sim_block
        
    return i 
        
if __name__ == "__main__":
    arr_moving = [(0, 0), (1, 0), (2, 0), (3, 0)]
    print(PathFollowing2(arr_moving))
