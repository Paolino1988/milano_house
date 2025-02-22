from dash import Dash, html

app = Dash(__name__)
server = app.server  # Render ha bisogno di questa variabile per Gunicorn

app.layout = html.Div("Hello, World!")

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5000)
