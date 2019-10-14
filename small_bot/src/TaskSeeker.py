#!/usr/bin/env python
import rospy
from std_msgs.msg import String
#from smallBot.TaskIdentifier import TaskIdentifier TODO optimize of ROS
from data.Task import Task
from data.srv import *
from support.EqualPriorityQueue import EqualPriorityQueue


"""
This class resquest a new task and sends that task off to be identified.
This class also updates the status for the avoid and return tasks
"""
class TaskSeeker:

    def __init__(self):
        rospy.init_node('task_seeker', anonymous=True)
        #self.TaskIdentifier = TaskIdentifier() TODO REMOVE QOUTES
        self.currentTask = None
        self.Tasks = EqualPriorityQueue()
        self.ID = -1
        self.request()
       # self.send_to_id() TODO REMOVE after TaskID Update


    def parseTask(self, taskResponse):
        task = Task(taskResponse.zone, taskResponse.priority)
        task.isActive = taskResponse.isActive
        task.isComplete = taskResponse.isComplete
        task.workerID = taskResponse.workerID
        return task


    #Requests a new task from the base bot and updates the currentTask variable
    def request(self):
        rospy.wait_for_service('give_zones')
        print("tryimg to request")
        try:
            zone_request = rospy.ServiceProxy('give_zones', GetCleanTask)
            clean_task = zone_request(self.ID)
            clean_task = self.parseTask(clean_task)
            if self.ID is -1:
                self.ID = clean_task.workerID
                rospy.loginfo("Tryimg to update worker ID")
                rospy.loginfo(clean_task.workerID)
            else:
                rospy.loginfo("mo meed to update")
            self.Tasks.put(clean_task.priority,clean_task.type)
        except rospy.ServiceException, e:
            rospy.loginfo("Service call failed: %s" % e)



    #When service is requested by the basebot, updates both the avoid status to true and the coordinate
    def update_avoid_status(self):
        return
    #TODO make the service to update the avoid status and avoid coordinate from Task



    #When service is requested, updates amd adds a dump task to the priority queue
    def update_dump_status(self):
        return



    #Send task to be identified for appropriate execution
    def send_to_id(self):
        self.currentTask = self.Tasks.get()
        self.TaskIdentifier.task_ID(self.currentTask)



if __name__ == "__main__":
    ts = TaskSeeker()