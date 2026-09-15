elif "fleet" in question.lower():

                available = fleet[
                    fleet["status"].str.lower().isin(
                        ["idle", "available"]
                    )
                ]

                st.success(
                    "### Fleet Vehicles Available for Redeployment"
                )

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

                    st.info(
                        "No idle or available fleet vehicles."
                    )

            elif "immediate attention" in question.lower():

                urgent = shipments[
                    shipments["risk_level"].isin(
                        ["High", "Critical"]
                    )
                ].sort_values(
                    "risk_score",
                    ascending=False
                )

                st.success(
                    "### Shipments Requiring Immediate Attention"
                )

                if len(urgent) > 0:

                    for _, row in urgent.iterrows():

                        st.write(
                            f"**{row['shipment_id']}** — "
                            f"{row['origin']} → "
                            f"{row['destination']} | "
                            f"Risk: **{row['risk_score']} "
                            f"({row['risk_level']})** | "
                            f"Status: **{row['current_status']}**"
                        )

                else:

                    st.info(
                        "No high-risk shipments require immediate attention."
                    )


# ChainGuard AI MVP
