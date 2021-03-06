# Ribitter-web

Live at http://18.133.188.73:5000/
  
## Snippets of UI:
  
  <h4>Authenticate using twitter</h4>
  <p>Authorize user using their twitter account so that the app can have access to their timeline and profile information</p>
  
  ![Screenshot from 2020-11-22 15-20-10](https://user-images.githubusercontent.com/37112252/99900648-f336a400-2cd6-11eb-949f-d6ae144c11fb.png)
  
  <h4>Checkout your feed</h4>
  <p>User can view their timeline on our app and go through the tweets of their followed accounts</p>
  
  ![Screenshot from 2020-11-22 17-18-54](https://user-images.githubusercontent.com/37112252/99902903-03ef1600-2ce7-11eb-878c-17df6ddfd4c9.png)
  
  <h4>Verify tweets for misinformation</h4>
  <p>User can check for misinformation in tweets by simply clicking the verify button available next to each post on their timeline on our app</p>
  
  ![Screenshot from 2020-11-22 17-21-35](https://user-images.githubusercontent.com/37112252/99902940-313bc400-2ce7-11eb-81cf-ab94a94b97fe.png)
  
  <h4>Filter data</h4>
  <p>Users can send customized labels to filter the data they see on their tweets and manage what content they consume from our app</p>
  
  ![1](https://user-images.githubusercontent.com/37112252/99903003-8972c600-2ce7-11eb-99a9-0f98a12c1e74.png)
  
  
## How to run the file on your system:

  1. Clone / Download the repository

  2. Navigate to Ribbter-web folder on your terminal
  
  3. Rename config.ini.example to config.ini
  
  4. Replace config.ini values with your keys from https://developer.twitter.com/en/apps and URL links to Elixr and MisMatch server
  
  5. Install requirements using `pip install -r requirements.txt`
  
  6. Execute command `python app.py` to start the server
 
  7. In your browser, open http://127.0.0.1:5000/ to view the website
