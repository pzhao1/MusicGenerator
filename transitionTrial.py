import midi
import glob

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


def getInfoForOne(inFileName):
	
	# Read in the midi file 
	inFilePattern = midi.read_midifile(inFileName)
	print inFileName
	tickList = []
	pitchList = []
	velocityList = []

	# Go through the notes. Record transitions
	for event in inFilePattern[1]:
		if isinstance(event, midi.events.NoteOnEvent):
			tickList.append(event.tick)
			pitchList.append(event.get_pitch())
			velocityList.append(event.get_velocity())

	# return these information
	return tickList, pitchList, velocityList


def getTransitionMatrix(inFileNames):
	tickByFile = {}
	pitchByFile = {}
	velocityByFile = {}
	tickStates = set()
	pitchStates = set()
	velocityStates = set()

	# Read all files and find the all the states that appeared in the files
	for name in inFileNames:
		tickByFile[name], pitchByFile[name], velocityByFile[name] = getInfoForOne(name)
		tickStates = tickStates.union(tickByFile[name])
		pitchStates = pitchStates.union(pitchByFile[name])
		velocityStates = velocityStates.union(velocityByFile[name])
	tickStates = list(tickStates)
	pitchStates = list(pitchStates)
	velocityStates = list(velocityStates)

	# Initialize a transition matrix for tick, pitch and velocity with all 0s
	# The states are all the states that appeared in all the input files
	tickM = {tick1: {tick2: 0.0 for tick2 in tickStates} for tick1 in tickStates}
	pitchM = {pitch1: {pitch2: 0.0 for pitch2 in pitchStates} for pitch1 in pitchStates}
	velocityM = {velocity1: {velocity2: 0.0 for velocity2 in velocityStates} for velocity1 in velocityStates}

	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		for i in range(len(tickByFile[name])-1):
			tickM[tickByFile[name][i]][tickByFile[name][i+1]] += 1
			pitchM[pitchByFile[name][i]][pitchByFile[name][i+1]] += 1
			velocityM[velocityByFile[name][i]][velocityByFile[name][i+1]] += 1
	tickM = normalize(tickM)
	pitchM = normalize(pitchM)
	velocityM = normalize(velocityM)

	return tickM, pitchM, velocityM




def main():
	files = glob.glob('midis/*.mid')
	print files
	tickM, pitchM, velocityM = getTransitionMatrix(files)
	# Just checking dimension is correct. 0 is not a key in pitch
	print "tickM size: ", len(tickM), "*", len(tickM[0])
	print "pitchM size: ", len(pitchM), "*", len(pitchM[pitchM.keys()[0]])
	print "velocityM size: ", len(velocityM),"*", len(velocityM[0])

if __name__ == "__main__":
	main()
