import os
import streamlit as st

import requests
import joblib
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Getaround Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Force white text globally */
* {
    color: white !important;
}

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #4a5568 0%, #553c9a 100%) !important;
}

/* Force text color in all common elements */
p, span, div, label, li, td, th, h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Streamlit specific elements */
[data-testid="stMarkdownContainer"] p,
[data-testid="stText"],
.stMarkdown,
[data-testid="stExpander"] {
    color: white !important;
}

/* Main containers */
section.main > div.block-container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    padding: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.10);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Metric blocks */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

div[data-testid="metric-container"] * {
    color: white !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
}

[data-testid="stExpander"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.1));
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #10b981, #34d399);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4);
}

/* Headers */
h1, h2, h3 {
    background: linear-gradient(45deg, #ffffff, #e0e6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Input fields */
input, textarea {
    color: white !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Charts */
.js-plotly-plot {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# ************************************************************************************************************
# CACHE
# Load model
# @st.cache_resource
# def load_model():
#    return joblib.load("/app/models/model.pkl")
#
# model = load_model()"""

# ************************************************************************************************************
# ENV
# URL_API defined :
# in .env for deployment ready configuration
# or overriden in docker-compose for local dev
#
# api adressed locally through docker network @ http://api:8000/ 
# proxifyed with nginx (default.conf)
# apis adressed within frontend or backend containers
# by internal services defined in .env, set to http://127.0.0.1:8000 or in HF SECRETS: http://127.0.0.1:8000
url_api = os.getenv("URL_API")

# ************************************************************************************************************
if st.button("⬅️ Accueil", key="back_button"):
        st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)

st.title("🚗 Getaround Dashboard")


# ************************************************************************************************************
# Display rentals dataset structure
with st.expander("Rentals dataset structure"):
    
    # API call via entry point (ep)
    ep_rentals_stats = f'{url_api}/rentals_stats'
    resp_rentals_stats = requests.get(ep_rentals_stats)    # Waiting for json format
    js_rentals_stats = resp_rentals_stats.json()
    
    if st.button("Get structure", key="rentals_structure"):
        st.json(js_rentals_stats)
    
    
    
    rental_id = st.text_input('Get rental id:')
    if st.button("Get one rental"):
        try:
            rental_id = int(rental_id)
            ep_rental_by_id = f"{url_api}/rentals/{rental_id}"
            resp = requests.get(ep_rental_by_id)

            if resp.status_code == 200:
                st.write(resp.json())
            else:
                st.error(f"Rental ID {rental_id} not found (code {resp.status_code}).")

        except ValueError:
            st.warning("Enter valid rental_id.")

         

# ************************************************************************************************************
# Display rentals
with st.expander("Get all rentals"):
    
    ep_rentals = f'{url_api}/rentals'
    resp_rentals = requests.get(ep_rentals)
    js_rentals = resp_rentals.json()
    
    if st.button("Get all rentals"):
        st.write(js_rentals)


# ************************************************************************************************************
# Display cars dataset structure
with st.expander("Cars dataset structure"):
    
    # API call via entry point (ep)
    ep_cars_stats = f'{url_api}/cars_stats'
    resp_cars_stats = requests.get(ep_cars_stats)    # Waiting for json format
    js_cars_stats = resp_cars_stats.json()
    
    if st.button("Get structure", key="cars_structure"):
        st.json(js_cars_stats)


# ************************************************************************************************************
# Display cars
with st.expander("Get all cars"):
    
    ep_cars = f'{url_api}/cars'
    resp_cars = requests.get(ep_cars)
    js_cars = resp_cars.json()
    
    if st.button("Get all cars"):
        st.write(js_cars)


# ************************************************************************************************************
# Q1
with st.expander("🎚️ 1. Rentals affected by a threshold setup "):
    df_rentals = pd.DataFrame(js_rentals)
    
    # Select connect checkin
    mask = df_rentals["checkin_type"] == 'connect'
    df_rentals_connect = df_rentals[mask].copy()
    locations_connect_count = df_rentals_connect.shape[0]
    st.write(f"➡️ SCOPE: Locations of connect type: {locations_connect_count}")
    
    # Define threshold
    THRESHOLD = 60

    # Use of np.where
    condition = (df_rentals_connect['delta_with_previous'] <= THRESHOLD) & (df_rentals_connect['delta_with_previous'].notna())
    df_rentals_connect['threshold'] = np.where(condition, 'below', 'above')

    # Count values in threshold
    counts = df_rentals_connect['threshold'].value_counts().reset_index()
    counts.columns = ["threshold", "count"]
    count_below = counts.loc[counts['threshold'] == 'below', 'count'].values[0]

    fig = px.pie(
        counts,
        values='count',
        names='threshold', 
        color='threshold',
        title=f"Connect rentals by threshold = {THRESHOLD}: {count_below} set aside on {locations_connect_count} locations",
        width=600,
        height=250,
        color_discrete_sequence=px.colors.qualitative.Set3,
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10)  # left, right, top, bottom
        )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    
    ###############################################
    # Use of np.where - different condition
    condition = (df_rentals['delta_with_previous'] <= THRESHOLD) & (df_rentals['delta_with_previous'].notna())
    df_rentals['threshold'] = np.where(condition, 'below', 'above')
    locations_count = df_rentals.shape[0]
    st.write(f"➡️ SCOPE: All types of locations: {locations_count}")

    # Count values in threshold
    # Whole dataset vs. previous scope
    counts = df_rentals['threshold'].value_counts().reset_index()
    counts.columns = ["threshold", "count"]
    count_below = counts.loc[counts['threshold'] == 'below', 'count'].values[0]

    fig = px.pie(
        counts,
        values='count',
        names='threshold', 
        color='threshold',
        title=f"All rentals by threshold = {THRESHOLD}: {count_below} set aside on {locations_count} locations",
        width=600,
        height=250,
        color_discrete_sequence=px.colors.qualitative.Set3,
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10)  # left, right, top, bottom
        )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')

    df_rentals.drop("threshold", axis=1, inplace=True)


# ************************************************************************************************************
# Q2
with st.expander("🕒 2. Drivers being late for the next check in - Impact on the next driver"):
    st.write("Sur l'ensemble des locations avec une heure de retour renseignée (delay_at_checkout non nulle), on observe le ratio retard/avance.")
    # Get all the rentals, even the cars rented only once a day
    # Get the rentals for which we know the delay at checkout
    df_rentals_noNA = df_rentals.loc[df_rentals["delay_at_checkout"].notna()].copy()
    st.write(f"Rentals for which we know the delay at checkout: {df_rentals_noNA.shape[0]}")
    
    # Create column delay_label with value "advance/late"
    df_rentals_noNA["delay_label_with_next"] = df_rentals_noNA["delay_at_checkout"].apply(lambda x: "advance" if x<=0 else "late")

    # Display the ratio advance/late
    fig = px.pie(
        df_rentals_noNA,
        names='delay_label_with_next',
        color=df_rentals_noNA['delay_label_with_next'],
        title='Ratio advance/late among drivers for all rentals (including uniques)',
        width=600,
        height=250,
        color_discrete_map={"advance": "lightgreen", "late": "steelblue"},
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10)  # left, right, top, bottom
        )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    st.write("Pour étudier l'impact du retard sur la location suivante, il faut sélectionner les voitures qui sont utilisées plusieurs fois dans la même journée.")
    st.divider()
        
    #####################################
    # Get ONLY the rentals of cars rented several times a day
    df_multi_rentals_noNA = df_rentals_noNA.loc[df_rentals_noNA["previous_ended_rental_id"].notna()].copy()

    # Display the ratio advance/late
    fig = px.pie(
        df_multi_rentals_noNA['delay_label_with_next'].value_counts(),
        values='count',
        names=df_multi_rentals_noNA['delay_label_with_next'].value_counts().index, 
        color=df_multi_rentals_noNA['delay_label_with_next'].value_counts().index,
        title='Ratio advance/late among drivers for cars with several rentals per day',
        width=600,
        height=250,
        color_discrete_map={"advance": "lightgreen", "late": "steelblue"},
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10)  # left, right, top, bottom
        )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    
    st.write("Drivers are late more than half of the time")
    st.write("Pour étudier l'impact sur la location suivante d'un retour hors délai prévu, il faut référencer le delay_at_checkout de la précédente location dans une colonne pour la location courante.\
            Remarque: on prend toutes les locations, même celles qui sont uniques dans la journée ou celles pour lesquelles l'heure de retour n'est pas mentionnée (annulation), pour observer l'effet du retard (annulation) sur la location courante.")
    st.divider()
    
    
    #####################################
    # Merge current rental info and the previous rental of the same car if possible
    df_rentals_merged = pd.merge(
        df_rentals,
        df_rentals[["rental_id", "delay_at_checkout"]],
        how='left',
        left_on='previous_ended_rental_id',
        right_on='rental_id',
        suffixes=('_current', '_previous')
        )
    print(df_rentals_merged.columns)

    # Rename columns
    l_cols = ['rental_id', 'car_id', 'checkin_type', 'state',
        'delay_at_checkout', 'previous_ended_rental_id',
        'delta_with_previous', 'rental_id_previous',
        'previous_delay']
    df_rentals_merged.columns = l_cols
    # Drop redundant joint key column
    df_rentals_merged.drop("rental_id_previous", axis=1, inplace=True) 

    # Identify ovelaps conflicts case in a new column
    df_rentals_merged["checkin_conflict"] = (
        df_rentals_merged["previous_delay"].notna() &
        df_rentals_merged["delta_with_previous"].notna() &
        (df_rentals_merged["previous_delay"] > df_rentals_merged["delta_with_previous"])
        )
    st.write("On peut étudier les taux d'annulation de location en fonction des conflits de checkin")
    st.divider()
    

    #####################################
    # Create df of cancellations rates
    # Filter only rentals with a previous rental ie previous_delay notna
    df_conflict_cancel_rates = df_rentals_merged[df_rentals_merged["previous_delay"].notna()]\
        .groupby("checkin_conflict")["state"]\
        .value_counts(normalize=True)\
        .rename("ratio")\
        .reset_index()
    print(len(df_rentals_merged))

    # Visualize
    fig = px.bar(
        df_conflict_cancel_rates,
        x="checkin_conflict",
        y="ratio",
        color="state",
        barmode="stack",
        text_auto=".1%",
        title="Effect on cancellations rates of checkin conflicts ",
        width=600,
        height=300,
        color_discrete_map={"ended": "lightgreen", "canceled": "steelblue"},
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend_title_text="Rental state"
    )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    
    st.write("Il y a 6 points d'annulations supplémentaires en cas de dépassement du delta prévu pour le retour de location.\
            Est-ce que ce taux est différent selon le mode de location (checkin_type) ?")
    st.divider()
    
    
    #####################################
    # Get cancellation rates by checkin_conflict AND checkin_type
    df_conflict_cancel_rates_by_checkin_type = (
        df_rentals_merged[df_rentals_merged["previous_delay"].notna()]
        .groupby(["checkin_type", "checkin_conflict"])["state"]
        .value_counts(normalize=True)
        .rename("ratio")
        .reset_index()
    )
    df_conflict_cancel_rates_by_checkin_type

    fig = px.bar(
        df_conflict_cancel_rates_by_checkin_type,
        x="checkin_conflict",
        y="ratio",
        color="state",
        barmode="stack",
        facet_col="checkin_type",  # graph per checkin_type
        text_auto=".1%",
        title="Effect on cancellations rates of checkin conflicts depending on checkin_type",
        width=900,
        height=400,
        color_discrete_map={"ended": "lightgreen", "canceled": "steelblue"},
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend_title_text="Rental state"
    )
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    st.write("Les locations par connect débouchent sur des annulations plus nombreuses en cas de dépassement de délai que les locations par mobile.")


