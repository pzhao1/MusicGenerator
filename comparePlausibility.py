import transitionTrial as tt
import highestPlausibility as hp
import glob
import midi
import numpy as np

def comparePlausibility(tickM, pitchM, velocityM):
	"""
	In this function, we compare our randomly generated piece to a predetermined 
	good Bach piece.
	"""
	tickByFile = {}
	pitchByFile = {}
	velocityByFile = {}
	tickStates = set()		# There seems to be no set number of tick values

	goodPiece = []
	inFileNames = glob.glob('midis/midiworld/classic/bach_acttrag.mid')
	for name in inFileNames:
		tickByFile[name], pitchByFile[name], velocityByFile[name] = tt.getInfoForOne(name)
		for track in range(len(tickByFile[name])):
			tickStates = tickStates.union(tickByFile[name][track])
	tickStates = list(tickStates)

	for name in inFileNames:
		for track in range(len(tickByFile[name])):
				curTick = tickByFile[name][track]
				curPitch = pitchByFile[name][track]
				curVelocity = velocityByFile[name][track]
				for i in range(len(tickByFile[name][track])-1):

					goodPiece.append([curTick[i], curPitch[i], curVelocity[i]])

	logplGoodPiece = 0.0
	prevNote = None
	for note in goodPiece:
		#here we will find the log plausibility using all 3 categories, tick pitch and velocity
		if prevNote == None:
			#we dont count the first iteration
			prevNote = note
			pass
		logplGoodPiece += (np.log(tickM[prevNote[0]][note[0]]) + 
				np.log(pitchM[prevNote[1]][note[1]]) +
				np.log(velocityM[prevNote[2]][note[2]]))
		prevNote = note

	print logplGoodPiece
	return goodPiece


def main():
	#files = glob.glob('midis/midiworld/classic/bach*.mid')
	files = glob.glob('midis/midiworld/classic/bach_acttrag.mid')
	tickM, pitchM, velocityM = tt.getTransitionMatrix(files)
	#print files[0]
	newPiece = comparePlausibility(tickM, pitchM, velocityM)
	#print newPiece

if __name__ == '__main__':
	main()
