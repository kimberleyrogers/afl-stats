from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return {"members": ["Member 1", "Member 2", "Member 3"]}

if __name__ == '__main__':
    app.run(debug=True)