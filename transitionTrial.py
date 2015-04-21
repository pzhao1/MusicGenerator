import midi
import glob
import warnings

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
	print "reading", inFileName, "pattern length = ", len(inFilePattern)
	tickList = {}
	pitchList = {}
	velocityList = {}

	# Go through the notes. Record transitions
	num_tracks = len(inFilePattern)
	for track in range(num_tracks):
		tickList[track] = []
		pitchList[track] = []
		velocityList[track] = []
		for event in inFilePattern[track]:
			if isinstance(event, midi.events.NoteOnEvent):
				tickList[track].append(event.tick)
				pitchList[track].append(event.get_pitch())
				velocityList[track].append(event.get_velocity())
		#print "   track", track, ":", len(tickList[track])

	# return these information
	return tickList, pitchList, velocityList


def getTransitionMatrix(inFileNames):
	tickByFile = {}
	pitchByFile = {}
	velocityByFile = {}
	tickStates = set()		# There seems to be no set number of tick values

	# Read all files and find the all the tick states that appeared in the files
	for name in inFileNames:
		tickByFile[name], pitchByFile[name], velocityByFile[name] = getInfoForOne(name)
		for track in range(len(tickByFile[name])):
			tickStates = tickStates.union(tickByFile[name][track])
	tickStates = list(tickStates)

	# Initialize a transition matrix for tick, pitch and velocity with all 0s
	tickM = {tick1: {tick2: 0.0 for tick2 in tickStates} for tick1 in tickStates}
	pitchM = {pitch1: {pitch2: 0.0 for pitch2 in range(128)} for pitch1 in range(128)}
	velocityM = {velocity1: {velocity2: 0.0 for velocity2 in range(128)} for velocity1 in range(128)}

	# Update the transition matrix based on oberservations from each file
	for name in inFileNames:
		for track in range(len(tickByFile[name])):
			curTick = tickByFile[name][track]
			curPitch = pitchByFile[name][track]
			curVelocity = velocityByFile[name][track]
			for i in range(len(tickByFile[name][track])-1):
				tickM[curTick[i]][curTick[i+1]] += 1
				pitchM[curPitch[i]][curPitch[i+1]] += 1
				velocityM[curVelocity[i]][curVelocity[i+1]] += 1
	tickM = normalize(tickM)
	pitchM = normalize(pitchM)
	velocityM = normalize(velocityM)

	return tickM, pitchM, velocityM




def main():
	files = glob.glob('midis/midiworld/classic/bach*.mid')
	#print files
	tickM, pitchM, velocityM = getTransitionMatrix(files)
	# Just checking dimension is correct. 0 is not a key in pitch
	print "tickM size: ", len(tickM), "*", len(tickM[0])
	print "pitchM size: ", len(pitchM), "*", len(pitchM[pitchM.keys()[0]])
	print "velocityM size: ", len(velocityM),"*", len(velocityM[0])

if __name__ == "__main__":
	main()
