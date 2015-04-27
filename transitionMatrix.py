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


def getTransitionMatrix(inFileNames, savePrefix):
	# Initialize a transition matrix for tick, pitch and velocity with all 0s
	lengthM = {length1: {length2: 1.0 for length2 in range(1,Note.UNIT+1)} for length1 in range(1,Note.UNIT+1)}
	pitchM = {pitch1: {pitch2: 1.0 for pitch2 in range(128)} for pitch1 in range(128)}
	velocityM = {velocity1: {velocity2: 1.0 for velocity2 in range(128)} for velocity1 in range(128)}


	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		print "reading", name
		sheet = getSheet(name)
		for track in sheet.getTracks():
			notes = track.getNotes()
			for i in range(len(notes)-1):
				curNote = notes[i]
				nextNote = notes[i+1]
				lengthM[curNote.length][nextNote.length] += 1
				pitchM[curNote.pitch][nextNote.pitch] += 1
				velocityM[curNote.volume][nextNote.volume] += 1
	
	lengthM = normalize(lengthM)
	pitchM = normalize(pitchM)
	velocityM = normalize(velocityM)

	saveMatrixToFile(lengthM, "matrices/" + savePrefix + "LengthM.dat")
	saveMatrixToFile(pitchM, "matrices/" + savePrefix + "PitchM.dat")
	saveMatrixToFile(velocityM, "matrices/" + savePrefix + "VelocityM.dat")


def getTransitionMatrix2(inFileNames, savePrefix):
	# Initialize a transition matrix for tick, pitch and velocity with all 0s
	lengthM = {length1: {length2: 1.0 for length2 in range(1,Note.UNIT+1)} for length1 in range(1,Note.UNIT+1)}
	listOfTuples = []
	for item1 in range(128):
		for item2 in range(128):
			listOfTuples.append((item1, item2))
	pitchM = {(pitch1, pitch2): 
		{pitch3: 1.0 for pitch3 in range(128)} for (pitch1,pitch2) in listOfTuples}
	velocityM = {velocity1: {velocity2: 1.0 for velocity2 in range(128)} for velocity1 in range(128)}


	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		print "reading", name
		sheet = getSheet(name)
		for track in sheet.getTracks():
			notes = track.getNotes()
			for i in range(len(notes)-2):
				curNote = notes[i]
				nextNote = notes[i+1]
				nextNote2 = notes[i+2]
				lengthM[curNote.length][nextNote.length] += 1
				pitchM[(curNote.pitch,nextNote.pitch)][nextNote2.pitch] += 1
				velocityM[curNote.volume][nextNote.volume] += 1
			# Last transition for length and velocity
			curNote = notes[len(notes)-2]
			nextNote = notes[len(notes)-1]
			lengthM[curNote.length][nextNote.length] += 1
			velocityM[curNote.volume][nextNote.volume] += 1

	lengthM = normalize(lengthM)
	pitchM = normalize(pitchM)
	velocityM = normalize(velocityM)

	saveMatrixToFile(lengthM, "matrices/" + savePrefix + "LengthM2.dat")
	saveMatrixToFile(pitchM, "matrices/" + savePrefix + "PitchM2.dat")
	saveMatrixToFile(velocityM, "matrices/" + savePrefix + "VelocityM2.dat")


def getTransitionMatrixForKeys(inFileNames):
	# Initialize a transition matrix for tick, pitch and velocity with all 0s

	pitchMList = []
	lengthM = {length1: {length2: 1.0 for length2 in range(1,Note.UNIT+1)} for length1 in range(1,Note.UNIT+1)}
	velocityM = {velocity1: {velocity2: 1.0 for velocity2 in range(128)} for velocity1 in range(128)}

	for i in range(12):
		pitchMList.append({pitch1: {pitch2: 1.0 for pitch2 in range(128)} for pitch1 in range(128)})


	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		print "reading", name
		sheet = getSheet(name)
		keySignature = sheet.getKeySignature()
		for track in sheet.getTracks():
			notes = track.getNotes()
			for i in range(len(notes)-1):
				curNote = notes[i]
				nextNote = notes[i+1]
				pitchMList[keySignature][curNote.pitch][nextNote.pitch] += 1
				lengthM[curNote.length][nextNote.length] += 1
				velocityM[curNote.volume][nextNote.volume] += 1
	
	for i in range(12):
		pitchMList[i] = normalize(pitchMList[i])
	lengthM = normalize(lengthM)
	velocityM = normalize(velocityM)

	for i in range(12):
		saveMatrixToFile(pitchMList[i], "matrices/key" + Note.KEY_TABLE[i] + "PitchM.dat")
	saveMatrixToFile(lengthM, "matrices/allLengthM.dat")
	saveMatrixToFile(velocityM, "matrices/allVelocityM.dat")

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
