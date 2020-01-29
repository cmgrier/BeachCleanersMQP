#!/usr/bin/python
from math import *
from support.Constants import *
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Kinematics:


    def __init__(self):

    def fwkin(self, ang0, ang1):
        """ Takes the angles of the joints in the arm, ang0 and ang1 referring to the
        shoulder and elbow joints respectively, and calculates the position of the
        end effector as a 3x1 matrix
        """
        ang0 = radians(ang0)
        ang1 = radians(ang1)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        matrix = self.transformMatrix(ang0+THETA1, ALPHA1, A1, D1)
        matrix2 = numpy.dot(self.transformMatrix(ang0 + THETA1, ALPHA1, A1, D1), self.transformMatrix(ang1 + THETA2, ALPHA2, A2, D2))
        ax.plot([0,matrix[0][3]], [0,matrix[1][3]], [0,matrix[2][3]],color='g',marker='o')
        ax.plot([matrix[0][3],matrix2[0][3]], [matrix[1][3], matrix2[1][3]], [matrix[2][3],matrix2[2][3]], color='b',marker='o')
        ax.set_xlabel('x-axis')
        ax.set_ylabel('y-axis')
        ax.set_zlabel('z-axis')
        ax.set(xlim=(-.5, .5), ylim=(-.5, .5),zlim=(-.5, .5))
        plt.show()
        return numpy.dot(self.transformMatrix(ang0+THETA1, ALPHA1, A1, D1), self.transformMatrix(ang1+THETA2, ALPHA2, A2, D2))

    def getEndEffectorFromAngles(self,ang0,ang1):
        """
        Gets the end effector's final position after the joints rotate to a certain angle
        :param ang0: joint 0 angle
        :param ang1: joint 1 angle
        :return: [x,y,z] position in meters
        """
        matrix = self.fwkin(ang0, ang1)
        print(matrix)
        return [matrix[0][3], matrix[1][3], matrix[2][3]]

    def transformMatrix(self, theta, alpha, a, d):
        T = [
                [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
                [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
                [0, sin(alpha), cos(alpha), d],
                [0, 0, 0, 1]
             ]
        return T

    def invkin(self,x,y):
        """
        Inverse kinematics of 2-deg of freedom arm
        :param x: end effector x-coord
        :param y: end effector y-coord
        :return: joint angles to result in the end effector reaching the desired position
        """
        d3 = sqrt((y*y)+(x*x))
        print("D3: ",d3)
        a3 = acos(((A1*A1)+(A2*A2)-(d3*d3))/(-2*A1*A2))
        print("A3: ", a3)
        theta1 = 180 - a3
        a4 = acos(((d3*d3)+(A1*A1)-(A2*A2)/(-2*A1*d3)))
        a5 = acos(y/d3)
        theta2 = 90 - a4 - a5
        return (theta1,theta2)

if __name__=="__main__":
    k = Kinematics(2)
    print(k.getEndEffectorFromAngles(0, 0))
    k.getEndEffectorFromAngles(k.invkin(0,0)[0],k.invkin(0,0)[1])