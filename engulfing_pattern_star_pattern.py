import plotly.graph_objects as go
def detectCustomPatterns(financial_data, fig: go.Figure = None):

    length = len(financial_data)
    highs = list(financial_data['High'])
    lows = list(financial_data['Low'])
    closes = list(financial_data['Close'])
    opens = list(financial_data['Open'])
    bdiffs = [0] * length

    hdiffs = [0] * length
    ldiffs = [0] * length
    r1vals = [0] * length
    r2vals = [0] * length

    def analyzeEngulf(index):
        current = index
        bdiffs[current] = abs(opens[current] - closes[current])

        if bdiffs[current] < 0.000001:
            bdiffs[current] = 0.000001

        bdiff_min = 0.0020

        if (bdiffs[current] > bdiff_min and bdiffs[current - 1] > bdiff_min and
            opens[current - 1] < closes[current - 1] and
            opens[current] > closes[current] and
                (opens[current] - closes[current - 1]) >= -1e-6 and closes[current] < opens[current - 1]):
            return 1, opens[current], closes[current]

        elif (bdiffs[current] > bdiff_min and bdiffs[current - 1] > bdiff_min and
              opens[current - 1] > closes[current - 1] and
              opens[current] < closes[current] and
              (opens[current] - closes[current - 1]) <= 1e-6 and closes[current] > opens[current - 1]):
            return 2,  opens[current], closes[current]

        else:
            return 0, 0, 0

    def identifyStar(index):
        bdiff_min = 0.0020
        current = index

        hdiffs[current] = highs[current] - max(opens[current], closes[current])
        ldiffs[current] = min(opens[current], closes[current]) - lows[current]
        bdiffs[current] = abs(opens[current] - closes[current])

        if bdiffs[current] < 0.000001:
            bdiffs[current] = 0.000001

        r1vals[current] = hdiffs[current] / bdiffs[current]
        r2vals[current] = ldiffs[current] / bdiffs[current]

        if (r1vals[current] > 0.9 and ldiffs[current] < 0.25 * hdiffs[current] and bdiffs[current] > bdiff_min):
            return 1, opens[current], closes[current]

        elif (r2vals[current] > 1.0 and hdiffs[current] < 0.22 * ldiffs[current] and bdiffs[current] > bdiff_min):
            return 2, opens[current], closes[current]

        else:
            return 0, 0, 0

    # activate the functions above to detect engulfing and star patterns on the chart
    results = {"engulfing_1": 0, "engulfing_2": 0, "star_1": 0, "star_2": 0}
    
    # Engulfing Pattern 1: Bullish
    # Engulfing Pattern 2: Bearish
    # Star Pattern 1: Bullish
    # Star Pattern 2: Bearish
    

    for i in range(1, length):
        if (analyzeEngulf(i)[0] == 1):
            results["engulfing_1"] += 1
            fig.add_trace(go.Scatter(x=[i], y=[analyzeEngulf(i)[1]], name=f'Engulfing 1', marker=dict(size=12, color="turquoise"), mode="markers"))
            fig.add_trace(go.Scatter(x=[i], y=[analyzeEngulf(i)[2]], name=f'Engulfing 1', marker=dict(size=12, color="turquoise"), mode="markers"))
            financial_data["signal"] = 2
        elif (analyzeEngulf(i)[0] == 2):
            results["engulfing_2"] += 1
            fig.add_trace(go.Scatter(x=[i], y=[analyzeEngulf(i)[1]], name=f'Engulfing 2', marker=dict(size=12, color="orange"), mode="markers"))
            fig.add_trace(go.Scatter(x=[i], y=[analyzeEngulf(i)[2]], name=f'Engulfing 2', marker=dict(size=12, color="orange"), mode="markers"))
            financial_data["signal"] = 1
        if (identifyStar(i)[0] == 1):   
            results["star_1"] += 1
            fig.add_trace(go.Scatter(x=[i], y=[identifyStar(i)[1]], name=f'Star 1', marker=dict(size=12, color="pink"), mode="markers"))
            fig.add_trace(go.Scatter(x=[i], y=[identifyStar(i)[2]], name=f'Star 1', marker=dict(size=12, color="pink"), mode="markers"))
            financial_data["signal"] = 2
        elif (identifyStar(i)[0] == 2):
            results["star_2"] += 1
            fig.add_trace(go.Scatter(x=[i], y=[identifyStar(i)[1]], name=f'Star 2', marker=dict(size=12, color="brown"), mode="markers"))
            fig.add_trace(go.Scatter(x=[i], y=[identifyStar(i)[2]], name=f'Star 2', marker=dict(size=12, color="brown"), mode="markers"))
            financial_data["signal"] = 1
            
    print(results)
    return financial_data

