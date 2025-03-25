import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px




#set page title and layout
st.set_page_config(page_title="Movie Data Analysis", layout="wide")
st.title("Movie Data Analysis and visualization")

#Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("imdb_2024.csv")

df = load_data()

#sidebar for filters
st.sidebar.header("Filters")

#Genre filter
Genre_filter = st.sidebar.multiselect("Select Genres", df["Genre"].unique())

#Duration filter
st.sidebar.write("### Duration (Hours)")
Duration_options = ["<2 hrs", "2-3 hrs", ">3 hrs", "all"]
Duration_filter = st.sidebar.selectbox("Select Duration Range", Duration_options)

#Rating filter
st.sidebar.write("### Ratings")
Rating_filter = st.sidebar.slider("Select Minimum Rating, min_value = 0.0", max_value=10.0, value=8.0)

#Voting counts filter
st.sidebar.write("### Voting Counts")
Votes_filter = st.sidebar.number_input("Select Minimum Voting Counts", min_value = 0, value = 10000)

#Apply filters
Filtered_df = df.copy()

#Genre filter
if Genre_filter:
    Filtered_df = Filtered_df[Filtered_df["Genre"].isin(Genre_filter)]

#Duration filter
if Duration_filter == "< 2 hrs":
    Filtered_df = Filtered_df[Filtered_df["Duration"]< 120]
elif Duration_filter == "2-3 hrs":
    Filtered_df = Filtered_df[(Filtered_df["Duration"]>= 120) & (Filtered_df["Duration"]<=180)]
elif Duration_filter == "> 3 hrs":
    Filtered_df = Filtered_df[Filtered_df["Duration"] > 180]
elif Duration_filter == "all":
    Filtered_df = Filtered_df

# Rating filter
Filtered_df = Filtered_df[Filtered_df["Rating"] >= Rating_filter]

# Voting counts filter
Filtered_df = Filtered_df[Filtered_df["Votes"] >= Votes_filter]

# Display filtered data
st.write("### Filtered Results")
st.dataframe(Filtered_df)

# Download filtered data
st.sidebar.markdown("### Download Filtered Data")
st.sidebar.download_button(
    label="Download as CSV",
    data=Filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_movies.csv",
    mime="text/csv",
)

# Top 10 Movies by Rating and Voting Counts
st.write("### Top 10 Movies by Rating")
top_10_movies = Filtered_df.nlargest(10, ["Rating"])
st.dataframe(top_10_movies[["Title", "Genre", "Rating", "Votes", "Duration"]])

st.write("### Top 10 Movies by Voting Counts")
top_10_movies = Filtered_df.nlargest(10, ["Votes"])
st.dataframe(top_10_movies[["Title", "Genre", "Rating", "Votes", "Duration"]])

# Visualizations
st.write("## Visualizations")

# 1. Genre Distribution
st.write("### Genre Distribution")
genre_counts = Filtered_df["Genre"].value_counts()
fig1 = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={"x": "Genre", "y": "Count"})
st.plotly_chart(fig1)

# 2. Average Duration by Genre
st.write("### Average Duration by Genre")
avg_duration = Filtered_df.groupby("Genre")["Duration"].mean().reset_index()
fig2 = px.bar(avg_duration, x="Duration", y="Genre", orientation="h", labels={"Duration": "Average Duration", "Genre": "Genre"})
st.plotly_chart(fig2)

# 3. Voting Trends by Genre
st.write("### Voting Trends by Genre")
avg_votes = Filtered_df.groupby("Genre")["Votes"].mean().reset_index()
fig3 = px.bar(avg_votes, x="Genre", y="Votes", labels={"Genre": "Genre", "Votes": "Average Votes"})
st.plotly_chart(fig3)

# 4. Rating Distribution
st.write("### Rating Distribution")
fig4 = px.histogram(Filtered_df, x="Rating", nbins=20, labels={"Rating": "Rating"})
st.plotly_chart(fig4)

# 5. Genre-Based Rating Leaders
st.write("### Genre-Based Rating Leaders")
top_rated_movies = Filtered_df.loc[Filtered_df.groupby("Genre")["Rating"].idxmax()]
st.dataframe(top_rated_movies[["Title", "Genre", "Rating"]])

# 6. Most Popular Genres by Voting
st.write("### Most Popular Genres by Voting")
total_votes_by_genre = Filtered_df.groupby("Genre")["Votes"].sum().reset_index()
fig5 = px.pie(total_votes_by_genre, values="Votes", names="Genre", title="Most Popular Genres by Voting")
st.plotly_chart(fig5)

# 7. Duration Extremes
st.write("### Duration Extremes")
shortest_movie = Filtered_df.loc[Filtered_df["Duration"].idxmin()]
longest_movie = Filtered_df.loc[Filtered_df["Duration"].idxmax()]
st.write("**Shortest Movie:**", shortest_movie["Title"], "| Duration:", shortest_movie["Duration"])
st.write("**Longest Movie:**", longest_movie["Title"], "| Duration:", longest_movie["Duration"])

# 8. Ratings by Genre (Heatmap)
st.write("### Ratings by Genre (Heatmap)")
heatmap_data = Filtered_df.pivot_table(index="Genre", values="Rating", aggfunc="mean")
fig6 = px.imshow(heatmap_data, labels=dict(x="Genre", y="Rating", color="Average Rating"))
st.plotly_chart(fig6)

# # 9. Correlation Analysis: Ratings vs. Voting Counts
import pandas as pd

df = pd.DataFrame({
    'Rating': Filtered_df["Rating"],
    'Votes': Filtered_df["Votes"],
    'Duration': Filtered_df["Duration"]
})

# Visualize with a heatmap (requires matplotlib/seaborn)
df.corr().style.background_gradient(cmap='coolwarm')
# Streamlit visualization example
st.write("### Correlation Matrix")
st.dataframe(df.corr())

# Heatmap visualization
fig = px.imshow(df.corr(), text_auto=True, color_continuous_scale='RdBu')
st.plotly_chart(fig)