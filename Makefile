all:
	nosetests

clean:
	find whatthepatch tests -name '*.pyc' -exec rm {} \;

test:
	. env2/bin/activate && nosetests || true
	. env3/bin/activate && nosetests || true

init: init2 init3

init2:
	virtualenv --python=python2 env2
	. env2/bin/activate && pip install nose
	. env2/bin/activate && pip install --editable .

init3:
	virtualenv --python=python3 env3
	. env3/bin/activate && pip install nose
	. env3/bin/activate && pip install --editable .

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
