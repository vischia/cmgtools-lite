import os

lines = [line.rstrip('\n') for line in open('try.txt')]

for content in lines:
    os.system("cat adding_branch.py | sed 's?INPUT_FILE?"+str(content)+"?g' > adding_branch_mod.py")
    os.system("python adding_branch_mod.py")
    os.system("rm adding_branch_mod.py")
