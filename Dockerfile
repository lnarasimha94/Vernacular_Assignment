FROM top20/python3.6:latest

LABEL Lakshmi Narasaiah Bodicherla < lakshminarasaiah.b@jotter.ai>

ADD ./* App/
ADD assignment App/assignment
ADD vernacular App/vernacular

RUN python -m pip install -r App/requirements.txt

WORKDIR App/

#initiates the scheduler
EXPOSE 8123
CMD ["python", "manage.py", "runserver", "0.0.0.0:8123"]