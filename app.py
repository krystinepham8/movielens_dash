import streamlit as st
import pandas as pd
import plotly.express as px

st.title("MovieLens Movie Ratings Dashboard")
st.write("Welcome to my MovieLens Dashboard!")

df=pd.read_csv('movie_ratings.csv')

#Question 1
st.header("Genre Breakdown")

#Split movies with multiple genres
genre_data = df["genres"].str.split("|").explode()

#Count each genre
genre_counts = genre_data.value_counts().reset_index()

genre_counts.columns = ["Genre", "Count"]

# Create chart
fig=px.bar(
    genre_counts,
    x="Genre",
    y="Count",
    title="Distribution of Genres Among Rated Movies"
)
st.plotly_chart(fig)


#Question 2
st.header("Genre Satisfaction")

#Split movies with multiple genres
df_genres=df.copy()
df_genres["genres"]=df_genres["genres"].str.split("|")

#Create one row for each genre
df_genres=df_genres.explode("genres")

#Calculate average rating for each genre
genre_ratings=(
    df_genres
    .groupby("genres")["rating"]
    .mean()
    .reset_index()
)

genre_ratings.columns=["Genre", "Average Rating"]

#Sort from highest to lowest
genre_ratings=genre_ratings.sort_values(
    "Average Rating",
    ascending=False
)
fig2=px.bar(
    genre_ratings,
    x="Genre",
    y="Average Rating",
    title="Average Rating by Genre"
)
st.plotly_chart(fig2)

highest_genre = genre_ratings.iloc[0]
lowest_genre = genre_ratings.iloc[-1]

st.write(
    "Highest average rating:",
    highest_genre["Genre"],
    highest_genre["Average Rating"]
)

st.write(
    "Lowest average rating:",
    lowest_genre["Genre"],
    lowest_genre["Average Rating"]
)



#Question 3
st.header("Question 3: Ratings Over Time")

#Calculate the average rating for each movie release year
year_ratings=(
    df.groupby("year")["rating"]
    .mean()
    .reset_index()
)

year_ratings.columns=["Year", "Average Rating"]

#Sort by year
year_ratings=year_ratings.sort_values("Year")

fig3=px.line(
    year_ratings,
    x="Year",
    y="Average Rating",
    title="Average Movie Rating by Release Year",
    markers=True
)
st.plotly_chart(fig3)


#Question 4
st.header("Best Movies With a Rating Floor")
movie_stats = (
    df.groupby(["movie_id", "title"])["rating"]
    .agg(["mean", "count"])
    .reset_index()
)

movie_stats.columns=[
    "Movie ID",
    "Title",
    "Average Rating",
    "Number of Ratings"
]
movies_50=movie_stats[
    movie_stats["Number of Ratings"]>=50
]
top_5_50=movies_50.sort_values(
    "Average Rating",
    ascending=False
).head(5)
st.subheader("Top 5 Movies With at Least 50 Ratings")

st.dataframe(top_5_50)

#150
movies_150=movie_stats[
    movie_stats["Number of Ratings"] >= 150
]

top_5_150=movies_150.sort_values(
    "Average Rating",
    ascending=False
).head(5)

st.subheader("Top 5 Movies — At Least 150 Ratings")

st.dataframe(top_5_150)