import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
import streamlit as st
st.title("Game Recommender System : ")
def user_input():
    story=st.slider("Enter value for STORY :",0,10)
    graphics=st.slider("Enter value for GRAPHICS :",0,10)
    combat=st.slider("Enter value for COMBAT :",0,10)
    exploration=st.slider("Enter value for EXPLORATION :",0,10)
    genre_shooter=st.slider("Enter 0/1 for SHOOTER type game or not : ",0,1)
    genre_action=st.slider("Enter 0/1 for ACTION type game or not : ",0,1)
    genre_stealth=st.slider("Enter 0/1 for STEALTH type game or not : ",0,1)
    genre_horror=st.slider("Enter 0/1 for HORROR type game or not : ",0,1)
    genre_racing=st.slider("Enter 0/1 for RACING type game or not : ",0,1)
    genre_openworld=st.slider("Enter 0/1 for OPEN-WORLD type game or not : ",0,1)
    genre_multiplayer=st.slider("Enter 0/1 for MULTIPLAYER type game or not : ",0,1)
    series = 0
    release_year = int(df['ReleaseYear'].mean())
    return[[story,graphics,combat,exploration,genre_shooter,genre_action,genre_stealth,genre_horror,genre_racing,genre_openworld,genre_multiplayer,release_year]]
df = pd.read_csv('GameRecommendation.csv')
user_features = user_input()

genre_values = user_features[0][4:11]
genre_columns = ['Genre_Shooter', 'Genre_Action', 'Genre_Stealth', 'Genre_Horror',
                 'Genre_Racing', 'Genre_OpenWorld', 'Genre_Multiplayer']
genre_mask = np.ones(len(df), dtype=bool)
for i, val in enumerate(genre_values):
    genre_mask &= df[genre_columns[i]] == val
if genre_mask.sum() > 0:
    filtered_df = df[genre_mask].copy()
    st.subheader(f":rainbow[{genre_mask.sum()} games matched exactly as per selected genres.]")
else:
    st.error("❌ No games matched the exact genre selection. Try adjusting genre filters.")
    st.stop()
X = filtered_df.drop(columns=['Game', 'Ratings','Series'])
y = filtered_df['Ratings']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
user_features_scaled = scaler.transform(user_features)   
poly=PolynomialFeatures(degree=2)
x_poly=poly.fit_transform(X_scaled)
model_two=Ridge(alpha=1.0).fit(x_poly,y)
user_features_poly = poly.transform(user_features_scaled) 
user_predicted_two=model_two.predict(user_features_poly)
user_predicted_two = np.clip(user_predicted_two, 0, 10)
predicted_value = float(user_predicted_two)
st.subheader(f":orange[The user's predicted rating for the game is: {predicted_value:.2f}]")
pca_components = min(4, len(filtered_df))
pca = PCA(n_components=pca_components)
X_pca = pca.fit_transform(X_scaled)
user_pca = pca.transform(user_features_scaled)
distances=euclidean_distances(X_pca,user_pca)
num_recommendations = min(4, len(filtered_df))
top_indices = distances.flatten().argsort()[:num_recommendations]
top_games = filtered_df.iloc[top_indices][['Game','Ratings','Series']]
plt.figure(figsize=(8, 5))
plt.plot(top_games['Game'],top_games['Ratings'], color='green')
plt.xlabel("Game")
plt.ylabel("Ratings")
plt.tight_layout()
plt.axhline(user_predicted_two[0], color='red', linestyle='--', label='Predicted Score')
plt.legend()
plt.title("Top Game Recommendations")
st.subheader(f":blue[The Top {num_recommendations} recommended games for you are :] \n")
for game in top_games['Game']:
    st.write(game)
st.subheader('Note :')
for _, row in top_games.iterrows(): 
    if row['Series'] == 1:
        st.write(f"\n- {row['Game']}: Prequel/sequel exists. Consider playing related parts first.")
    elif row['Series'] == 2:
        st.write(f"\n- {row['Game']}: Can be played standalone, but it's part of a series.")  
st.pyplot(plt.gcf())
