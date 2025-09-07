import streamlit as st
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd
from numpy import load
from hybrid_recommendations import HybridRecommenderSystem


# load the data
cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

# load the track ids
track_ids_path = "data/track_ids.npy"
track_ids = load(track_ids_path, allow_pickle=True)

# load the filtered songs data
filtered_data_path = "data/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

# load the interaction matrix
interaction_matrix_path = "data/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)

# load the transformed hybrid data
transformed_hybrid_data_path = "data/transformed_hybrid_data.npz"
transformed_hybrid_data = load_npz(transformed_hybrid_data_path)


# Title
st.title('🎶 Spotify Song Recommender!')

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs')
st.markdown("Music Test Data —  \nSong name: **Crawling**,  Artist name: **Linkin Park**" \
"  \nSong name: **no angel**,  Artist name: **beyoncé**" \
"  \nSong name: **no shame**,  Artist name: **5 seconds of summer**" \
"  \nSong name: **born to die**,  Artist name: **lana del rey**" \
)



# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)
artist_name = st.text_input('Enter the artist name:')
st.write('You entered:', artist_name)

# lowercase inputs
song_name = song_name.lower()
artist_name = artist_name.lower()

# user selects recommender type
filtering_type = st.radio(
    "Which recommender would you like to use?",
    ("Content-Based Filtering", "Hybrid Recommender System")
)

# number of recommendations
k = st.selectbox('How many recommendations do you want?', [5, 10, 15, 20], index=1)

# If hybrid, show slider + bar chart
if filtering_type == "Hybrid Recommender System":
    diversity = st.slider(
        label="Diversity in Recommendations",
        min_value=1,
        max_value=9,
        value=5,
        step=1
    )
    content_based_weight = 1 - (diversity / 10)

    chart_data = pd.DataFrame({
        "type": ["Personalized", "Diverse"],
        "ratio": [10 - diversity, diversity]
    })
    st.bar_chart(chart_data, x="type", y="ratio")


# Button + logic
if filtering_type == 'Content-Based Filtering':
    if st.button('Get Recommendations'):
        if ((songs_data["name"].str.lower() == song_name) &
            (songs_data['artist'].str.lower() == artist_name)).any():

            st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")

            recommendations = content_recommendation(
                song_name=song_name,
                artist_name=artist_name,
                songs_data=songs_data,
                transformed_data=transformed_data,
                k=k
            )

            # Display Recommendations
            for ind, recommendation in recommendations.iterrows():
                rec_song = recommendation['name'].title()
                rec_artist = recommendation['artist'].title()

                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{rec_song}** by **{rec_artist}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                elif ind == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
                else:
                    st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                    st.audio(recommendation['spotify_preview_url'])
                    st.write('---')
        else:
            st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")

elif filtering_type == "Hybrid Recommender System":
    if st.button('Get Recommendations'):
        st.write('Recommendations for', f"**{song_name}** by **{artist_name}**")
        recommender = HybridRecommenderSystem(
            number_of_recommendations=k,
            weight_content_based=content_based_weight
        )

        # get the recommendations
        recommendations = recommender.give_recommendations(
            song_name=song_name,
            artist_name=artist_name,
            songs_data=filtered_data,
            transformed_matrix=transformed_hybrid_data,
            track_ids=track_ids,
            interaction_matrix=interaction_matrix
        )

        # Display Recommendations
        for ind, recommendation in recommendations.iterrows():
            rec_song = recommendation['name'].title()
            rec_artist = recommendation['artist'].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{rec_song}** by **{rec_artist}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            elif ind == 1:
                st.markdown("### Next Up 🎵")
                st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            else:
                st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
