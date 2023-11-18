import boto3
import json
import multiprocessing as mp
import os


from collections import deque
from glob import glob

from pillow_strategy import PillowStrategy

class ImageProcessing:
    
    def __init__(self):
        try:
           with open("config/config.json", 'r') as configf:
               config = json.load(configf)
        except FileNotFoundError as err:
            raise FileNotFoundError("Config should be in the same directory as the script") from err
            
        self.input_dir = config.get("input_dir")
        self.strategy = config.get("strategy", "Pillow")
        
        self.resultq = mp.Queue()
        
    def getfiles(self, path):
        file_match_expr = os.path.join(path, "*")
        filenames = glob(file_match_expr)
        
        job_list = []
        for file in filenames:
            size = os.path.getsize(file)
            job_list.append((size, file))
            
        return job_list
            
    def assign_tasks_per_core(self, cores, jlist):
        queues = [deque() for _ in range(cores)]
        
        counter = 0
        for job in jlist:
            queues[counter].append(job[1])
            counter += 1
            if counter == cores:
                counter = 0
            
        return [q for q in queues if len(q) != 0]
    
    def upload_in_bulk(self, path):
        os.system("aws s3 sync {} {}".format(path, self.config.get("s3_bucket")))
    
    def run_job(self, job_queue, strategy, job_num):
        try:
            strat_obj = None
            if strategy == "Pillow":
                strat_obj = PillowStrategy()
            elif strategy == "OpenCV":
                pass
            else:
                raise Exception("Strategy Not Found")
        

            output_dir = os.path.join(os.getcwd(), "data")
        
            for job in job_queue:
                img = strat_obj.open(job)
                height, width = strat_obj.find_size(img)
                if height != 600 or width != 480:
                    img = strat_obj.resize(img)
                
                strat_obj.save_image(img, os.path.join(output_dir, os.path.basename(job)))
                
            #self.upload_in_bulk(output_dir)
            
            self.resultq.put("Success", block = True)
        except Exception as e:
            self.resultq.put("Failure")
            

    def run(self):
        if not os.path.isdir(self.input_dir):
            raise Exception("Folder path is Invalid")
        
        jlist = self.getfiles(self.input_dir)
        jlist.sort(key=lambda x:x[0], reverse=True)
        
        cpu_count = mp.cpu_count()
        
        job_qs = self.assign_tasks_per_core(cpu_count, jlist)
        
        processes = []
        for i, jobq in enumerate(job_qs):
            p = mp.Process(target=self.run_job, args=(jobq, self.strategy, i))
            processes.append(p)
            p.start()    
           
        for p in processes:
            p.join()

        flag = 0
        while not self.resultq.empty():
            if self.resultq.get() == "Failure":
                flag = 1
                break
                
            
        if not flag:
            print("Success: Saved all Images")
        else:
            print("Failure: Failed to save all images")

if __name__ == "__main__":
    ImageProcessing().run()

