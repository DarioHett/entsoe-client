# Extract-Load data using ENTSO-E Client.
import entsoe_client as ec
from settings import api_key

client = ec.Client(api_key)
parser = ec.Parser()

gen_query = ec.Queries.Generation.AggregatedGenerationPerType(
    in_Domain=ec.ParameterTypes.Area("DE_LU"),
    periodStart=202109050200,
    periodEnd=202109070200,
)
px_query = ec.Queries.Transmission.DayAheadPrices(
    in_Domain=ec.ParameterTypes.Area("DE_LU"),
    periodStart=202109050200,
    periodEnd=202109070200,
)
response = client(gen_query)
df = parser(response)
px = parser(client(px_query))

# Transform data.
import pandas as pd
from entsoe_client import ParameterTypes

df["quantity"] = df["quantity"].astype(float)
px["price.amount"] = px["price.amount"].astype(float)

consumption_mask = df["TimeSeries.outBiddingZone_Domain.mRID"].notna()
production = df[~consumption_mask][["quantity", "TimeSeries.MktPSRType.psrType"]]
production["GenerationType"] = production["TimeSeries.MktPSRType.psrType"].apply(
    lambda x: ParameterTypes.PsrType[x].value
)  # Use ParameterTypes to transform ENTSO-E Code into readable string.
production_by_type = pd.pivot_table(
    production, index=production.index, columns="GenerationType", values="quantity"
)

ec.ParameterTypes.DocumentType.help()
ec.ParameterTypes.BusinessType.help()

# Plot data.
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use("seaborn-ticks")
plot_params = dict(
    stacked=True,
    grid=True,
    legend=True,
    cmap="tab20c",
    width=1.0,
    rot=15,
    ec="lightgrey",
)

## Primary plot - Generation by type.
fig, ax = plt.subplots(figsize=(12, 8))
production_by_type.plot.bar(
    title="Production by Generation Type in DE-LU",
    xlabel="UTC",
    ylabel="MWh",
    ax=ax,
    **plot_params
)

## Adjust x-axis ticks.
each_n_label = 12
ticks = ax.xaxis.get_ticklocs()
ticklabels = [label.get_text()[2:16] for label in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::each_n_label])
ax.xaxis.set_ticklabels(ticklabels[::each_n_label])

## Plot prices on top of primary plot.
_px = px.loc[production_by_type.index[production_by_type.index.isin(px.index)]]
ax2 = ax.twinx()
ax2.plot(ticks[::4], _px["price.amount"], color="blue", marker="o")
ax2.set_ylabel("EUR")

plt.savefig("sample_plot.png")
