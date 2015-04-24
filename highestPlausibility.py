from transitionMatrix import *
import random
import glob
import midi

def highestPlausibility(lengthM, pitchM, velocityM):
	"""
	This function takes 3 matrices as parameters, and outputs a list of notes
	corresponding to randomly chosen length, pitch and volume (velocity) based on the
	transition probabilieies obtained from the 3 matrices.

	returns a list of notes
	"""
	lengthOfPiece = 100
	notesList = []
	currentLength = random.choice(lengthM.keys())
	currentPitch = random.choice(pitchM.keys())
	currentVelocity = random.choice(velocityM.keys())

	notesList.append(Note(currentPitch, currentLength, currentVelocity))

	for number in range(lengthOfPiece-1):
		r = random.random()
		i = 0
		for item in lengthM[currentLength]:
			i += lengthM[currentLength][item]
			if r<i:
				currentLength = item
				break

		r2 = random.random()
		i2 = 0
		for item in pitchM[currentPitch]:
			i2 += pitchM[currentPitch][item]
			if r2<i2:
				currentPitch = item
				break

		r3 = random.random()
		i3 = 0
		for item in pitchM[currentVelocity]:
			i3 += velocityM[currentVelocity][item]
			if r3<i3:
				currentVelocity = item
				break

		note = Note(currentPitch, currentLength, currentVelocity)
		notesList.append(note)

	return notesList

def main():
	#inputFiles = glob.glob('midis/midiworld/classic/bach_acttrag.mid')
	inputFiles = glob.glob('midis/midiworld/classic/bach*.mid')
	createNewTransition = True
	if createNewTransition:
		getTransitionMatrix(inputFiles)
	
	lengthM = loadMatrixFromFile("matrices/bachLengthM.dat")
	pitchM = loadMatrixFromFile("matrices/bachPitchM.dat")
	velocityM = loadMatrixFromFile("matrices/bachVelocityM.dat")		

	notesList = highestPlausibility(lengthM, pitchM, velocityM)
	outFileName = "midis/new.mid"
	# Instantiate a MIDI Pattern (contains a list of tracks)
	pattern = midi.Pattern()
	resolution = pattern.resolution
	# Instantiate a MIDI Track (contains a list of MIDI events)
	track = midi.Track()
	# Append the track to the pattern
	pattern.append(track)
	
	for note in notesList:
		tick = note.lengthToTick(note.length, resolution)
		pitch = note.pitch
		velocity = note.volume
		# Append the new note
		track.append(midi.NoteOnEvent(tick=0, pitch = pitch, velocity=velocity))
		# Stop the previous note to avoid unpleasant mixing
		track.append(midi.NoteOnEvent(tick=tick, pitch=pitch,velocity=0))

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=0)
	track.append(eot)

	print pattern
	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"


if __name__ == '__main__':
	main()