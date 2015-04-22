import transitionTrial as tt
import random
import glob

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

	print tickPitchVelocityList
	return tickPitchVelocityList

def main():
	files = glob.glob('midis/midiworld/classic/bach*.mid')
	tickM, pitchM, velocityM = tt.getTransitionMatrix(files)

	tickPitchVelocityList = highestPlausibility(tickM, pitchM, velocityM)

if __name__ == '__main__':
	main()