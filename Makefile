test:
	python -m unittest tests/*_test.py

# TODO: manually increment version in setup.py, run . bump.sh, then this
release: cleandist
	python setup.py sdist bdist_wheel
	twine upload dist/*

cleandist:
	rm dist/* || true
