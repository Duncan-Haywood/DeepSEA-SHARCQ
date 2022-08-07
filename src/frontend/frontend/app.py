from dash import Dash, dcc, html
from flask import Flask


def main():
    app = Dash(__name__)
    server = app.server
    app.layout = html.Div(
        [
            html.H1("DeepSea-Sharcq"),
            html.P("upload your zipped folders of files you want to process"),
            html.P(
                "please keep your folder (pre-zip) under 8 gb or the application will fail, and you won't get results. We set file limit at approximately 4 gb since zip should cut file size in half"
            ),
            html.P("it takes a few minutes for the ai to process all files"),
            dcc.Upload(
                html.Button("Upload zip folder"),
                max_size=4 * 10**9,
                filetypes=["zip"],
            ),
            html.Button("Download results", id="download_button"),
            dcc.Download(children="download_button"),
        ]
    )

    def upload_zip_folder(zip_folder):
        # url = requests.post(self.rest_api_url/upload_url, username, api_key, "POST")
        # response = request.post(url, zip_folder)
        pass

    def download_results():
        # url = requests.post(f'{self.rest_api_url}/download_url', username, api_key, "GET")
        # response = request.post(url, zip_folder)
        pass

    return app


if __name__ == "__main__":
    app = main()
    app.run_server(debug=True)
