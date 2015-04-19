import midi


def main():
	
	inFileName = "midis/FurElise.mid"
	outFileName = "midis/FurEliseWeird.mid"

	# Read in the "Fur Elise" midi file
	elisePattern = midi.read_midifile(inFileName)
	
	# Create a new pattern for output, and set the control stuff to the same 
	# as the original midi.
	pattern = midi.Pattern(format=1, resolution=256)
	pattern.append(elisePattern[0])

	# Go through the notes. Change all C to C#
	track = midi.Track()
	pattern.append(track)
	for event in elisePattern[1]:
		if isinstance(event, midi.events.NoteOnEvent):
			if (event.data[0] % 12 == 0):
				event.data[0] += 1
		track.append(event)


	# Write the new file to disk.
	midi.write_midifile(outFileName, pattern)
	print "\nMusic written to " + outFileName + "\n"

if __name__ == "__main__":
	main()
	