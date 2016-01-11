from blog.forms import QueryForm

def run():
	qf = QueryForm()
	print(qf.__dict__)
	print(qf.measure)
	print("ok")