# Sidemen Tinder: Pickup Line Prediction Using K-Nearest Neighbors 

## Introduction.

In this Machine Learning Project, I collected over 500 pickup lines from a youtube dating show called “Sidemen Tinder”, 
and built a K-Nearest Neighbors classification model to predict whether a pickup line was a success or failure.

Link to web app: https://share.streamlit.io/fentresspaul61b/pickup_line_predictions/stream.py

Link to write up: https://www.notion.so/Sidemen-Tinder-Pickup-Line-Prediction-Using-K-Nearest-Neighbors-b9286425b5bc4f5796aae23dd00a2158

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
<img src=“![https://www.notion.so/Sidemen-Tinder-Pickup-Line-Prediction-Using-K-Nearest-Neighbors-b9286425b5bc4f5796aae23dd00a2158#88a7047834984fc5a53e82d1f6e2f1f3]”>


From the bar charts above, we can see that toby has the highest success rate of around 61%. Toby has the overall highest number of right swipes which is 40. Stephen has the lowest success rate of 16.7%; however, Ethan has the highest number of failures at 48. After seeing that Toby was the most successful, its time to look into why is this the case? Also, why were Stephen and Ethan so unsuccessful? Understanding these questions helped me during the feature engineering process.# EDA.

## Looking into Player Performance.

The plot below shows the Success rate for each player, and then the total number of right and left swipes they received.  

![Screen Shot 2021-12-26 at 1.41.15 AM.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/21e34d20-86ec-428a-81c5-e7adaed38d4e/Screen_Shot_2021-12-26_at_1.41.15_AM.png)

From the bar charts above, we can see that toby has the highest success rate of around 61%. Toby has the overall highest number of right swipes which is 40. Stephen has the lowest success rate of 16.7%; however, Ethan has the highest number of failures at 48. After seeing that Toby was the most successful, its time to look into why is this the case? Also, why were Stephen and Ethan so unsuccessful? Understanding these questions helped me during the feature engineering process.


