import numpy as np
import math
import dtaidistance as dtai
from dtaidistance import dtw
from dtaidistance import dtw_barycenter as bct

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)
def vec_vec_angle(v1, v2):
    #Returns the angle in degrees between vectors 'v1' and 'v2'::
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def plane_vec_angle(a, b, c, d, v):
    #plane eq ax + by + cz = d, vector v (l, m, n)
    #return angle in degrees between plane and vector
    A = abs(a*v[0] + b*v[1] + c*v[2])
    B = math.sqrt(a*a + b*b + c*c) * math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return np.degrees(np.arcsin(A/B))

def multiDimenDist(point1,point2):
   #find the difference between the two points, its really the same as below
   deltaVals = [point2[dimension]-point1[dimension] for dimension in range(len(point1))]
   runningSquared = 0
   #because the pythagarom theorm works for any dimension we can just use that
   for coOrd in deltaVals:
       runningSquared += coOrd**2
   return runningSquared**(1/2)

def findVec(point1,point2,unitSphere = False):
  #setting unitSphere to True will make the vector scaled down to a sphere with a radius one, instead of it's orginal length
  finalVector = [0 for coOrd in point1]
  for dimension, coOrd in enumerate(point1):
      #finding total differnce for that co-ordinate(x,y,z...)
      deltaCoOrd = point2[dimension]-coOrd
      #adding total difference
      finalVector[dimension] = deltaCoOrd
  if unitSphere:
      totalDist = multiDimenDist(point1,point2)
      unitVector =[]
      for dimen in finalVector:
          unitVector.append( dimen/totalDist)
      return unitVector
  else:
      return finalVector

def midpoint (pt1, pt2):
    return ((pt1 + pt2)/2)

def planefunc_fr_3pts (pt1, pt2, pt3):
    #get plane equation from 3 points
    cp = np.cross(pt3 - pt1, pt2 - pt1) #get cross product of 2 vectors from 3 points
    a, b, c = cp #use cross product vector as plane normal vector
    d = np.dot(cp, pt3) 
    return a, b, c, d

def planefunc_fr_1vec_2pts (v, pt1, pt2):
    cp = np.cross(v, pt2 - pt1)
    a, b, c, = cp
    d = np.dot(cp, pt1)
    return a, b, c, d

def planefunc_fr_2vecs_1pt (v1, v2, pt):
    cp = np.cross(v1, v2)
    a, b, c = cp
    d = np.dot(cp, pt)
    return a, b, c, d

def dtwDistanceScore (subject, center):
    warp, path = dtw.warp(subject, center)
    distance = dtw.distance(warp, center)
    score = 0
    if distance <= 40:
        score += 2
    elif distance <= 80:
        score += 1
    return score, distance

def calculateAngle(sequence):
    step_size = 1
    mrightArmCorAngle = []
    mrightElbowAngle = []
    mupperRightLowerBodyAngle = []
    mrightKneeAngle = []
    mrightAnkleAngle = []
    for i in range(len(sequence)):       
        # print(skeleton_data[step_size*i][0][0])
        skel = np.array([float(sequence[step_size*i][0][0]), float(sequence[step_size*i][0][1]), float(sequence[step_size*i][0][2])])
        for index in range(1, 33):
            skel_i = np.array([float(sequence[step_size*i][index][0]), float(sequence[step_size*i][index][1]), float(sequence[step_size*i][index][2])])
            skel = np.vstack([skel, skel_i])
        
        thorax = midpoint(skel[12], skel[11]) #thorax = midpoint(R and L shoulder)
        crotch = midpoint(skel[24], skel[23]) #hip = midpoint(R and L hip)
        
        a1, a2, a3, a4 = planefunc_fr_3pts(skel[12], skel[11], crotch) #coronal plane with LRshoulder + crotch
        coronalPlaneNorVec = np.array([a1, a2, a3])

        b1, b2, b3, b4 = planefunc_fr_1vec_2pts(coronalPlaneNorVec, thorax, crotch)
        sagittalPlaneNorVec = np.array([b1, b2, b3])

        mrightArmCorAngle.append(plane_vec_angle(a1, a2, a3, a4, findVec(skel[16], skel[12])))
        mrightElbowAngle.append(vec_vec_angle(findVec(skel[14], skel[16]), findVec(skel[14], skel[12])))
        mupperRightLowerBodyAngle.append(plane_vec_angle(a1, a2, a3, a4, findVec(skel[24], skel[26])))
        mrightKneeAngle.append(vec_vec_angle(findVec(skel[26], skel[24]), findVec(skel[26], skel[28])))
        mrightAnkleAngle.append(vec_vec_angle(findVec(skel[26], skel[28]), findVec(skel[28], skel[32])))
    return mrightArmCorAngle, mrightElbowAngle, mupperRightLowerBodyAngle, mrightKneeAngle, mrightAnkleAngle

