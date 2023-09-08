FROM python:3.6.9

COPY requirements.txt fall_detection.py skeleton.png projectDescription.md /app/

RUN mkdir /app/data
COPY data /app/data/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN jupyter notebook --generate-config \
    && echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py

EXPOSE 8080 

CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8080", "--allow-root"]
