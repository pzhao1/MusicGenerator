import midi
import glob
import fractions
import operator

class Note(object):
	# The smallest note we 
	UNIT = 384
	KEY_TABLE = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
	
	"""
	resolution is defined in header of midi. It's (#Ticks)/(quarter note)
	Our definition of length is (fraction of whole note)*Note.UNIT
	"""
	@staticmethod
	def tickToLength(ticks, resolution):
		return ( (ticks*Note.UNIT)/(4*resolution) )

	@staticmethod
	def lengthToTick(length, resolution):
		return ( (length*4*resolution)/Note.UNIT )
	

	"""
	pitch : 0-127. 48 is C_4.
	length:	Length of this note in terms of 1/UNIT whole notes.
	volume: 0-127  
	"""
	def __init__(self, pitch_in, length_in, volume_in):
		self.pitch = pitch_in			
		self.length = length_in
		self.volume = volume_in


	@property
	def pitch(self):
		return self._pitch
	@pitch.setter
	def pitch(self, pitch_in):
		if pitch_in < 0 or pitch_in > 127:
			raise ValueError("Note: " + str(pitch_in) + " is not a valid pitch value")
		self._pitch = pitch_in


	@property
	def length(self):
		return self._length
	@length.setter
	def length(self, length_in):
		if length_in < 1:
			raise ValueError("Note: " + str(length_in) + " is not a valid length value")
		if length_in > Note.UNIT:
			length_in = Note.UNIT
		self._length = length_in


	@property
	def volume(self):
		return self._volume
	@volume.setter
	def volume(self, volume_in):
		if volume_in < 0 or volume_in > 127:
			raise ValueError("Note: " + str(volume_in) + " is not a valid volume value")
		self._volume = volume_in
	

	"""Added so we can use str(note)"""
	def __str__(self):
		pitch_str = Note.KEY_TABLE[self.pitch%12] + str(self.pitch/12)
		gcd1 = fractions.gcd(self.length, Note.UNIT)
		length_str = ("%3d/%-3d" %(self.length/gcd1, Note.UNIT/gcd1))
		return ("Note(%4s, %s, %3d)" %(pitch_str, length_str, self.volume))
	

	"""Added so we can use Note as keys in dictionary"""
	def __hash__(self):
		return hash((self.pitch, self.length, self.volume))

	
	"""Added so we can use Note as keys in dictionary"""
	def __cmp__(self, other):
		
		return cmp((self.pitch, self.length, self.volume), (other.pitch, other.length, other.volume))

	
	"""Added to get prettier representations in error messages
	   KeyError: Note(x, y, z) instead of KeyError: Note instance at 0x12345678"""
	def __repr__(self):
		return str(self) 



class Bar(object):
	def __init__(self, numerator_in, denominator_in, extend_in):
		if numerator_in < 1:
			raise ValueError("Bar: " + str(numerator_in) + " is not a valid numerator value")
		if denominator_in < 1:
			raise ValueError("Bar: " + str(denominator_in) + " is not a valid denominator value")
		if not isinstance(extend_in, bool):
			raise ValueError("Bar: " + str(extend_in) + " is not a boolean value")

		self.numerator = numerator_in
		self.denominator = denominator_in
		self.extend = extend_in
		self.notes = []
	

	def __str__(self):
		timeSignature = "%d/%d" %(self.numerator, self.denominator)
		if len(self.notes) == 0:
			return "Bar(" + timeSignature + " [ ])"

		toReturn = "Bar(" + timeSignature + " [ "
		for note in self.notes[:-1]:
			toReturn += (str(note) + ", ")
		toReturn += (str(self.notes[-1]) + " ])")
		return toReturn 


	def __repr__(self):
		return "Bar(%d/%d, %d notes)" %(self.numerator, self.denominator, len(self.notes))


	def spaceLeft(self):
		totalLength = self.numerator*(Note.UNIT/self.denominator)
		filledLength = sum([x.length for x in self.notes])
		return (totalLength - filledLength)

	"""
	Try to append a note to this channel.
	If overflows, don't append and return False. Else, append and return True.
	"""
	def addNote(self, note_in):
		if (note_in.length > self.spaceLeft()):
			return False
		self.notes.append(note_in)
		return True


