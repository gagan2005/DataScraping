# Football Player Data Scraper


## Description 

Fbref contains a lot of data points  about  soccer players which can be very useful in Data Analysis and Machine Learning Applications.This script scrapes various performance statistics (see features for a full list of features that are scraped)  about football players'  in a certain league. 

## Usage

Install the requirements using 

`pip3 install -r requirements.txt`

Run the scraper by

`scrapy runspider player_spider.py -o output/data.json` 

## Features Scraped

goals_per90,assists_per90,goals_assists_pens_per90, goals_pens_per90, goals_assists_pens_per90,goals,shots_total_per90, shots_on_target_per90, shots_free_kicks, pens_made,passes_completed,passes,passes_completed_short,passes_completed_medium,passes_completed_long ,sca,sca_per90,gca_per90, tackles, tackles_won, dribbles_vs, pressures, pressure_regains, blocks, blocked_shots, dribbles_completed, carry_distance, fouls,aerials_won, ball_recoveries


You can choose your selected features by editing the features variable
