from itertools import permutations

context = [ "John Wayne", "Tom Hanks", "Tom Cruise", "Clint Eastwood", "Jon Hamm", "John Nolan", "William", "Fitcher" ]

def main():
	r = correctNames( "tomorrow I have a meeting with Tim Hanks Tom Crus and Eastwud", context )
	print "** TO REPLACE: %s" % ( str(r) )
	r = correctNames( "Michael likes movies with Jon Way and Client East", context )
	print "** TO REPLACE: %s" % ( str(r) )
	r = correctNames( "Jonn invited me Jon Ham and Jon Wane, over for a lunch", context )
	print "** TO REPLACE: %s" % ( str(r) )

def correctNames( sentence, nameContext ):

	print "\n***************************************\nDoing '%s':" % (sentence)

	namesInSentence, wordsInSentence = retrieveNamesFromSentence( sentence )
	print "Names in sentence: " + str(namesInSentence)

	doubleNamesInSentence = []
	n = 1
	while n < len(namesInSentence):
		if namesInSentence[n][1] - namesInSentence[n-1][1] == 1:
			doubleNamesInSentence.append( [ namesInSentence[n-1][0] + " " + namesInSentence[n][0], namesInSentence[n-1][1] ] )
			n += 1
		n += 1
	print "Double names in sentence: " + str(doubleNamesInSentence)

	score, doubleNamesRecognized, newNameContext = findBestPermutation( nameContext, doubleNamesInSentence, 0.4 )
	print "score=%f, names=%s" % (score, str(doubleNamesRecognized))

	singleNameContext = []
	for name in newNameContext:
		nameSplitted = str.split( name )
		for i in range( len(nameSplitted) ):
			singleNameContext.append( nameSplitted[i] )
	print "Singe name context: " + str(singleNameContext)

	singleNamesInSentence = []
	for n in range( len(namesInSentence) ):
		isContinue = False
		for r in range(len(doubleNamesRecognized)):
			if namesInSentence[n][1] == doubleNamesRecognized[r][1] or namesInSentence[n][1] == doubleNamesRecognized[r][1]+1:
				isContinue = True
				break
		if isContinue:
			continue
		singleNamesInSentence.append( [ namesInSentence[n][0], namesInSentence[n][1] ] )
	print "Singe names in sentence: " + str(singleNamesInSentence)

	score, singleNamesRecognized, _ = findBestPermutation( singleNameContext, singleNamesInSentence, 0.75 )
	print "score=%f, names=%s" % (score, str(singleNamesRecognized))

	toSubstitute = []
	newWordsInSentence = list(wordsInSentence)
	for n in range(len(doubleNamesRecognized)):
		wordNum = doubleNamesRecognized[n][1]
		toSubstitute.append( (wordsInSentence[wordNum] + " " + wordsInSentence[wordNum+1], doubleNamesRecognized[n][0] ) )
		newWordsInSentence[ wordNum ] = doubleNamesRecognized[n][0]
		newWordsInSentence[ wordNum+1 ] = ""
	for n in range(len(singleNamesRecognized)):
		wordNum = singleNamesRecognized[n][1]
		toSubstitute.append( (wordsInSentence[wordNum], singleNamesRecognized[n][0] ) )
		newWordsInSentence[ wordNum ] = singleNamesRecognized[n][0]

	newSentence = ""
	for w in newWordsInSentence:
		newSentence += " " + w
	print "NEW SENTENCE: %s" % (newSentence) 
	return toSubstitute;
#end of main


def findBestPermutation( namesInContext, namesInSentence, threshold ):

	maxSum = 0.0
	namesFound = []
	newNamesInContext = []
	namesPermutations = permutations( namesInContext, len(namesInSentence) ) 
	for namesPermutationToTry in list(namesPermutations):
		curSum = 0.0
		curNamesInContext = list( namesInContext )
		curNamesFound = []
		for n in range( len(namesInSentence) ):
			distance = jaroDistance( namesPermutationToTry[n], namesInSentence[n][0] )
			if distance < threshold:
				continue
			curSum += distance
			for i in range(len(newNamesInContext)):
				if curNamesInContext[i] == namesPermutationToTry[n]:
					del curNamesInContext[i]
					break
			curNamesFound.append( [ namesPermutationToTry[n], namesInSentence[n][1] ] )
					
		if curSum > maxSum:
			maxSum = curSum
			namesFound = curNamesFound
			newNamesInContext = curNamesInContext
	return maxSum, namesFound, newNamesInContext	
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


def jaroDistance( s1, s2 ):

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
	# end of for

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
		# end of if
	# end of for

	# print "jaro distance (%s-%s): m=%d, t=%d"%(s1,s2,matchingsNum,transpositionsNum)

	return (1.0 / 3.0 ) * ( matchingsNum/s1Len + matchingsNum/s2Len + (matchingsNum - transpositionsNum/2.0) / matchingsNum )
# end of jaroDistance
 
main()


