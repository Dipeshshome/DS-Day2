import pandas as pd

from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint for answering natural language questions
@app.route('/answer_question', methods=['POST'])
def answer_question():
    try:
        question = request.json['question']

        # Rule-based approach to answer questions
        if 'top earning sale item' in question:
            answer = df.groupby('PRODUCTLINE')['SALES'].sum().idxmax()

        elif 'best sales city' in question:
            answer = df.groupby('CITY')['SALES'].sum().idxmax()
        else:
            answer = "Sorry, I don't understand the question."

        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)})


#end point for purchased items baased on specific order id
@app.route('/order_items', methods=['POST'])
def get_order_items():
    try:
        order_id = request.json['order_id']
        #items = df[df['ORDERNUMBER'] == order_id]['PRODUCTLINE'].tolist()
        items = df[df['ORDERNUMBER'] == order_id]['PRODUCTLINE'].unique()
        return jsonify({'items': items.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})


#endpoint for simple recommendation engine
@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    try:
        month = request.json['month']
        # Filter data for the specified month
        monthly_data = df[df['MONTH_ID'] == month]

        # Calculate mean sales for the specified month
        mean_sales = monthly_data['SALES'].mean()

        # Simple recommendation logic
        if mean_sales > overall_mean_sales:
            recommendation = "Positive sales trend"
        else:
            recommendation = "Potential anomaly in sales"

        return jsonify({'recommendation': recommendation})
    except Exception as e:
        return jsonify({'error': str(e)})


# Run the Flask app
if __name__ == '__main__':
    # Load the sales data into a DataFrame
    df = pd.read_csv('sales_data_sample.csv', encoding='latin-1')

    # Display the first few rows of the DataFrame
    print(df.head())

    overall_mean_sales = df['SALES'].mean()
    app.run(debug=True)
