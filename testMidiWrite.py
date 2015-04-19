import midi


def main():
	outFileName = "midis/twinkle.mid"

	# Instantiate a MIDI Pattern (contains a list of tracks)
	pattern = midi.Pattern()

	# Instantiate a MIDI Track (contains a list of MIDI events)
	track = midi.Track()

	# Append the track to the pattern
	pattern.append(track)


	# Write notes for Twinkle Twinkle Little Star.
	sheet = [("C_5", 0), ("C_5", 300), ("G_5", 300), ("G_5", 300), ("A_5", 300), ("A_5", 300), ("G_5", 300), 
	         ("F_5", 600), ("F_5", 300), ("E_5", 300), ("E_5", 300), ("D_5", 300), ("D_5", 300), ("C_5", 300), 
	         ("G_5", 600), ("G_5", 300), ("F_5", 300), ("F_5", 300), ("E_5", 300), ("E_5", 300), ("D_5", 300),
	         ("G_5", 600), ("G_5", 300), ("F_5", 300), ("F_5", 300), ("E_5", 300), ("E_5", 300), ("D_5", 300),
	         ("C_5", 600), ("C_5", 300), ("G_5", 300), ("G_5", 300), ("A_5", 300), ("A_5", 300), ("G_5", 300), 
	         ("F_5", 600), ("F_5", 300), ("E_5", 300), ("E_5", 300), ("D_5", 300), ("D_5", 300), ("C_5", 300)]

	prevNote = None
	for note, time in sheet:
		# Append the new note
		track.append(midi.NoteOnEvent(tick=time, velocity=20, pitch=midi.__dict__[note]))

		# Stop the previous note to avoid unpleasant mixing
		if prevNote != None and prevNote != note:
			track.append(midi.NoteOffEvent(tick=0, pitch=midi.__dict__[prevNote]))

		prevNote = note

	track.append(midi.NoteOffEvent(tick=300, pitch=midi.__dict__[prevNote]))

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=0)
	track.append(eot)

	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"

if __name__ == "__main__":
	main()
