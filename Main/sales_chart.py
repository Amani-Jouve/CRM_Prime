from .models import Order
import json
from datetime import datetime

def build_comparative_sales_chart():
    """ DocString for build_comparative_sales_chart """
    NUM_MONTHS=12
    months_tab = []

    for i in range(0,NUM_MONTHS):
        tmp_date = datetime.strptime(str(i+1), "%m")
        month_name = tmp_date.strftime("%B")
        months_tab.append(month_name)

    my_objects = Order.objects.all()

    today = datetime.now()

    previous_year = today.year-1
    current_year = today.year

    dataset_PY = {k:v for (k,v) in zip(months_tab, [0]*NUM_MONTHS)}
    dataset_CY = {k:v for (k,v) in zip(months_tab, [0]*NUM_MONTHS)}

    for obj in my_objects:
        ddate = obj.Delivery_date_expected
        if ddate.month <= NUM_MONTHS:
            if ddate.year == current_year:
                dataset_CY[months_tab[ddate.month-1]] += obj.get_total_order_price_TTC
            elif ddate.year == previous_year:
                dataset_PY[months_tab[ddate.month-1]] += obj.get_total_order_price_TTC

    PY_sales = list()
    CY_sales = list()

    for i in range(0,NUM_MONTHS):
        PY_sales.append(dataset_PY[months_tab[i]])
        CY_sales.append(dataset_CY[months_tab[i]])

    PY_series = {
        'name': previous_year,
        'data': PY_sales
    }

    CY_series  = {
        'name': current_year,
        'data': CY_sales
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Comparative monthly sales'},
        'xAxis': {'categories': months_tab},
        'yAxis': {'title':{'enabled':'true', 'text':'Sales (€)'}},
        'series': [PY_series, CY_series]
    }

    chart_dump = json.dumps(chart)

    return chart_dump
