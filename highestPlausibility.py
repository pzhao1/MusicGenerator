import transitionTrial as tt
import random
import glob
import midi

def highestPlausibility(tickM, pitchM, velocityM):
	"""
	This function takes 3 matrices as parameters, and outputs a list of lists
	corresponding to randomly chosen tick, pitch and velocity based on the
	highest plausibility of transitions obtained from the 3 matrices.

	returns a list of lists, with the inner list consisting of [tick, pitch,
	velocity] and the outer list ordering the nodes visited.
	"""
	lengthOfPiece = 100
	tickPitchVelocityList = []
	currentTick = random.choice(tickM.keys())
	currentPitch = random.choice(pitchM.keys())
	currentVelocity = random.choice(velocityM.keys())

	print "start:", currentTick, currentPitch, currentVelocity
	tickPitchVelocityList.append([currentTick, currentPitch, currentVelocity])

	for number in range(lengthOfPiece-1):
		element = [0,0,0]
		r = random.random()
		i = 0
		for item in tickM[currentTick]:
			i += tickM[currentTick][item]
			if r<i:
				currentTick = item
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
		#print "index", index, ":", tickPitchVelocityList[indexpitch]
		tickPitchVelocityList.append([currentTick, currentPitch, currentVelocity])

	print tickPitchVelocityList
	return tickPitchVelocityList

def main():
	inputFiles = glob.glob('midis/midiworld/classic/bach_acttrag.mid')
	#inputFiles = glob.glob('midis/midiworld/classic/bach*.mid')
	createNewTransition = True
	if createNewTransition:
		tickM, pitchM, velocityM = tt.getTransitionMatrix(inputFiles)
		print('tickM.txt', 'picthM.txt', 'velocityM.txt')
	else:
		pass
		# Somehow read in the transition matrices
		# Tentative file names are above, but we can change the file format
		

	tickPitchVelocityList = highestPlausibility(tickM, pitchM, velocityM)
	outFileName = "midis/new.mid"
	# Instantiate a MIDI Pattern (contains a list of tracks)
	pattern = midi.Pattern()
	# Instantiate a MIDI Track (contains a list of MIDI events)
	track = midi.Track()
	# Append the track to the pattern
	pattern.append(track)
	
	prevPitch = None
	for item in tickPitchVelocityList:
		tick = item[0]
		pitch = item[1]
		velocity = item[2]
		# Append the new note
		track.append(midi.NoteOnEvent(tick=tick, pitch = pitch, velocity=velocity))
		# Stop the previous note to avoid unpleasant mixing
		track.append(midi.NoteOnEvent(tick=112, pitch=pitch,velocity=0))
		prevPitch = pitch

	track.append(midi.NoteOffEvent(tick=300, pitch=prevPitch))

	print pattern

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=0)
	track.append(eot)

	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"


if __name__ == '__main__':
	main()