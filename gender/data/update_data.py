import pandas as pd
import json
import sys

json.dump(pd.DataFrame().from_dict(json.load(open(sys.argv[1])), orient='index') \
	.reset_index().sort_values('index').set_index('index') \
	.to_dict(orient='dict')[0], \
	open(sys.argv[1].split('.')[0] + '__.json','w'))