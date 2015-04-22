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
	tickPitchVelocityList = [[0, 0, 0] for i in range(lengthOfPiece)]
	currentTick = random.choice(tickM.keys())
	currentPitch = random.choice(pitchM.keys())
	currentVelocity = random.choice(velocityM.keys())
	#currentPitch = random.choice([pitch for pitch in pitchM.iterkeys() if sum(pitchM[pitch].values())!=0])
	#currentVelocity = random.choice([velocity for velocity in velocityM.iterkeys() if sum(velocityM[velocity].values())!=0])

	print "start:", currentTick, currentPitch, currentVelocity
	index = 0
	indexpitch = 0
	indexvelocity = 0
	for number in range(lengthOfPiece):
		r = random.random()
		i = 0
		for item in tickM[currentTick]:
			i += tickM[currentTick][item]
			if r<i:
				tickPitchVelocityList[index][0] = item
				index += 1
				currentTick = item
				break

		r2 = random.random()
		i2 = 0
		for item in pitchM[currentPitch]:
			i2 += pitchM[currentPitch][item]
			if r2<i2:
				tickPitchVelocityList[indexpitch][1] = item
				indexpitch += 1
				currentPitch = item
				break

		r3 = random.random()
		i3 = 0
		for item in pitchM[currentVelocity]:
			i3 += velocityM[currentVelocity][item]
			if r3<i3:
				tickPitchVelocityList[indexvelocity][2] = item
				indexvelocity += 1
				currentVelocity = item
				break
		#print "index", index, ":", tickPitchVelocityList[indexpitch]

	print tickPitchVelocityList
	return tickPitchVelocityList

def main():
	inputFiles = glob.glob('midis/midiworld/classic/bach_acttrag.mid')
	createNewTransition = True
	if createNewTransition:
		tickM, pitchM, velocityM = tt.getTransitionMatrix(inputFiles, 'tickM.txt', 'picthM.txt', 'velocityM.txt')
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
	for tick, pitch, velocity in tickPitchVelocityList:
		# Append the new note
		track.append(midi.NoteOnEvent(tick=tick, velocity=velocity, pitch=pitch))
		# Stop the previous note to avoid unpleasant mixing
		if prevPitch != None and prevPitch != pitch:
			track.append(midi.NoteOffEvent(tick=tick, pitch=pitch))
		prevPitch = pitch

	track.append(midi.NoteOffEvent(tick=300, pitch=prevPitch))

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=0)
	track.append(eot)

	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"


if __name__ == '__main__':
	main()