class NumberFact():

    def _display(self):
    	return " ".join(["10","green bottles"])

    render = property(_display)


nf = NumberFact()
print(nf)
print(nf.render)