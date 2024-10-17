# arXiv Newsletter Filter Bot

This bot helps you filter arXiv newsletters based on your specified keywords. It is built using Python and the Telegram Bot API. To make it work ensure your server is accesible
through HTTPS

## Setup with Docker                                                                     
                                                                                        
### Prerequisites                                                                        
                                                                                        
- [Docker](https://www.docker.com/get-started) installed on your machine.                
- [Docker Compose](https://docs.docker.com/compose/install/) installed.                  
                                                                                        
### Environment Variables                                                                
                                                                                        
Create a `.env` file in the project root by copying the example:                         
                                                                                        
```sh                                                                                    
cp .env.example .env                                                                     
```                                                                                      
                                                                                        
Then, update the `.env` file with your configurations:                                   
                                                                                        
- `TELEGRAM_TOKEN`: Your Telegram bot token.                                             
- `DATABASE_URL`: PostgreSQL connection string (already set for Docker Compose).         
- `WEBHOOK_URL`: URL where Telegram will send updates.                                   
- `WEBHOOK_PORT`: Port for the webhook (default is `8443`).                              
                                                                                        
### Building and Running the Services                                                    
                                                                                        
1. **Build and start the services using Docker Compose:**                                
                                                                                        
    ```sh                                                                                
    docker-compose up --build -d                                                         
    ```                                                                                  
                                                                                        
2. **Initialize the database:**                                                          
                                                                                        
    ```sh                                                                                
    docker-compose exec bot python -c "from database.db import init_db; init_db()"       
    ```                                                                                  
                                                                                        
3. **Verify that the bot is running:**                                                   
                                                                                        
    ```sh                                                                                
    docker-compose logs -f bot                                                           
    ```                                                                                  
                                                                                        
### Stopping the Services                                                                
                                                                                        
To stop the services, run:                                                               
                                                                                        
```sh                                                                                    
docker-compose down                                                                      
```                   

## Usage

### Commands

- `/start` - Start the bot and get a welcome message.
- `/add_keyword [keyword]` - Add a keyword to filter newsletters.
- `/remove_keyword [keyword]` - Remove a keyword from your list.
- `/list_keywords` - List all your keywords.
- `/filter_newsletter` - Filter a newsletter text based on your keywords.

### Example

1. **Start the bot:**
    ```
    /start
    ```

2. **Add a keyword:**
    ```
    /add_keyword machine learning
    ```

3. **List your keywords:**
    ```
    /list_keywords
    ```

4. **Filter a newsletter:**
    ```
    /filter_newsletter [paste newsletter text here]
    ```

## License

This project is licensed under the MIT License.