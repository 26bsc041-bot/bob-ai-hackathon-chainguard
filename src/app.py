import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="ChainGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ ChainGuard AI")
st.caption("Supply Chain Disruption Assistant & Fleet Utilisation Optimizer")

st.sidebar.title("CHAIN")
st.sidebar.title("GUARD AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Shipments",
        "Disruptions",
        "Fleet",
        "Cold Chain",
        "✦ AI Copilot"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Detect • Assess • Recommend • Act • Monitor")

# Demo data
shipments = pd.DataFrame([
    ["SHP001","Vadodara","Mumbai","Pharmaceuticals",850000,"High","2026-09-17","In Transit","Vadodara-Mumbai",True],
    ["SHP002","Ahmedabad","Pune","Electronics",420000,"Medium","2026-09-20","In Transit","Ahmedabad-Pune",False],
    ["SHP003","Surat","Delhi","Textiles",180000,"Low","2026-09-23","In Transit","Surat-Delhi",False],
    ["SHP004","Mumbai","Bengaluru","Pharmaceuticals",1200000,"High","2026-09-18","Delayed","Mumbai-Bengaluru",True],
    ["SHP005","Rajkot","Ahmedabad","Chemicals",650000,"High","2026-09-16","In Transit","Rajkot-Ahmedabad",False],
    ["SHP006","Vadodara","Jaipur","Food",275000,"Medium","2026-09-21","In Transit","Vadodara-Jaipur",False],
    ["SHP007","Pune","Hyderabad","Automotive Parts",310000,"Medium","2026-09-22","In Transit","Pune-Hyderabad",False],
    ["SHP008","Ahmedabad","Mumbai","Pharmaceuticals",950000,"High","2026-09-17","At Risk","Ahmedabad-Mumbai",True],
    ["SHP009","Delhi","Kolkata","Consumer Goods",390000,"Low","2026-09-25","In Transit","Delhi-Kolkata",False],
    ["SHP010","Mumbai","Chennai","Electronics",780000,"Medium","2026-09-24","In Transit","Mumbai-Chennai",False],
    ["SHP011","Bharuch","Vadodara","Chemicals",560000,"High","2026-09-16","At Risk","Bharuch-Vadodara",False],
    ["SHP012","Nashik","Pune","Food",220000,"Medium","2026-09-19","In Transit","Nashik-Pune",False],
], columns=[
    "shipment_id","origin","destination","cargo_type","cargo_value",
    "priority","expected_delivery","current_status","route","cold_chain"
])

disruptions = pd.DataFrame([
    ["D001","Road Closure","Mumbai","High",36,"Mumbai-Bengaluru"],
    ["D002","Heavy Rain","Ahmedabad","Medium",18,"Ahmedabad-Mumbai"],
    ["D003","Traffic Congestion","Pune","Medium",8,"Pune-Hyderabad"],
    ["D004","Flooding","Bharuch","High",30,"Bharuch-Vadodara"],
    ["D005","Border Check Delay","Delhi","Low",12,"Delhi-Kolkata"],
    ["D006","Accident","Vadodara","High",10,"Vadodara-Mumbai"],
], columns=[
    "disruption_id","disruption_type","location","severity",
    "estimated_duration_hours","affected_route"
])

fleet = pd.DataFrame([
    ["TRK001","Refrigerated Truck","Vadodara","Idle",12000],
    ["TRK002","Dry Van Truck","Ahmedabad","Available",18000],
    ["TRK003","Refrigerated Truck","Mumbai","Available",14000],
    ["TRK004","Container Truck","Pune","In Transit",22000],
    ["TRK005","Dry Van Truck","Rajkot","Idle",16000],
    ["TRK006","Refrigerated Truck","Bharuch","Idle",10000],
    ["TRK007","Container Truck","Delhi","Maintenance",24000],
    ["TRK008","Dry Van Truck","Nashik","Idle",15000],
], columns=[
    "vehicle_id","vehicle_type","current_location","status","capacity_kg"
])
# -----------------------------
# Risk calculation
# -----------------------------

severity_score = {
    "Low": 10,
    "Medium": 25,
    "High": 40,
    "Critical": 50
}

def calculate_risk(row):
    delivery_date = datetime.strptime(
        row["expected_delivery"], "%Y-%m-%d"
    ).date()

    days_left = (delivery_date - date(2026, 9, 15)).days

    if days_left <= 1:
        urgency = 20
    elif days_left <= 3:
        urgency = 15
    elif days_left <= 7:
        urgency = 10
    else:
        urgency = 5

    value = row["cargo_value"]

    if value >= 1000000:
        value_score = 20
    elif value >= 500000:
        value_score = 15
    elif value >= 250000:
        value_score = 10
    else:
        value_score = 5

    disruption = severity_score.get(
        row["disruption_severity"], 10
    )

    cold_chain = 10 if row["cold_chain"] else 0

    score = min(
        100,
        disruption + urgency + value_score + cold_chain
    )

    if score >= 70:
        level = "Critical"
    elif score >= 55:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return score, level


# Match each shipment with its route disruption
route_severity = {}

for _, disruption in disruptions.iterrows():
    route_severity[disruption["affected_route"]] = disruption["severity"]


shipments["disruption_severity"] = shipments["route"].map(
    route_severity
).fillna("Low")


results = shipments.apply(
    calculate_risk,
    axis=1,
    result_type="expand"
)

shipments["risk_score"] = results[0]
shipments["risk_level"] = results[1]

affected_routes = set(
    disruptions["affected_route"]
)

shipments["affected"] = shipments["route"].isin(
    affected_routes
)
# -----------------------------
# Overview Dashboard
# -----------------------------

if page == "Overview":

    st.header("Operations Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "ACTIVE DISRUPTIONS",
        len(disruptions)
    )

    col2.metric(
        "AFFECTED SHIPMENTS",
        int(shipments["affected"].sum())
    )

    col3.metric(
        "HIGH-RISK SHIPMENTS",
        int(
            shipments["risk_level"].isin(
                ["High", "Critical"]
            ).sum()
        )
    )

    idle_fleet = fleet[
        fleet["status"].str.lower().isin(
            ["idle", "available"]
        )
    ]

    col4.metric(
        "IDLE / AVAILABLE FLEET",
        len(idle_fleet)
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("⚠️ Active Disruptions")

        for _, d in disruptions.iterrows():

            affected = shipments[
                shipments["route"] ==
                d["affected_route"]
            ]

            st.warning(
                f"**{d['severity']} — "
                f"{d['disruption_type']}**\n\n"
                f"Location: {d['location']}  \n"
                f"Affected shipments: {len(affected)}  \n"
                f"Estimated duration: "
                f"{d['estimated_duration_hours']} hours"
            )

    with right:

        st.subheader("🚚 Fleet Status")

        fleet_counts = fleet["status"].value_counts()

        st.bar_chart(fleet_counts)

        st.metric(
            "Total Fleet",
            len(fleet)
        )

    st.divider()

    st.subheader("🔴 Highest-Risk Shipments")

    high_risk = shipments.sort_values(
        "risk_score",
        ascending=False
    ).head(6)

    st.dataframe(
        high_risk[
            [
                "shipment_id",
                "origin",
                "destination",
                "cargo_type",
                "risk_score",
                "risk_level",
                "current_status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
# -----------------------------
# Shipments
# -----------------------------

elif page == "Shipments":

    st.header("📦 Shipment Control Tower")

    search = st.text_input(
        "Search Shipment ID"
    )

    col1, col2, col3 = st.columns(3)

    risk_filter = col1.selectbox(
        "Risk",
        ["All", "Critical", "High", "Medium", "Low"]
    )

    status_filter = col2.selectbox(
        "Status",
        ["All"] +
        sorted(shipments["current_status"].unique())
    )

    cargo_filter = col3.selectbox(
        "Cargo Type",
        ["All"] +
        sorted(shipments["cargo_type"].unique())
    )

    filtered = shipments.copy()

    if search:
        filtered = filtered[
            filtered["shipment_id"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if risk_filter != "All":
        filtered = filtered[
            filtered["risk_level"] == risk_filter
        ]

    if status_filter != "All":
        filtered = filtered[
            filtered["current_status"] == status_filter
        ]

    if cargo_filter != "All":
        filtered = filtered[
            filtered["cargo_type"] == cargo_filter
        ]

    st.dataframe(
        filtered[
            [
                "shipment_id",
                "origin",
                "destination",
                "cargo_type",
                "current_status",
                "risk_score",
                "risk_level",
                "expected_delivery"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    if len(filtered) > 0:

        selected = st.selectbox(
            "Inspect Shipment",
            filtered["shipment_id"].tolist()
        )

        shipment = filtered[
            filtered["shipment_id"] == selected
        ].iloc[0]

        st.divider()

        st.subheader(
            f"Shipment {shipment['shipment_id']}"
        )

        a, b, c = st.columns(3)

        a.metric(
            "Risk Score",
            int(shipment["risk_score"])
        )

        b.metric(
            "Risk Level",
            shipment["risk_level"]
        )

        c.metric(
            "Cargo Value",
            f"₹{shipment['cargo_value']:,.0f}"
        )

        st.write(
            f"**Route:** "
            f"{shipment['origin']} → "
            f"{shipment['destination']}"
        )

        st.write(
            f"**Cargo:** {shipment['cargo_type']}"
        )

        st.write(
            f"**Status:** "
            f"{shipment['current_status']}"
        )

        if shipment["affected"]:

            disruption = disruptions[
                disruptions["affected_route"] ==
                shipment["route"]
            ].iloc[0]

            st.warning(
                f"Active disruption: "
                f"{disruption['disruption_type']} "
                f"({disruption['severity']})"
            )

            alternatives = {
                "Mumbai-Bengaluru":
                    "Mumbai → Pune → Bengaluru",

                "Ahmedabad-Mumbai":
                    "Ahmedabad → Vadodara → Surat → Mumbai",

                "Pune-Hyderabad":
                    "Pune → Solapur → Hyderabad",

                "Bharuch-Vadodara":
                    "Bharuch → Ankleshwar → Vadodara",

                "Delhi-Kolkata":
                    "Delhi → Lucknow → Varanasi → Kolkata",

                "Vadodara-Mumbai":
                    "Vadodara → Surat → Mumbai"
            }

            recommendation = alternatives.get(
                shipment["route"],
                "Manual route review required"
            )

            st.success(
                f"🤖 **AI Recommendation:** "
                f"Reroute through {recommendation}"
            )

        else:

            st.success(
                "No active disruption detected "
                "on this shipment's route."
            )
# -----------------------------
# Disruptions
# -----------------------------

elif page == "Disruptions":

    st.header("⚠️ Disruption Command Center")

    st.dataframe(
        disruptions,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Impact Analysis")

    for _, disruption in disruptions.iterrows():

        affected = shipments[
            shipments["route"] ==
            disruption["affected_route"]
        ]

        with st.expander(
            f"{disruption['severity']} — "
            f"{disruption['disruption_type']} — "
            f"{disruption['location']}"
        ):

            st.write(
                f"**Affected shipments:** "
                f"{len(affected)}"
            )

            st.write(
                f"**Estimated duration:** "
                f"{disruption['estimated_duration_hours']} hours"
            )

            if len(affected) > 0:

                st.write(
                    "**Affected shipment IDs:** "
                    + ", ".join(
                        affected["shipment_id"].tolist()
                    )
                )

                highest_risk = affected.sort_values(
                    "risk_score",
                    ascending=False
                ).iloc[0]

                st.info(
                    f"🤖 **AI Recommendation:** "
                    f"Prioritise {highest_risk['shipment_id']} "
                    f"for immediate review."
                )
# -----------------------------
# Fleet
# -----------------------------

elif page == "Fleet":

    st.header("🚚 Fleet Utilisation")

    active = len(
        fleet[fleet["status"] == "In Transit"]
    )

    idle = len(
        fleet[
            fleet["status"].str.lower().isin(
                ["idle", "available"]
            )
        ]
    )

    maintenance = len(
        fleet[fleet["status"] == "Maintenance"]
    )

    total = len(fleet)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("TOTAL FLEET", total)
    col2.metric("ACTIVE", active)
    col3.metric("IDLE / AVAILABLE", idle)
    col4.metric("MAINTENANCE", maintenance)

    st.divider()

    st.subheader("Fleet Assets")

    st.dataframe(
        fleet,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🤖 AI Redeployment Recommendations")

    available = fleet[
        fleet["status"].str.lower().isin(
            ["idle", "available"]
        )
    ].copy()

    affected_shipments = shipments[
        shipments["affected"]
    ].sort_values(
        "risk_score",
        ascending=False
    )

    if len(available) > 0 and len(affected_shipments) > 0:

        for _, shipment in affected_shipments.iterrows():

            suitable = available.copy()

            # Prefer refrigerated vehicles
            # for cold-chain shipments.
            if shipment["cold_chain"]:

                refrigerated = suitable[
                    suitable["vehicle_type"]
                    .str.contains(
                        "Refrigerated",
                        case=False,
                        na=False
                    )
                ]

                if len(refrigerated) > 0:
                    suitable = refrigerated

            if len(suitable) == 0:
                continue

            vehicle = suitable.iloc[0]

            st.info(
                f"""
                **{vehicle['vehicle_id']}**

                Current location: **{vehicle['current_location']}**

                Recommended support for:
                **{shipment['shipment_id']}**

                Route:
                **{shipment['origin']} → {shipment['destination']}**

                🤖 **Recommendation:**
                Redeploy this vehicle to support the
                affected shipment.
                """
            )

            available = available[
                available["vehicle_id"]
                != vehicle["vehicle_id"]
            ]

    else:

        st.success(
            "No immediate fleet redeployment "
            "is required."
        )
# -----------------------------
# Cold Chain
# -----------------------------

elif page == "Cold Chain":

    st.header("❄️ Cold-Chain Monitoring")

    cold_chain_shipments = shipments[
        shipments["cold_chain"] == True
    ].copy()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "COLD-CHAIN SHIPMENTS",
        len(cold_chain_shipments)
    )

    col2.metric(
        "TEMPERATURE MONITORED",
        len(cold_chain_shipments)
    )

    # Demo sensor analysis
    # Values are simulated for the MVP.
    temperature_data = {
        "SHP001": 5.2,
        "SHP004": 8.7,
        "SHP008": 4.1
    }

    excursions = 0

    for shipment_id, temperature in temperature_data.items():

        if temperature > 8:
            excursions += 1

    col3.metric(
        "TEMPERATURE EXCURSIONS",
        excursions
    )

    st.divider()

    st.subheader("🌡️ Temperature Status")

    for _, shipment in cold_chain_shipments.iterrows():

        temperature = temperature_data.get(
            shipment["shipment_id"],
            5.0
        )

        if temperature > 8:

            st.error(
                f"🚨 **{shipment['shipment_id']} — "
                f"Temperature Excursion**\n\n"
                f"Current temperature: "
                f"**{temperature}°C**\n\n"
                f"Recommended action: "
                f"Inspect refrigeration system immediately."
            )

        else:

            st.success(
                f"✅ **{shipment['shipment_id']} — "
                f"Temperature Normal**\n\n"
                f"Current temperature: "
                f"**{temperature}°C**"
            )

    st.divider()

    st.subheader("Cold-Chain Shipments")

    st.dataframe(
        cold_chain_shipments[
            [
                "shipment_id",
                "origin",
                "destination",
                "cargo_type",
                "current_status",
                "risk_score",
                "risk_level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Temperature readings shown in this MVP are simulated "
        "sensor data for demonstration purposes."
    )
# -----------------------------
# AI Copilot
# -----------------------------

elif page == "✦ AI Copilot":

    st.header("✦ ChainGuard AI Copilot")

    st.caption(
        "Ask questions about shipments, disruptions, "
        "risk and fleet operations."
    )

    st.subheader("Suggested Questions")

    suggestions = [
        "Which shipments are at highest risk?",
        "Which disruptions are affecting the most shipments?",
        "Which fleet vehicles can be redeployed?",
        "Which shipments require immediate attention?",
    ]

    for question in suggestions:

        if st.button(question, use_container_width=True):

            if "highest risk" in question.lower():

                top = shipments.sort_values(
                    "risk_score",
                    ascending=False
                ).head(3)

                st.success(
                    "### Highest-Risk Shipments"
                )

                for _, row in top.iterrows():

                    st.write(
                        f"**{row['shipment_id']}** — "
                        f"{row['origin']} → "
                        f"{row['destination']} | "
                        f"Risk: **{row['risk_score']} "
                        f"({row['risk_level']})**"
                    )

            elif "most shipments" in question.lower():

                disruption_impact = []

                for _, d in disruptions.iterrows():

                    count = len(
                        shipments[
                            shipments["route"]
                            == d["affected_route"]
                        ]
                    )

                    disruption_impact.append(
                        (
                            d["disruption_type"],
                            d["location"],
                            count
                        )
                    )

                disruption_impact.sort(
                    key=lambda x: x[2],
                    reverse=True
                )

                st.success(
                    "### Disruption Impact"
                )

                for name, location, count in disruption_impact:

                    st.write(
                        f"**{name}** in {location}: "
                        f"{count} affected shipment(s)"
                    )

            elif "fleet" in question.lower():
                available = fleet[
                    fleet["status"].str.lower().isin(
                        ["idle", "available"]
                    )
                ]

                st.success("### Fleet Vehicles Available for Redeployment")

                if len(available) > 0:
                    for _, vehicle in available.iterrows():
                        st.write(
                            f"**{vehicle['vehicle_id']}** — "
                            f"{vehicle['vehicle_type']} | "
                            f"Location: **{vehicle['current_location']}** | "
                            f"Status: **{vehicle['status']}** | "
                            f"Capacity: **{vehicle['capacity_kg']:,} kg**"
                        )
                else:
                    st.info("No idle or available fleet vehicles.")

            elif "immediate attention" in question.lower():
                urgent = shipments[
                    shipments["risk_level"].isin(
                        ["High", "Critical"]
                    )
                ].sort_values(
                    "risk_score",
                    ascending=False
                )

                st.success("### Shipments Requiring Immediate Attention")

                if len(urgent) > 0:
                    for _, row in urgent.iterrows():
                        st.write(
                            f"**{row['shipment_id']}** — "
                            f"{row['origin']} → {row['destination']} | "
                            f"Risk: **{row['risk_score']} "
                            f"({row['risk_level']})** | "
                            f"Status: **{row['current_status']}**"
                        )
                else:
                    st.info("No high-risk shipments require immediate attention.")

# ChainGuard AI MVP
