from flask import Flask, render_template, request, redirect, session
from google.cloud import bigquery
import json
import pandas


app = Flask(__name__, template_folder='./templates')

credentials = "msds434-week-5-3146d415eae0.json"
client = bigquery.Client.from_service_account_json(credentials)

app.secret_key = "super_secret_key"
app.config['BIGQUERY_PROJECT'] = 'msds434-week-5'
app.config['BIGQUERY_DATASET'] = 'msds434'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def results():
    data = request.get_json()
    year = data.get('year')
    month = data.get('month')
    yyyymmdd = str(year) + str(month) + "01"

    query = f"""
            SELECT *
            FROM ML.PREDICT(MODEL `msds434.sample_model`,
            (
                SELECT
                    IFNULL(totals.pageviews, 0) AS pageviews,
                    IFNULL(totals.timeOnSite, 0) AS timeOnSite,
                    IFNULL(totals.newVisits, 0) AS isNewVisit,
                    IF(device.deviceCategory = 'mobile', 1, 0) AS isMobile,
                    IF(device.deviceCategory = 'desktop', 1, 0) AS isDesktop,
                    IF(trafficSource.medium in ('affiliate', 'cpc', 'cpm'), 1, 0) AS isPaidTraffic
                FROM
                    `bigquery-public-data.google_analytics_sample.ga_sessions_*`
                WHERE
                    _TABLE_SUFFIX BETWEEN '{yyyymmdd}' AND '{yyyymmdd}'
            )
            )
            LIMIT 50
            """
    
    df = client.query(query).to_dataframe()

    df.reset_index(drop=False, inplace=True)

    probs = []
    for i in df["predicted_isBuyer_probs"]:
        j = json.loads(json.dumps(i[0]))
        probs.append(j["prob"])

    df["probability"] = probs
    df = df.drop("predicted_isBuyer_probs", axis=1)    

    results = df.to_json(orient='records')
    session['results'] = results

    return redirect('/results')

@app.route('/results', methods=['GET'])
def test():
    results = json.loads(session.get('results'))
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)