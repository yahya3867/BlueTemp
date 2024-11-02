# Use the official Python image
FROM continuumio/miniconda3:latest

# Labels
LABEL maintainer="Gian Sung <gian.sung.tech@gmail.com>"

# Set the working directory inside the container
WORKDIR /bluetemp

# Copy conda environment file
COPY ./environment/environment.yml /bluetemp/environment.yml

# Install conda environment
RUN conda env create -f environment.yml

# Copy rest of app code
COPY ./flaskr /bluetemp/flaskr
COPY ./templates /bluetemp/templates
COPY ./dist /bluetemp/dist
COPY ./lib /bluetemp/lib
COPY ./config.py /bluetemp/config.py
COPY ./app.py /bluetemp/app.py

# Expose the port Flask runs on
EXPOSE 5000

# Run app.py when the container launches
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "HorizonHacks2024"]
CMD ["python", "-u", "app.py"]
