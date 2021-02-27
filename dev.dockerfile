FROM python:3.8-buster
COPY . .

EXPOSE 8000
RUN pip install wheel
RUN python setup.py sdist bdist_wheel
ENTRYPOINT ["run.sh"]
