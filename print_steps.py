import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import multiprocessing
import warnings
import pandas as pd
from mpire import WorkerPool
from rich.console import Console 
from stepper import StepDefinition,StepStatus,Stepper

def get_lists(step_name,step_status):
    step = StepDefinition(step_name,eval(f"StepStatus.{step_status}"))
    return step
  
def automate_steps(list_of_stepsDict_to_print,progress_bar):
    steps = []
    results = []
    for my_dict in list_of_stepsDict_to_print:
        step_name,step_status = list(my_dict.keys())[0],list(my_dict.values())[0]
        my_dict = {
            "step_name":step_name,
            "step_status":step_status
        }
        results.append(my_dict)
    num_cores = max(multiprocessing.cpu_count()//2,1)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(get_lists, results, progress_bar=progress_bar)
    stepper = Stepper(steps=results)
    return stepper 

def print_steps(stepper):
    Console().print(stepper)   
    NEWLINE = "\n"
    print(NEWLINE)

def print_all_steps(list_of_stepsDict_to_prints,progress_bar):
    length = len(list_of_stepsDict_to_prints)
    status = "successfully executed!"
    step_num = 1
    for i in range(0,length,1000):
        print(f"Step {step_num}: execution happening!")
        list_of_stepsDict_to_print = list_of_stepsDict_to_prints[i:i+1000]
        stepper = automate_steps(list_of_stepsDict_to_print,progress_bar)
        print_steps(stepper)
        step_num += 1
    NEWLINE = f"{status}\n"
    return NEWLINE
    
if __name__=="__main__":
    list_of_stepsDict_to_prints = [
        {
            "Clone repository":"COMPLETED"
        },
        {
            "Install dependencies":"ACTIVE"
        },
        {
            "Run tests":"PENDING"
        },
        {
            "Deploy":"PENDING"
        }
    ]*2000
    progress_bar = True
    status = print_all_steps(list_of_stepsDict_to_prints,progress_bar)
    print(f"final status is {status}")
