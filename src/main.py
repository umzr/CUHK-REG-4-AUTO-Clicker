from pickle import TRUE
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests as req
import datetime
import os

TIME_ZONE = +8  # hong kong time
SET_CLICK_TIME = "20:30:00"  # HH:MM:SS
OFFSET = 0.125  # ms
TARGET_ELEMENT_ID = "DERIVED_SSR_FL_SSR_ENROLL_FL"
ISWINDOW = TRUE

def get_local_time():
    x = datetime.datetime.now()
    return x.strftime("%X")


def get_cusis_time():
    server_result = req.get(
        'https://cusis.cuhk.edu.hk/psc/CSPRD/EMPLOYEE/HRMS/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?')
    cusis_GMT_Time_all_str = server_result.headers['Date']
    _, _, _, _, cusis_str_time, _ = cusis_GMT_Time_all_str.split(' ')
    cusis_hh, cusis_mm, cusis_ss = cusis_str_time.split(':')
    cusis_hh = (int(cusis_hh) + TIME_ZONE - 24 if int(cusis_hh) +
                TIME_ZONE >= 24 else int(cusis_hh) + TIME_ZONE)
    cusis_real_time = "{}:{}:{}".format(str(cusis_hh).zfill(2), str(cusis_mm).zfill(2) , str(cusis_ss).zfill(2))
    return cusis_real_time


def get_up(n):
    return "\x1B[{}A".format(n+1)
def get_clean():
    try:
        if ISWINDOW:
            os.system('CLS')
        else:
            os.system('clear')
    except:
        print("ERROR: CANNNOT CLEAN SCREEN")

UP = "\x1B[3A"
CLR = "\x1B[0K"

while True:
    ans = input("Are You Using Window? [Y]/N :")
    if ans.upper() == "Y":
        break
    elif ans.upper() == "N":
        ISWINDOW = False
        break
    
while True:
    ans = input("Now is {} Plx, Set your reg 4 time (HH:MM:SS) auto default is: ".format(get_local_time()))
    if ans is not None:
        SET_CLICK_TIME = ans
        break
    else:
        print("set to Default time")
        break
    
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://cusis.cuhk.edu.hk/')
get_clean()



while True:
    size = os.get_terminal_size()
    cusis_real_time = get_cusis_time()
    output_time = "CUSIS Time: {}".format(cusis_real_time)

    local_real_time = get_local_time()
    output_local_time = "PC TIME: {}".format(local_real_time)

    try:
        
        driver.find_element(By.ID, TARGET_ELEMENT_ID)
        get_clean()
        target_output = "TARGET FOUND"
        set_time_output = "Target time: {}".format(SET_CLICK_TIME)
        res = target_output +"\t" + set_time_output +"\t" + output_time + "\t" + output_local_time + " github:umzr"
        res_len = len(res)
        space_res_num = (100 - (res_len)) // 2

        print('[' + ' '*(space_res_num) + res +
              ' '*(space_res_num) + ']', end="\r", flush=True)

        if cusis_real_time == SET_CLICK_TIME:
            sleep(OFFSET)
            button = driver.find_element(By.ID, TARGET_ELEMENT_ID)
            button.click()
            print("DONE", end="\r", flush=True)
            break
        
    except:
        err = "ERR: NO ENROLL BUTTON DETECT"
        res = err + "\t" + output_time + "\t" + output_local_time + " github:umzr"
        res_len = len(res)
        space_res_num = (100 - (res_len)) // 2

        print('[' + ' '*(space_res_num) + res +
              ' '*(space_res_num) + ']', end="\r" ,flush=True)
        sleep(0.5)

