# Adsfluence
Our goal is to help advertisers to find influential users on tweeters that can help advertise their products.
For example, an influential tweeter about food might be a good partner for new local restaurants.
We can measure their influence by analyzing the cascade of their retweets.

(Based on previous research, high followers count doesn't imply influence, and as we focus on different topics, this is even less likely.)
Finally, we want to find tweeters that connect to different communities so the advertiser can cascade the information to a wide audience.

# TODO
Start streaming and generate User Graph.
Filter the stream by given list of keywords related to a topic.
Based on tweets and retweets, generate cascade.
Model the user's influence on that topic based on the cascade (even better, try to do it by considering time as well).
