# Sidemen Tinder: Pickup Line Prediction Using K-Nearest Neighbors 

## Introduction/Overview. 

In this Machine Learning Project, I collected over 500 pickup lines from a Youtube dating show called “Sidemen Tinder”, 
and built a K-Nearest Neighbors classification model to predict whether a pickup line was a success or failure.

I achieved 70% accuracy on the test set, and deployed a web app which you can enter pickup lines by speech or text, 
and see if it was a success or failure.


### Model in Production: 
![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/77761564/147445221-d9976ea3-5871-43cb-b841-702d47d080a3.gif)




Link to web app: https://share.streamlit.io/fentresspaul61b/pickup_line_predictions/stream.py

Link to write up: https://www.notion.so/Sidemen-Tinder-Pickup-Line-Prediction-Using-K-Nearest-Neighbors-b9286425b5bc4f5796aae23dd00a2158

# Question.

Can I predict whether or not a pickup line is successful based on text alone? The answer is kind of. I was able to with 70% accuracy, however, this is on a small dataset, and pickup lines are much more complex than just the content of what is being said. However, this is a descent accuracy so now I will explain how I got there.

# **Data Collection/ Cleaning.**

## About the Data.

For data, I watched and collected pick up lines from 3 Youtube videos, including: 

- **SIDEMEN TINDER IN REAL LIFE (YOUTUBE EDITION):** 57,396,985 views, 1.7 Million Likes, 48:39 Runtime
    
    [https://www.youtube.com/watch?v=ex1iFyfLUTM](https://www.youtube.com/watch?v=ex1iFyfLUTM)
    
- **SIDEMEN TINDER IN REAL LIFE 2:** 59,159,475 views, 1.2 Million Likes, 51:46 Runtime
    
    [https://www.youtube.com/watch?v=aAOC71qqXxM](https://www.youtube.com/watch?v=aAOC71qqXxM)
    
- **SIDEMEN TINDER IN REAL LIFE:** 39,863,848 views, 835k Likes, 31:02 Runtime
    
    [https://www.youtube.com/watch?v=tDDEiUX38hc](https://www.youtube.com/watch?v=tDDEiUX38hc)
    
- **SIDEMEN TINDER IN LOCKDOWN:** 13,759,813 views, 668k Likes, Runtime 42:01
    
    [https://www.youtube.com/results?search_query=sidemen+tinder+covid](https://www.youtube.com/results?search_query=sidemen+tinder+covid)
    
- There are 9 Sidemen across all 4 videos, which I wall call “Players”.
    
    
    | Name | Age |
    | --- | --- |
    | JJ | 25 |
    | Ethan  | 23 |
    | Josh | 26 |
    | Simon | 26 |
    | Toby | 27 |
    | Callum  | 25 |
    | Callum 2 | 28 |
    | Vick | 24 |
    | Stephen  | 24 |
    | Harry | 23 |
- **I Collected 509 Samples which I collected by typing them into an Excel Spreadsheet.** I initially tried using the google transcription of the Youtube video; however, it seemed too cumbersome to go back and fix all the typos, and have to re-watch the videos where the pickup lines were miss translated.
- About the Columns:
    - **Name (str):** Name of Sidemen delivering the pickup line.
    - **Right (int):** 1 if the line worked, 0 if the line failed.
    - **Left (int):** 1 if the line failed, 0 if the line worked.
    - **Line_Type (str):** I created categories for the pickup lines which were nice, weird, random, flex, based on the previous, sexual, automatic, joke, looks/compliment, and taken. These categories were primarily used during EDA and not used during modeling or deployment because they were really acting as another label, and were too subjective to use, so I ended up dropping them later.
    - **Age (str):** Age of the Sidemen delivering the pickup line. This feature ended up being dropped as well. The initial idea behind using the age was that maybe certain dates swiped on older sidemen, while others were younger. This would be good to add for further data analysis; however, I decided not to add age into the final model, because the pickup line prediction algorithm is purely based on the text.
    - **Line (str):** The actual pickup line.
    
    
| Name | Right | Left | Line_Type | Age | Line |
| --- | --- | --- | --- | --- | --- |
| JJ | 0 | 1 | Flex | 25 | “Hi, I'm 25, JJ, and I'm rich” |

## Data Collection (Typing Samples Into Excel).

As mentioned before I had to choose whether to use the google Youtube translation of the video as data or collect the data myself by typing the lines into excel. I chose to type the lines into excel for these reasons: 

- I was only collecting the pickup lines as data, so if I used the youtube transcript I would have to parse out the pickup lines from all the speech which included the back and forth convos, the side jokes, the laughing, and the commentating.
- The Youtube transcript made errors, and although it performed very well, I could not simply just download the data and start working because I needed to know where the error had occurred, which meant I needed to watch the video in either scenario. Due to having to watch the video in both using the Youtube transcript, and when collecting the data by hand through excel, I went with excel because there was significantly less data cleaning that would have to be done.
- The sample size was small enough where typing in the samples was feasible.

## Draw Backs of Typing Samples Into Excel.

- This method does not scale. It is not feasible if this was scaled to 2000 or 1 million pickup lines.
- I made typos. Although I didn't mistake a phrase like “high five” for “five guys” as the Youtube translator would, I still made minor errors including spelling errors, capitalizing words, unneeded spaces, and punctuation errors.

## Data Improvements.

Now that I had around 500 samples, I went through and cleaned the data. Some of the issues I ran into were strings needed to be changed into integers and vise versa. Also, I made a helper function that I mapped over the pickup lines in order to remove unneeded spaces. I replaced Nan values with 0’s which only occurred in the age column but then ended up dropping the age column during modeling. There were no Nan rows that needed to be dropped or replaced because I collected all the data by hand, so every row in the table was there and was meant to be included. 

Now that data was cleaned, I began exploring the data.


# EDA.

## Looking into Player Performance.

The plot below shows the Success rate for each player, and then the total number of right and left swipes they received.  

<img width="1000" alt="plot_1" src="https://user-images.githubusercontent.com/77761564/147438420-b9e80d8c-e9f1-42f6-a2a8-964bd5e96885.png">


From the bar charts above, we can see that toby has the highest success rate of around 61%. Toby has the overall highest number of right swipes which is 40. Stephen has the lowest success rate of 16.7%; however, Ethan has the highest number of failures at 48. After seeing that Toby was the most successful, its time to look into why is this the case? Also, why were Stephen and Ethan so unsuccessful? Understanding these questions helped me during the feature engineering process.# EDA.

## Toby’s Stats (Most Successful Player)
<img width="314" alt="toby" src="https://user-images.githubusercontent.com/77761564/147438427-7ac9378c-b216-41db-bace-ace165bd0487.png">

Toby was the most successful player. Although I did not end up using the Line types for modeling, it was a useful feature during EDA to understand why certain players succeeded and others did not. Toby’s most popular line type was “nice”. An example of a “nice” line from toby is: “My name is Toby, I'm 26 and I would like to take you to see the Northern Lights ”. 

Breakdown: 

- Toby’s Nice Lines worked 86% of the time.
- Toby only tried 4 Sexual lines, which only of them was successful.
- Toby had a 60.6% success rate and was the only player who received more right swipes than lefts (40 right swipes, 26 left).
- Toby’s top 3 line types used were Nice, Joke, and Random

<img width="460" alt="plot_2" src="https://user-images.githubusercontent.com/77761564/147438447-1a987da4-f2af-4ad1-a1d5-77aa07c6b6e8.png">

## Ethan’s Stats (Least Successful Player).
<img width="171" alt="Ethan" src="https://user-images.githubusercontent.com/77761564/147438485-da142407-6548-4bf4-9eaf-4c4ea438f7be.png">

Ethan was the least successful player. Throughout all 4 videos, Ethan used jokes or sexual comments in the majority of his lines. 

Breakdown: 

- Ethans Sexual Lines were successful 8% of the time
- Ethan's most used Line Types were: Sexual, Jokes, or Flex
- Ethans Success ratio was 28%
- Ethan had 19 right swipes and 48 left swipes.
- Ethan used 4 nice lines, and 2 of them were successful

<img width="458" alt="plot_3" src="https://user-images.githubusercontent.com/77761564/147438515-aa29ac7e-173a-45e0-9576-c394628a518d.png">

## Take Away from Comparing Toby and Ethan’s Stats.

By comparing the most successful player Toby, and the least Ethan, I created a hypothesis that “nice” lines worked the best, and sexual lines worked the worst. Below is a chart that shows the effectiveness of each line type: 

We can see that the “Nice” and “Compliment” lines were the most successful. While “Weird”, “Automatic”, and “Sexual” were the least successful.

<img width="467" alt="plot_4" src="https://user-images.githubusercontent.com/77761564/147438539-f2f10423-3a63-4a9a-895b-a6db07c3107e.png">

# Feature Engineering

Now I had to ask what is it specifically about "Nice" lines that made them nice, or what makes a line not so nice going into the "Weird" or "Sexual" realm? What makes those lines weird or sexual, can be boiled down into the words being used, for example, if the player used highly sexual words, that line was considered sexual. Nice lines had a seem to have a positive sentiment while failing lines sometimes would seem to have a negative sentiment. So for feature engineering, I used TextBlob to extract sentiment and polarity from the pickup lines, and I drew upon an external data source from Kaggle called “Bad Words”, to assign a score to each line based on the number of bad words the line contained. 

## TextBlob Sentiment and Polarity

**Polarity:** Polarity is a score between -1 and 1 which is an indicator of how emotional a phrase is. 

**Subjectivity:** Subjectivity is a score between -1 and 1 which is to show how much a phrase expresses some personal feelings, views, or beliefs.

**Sentiment:** A score to a given pickup line which is based on the sentiment of the pickup line I created weights to tweak how important subjectivity is vs polarity. The output is the sum of the score + polarity * weight1 and Subjectivity * weight2. The score is the sum of each word's individual sentiment based on an external Data Set called “Affin” which was 2477 words with sentiment scores ranging from -5 to 5. 

## Kaggle “Bad Words” Dataset

bad words were only used in 62 out of the 509 pickup lines (12%).  Out of the 62 lines that contained bad words, only 26% of them were successful. This begs the question, do lines with bad words actually perform worse, or is this simply due to random chance? In order to verify this, I performed a hypothesis test. 

**Null:** Bad words have no effect on whether the date swiped right, and if bad words were used, and they did not swipe right, that is simply due to random chance.

**Alt:** Bad words do have an effect on whether the date swiped right, and this is not due to random chance

### **Test conclusion:**

In 1000 simulations, there was never a simulation where the pickup lines with bad words performed equally or better than those without bad words. Therefore we can say that there is an association between the use of bad words and the efficacy of lines and that the use of bad words is a good indicator of the efficacy of pick-up lines. 

## Final Set of Features Chosen.

I ended up settling on 6 features which were: 

- bad_words_score: A score that increases assigned to lines by the number number of bad words in the line. Pickup lines with more than one bad word are more than twice the score of a line with a single bad word, same for 3 bad words, etc..  Then weight is multiplied to the score at the end depending on how much I wanted to weigh the importance of bad words during modeling.
    
    ```python
    def bad_words_score(string,weight=100):
        score = 0
        multiple=False
        for word in string.split():
            if word in bad_words and multiple:
                score += 1 
                score = score * score
            elif word in bad_words and not multiple:
                score += 1 
                multiple=True
            
        return score * weight
    ```
    
- Lengths: (float)number of words in the pickup line
- Sentiment: Score described above (float) between -1,1
- score_array: (float) Sum of the sentiment and the bad_words_score (adds more numerical variation)
- Polarity (float) between -1,1
- Subjectivity (float) between -1,1

Below I used a heat map to evaluate the correlation between the features.
<img width="588" alt="plot_5" src="https://user-images.githubusercontent.com/77761564/147438572-a20e3caa-cebf-4903-9d00-9413e6cfd8fb.png">

# Model Building

I initially chose to use KNN because it was the first classification algorithm I learned; however, after learning more about more algorithms, I still believe that KNN is a good choice, and KNN still continues to perform the best after trying logistic regression and Random Forrest. The reason why I used KNN is that it performs well on small amounts of data. Also, the way I have designed the features, it makes sense to use a distance-based algorithm because of the “score” features I have engineered. 

I tried using other classification models including logistic and regression and Random Forrest because those are also known to work well with small amounts of data, but they did not perform as well in terms of accuracy as KNN so I stay with KNN. 

## Model Performance. 70% Accuracy Achieved

The final model performed with 70% accuracy average on the test set. I used Sci kit learn to perform KNN and Iterated through a number of neighbors and landed on 3 which was returning the highest accuracy. 

## Future Model Improvements.

- Adding more data would lead to a better performing more generalized model. There is a new episode of Sidemen Tinder which I have not added to the data set.
- Adding more ML Dimensions, for example, add Speech Emotion Recognition, or Facial Emotion Recognition to create a more intelligent model.
- Increasing the number of neighbors to avoid over fitting.
- Apply more advanced NLP techniques such as TfidfVectorizer with my current features to create a more generalized model.

# Deployment.

I used Streamlit to create a web app where you can test out pickup lines, by entering a pickup line in text, and using the predict button to see if would be a successful pickup line or a failure. 

Link to web app: https://share.streamlit.io/fentresspaul61b/pickup_line_predictions/stream.py


# Contact Info.

---


🤍 Email: fenresspaul@berkeley.edu

🤍 Linkedin: [https://www.linkedin.com/in/paul-fentress-985ab7112/](https://www.linkedin.com/in/paul-fentress-985ab7112/)

🤍 Github: [https://github.com/fentresspaul61B](https://github.com/fentresspaul61B)









