states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
          'ALABAMA','ALASKA','ARIZONA','ARKANSAS','CALIFORNIA','COLORADO',
         'CONNECTICUT','DELAWARE','FLORIDA','GEORGIA','HAWAII','IDAHO', 
         'ILLINOIS','INDIANA','IOWA','KANSAS','KENTUCKY','LOUISIANA',
         'MAINE' 'MARYLAND','MASSACHUSETTS','MICHIGAN','MINNESOTA',
         'MISSISSIPPI', 'MISSOURI','MONTANA','NEBRASKA','NEVADA',
         'NEW HAMPSHIRE','NEW JERSEY','NEW MEXICO','NEW YORK',
         'NORTH CAROLINA','NORTH DAKOTA','OHIO',    
         'OKLAHOMA','OREGON','PENNSYLVANIA','RHODE ISLAND',
         'SOUTH CAROLINA','SOUTH DAKOTA','TENNESSEE','TEXAS','UTAH',
         'VERMONT','VIRGINIA','WASHINGTON','WEST VIRGINIA',
         'WISCONSIN','WYOMING']

def extractPrevNextWords(example, when, what):
	before_keyword, keyword, after_keyword = example[0].partition(what)
	if (when == 'after'):
		if after_keyword == '':
			return None	
		if after_keyword == '\n' or after_keyword == '\r' or after_keyword == '\r\n' or after_keyword == ' ':
			nextWord = None
		else:
			nextWord = after_keyword.split()[0]
		return nextWord
	if (when == 'before'):
		if before_keyword == '':
			return None
		return before_keyword

def applyRules(example, fvtype):
        ruleList = ['FirstLetterUppercase',  'stateAfter' ,'City:',
                    'CommaAfter', 'CommaBefore', 'AfterInkeyword',
                    'CitykeywordAfter', 'AllCapital', 'Class']
	instance = []
	if fvtype == True:
		searchString = '<city>'+example[1]+'</city>'
	else:
		searchString = example[1]
	for ruleName in ruleList:
		if ruleName == 'FirstLetterUppercase':
			if example[1][0].isupper():
				instance.append(1)
			else:
				instance.append(0)
		if ruleName == 'StateAfter': 
			nextWord = extractPrevNextWords(example, 'after',  searchString+',')
			if nextWord == None:
				nextWord = extractPrevNextWords(example, 'after',  searchString+' ')
				if nextWord != None:
					nextWord = nextWord.upper()
			if str(nextWord)[:-1] in states or nextWord in states:
				instance.append(1)
			else:
				instance.append(0)
		if ruleName == 'City:':
			nextWord = extractPrevNextWords(example, 'after', 'City:')
			if nextWord == None:
				instance.append(0)
			else:
				instance.append(1)
		if ruleName == 'CommaAfter':
			nextWord = extractPrevNextWords(example, 'after', searchString)
			if nextWord == ',':
				instance.append(1)
			else:
				instance.append(0)
		if ruleName == 'CommaBefore':
			prevWord = extractPrevNextWords(example, 'before', ' '+searchString)
			if prevWord == None:
				instance.append(0)
			else:
				if prevWord[-1] == ',':
					instance.append(1)
				else:
					instance.append(0)
		if ruleName ==	'AfterInkeyword':
			prevWord = extractPrevNextWords(example, 'before', ' '+searchString)
			if prevWord == None:
				instance.append(0)
			else:
				if prevWord[-2:] == 'in' or prevWord[-2:] == 'IN' or prevWord[-2:] == 'In':
					instance.append(1)
				else:
					instance.append(0)
		if ruleName == 'CitykeywordAfter':
			nextWord = extractPrevNextWords(example, 'after', searchString)
			if nextWord == 'city' or nextWord == 'City':
				instance.append(1)
			else:
				instance.append(0)
		if ruleName == 'AllCapital':
			isCap = True
			for i in range(0, len(example[1])):
				if not example[1][i].isupper():
					isCap = False
					break
			if isCap:
				instance.append(1)
			else:
				instance.append(0)
		if ruleName == 'Class':
			if fvtype == True:
					instance.append(1)
			else:
				instance.append(0)
			
	return instance


def generateFV(example, fvtype):
	return applyRules(example, fvtype)

if __name__ == '__main__':
	generateFV(param, fvtype)
