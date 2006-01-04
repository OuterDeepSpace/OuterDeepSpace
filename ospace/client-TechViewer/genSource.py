import sys, os, os.path, shutil

targetDir = "src"

try:
	shutil.rmtree(os.path.join(targetDir), ignore_errors = 1)
except:
	pass

try:
	os.mkdir(targetDir)
except:
	pass


excluded = ["build", "dist", targetDir]

copyFiles = []
for filename in os.listdir(os.getcwd()):
	if filename == "genSource.py":
		continue
	if os.path.splitext(filename)[1] == ".py":
		copyFiles.append(filename)

for cpFile in copyFiles:
	shutil.copy2(cpFile, targetDir)
