import heapq
import sys

class Activity(object):
	'''
	represents an activity to be assigned to a LectureHall

	instance attributes:
	s : int, start time
	f : int, finish time
	'''

	def __init__(self, start, finish):
		self.s = int(start)
		self.f = int(finish)



class LectureHall(object):
	'''
	class that represents a lecture hall
	for the purposes of assigning Activity objs

	class attributes:
	count : int, incrementer used to give instances unique ids
	available_times : min heap, latest Activity finish time for each LectureHall
	
	class methods:
	first_available_time()
	reset()

	instance attributes:
	activities : list of Activity objs assigned to the instance

	instance methods:
	__init__(Activity)
	assign(Activity)

	'''

	# number of LectureHalls, used to give them int IDs
	count = 0

	# min heap
	available_times = [] 


	@classmethod
	def first_available_time(c):
		'''
		returns top of LectureHall.end_times min heap, without popping it off
		'''
		return LectureHall.available_times[0]

	@classmethod
	def reset(c):
		'''
		resets all class attributes
		'''
		LectureHall.count = 0
		LectureHall.available_times = []

	def __init__(self, activity):
		'''
		initialize by adding Activity to instance's list
		and pushing the activity's finish time onto available_times
		'''
		self.activities = [activity]

		self.id = str(LectureHall.count)
		LectureHall.count = LectureHall.count + 1
	
		time_tup = (activity.f,self.id)
		heapq.heappush(LectureHall.available_times,time_tup)


	def assign(self, activity):
		'''
		append Activity to the LectureHall instance's activites list
		and replace the top of the heap with the new available time 
		'''
		self.activities.append(activity)

		time_tup = (activity.f, self.id)
		heapq.heapreplace(LectureHall.available_times,time_tup)




def AssignActivities(file_name):
	'''
	Greedy algorithm to assign Activitys to LectureHalls
	based on the machine scheduling problem

	params
	file_name : str, containing the path to a file of the following format

	{n}
	{s1,f1}
	{s2,f2}
	...
	{sn,fn}

	where {n} is the number of activities to be assigned
	and all n lines afterward contain the start and finish times
	of those activities {s,f}
	'''

	# reset LectureHall class variables so that you can run
	# different inputs in succession on shell
	LectureHall.reset() 

	activities = []
	lecture_halls = {}


	with open(file_name) as f:
		doc = f.readlines()
	
	n = int(doc[0])

	activity_data = [a.strip().split(',') for a in doc[1:]]

	# put all Activity objects in a list
	for i in range(0,n):
		activities.append(Activity(activity_data[i][0],activity_data[i][1]))
	
	# sort activities by their finish times, increasing order
	activities.sort(key=lambda a : a.f)
	
	for a in activities:
		if not LectureHall.available_times or LectureHall.first_available_time()[0] > a.s:
			# if there aren't any schedule activities yet
			# or the one with the earliest end time is later than this activity's start
			# assign the activity to a new lecture hall
			# and key the lecture hall into the dict
			lh = LectureHall(a)
			lecture_halls[lh.id] = lh

		else:
			# get the lecture hall key from the top of the min heap of times
			# and assign this activity to that key's entry in the dictionary
			key = LectureHall.first_available_time()[1]
			lecture_halls[key].assign(a)


	# print the final assignments
	for key in lecture_halls:
		print "Lecture hall : ",key
		print "Activity's start and finish times:"
		for a in lecture_halls[key].activities:
			print a.s,",",a.f
		print


#
# run it from cmd line if filename arg is given
#
if len(sys.argv) > 1:
	AssignActivities(sys.argv[1])
