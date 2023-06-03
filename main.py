import sys
from template import TemplateModel

if (len(sys.argv) != 4):
    exit('Wrong number of arguments')

name = sys.argv[1]
action = sys.argv[2]
folder = sys.argv[3]

if name == 'template':
    model = TemplateModel()
elif name == 'hmm':
    exit('TODO')
else:
    exit('Model name should be template/hmm')

if action == 'test':
    model.test(folder)
elif action == 'predict':
    model.predict(folder)
else:
    exit('Action should be test/predict')