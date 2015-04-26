import midi
import glob
import fractions

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
	def appendNote(self, note_in):
		if (note_in.length > self.spaceLeft()):
			return False
		self.notes.append(note_in)
		return True


class Channel(object):
	def __init__(self, index_in):
		self.index = index_in
		self.notes = []


	def __str__(self):
		toReturn = "Channel %d: %d notes" %(self.index, len(self.notes))
		toReturn += ("\n" + "-"*60)
		for index in range(len(self.notes)):
			if (index%4) == 0:
				toReturn += "\n"
			toReturn += (" %s " %(str(self.notes[index])))
		return toReturn


	def __repr__(self):
		return "Channel(%d, %d notes)" %(self.index, len(self.notes))

	def appendNote(self, note_in):
		self.notes.append(note_in)

	def getNotes(self):
		return self.notes



class Sheet(object):

	def __init__(self, name_in, resolution_in):
		self.name = name_in
		self.resolution = resolution_in
		self.channels = {}

	def __str__(self):
		toReturn = "\nTrack: " + self.name
		for channel in self.getChannels():
			toReturn += ("\n\n" + str(channel))
		toReturn += "\n"
		return toReturn

	def __repr__(self):
		return "Sheet(%s, %d channels)" %(self.name, len(self.channels))

	def addNote(self, channel_in, note_in):
		if channel_in not in self.channels:
			self.channels[channel_in] = Channel(channel_in)
		self.channels[channel_in].appendNote(note_in)
		
	def addChannel(self, channel_in):
		if channel_in.index in self.channels:
			raise ValueError("Sheet::addChannel(): channel index %d already exists" %(channel_in.index))
		self.channels[channel_in.index] = channel_in

	def getChannels(self):
		return [value for (key, value) in sorted(self.channels.items())]





def handleNoteOnEvent(sheet, currentNotes, tickCount, event):
	# NoteOnEvent with volume=0 are rests. We ignore them.
	# Notice rest time is still counted into current not length.
	if event.data[1] > 0:
		curNoteInfo = currentNotes[event.channel]

		# We are getting a new note. Write current note if there is one.
		if curNoteInfo["hasNote"]:
			newNoteLen = Note.tickToLength(tickCount - curNoteInfo["startTick"], sheet.resolution)
			
			# This happens when we have a chord. For now we only get the highest note of chord.
			if newNoteLen == 0:
				if event.data[0] > curNoteInfo["pitch"]:
					curNoteInfo["pitch"] = event.data[0]
				return

			newNote = Note(curNoteInfo["pitch"], newNoteLen, curNoteInfo["volume"])
			sheet.addNote(event.channel, newNote)

		# Store new note as current note.
		curNoteInfo["hasNote"] = True
		curNoteInfo["startTick"] = tickCount
		curNoteInfo["pitch"] = event.data[0]
		curNoteInfo["volume"] = event.data[1]


def getSheet(inFileName):

	# Read in the input midi file
	inFilePattern = midi.read_midifile(inFileName)
	resolution = inFilePattern.resolution

	# Tracks happen in parallel. Loop through tracks to gather event information
	eventSchedule = {}
	for track in inFilePattern:
		tickCount = 0
		for event in track:
			tickCount += event.tick
			if tickCount not in eventSchedule:
				eventSchedule[tickCount] = []
			eventSchedule[tickCount].append(event)


	# Loop through events from beginning to end and generate sheet
	sheet = Sheet(inFileName, resolution)
	currentNotes = []
	for i in range(16):
		currentNotes.append({"hasNote":False, "startTick":0, "pitch":-1, "volume":-1})

	for tickCount, eventList in sorted(eventSchedule.items()):
		for event in eventList:
			if isinstance(event, midi.events.NoteOnEvent):
				handleNoteOnEvent(sheet, currentNotes, tickCount, event)
			else:
				# Handle other events later.
				pass

	return sheet


def main():
	pass
	#fileNames = glob.glob("midis/midiworld/classic/*.mid")
	#for fileName in fileNames:
	#	sheet = getSheet(fileName)
	#	print fileName, len(sheet.channels)

if __name__ == "__main__":
	main()


