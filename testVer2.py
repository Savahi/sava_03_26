
nameContext = [ ["John", "Wayne"], ["Tom", "Hanks"], ["Tom", "Cruise"], ["Clint", "Eastwood"], ["Jon", "Hamm"], ["John", "Nolan"], ["William"], ["Fitcher"] ]

def main():
	print correctNames( "tomorrow I have a meeting with Tim Hanks Tom Crus and Eastwud" )
	print correctNames( "Michael likes movies with Jon Way and Client East" )
	print correctNames( "Jonn invited me Jon Ham and Jon Wane, over for a lunch" )
	print correctNames( "I like movies with Jon Way Cruis Client East" )
	print correctNames( "the guests are Tim Hencs Clunt Tpm Kruse" )

def correctNames( sentence ):

	print "\n***********************************************\nDoing '%s':" % (sentence)

	namesInContext = []
	for n in range(len(nameContext)):
		fullName = nameContext[n]
		for i in range( len(fullName) ):
			namesInContext.append( [ fullName[i], n ] )
	#print "Singe name context: " + str(namesInContext)

	namesInSentence, wordsInSentence = retrieveNamesFromSentence( sentence )
	#print "Names in sentence: " + str(namesInSentence)

	score, namesRecognized = recognize( namesInContext, namesInSentence, 0.75, 0.60, 1.0 )
	print "score=%f, names=%s" % (score, str(namesRecognized))

	correctedNames = []
	for n in range(len(namesRecognized)):
		wordNum = namesRecognized[n][1]
		wordsInSentence[wordNum] = namesRecognized[n][4]
		correctedNames.append( (namesRecognized[n][3], namesRecognized[n][4] )  )

	fixedSentence = "";
	for w in wordsInSentence:
		fixedSentence += " " + w
	print fixedSentence
 
	return correctedNames
#end of fixSentence

from itertools import permutations

def recognize( namesInContext, namesInSentence, singleNameThreshold=0.75, fullNameThreshold=0.60, fullNameBonus=1.0 ):

	bestSumOfScores = 0.0
	bestNamesRecognized = ""
	for namesInContextTry in permutations( namesInContext, len(namesInSentence) ):
		namesRecognized = []
		for n in range( len(namesInSentence) ):
			score = jaroScore( namesInContextTry[n][0], namesInSentence[n][0] )
			namesRecognized.append( [ score, namesInSentence[n][1], namesInContextTry[n][1], namesInSentence[n][0], namesInContextTry[n][0], 's' ] )				
		if len(namesRecognized) == 0:
			continue

		for n in range( 1, len(namesRecognized) ):
			if namesRecognized[n][2] == namesRecognized[n-1][2] and namesRecognized[n][1] - namesRecognized[n-1][1] == 1:
				fullNameInSentence = namesRecognized[n-1][3] + " " + namesRecognized[n][3]
				fullNameInContext = namesRecognized[n-1][4] + " " + namesRecognized[n][4]
				score = jaroScore( fullNameInSentence, fullNameInContext )	
				namesRecognized[n-1][0] = score * fullNameBonus				
				namesRecognized[n-1][5] = 'f'
				namesRecognized[n][0] = score * fullNameBonus				
				namesRecognized[n][5] = 'f'

		for n in range( len(namesRecognized)-1, -1, -1 ):
			if namesRecognized[n][5] == 's':
				if namesRecognized[n][0] < singleNameThreshold:
					del namesRecognized[n]
					continue
			if namesRecognized[n][5] == 'f':
				if namesRecognized[n][0] < fullNameThreshold:
					del namesRecognized[n]

		if len(namesRecognized) == 0:
			continue

		sumOfScores = 0.0
		for n in range( 1, len(namesRecognized) ):
			sumOfScores += namesRecognized[n][0]

		#sumOfScores = sumOfScores / float(len(namesRecognized))
		if sumOfScores > bestSumOfScores:
			bestSumOfScores = sumOfScores
			bestNamesRecognized = namesRecognized
	return bestSumOfScores, bestNamesRecognized	
# end of def 

def	retrieveNamesFromSentence( sentence ):
	names = []
	words = str.split( sentence )
	for i in range( len( words ) ):
		if words[i][0].isupper() == False:
			continue
		if words[i] == "I":
			continue
		names.append( [ words[i], i ] )
	# end if for
	return names, words
# end of def 


def jaroScore( s1, s2 ):

	matchingsNum = 0.0
	transpositionsNum = 0.0
	s1Len = len(s1)
	s2Len = len(s2)
	s1Matchings = [ False for i in range( s1Len ) ] 
	s2Matchings = [ False for i in range( s2Len ) ] 

	maxDistanceAllowed = int( max( s1Len, s2Len ) / 2.0 - 1.0 )

	for s1Index in range( s1Len ):
		s2StartIndex = s1Index - maxDistanceAllowed
		if s2StartIndex < 0:
			s2StartIndex = 0

		s2EndIndex = s1Index + maxDistanceAllowed
		if s2EndIndex >= s2Len:
			s2EndIndex = s2Len-1

		for s2Index in range( s2StartIndex, s2EndIndex + 1 ):
			if s2Matchings[ s2Index ]:
				continue
			if s1[ s1Index ] == s2[ s2Index ]:
				s1Matchings[ s1Index ] = True
				s2Matchings[ s2Index ] = True
				matchingsNum += 1.0
				break
	if matchingsNum == 0:
		return 0

	s2Index = 0
	for s1Index in range( s1Len ):
		if s1Matchings[ s1Index ]:
			while not s2Matchings[ s2Index ]:
				s2Index += 1
			if s1[ s1Index ] != s2[ s2Index ]:
				transpositionsNum += 1.0
			s2Index += 1

	return (1.0 / 3.0 ) * ( matchingsNum/s1Len + matchingsNum/s2Len + (matchingsNum - transpositionsNum/2.0) / matchingsNum )
# end of jaroDistance
 
main()


