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
	sheet = [("C_4", 0), ("C_4", 500), ("G_4", 500), ("G_4", 500), ("A_4", 500), ("A_4", 500), ("G_4", 500), 
	         ("F_4", 1000), ("F_4", 500), ("E_4", 500), ("E_4", 500), ("D_4", 500), ("D_4", 500), ("C_4", 500), 
	         ("G_4", 1000), ("G_4", 500), ("F_4", 500), ("F_4", 500), ("E_4", 500), ("E_4", 500), ("D_4", 500),
	         ("G_4", 1000), ("G_4", 500), ("F_4", 500), ("F_4", 500), ("E_4", 500), ("E_4", 500), ("D_4", 500),
	         ("C_4", 1000), ("C_4", 500), ("G_4", 500), ("G_4", 500), ("A_4", 500), ("A_4", 500), ("G_4", 500), 
	         ("F_4", 1000), ("F_4", 500), ("E_4", 500), ("E_4", 500), ("D_4", 500), ("D_4", 500), ("C_4", 500)]

	for note, time in sheet:
		track.append(midi.NoteOnEvent(tick=time, velocity=20, pitch=midi.__dict__[note]))

	# Instantiate a MIDI note off event, append it to the track
	off = midi.NoteOffEvent(tick=500, pitch=midi.G_3)
	track.append(off)

	# Add the end of track event, append it to the track
	eot = midi.EndOfTrackEvent(tick=1)
	track.append(eot)

	# Save the pattern to disk
	midi.write_midifile(outFileName, pattern)

	print "\nMusic written to " + outFileName + "\n"

if __name__ == "__main__":
	main()
