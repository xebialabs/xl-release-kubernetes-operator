def checkNotApplicable(p, i):
	try:
		security.grant(p, 'security-model-user', [i])
	except:
		print('ok')
	else:
		raise Exception("Can not grant %s on %s" % (p, i))

checkNotApplicable('deploy#initial', 'Applications/security-model-dir')
checkNotApplicable('deploy#initial', 'Infrastructure/security-model-dir')
checkNotApplicable('deploy#upgrade', 'Applications/security-model-dir')
checkNotApplicable('deploy#upgrade', 'Infrastructure/security-model-dir')
checkNotApplicable('import#initial', 'Infrastructure/security-model-dir')
checkNotApplicable('import#initial', 'Environments/security-model-dir')
checkNotApplicable('import#upgrade', 'Infrastructure/security-model-dir')
checkNotApplicable('import#upgrade', 'Environments/security-model-dir')
checkNotApplicable('security#edit', 'Environments/security-model-dir')
checkNotApplicable('security#edit', 'Applications/security-model-dir')
checkNotApplicable('security#edit', 'Infrastructure/security-model-dir')
