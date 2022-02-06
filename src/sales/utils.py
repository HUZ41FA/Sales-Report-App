import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def get_code():
    code = str(uuid.uuid4()).replace('-','')[:12]
    return code


def get_salesman_from_id(uid):
    return Profile.objects.get(id=uid)

def get_customer_from_id(uid):
    return Customer.objects.get(id=uid)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_key(res_by):
    if res_by == '#1':
        key = 'transaction_id'
    elif res_by == '#2':
        key = 'created'
    return key

def get_chart(chart_type, data, result_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    key = get_key(result_by)
    d = data.groupby(key, as_index=False)["total_price"].agg('sum')
    if chart_type == '#1':
        #plt.bar(data['transaction_id'], data['price']) #We are doing this with seaborn
        sns.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data=d, x='total_price', labels=labels )
    elif chart_type == '#3':
        plt.plot(d[key], d['total_price'], color='red', marker="x")
    else: 
        print("unable to identify chart")
    plt.tight_layout()
    chart = get_graph
    return chart