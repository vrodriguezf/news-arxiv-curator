# Use the official Python image from the Docker Hub                                      
FROM python:3.10-slim                                                                    
                                                                                        
# Set environment variables                                                              
ENV PYTHONDONTWRITEBYTECODE=1                                                            
ENV PYTHONUNBUFFERED=1                                                                   
                                                                                        
# Set work directory                                                                     
WORKDIR /app                                                                             
                                                                                        
# Install system dependencies                                                            
RUN apt-get update && apt-get install -y \                                               
    build-essential \                                                                    
    && rm -rf /var/lib/apt/lists/*                                                       
                                                                                        
# Install Python dependencies                                                            
COPY requirements.txt .                                                                  
RUN pip install --upgrade pip                                                            
RUN pip install -r requirements.txt                                                      
                                                                                        
# Copy the rest of the application code                                                  
COPY . .                                                                                 
                                                                                        
# Expose the webhook port                                                                
EXPOSE 8443                                                                              
                                                                                        
# Define the default command to run the bot                                              
CMD ["python", "bot/main.py"]  