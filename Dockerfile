# Use the official Python image with the specified version
FROM python:3.11.9

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-pyaudio -y

# Set the working directory in the container

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

RUN mkdir -p /home/user/app && chmod 755 /home/user/app
WORKDIR /home/user/app

# Copy the requirements.txt file into the container
COPY --chown=user:user requirements.txt .

# Install Cython first
RUN pip install cython

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY --chown=user:user . .

# Expose the port FastAPI runs on
#EXPOSE 8000

# Define the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
