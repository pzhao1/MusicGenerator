import midi
import glob
import warnings
import pickle
from processMidi import *

def saveMatrixToFile(matrix, filePath):
	pickle.dump(matrix, open(filePath,"wb"))
	print "Saved matrix to " + filePath

def loadMatrixFromFile(filePath):
	matrix = pickle.load(open(filePath, "rb"))
	print "Loaded matrix" + filePath
	return matrix


def normalize(matrix):
	for key1 in matrix:
		total = sum(matrix[key1].values())
		# This note has never transitioned to other notes 
		# (rare, but can happen if it only appears at the end)
		if total == 0:
			for key2 in matrix[key1]:
				matrix[key1][key2] = 1/len(matrix)
		# Otherwise, normalize the row by dividing each entry by the row sum
		else:
			for key2 in matrix[key1]:
				matrix[key1][key2] = matrix[key1][key2]/total
	return matrix


def getTransitionMatrix(inFileNames):
	lengthByFile = {}
	pitchByFile = {}
	velocityByFile = {}

	# Initialize a transition matrix for tick, pitch and velocity with all 0s
	lengthM = {length1: {length2: 1.0 for length2 in range(1,Note.UNIT+1)} for length1 in range(1,Note.UNIT+1)}
	pitchM = {pitch1: {pitch2: 1.0 for pitch2 in range(128)} for pitch1 in range(128)}
	velocityM = {velocity1: {velocity2: 1.0 for velocity2 in range(128)} for velocity1 in range(128)}


	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		print "reading", name
		sheet = getSheet(name)
		channels = sheet.getChannels()
		for channel in channels:
			notes = channel.getNotes()
			for i in range(len(notes)-1):
				curNote = notes[i]
				nextNote = notes[i+1]
				lengthM[curNote.length][nextNote.length] += 1
				pitchM[curNote.pitch][nextNote.pitch] += 1
				velocityM[curNote.volume][nextNote.volume] += 1
	
	lengthM = normalize(lengthM)
	pitchM = normalize(pitchM)
	velocityM = normalize(velocityM)

	saveMatrixToFile(lengthM, "matrices/bachLengthM.dat")
	saveMatrixToFile(pitchM, "matrices/bachPitchM.dat")
	saveMatrixToFile(velocityM, "matrices/bachVelocityM.dat")




def main():

	# Code used to generate and save matrices to file
	files = glob.glob('midis/midiworld/classic/bach*.mid')
	getTransitionMatrix(files)

	# Code used to load matrices from file
	lengthM = loadMatrixFromFile("matrices/bachLengthM.dat")
	pitchM = loadMatrixFromFile("matrices/bachPitchM.dat")
	velocityM = loadMatrixFromFile("matrices/bachVelocityM.dat")

	print "pitchM size: ", len(pitchM), "*", len(pitchM[pitchM.keys()[0]])
	print "lengthM size: ", len(lengthM), "*", len(lengthM[1])
	print "velocityM size: ", len(velocityM),"*", len(velocityM[0])
	

if __name__ == "__main__":
	main()
