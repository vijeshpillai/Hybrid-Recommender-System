# Project Overview: Spotify Hybrid Recommender System

## What are Recommender Systems?
Recommender systems are algorithms that suggest content to users based on their preferences and behavior. Think of them as a friend who knows your likes and dislikes and adapts to your current mood. For example, if you enjoy horror movies but just went through a breakup, the system might avoid romantic-horror films and recommend a pure horror movie like *Hannibal* instead. These systems adapt to dynamic user preferences, making recommendations more relevant over time.

### Where Are Recommender Systems Used?
Recommender systems are ubiquitous:
- **Media and Streaming Platforms**: Netflix, YouTube, and Spotify use them to suggest movies, videos, or songs.
- **E-commerce**: Amazon and Flipkart recommend products based on user behavior.
- **Social Media**: Instagram, TikTok, Facebook, and Twitter shape feeds with recommended posts, reels, and ads.

## Types of Recommender Systems

### 1. Popularity-Based Recommendation
This approach recommends the most popular or top-rated items overall, without requiring user data. For example, displaying the top 10 trending movies.

**Advantages**:
- Easy to implement.
- No need for user history.
- Works well for cold-start scenarios.
- Scales easily.

**Disadvantages**:
- Not personalized.
- Biased toward items favored by a small group of high raters.
- Lacks diversity (e.g., over-recommending Hindi movies if they dominate).

### 2. Content-Based Recommendation
This method uses content attributes (e.g., tags like genre or mood). If you watch a data science video, the system suggests similar content like machine learning videos.

**Advantages**:
- More personalized than popularity-based systems.
- Relies on content metadata.

**Disadvantages**:
- Overspecializes, limiting variety (e.g., only recommending study videos after watching one).
- Faces cold-start issues for new users with limited history.

### 3. Collaborative Filtering
This approach uses user-item interactions (e.g., ratings or likes) to identify patterns in user behavior. It has two subtypes:

#### User-Based Collaborative Filtering
Finds users similar to you and recommends items they liked. For example, if User A is similar to User B, movies watched by A but not B are recommended to B.

#### Item-Based Collaborative Filtering
Compares items based on user interactions. If many users who liked Movie A also liked Movie B, Movie B is recommended to others who liked Movie A.

**When to Use**:
- **Item-based**: Efficient when users greatly outnumber items (e.g., Netflix).
- **User-based**: Better when items outnumber users (e.g., Instagram reels).

**Advantages**:
- Provides diversity by recommending unexposed items.
- Scales well.
- Independent of content metadata.

**Disadvantages**:
- Cold-start problem for new users or items.
- Computationally expensive.
- Requires large datasets.

## Why Hybrid Systems Are Better
Most platforms (e.g., Netflix, Amazon, YouTube) use hybrid recommender systems to combine the strengths of content-based and collaborative filtering methods:
- **Popularity-based**: Lacks personalization.
- **Content-based**: Overspecializes, reducing variety.
- **Collaborative filtering**: Offers diversity but may not align with specific user preferences.

A hybrid system balances personalization (content-based) with variety (collaborative filtering), resulting in more accurate and dynamic recommendations.

### How It Works
A hybrid system uses a weighted approach:
- Weights: \( W_{cb} + W_{cf} = 1 \) (e.g., 60% content-based, 40% collaborative).
- Similarity is calculated using metrics like Euclidean distance, Manhattan distance, or cosine similarity.
- Cosine similarity was chosen for this project because:
  - It handles high-dimensional data better than Euclidean distance.
  - Outputs values between –1 (opposite) and 1 (perfectly similar).

## Spotify Recommender System
This project builds a hybrid recommender system for Spotify, a subscription-based music streaming platform, to enhance user engagement and retention.

### Datasets
1. **Songs Dataset**: Contains metadata (genre, mood, tempo, artist) for content-based recommendations.
2. **User-Item Interaction Dataset**: Tracks song play counts to enable collaborative filtering based on user behavior patterns.

By combining these datasets, the system ensures personalized recommendations (content-based) and introduces variety (collaborative filtering).

### Project Goal
The objective is to increase user engagement and retention by providing personalized and diverse song recommendations. The system was built using the [Million Song Dataset with Spotify and Last.fm metadata](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm/data) from Kaggle, which includes song attributes and user interaction data.

### Improving Business Metrics
The hybrid system supports Spotify’s revenue models (ads and subscriptions):
- **Increased Engagement**: More song plays lead to more ad impressions for free users and encourage upgrading to ad-free subscriptions.
- **Higher CTR**: Relevant recommendations increase click-through rates.
- **Conversion from Free to Paid**: Engaged users are more likely to subscribe.
- **Lower Churn Rate**: Personalized and varied recommendations improve user satisfaction, encouraging subscription renewals.

### Implementation
A Streamlit app was developed using a sample of 50,000 songs, offering three recommendation types:
1. **Content-Based Filtering**: Recommends 10 similar songs based on metadata.
2. **Collaborative Filtering**: Recommends 10 songs based on similar users’ listening patterns.
3. **Hybrid System**: Combines both methods using weighted similarity scores, with tested weighting strategies to balance personalization and diversity.

## Major Challenges and Solutions
### Dataset Size
- **Challenge**: The original dataset had 9.7 million entries, resulting in a 28GB user-item matrix (30,000 unique songs × 1 million unique users).
- **Solution**: Used the Dask library for chunking, processing data in smaller row-based chunks to avoid memory crashes.

### Weight Assignment in Hybrid System
- **Challenge**: Weights needed adjustment based on user type (new vs. long-term).
- **Solution**: Assigned higher weight to content-based filtering for new users (limited collaborative data) and collaborative filtering for long-term users (rich history).

## Evaluation Metrics
Since labeled ground-truth data was unavailable, standard metrics like **Precision@K** and **Recall@K** were considered:
- **Precision@K**: Measures the proportion of recommended items (top K) that are relevant.
- **Recall@K**: Measures the proportion of relevant items captured in the top K recommendations.

These metrics assess the quality and completeness of recommendations.

## Model-Based Recommender Systems
Collaborative filtering often uses model-based approaches like **Singular Value Decomposition (SVD)** to uncover latent patterns in user-item interactions.

### SVD Application
The dataset included user listening history (track_id, user_id, playcount). SVD factorizes the interaction matrix:
\[ A = U \Sigma V^T \]
- \( U \): Latent features of tracks.
- \( V^T \): Latent features of users.
- \( \Sigma \): Diagonal matrix prioritizing important latent features.

This creates a dense matrix to predict missing play counts, enabling song recommendations.

### Evaluation Metrics for SVD
Regression metrics were used to evaluate predicted play counts:
- **MAE (Mean Absolute Error)**.
- **MSE (Mean Squared Error)**.
- **RMSE (Root Mean Squared Error)**.

These metrics measure how closely predictions match actual user behavior.

Advanced models like boosting algorithms (e.g., XGBoost) could be explored but require well-labeled data.