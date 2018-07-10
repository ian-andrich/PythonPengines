test:
	pytest tests/srctest_test.py

# TODO: manually increment version in setup.py, run . bump.sh, then this
release: cleandist
	python setup.py sdist bdist_wheel bdist_egg
	twine upload dist/*

cleandist:
	rm dist/* || true
