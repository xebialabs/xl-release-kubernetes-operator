package = repository.read("Applications/IssuesApp4/1.0")

readFile = repository.read(package.id + '/file')
readFolder = repository.read(package.id + '/folder')
readArchive = repository.read(package.id + '/archive')

deployit.print(readFile)
deployit.print(readFolder)
deployit.print(readArchive)
