import csv
import numpy as np 
import pandas as pd 

cr = csv.reader(open("UserRating2.csv","rb"))

userRatingList = []

for row in cr:
	userRatingList.append(row)

numproblems = len(userRatingList) 
numusers = len(userRatingList[0]) 

#userWeightsList = [[0]*(numusers-1)]*(numusers-1)     
userWeightsList = []
userAverageList = []
temp = 0
count = 0

#initialising user weights to zero

for i in xrange(0,numusers-1):
	row = []
	for j in xrange(0,numusers-1):
		row.append(0)
	userWeightsList.append(row)

#print userWeightsList

# calculating the average rating for each user

for i in xrange(1,numusers):
	temp = 0
	count = 0	
	for j in xrange(1,numproblems):
		if userRatingList[j][i] != "":
			temp = temp + float(userRatingList[j][i])
			count = count + 1
	userAverageList.append(temp/count)


# calculating the weights between users

#print userWeightsList 
for i in xrange(0,numusers-2):
	for k in xrange(i + 1,numusers-1):
		temp = 0
		sigmaA = 0
		sigmaB = 0
		for j in xrange(0,numproblems-1):
			if userRatingList[j+1][i+1] != "" and userRatingList[j+1][k+1] != "" :
				temp = temp + ((float(userRatingList[j+1][i+1]) - userAverageList[i]) * (float(userRatingList[j+1][k+1]) - userAverageList[k]))
			if userRatingList[j+1][i+1] != "" :
				sigmaA = sigmaA + ((float(userRatingList[j+1][i+1]) - userAverageList[i])**2)
			if userRatingList[j+1][k+1] != "" :
				sigmaB = sigmaB + ((float(userRatingList[j+1][k+1]) - userAverageList[k])**2)
			
		sigmaA = sigmaA**0.5
		sigmaB = sigmaB**0.5
		userWeightsList[i][k]=temp/(sigmaA * sigmaB)
		userWeightsList[k][i]=temp/(sigmaA * sigmaB)
		# print "temp: ",temp
		# print "sigmaA: ",sigmaA
		# print "sigmaB: ",sigmaB
		# print userWeightsList[i][k],userWeightsList[k][i]
		# print userWeightsList
#print userWeightsList


predictionList = []    #predicting the scores by user for a problem
checkPredict = []		# checking if the problem is rated by the user or not
for i in xrange(0,numusers-1):  # predict the probelem for users
	row1 = []
	row2 = []
	for j in xrange(0,numproblems-1):
		row1.append(0)
		row2.append(99)
	predictionList.append(row1)
	checkPredict.append(row2)


recommendProblemList = []
for j in xrange(0,numproblems-1):  # loop for recommending problems
	row = []
	for i in xrange(0,3):
		row.append(0)
	recommendProblemList.append(row)


for i in xrange(0,numusers-1):
	for j in xrange(0,numproblems-1):
		if userRatingList[j+1][i+1] == "" :
			temp = 0
			tempWeight = 0
			for k in xrange(0,numusers-1):
				if userRatingList[j+1][k+1] != "" :
					temp = temp + (float(userRatingList[j+1][k+1]) - userAverageList[k]) * userWeightsList[i][k]
				tempWeight = tempWeight +  abs(userWeightsList[i][k])
			predictionList[i][j] = userAverageList[i] + (temp/tempWeight)
			checkPredict[i][j] = 1
		else:
			predictionList[i][j] = float(userRatingList[j+1][i+1])
	#print predictionList[i]


userID = 1		#userID is passed to this page  predictionList[userID]

for j in xrange(0,numproblems-1):
	recommendProblemList[j][0] = int(userRatingList[j+1][0])
	recommendProblemList[j][1] = predictionList[userID][j]	
	recommendProblemList[j][2] = checkPredict[userID][j]

print recommendProblemList

temp = 0
for j in xrange(0,numproblems-2):			#sorting the problem ID's
	for k in xrange(j+1,numproblems-1):
		if recommendProblemList[j][1] < recommendProblemList[k][1] :
			temp = recommendProblemList[j]
			recommendProblemList[j] = recommendProblemList[k]
			recommendProblemList[k] = temp

#print recommendProblemList

finalRecommendation = [0 , 0 , 0, 0, 0]
count = 0
for j in xrange(0,numproblems-1):
	if recommendProblemList[j][2] == 1 :
		print recommendProblemList[j]
		finalRecommendation[count] = recommendProblemList[j][0]
		count = count + 1
	if count > 3 :
		break

#print "Recommendation for the user: " , finalRecommendation

c = csv.reader(open("app_data.csv","rb"))

data = []

for row in c:
	data.append(row)

numproblems = len(data) 
numusers = len(data[0]) 

# print data[0][0]
# print data[1]
# print data[2]
for j in xrange(0,numproblems-1):
	for i in xrange(0,3):
		if finalRecommendation[i] == int(data[j][0]) :
			print data[j]
			break 


# Notes for the entire process:

# We'll be having 4 tables for different attributes, Authors, Level of the User, Format and whatever...
# For each table each and every cell will be filled with a value as we have already initialed it with some value in the 
# beginning. We are suppose to update those values. 
# For every table we'll be calculating a User weight matrix. Using that user weight matrix we'll be predicting a score for the learning object.
# This can be done as the user matrix will be formed using the author table, even though all values a filled; this will only give a better user matrix.
# Now values for the learning object will be predicted using this User matrix. Finally, using a manual weight for all the attributes, we'll predict a final 
# score for the object.