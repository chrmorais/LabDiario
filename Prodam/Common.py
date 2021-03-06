#coding: utf-8
import re

class Tag(object):
    def __init__(self, startExpr, startReplace, endExpr, endReplace):
	self.se = "\(\(" + startExpr + "\)\)"
	self.sr = startReplace
	self.ee = "\(\(" + endExpr + "\)\)"
	self.er = endReplace
    
    def Apply(self, text):
	newText = text	
	expressions = re.findall(self.se + ".*?" + self.ee, newText, re.I| re.S)
	for expression in expressions:	    
	    newExpression = expression
	    newExpression = re.sub(self.se, self.sr, newExpression, 1, re.I|re.S)
	    newExpression = re.sub(self.ee, self.er, newExpression, 1, re.I|re.S)
	    newText = newText.replace(expression, newExpression)
	return newText

class DlTagsProcessor(object):
    def __init__(self, reOfInterest):
	bold = Tag("NG", "<b>", "CL", "</b>")
	self.reOfInterest = reOfInterest
	self.tags = [bold]

    def Process(self, text):
	parsedText = text
	for tag in self.tags:
	    parsedText = tag.Apply(parsedText)
	parsedText = re.sub("\(\(T.TULO\)\)","", parsedText)
	parsedText = re.sub("\(\(TÍTULO\)\)","", parsedText)
	parsedText = re.sub("\(\(TEXTO\)\)","", parsedText)
	parsedText = re.sub("\(\(NG\)\)","", parsedText)
	parsedText = re.sub("\(\(CL\)\)","", parsedText)
	parsedText = re.sub("^\s*","", parsedText)
	parsedText = re.sub("^(.*)","<h2>\\1</h2>", parsedText)

	
	for line in parsedText.splitlines():
	    for word in self.reOfInterest:		
		if re.search(word, line, re.I) is not None:		
		    expression = re.search("[^\>]*" + word + "[^\<]*", line, re.I).group(0)
		    parsedText = parsedText.replace(expression, "<span style='background-color: #ffff00'>" + expression + "</span>")
		    break
	return parsedText