# ************************************************************************************************************
# Q3
with st.expander("🧩 3. Number of problematic cases solved depending on the threshold and scope"):
    st.write("Un checkout est problématique si la location suivante est impactée par le retard de checkout.")
    
    # Filter by threshold
    l_thresholds = [0, 60, 120, 180]
    l_results = []

    for th in l_thresholds:
        df_th = df_rentals_merged[df_rentals_merged["delta_with_previous"] >= th].copy()
        total_conflicts = df_th["checkin_conflict"].sum()
        l_results.append({
            "threshold": th,
            "conflicts": total_conflicts
        })

    df_results = pd.DataFrame(l_results)

    fig = px.bar(
        df_results,
        x="threshold",
        y="conflicts",
        text="conflicts",
        title="Problematic cases by threshold of delta_with_previous",
        labels={"threshold": "Threshold (min)", "conflicts": "problematic cases"},
        width=600,
        height=380
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    st.divider()
        
    ###############################################
    # Filter by threshold
    l_thresholds = [0, 60, 120, 180]
    l_results = []

    for th in l_thresholds:
        for checkin in ["connect", "mobile"]:
            df_th = df_rentals_merged[
                (df_rentals_merged["delta_with_previous"] >= th) &
                (df_rentals_merged["checkin_type"] == checkin)
            ].copy()
            total_conflicts = df_th["checkin_conflict"].sum()
            l_results.append({
                "threshold": th,
                "checkin_type": checkin,
                "conflicts": total_conflicts
            })

    df_results = pd.DataFrame(l_results)

    # Barplot côte à côte
    fig = px.bar(
        df_results,
        x="threshold",
        y="conflicts",
        color="checkin_type",
        barmode="group",  # side by side
        text="conflicts",
        title="Problematic cases by threshold of delta_with_previous and checkin_type",
        labels={"threshold": "Threshold (min)", "conflicts": "Problematic cases", "checkin_type": "Check-in type"},
        width=900,
        height=400
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    st.write("Le nombre de cas problématiques suit la même tendance entre connect et mobile.\
            Un seuil de 60min résoud les 2/3 de cas problématiques.")
 
 
# ************************************************************************************************************
# Q4
with st.expander("💸 4. Share of our owner’s revenue would potentially be affected by the feature"):
    st.write(
        "Il y a 260 locations de type connect qui ont un delta_with_previous < Seuil. "
        "Sur ces 260, il y a 69 cas problématiques (cf. ci-dessus)."
        "Si on applique ce seuil aux locations connect on perd donc 260 locations (cf. Q1.), "
        "soit 6% du nombre des <u>locations connect</u> (260/4307). "
        "Pour estimer la perte de revenu, il faut analyser le dataset cars : "
        "en filtrant les voitures qui ont getaround_connect, "
        "on peut visualiser et analyser les prix de location de ces voitures."
        )

    # Select in dataset cars, cars with the connect option
    df_cars = pd.DataFrame(js_cars)
    
    df_cars_connect = df_cars[df_cars["has_getaround_connect"] == True]
    total_connect_cars = len(df_cars_connect)
    st.write(f"Number of cars with connect option: {total_connect_cars}")

    # Display
    fig = px.histogram(
        df_cars_connect,
        'rental_price_per_day',
        color='has_getaround_connect',
        title="Price distribution of cars with connect option",
        width=600,
        height=300
        )

    # Compute business values
    # Get mean price
    mean_price = df_cars_connect['rental_price_per_day'].mean()
    st.write(f"mean_price: {mean_price}")

    fig.add_vline(
        x=mean_price,
        line_dash = 'dash',
        line_color = 'blue'
        )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    # Streamlit display style
    st.plotly_chart(fig, width='stretch')
    st.divider()
        
    ###############################################
    st.markdown("""
        ### Pour estimer l'impact de l'application du seuil

        On pose les hypothèses suivantes :

        - La moyenne des prix des voitures qui ont l'option connect est de **132 $** (Q3)  
        - Le CA est le produit du nombre de locations par la moyenne des prix  
        - Les locations effectuées et filtrées ont des durées équivalentes, donc le CA est amputé proportionnellement au nombre de locations filtrées  

        On peut donc calculer la perte de CA à cause du filtrage au-delà du seuil.  

        Un seuil de **60 min** minimum entre une location et la suivante concerne **260 locations sur 4307**, soit **6%** du volume des locations de type *connect*.  

        Or sur ces 260 locations, **69 auraient posé un problème d'overlap**.  

        D’après Q2, il y a **27.5 – 14.1 = 13.4 points** d’annulation en plus en cas de conflit, soit **15.6%** (13.4 / (100 - 14.1)).  

        Cela signifie que sur les 69 conflits en-dessous du seuil, **15.6% auraient été annulés**, soit **11 cas**.  

        👉 *Pour éviter 11 annulations pour conflits de retour, on a annulé 260 locations possibles.*  

        On a donc réellement perdu **249 locations** (260 - 11) en appliquant ce seuil, soit une perte de CA de **32 993 $**.  

        On sélectionne les locations filtrées (les 260).  
        Il faudrait écarter 11 locations du calcul parce qu'elles auraient été annulées pour conflit, mais on les conserve.  
        En revanche, on regroupe par `car_id` pour évaluer l’impact du seuil sur les multi-locations dans une même journée.
        """, unsafe_allow_html=True)
    
    st.divider()
        
    ###############################################
    # Percentage of filtered rentals (below threshold)
    # Select connect checkin
    df_rentals_connect = df_rentals[df_rentals["checkin_type"] == 'connect'].copy()
    locations_connect_count = len(df_rentals_connect)
    st.write(f"Locations of connect type: {locations_connect_count}")

    # Define threshold
    THRESHOLD = 60

    # Use of np.where
    condition = (df_rentals_connect['delta_with_previous'] <= THRESHOLD) & (df_rentals_connect['delta_with_previous'].notna())
    df_rentals_connect['threshold'] = np.where(condition, 'below', 'above')

    # Count values in threshold
    df_rentals_connect['threshold'].value_counts()
    count_below = df_rentals_connect[df_rentals_connect['threshold'] == 'below'].shape[0]
    st.write(f"Filtered values below threshold: {count_below}")

    # Get percentage of filtered rentals
    percentage_rentals_below_threshold = 100 * count_below / locations_connect_count
    st.write(f"Percentage of rentals below threshold: {percentage_rentals_below_threshold:.2f}%")

    # Get conflicts of connect rentals below threshold
    conflicts_rentals = l_results[0]["conflicts"]
    st.write(f"Conflicts of connect rentals below threshold: {conflicts_rentals}")

    # Get the difference between cancellations between conflict and no conflict for connect
    connect = df_conflict_cancel_rates_by_checkin_type["checkin_type"] == "connect"
    canceled = df_conflict_cancel_rates_by_checkin_type["state"] == "canceled"
    conflict = df_conflict_cancel_rates_by_checkin_type["checkin_conflict"] == True
    diff_canceled_rentals_conflict_below_thhreshold = (
            df_conflict_cancel_rates_by_checkin_type.loc[connect & canceled & conflict, "ratio"].values[0] 
            - df_conflict_cancel_rates_by_checkin_type.loc[connect & canceled & ~conflict, "ratio"].values[0]
            )*100
    st.write(f"Difference between canceled rentals with and without conflict below threshold: {diff_canceled_rentals_conflict_below_thhreshold:.2f} points")

    # Get the percentage of cancellations because of conflicts
    percentage_canceled_rentals_conflict_below_thhreshold = (
            diff_canceled_rentals_conflict_below_thhreshold 
            / (100 - 100 * df_conflict_cancel_rates_by_checkin_type.loc[connect & canceled & ~conflict, "ratio"].values[0])
            )*100
    st.write(f"Percentage of canceled rentals with conflict below threshold: {percentage_canceled_rentals_conflict_below_thhreshold:.2f}%")

    # Canceled conflicts among the conflicts below threshold
    canceled_conflicts_rentals = int(percentage_canceled_rentals_conflict_below_thhreshold / 100 * conflicts_rentals) + 1
    st.write(f"Canceled conflicts among the conflicts below threshold: {canceled_conflicts_rentals}")

    # Lost rentals apart from those which would have been canceled
    lost_rentals = count_below - canceled_conflicts_rentals
    st.write(f"Lost rentals apart from those which would have been canceled: {lost_rentals}")

    # Business loss
    business_loss = int(lost_rentals * mean_price)
    st.write(f"Total business loss: {business_loss}")

    # Group by car_id the filtered connect rentals below threshold
    df_filtered = df_rentals_connect[df_rentals_connect['threshold'] == 'below'].copy()

    df_rentals_lost =(df_filtered
            .groupby("car_id")
            .size()
            .reset_index(name="count")
            ).copy()
    df_rentals_lost["loss"] = np.round(df_rentals_lost["count"] * mean_price, 2)
    #df_rentals_lost

    fig = px.bar(
            df_rentals_lost,
            x="loss",
            y="count",
            title="Threshold impact on business loss for connect cars with and w/o conflicts",
            width=600,
            height=350
            )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, width='stretch')
    st.divider()
    
    st.markdown("""
    Ce résultat suggère que la mesure de sécurité est **efficace pour réduire les conflits**,  
    mais **trop coûteuse en termes de perte de volume**.  

    Des stratégies plus fines — *seuils variables, ciblage par véhicule ou par période* —  
    devraient être envisagées pour limiter cet impact.
    """)

    
    
# ************************************************************************************************************
# Predict
with st.expander("🔮 Predict"):
    st.write("🚗 Car Rental Price Prediction (Linear Regression)")
    
    # Get values from dataset cars
    # Get cars dataset from API call
    ep_cars = f"{url_api}/cars"
    resp_cars = requests.get(ep_cars)
    js_cars = resp_cars.json()
    df_cars = pd.DataFrame(js_cars)
    
    # Get unique values in categorical columns
    l_cat_cols = ["model_key", "fuel", "paint_color", "car_type"]
    unique_values = {col: sorted(df_cars[col].dropna().unique().tolist())
                    for col in l_cat_cols}
    # Get range values in numerical columns
    l_num_cols = ["mileage", "engine_power"]
    ranges = {
        col: {"min": int(df_cars[col].min()), "max": int(df_cars[col].max())}
        for col in l_num_cols
    }
    # Define bool columns
    l_bool_cols = [
        "private_parking_available",
        "has_gps",
        "has_air_conditioning",
        "automatic_car",
        "has_getaround_connect",
        "has_speed_regulator",
        "winter_tires"
    ]
    metadata = {
        "categorical_values": unique_values,
        "numeric_ranges": ranges,
        "boolean_fields": l_bool_cols
    }
        
    # Dynamically display the values in the streamlit selectors
    col1, col2 = st.columns(2)

    # Store user input data
    input_data = {}
    
    # Categorical
    with col1:
        for col in l_cat_cols:
            input_data[col] = st.selectbox(
                label=col.replace("_", " ").title(),
                options=metadata["categorical_values"][col]
            )

    # Numerical
    with col2:
        for col in l_num_cols:
            input_data[col] = st.slider(
                label=col.replace("_", " ").title(),
                min_value=metadata["numeric_ranges"][col]["min"],
                max_value=metadata["numeric_ranges"][col]["max"],
                value=(metadata["numeric_ranges"][col]["min"] + metadata["numeric_ranges"][col]["max"]) // 2
            )
    
    # Boolean
    st.subheader("Optional features")
    for col in l_bool_cols:
        input_data[col] = st.checkbox(label=col.replace("_", " ").title())
        
    
    # ---------------------------------------------------
    if st.button("Predict rental price 💰"):
        try:
            entry_point = f"{url_api}/predict_lr"
            response = requests.post(entry_point, json=input_data)
            response.raise_for_status()
            predicted_price = response.json()["predicted_price"]
            st.success(f"Predicted rental price: €{predicted_price:.2f} per day")
        except Exception as e:
            st.error(f"Prediction failed: {e}")