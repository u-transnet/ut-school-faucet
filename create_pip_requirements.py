from setup import requirements

reqs_file = open('requirements.txt', 'w+')

for req in requirements:
    reqs_file.write(req + '\n')

reqs_file.close()