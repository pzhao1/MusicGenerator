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
		for item in range(128):
			i2 += pitchM[currentPitch][item]
			if r2<i2:
				currentPitch = item
				break

		r3 = random.random()
		i3 = 0
		for item in range(128):
			i3 += velocityM[currentVelocity][item]
			if r3<i3:
				currentVelocity = item
				break

		note = Note(currentPitch, currentLength, currentVelocity)
		notesList.append(note)

	return notesList

def main():

	composerName = "mozart"
	createNewTransition = False

	inputFiles = glob.glob('midis/midiworld/classic/' + composerName + '*.mid')
	if createNewTransition:
		getTransitionMatrix(inputFiles, composerName)
	
	lengthM = loadMatrixFromFile("matrices/" + composerName + "LengthM.dat")
	pitchM = loadMatrixFromFile("matrices/" + composerName + "PitchM.dat")
	velocityM = loadMatrixFromFile("matrices/"  + composerName + "VelocityM.dat")		

	notesList = highestPlausibility(lengthM, pitchM, velocityM)
	outFileName = "midis/" + composerName + "New.mid"

	# Instantiate a MIDI Pattern (contains a list of tracks)
	resolution=384
	pattern = midi.Pattern(resolution=resolution)
	

	# Instantiate a MIDI Track (contains a list of MIDI events)
	track = midi.Track()

	# Append the track to the pattern
	pattern.append(track)

	# Set Instrument to piano
	pEvent = midi.ProgramChangeEvent(tick=0, channel=0)
	pEvent.set_value(1)
	track.append(pEvent)

	# Set tempo to 150 bpm
	tEvent = midi.SetTempoEvent(tick=0)
	tEvent.set_bpm(150)
	track.append(tEvent)
	
	for note in notesList:
		tick = Note.lengthToTick(note.length, resolution)
		pitch = note.pitch
		velocity = note.volume

		
		# Append the new note
		track.append(midi.NoteOnEvent(channel=0, tick=0, pitch = pitch, velocity=velocity))
		# Stop the previous note to avoid unpleasant mixing
		track.append(midi.NoteOnEvent(channel=0, tick=tick, pitch=pitch,velocity=0))

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=0)
	track.append(eot)

	print pattern
	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"


if __name__ == '__main__':
	main()