class Track(object):
	def __init__(self, index_in, channel_in):
		self.index = index_in
		self.channel = channel_in
		self.notes = []


	def __str__(self):
		toReturn = ("Track %d on Channel %d: %d notes" %(self.index, self.channel, len(self.notes)))
		toReturn += ("\n" + "-"*60)
		for index in range(len(self.notes)):
			if (index%4) == 0:
				toReturn += "\n"
			toReturn += (" %s " %(str(self.notes[index])))
		return toReturn


	def __repr__(self):
		return ("Track %d on Channel %d: %d notes" %(self.index, self.channel, len(self.notes)))

	def addNote(self, note_in):
		self.notes.append(note_in)

	def getNotes(self):
		return self.notes



class Sheet(object):

	def __init__(self, name_in, resolution_in):
		self.name = name_in
		self.resolution = resolution_in
		self.tracks = {}

	def __str__(self):
		toReturn = "\nTrack: " + self.name
		for track in self.getTracks():
			toReturn += ("\n\n" + str(track))
		toReturn += "\n"
		return toReturn

	def __repr__(self):
		return "Sheet(%s, %d channels)" %(self.name, len(self.tracks))

	def addNote(self, trackIndex, channelIndex, note):
		if (trackIndex, channelIndex) not in self.tracks:
			self.tracks[(trackIndex, channelIndex)] = Track(trackIndex, channelIndex)

		self.tracks[(trackIndex, channelIndex)].addNote(note)
		

	def getTracks(self):
		return [value for (key, value) in sorted(self.tracks.items())]

	def getKeySignature(self):

		majorKeys = [
						[0, 2, 4, 5, 7, 9, 11],
						[1, 3, 5, 6, 8, 10, 0],
						[2, 4, 6, 7, 9, 11, 1],
						[3, 5, 7, 8, 10, 0, 2],
						[4, 6, 8, 9, 11, 1, 3],
						[5, 7, 9, 10, 0, 2, 4],
						[6, 8, 10, 11, 1, 3, 5],
						[7, 9, 11, 0, 2, 4, 6],
						[8, 10, 0, 1, 3, 5, 7],
						[9, 11, 1, 2, 4, 6, 8],
						[10, 0, 2, 3, 5, 7, 9],
						[11, 1, 3, 4, 6, 8, 10]
					]

		pitchDistribution = {x:0 for x in range(12)}
		for track in self.getTracks():
			for note in track.getNotes():
				pitchDistribution[(note.pitch)%12] += 1

		keyFreqSorted = sorted(pitchDistribution.items(), key=operator.itemgetter(1))
		
		bestMatch = -1
		bestScore = -1
		for guess in range(12):
			score = 0
			for key, freq in keyFreqSorted:
				if key in majorKeys[guess]:
					score += freq

			if score > bestScore:
				bestScore = score
				bestMatch = guess

		return bestMatch




def handleNoteOnEvent(sheet, event, currentNotes, currentTick, currentTrack):
	# NoteOnEvent with volume=0 are rests. We ignore them.
	# Notice rest time is still counted into current note length.
	if event.data[1] > 0:
		curNoteInfo = currentNotes[event.channel]

		# We are getting a new note. Write current note if there is one.
		if curNoteInfo["hasNote"]:
			newNoteLen = Note.tickToLength(currentTick - curNoteInfo["startTick"], sheet.resolution)
			
			# This happens when we have a chord. For now we only get the highest note of chord.
			if newNoteLen == 0:
				if event.data[0] > curNoteInfo["pitch"]:
					curNoteInfo["pitch"] = event.data[0]
				return

			newNote = Note(curNoteInfo["pitch"], newNoteLen, curNoteInfo["volume"])
			sheet.addNote(currentTrack, event.channel, newNote)

		# Store new note as current note.
		curNoteInfo["hasNote"] = True
		curNoteInfo["startTick"] = currentTick
		curNoteInfo["pitch"] = event.data[0]
		curNoteInfo["volume"] = event.data[1]


def getSheet(inFileName):

	# Read in the input midi file
	inFilePattern = midi.read_midifile(inFileName)
	resolution = inFilePattern.resolution


	sheet = Sheet(inFileName, resolution)

	# Loop through events from beginning to end and generate sheet
	for currentTrack in range(len(inFilePattern)):
		track = inFilePattern[currentTrack]
		currentTick = 0
		currentNotes = [{"hasNote":False, "startTick":0, "pitch":-1, "volume":-1} for x in range(16)]
		for event in track:
			currentTick += event.tick
			if isinstance(event, midi.events.NoteOnEvent):
				handleNoteOnEvent(sheet, event, currentNotes, currentTick, currentTrack)
			else:
				# Handle other events later.
				pass

	return sheet


def main():
	pass
	#pattern = midi.read_midifile("midis/midiworld/classic/chopin_fantaisie.mid")
	#print pattern

if __name__ == "__main__":
	main()


