import base64
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import io
import json
import pandas as pd
import plotly.graph_objs as go
import re




# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Function to generate hover text
def generate_hover_text(row, columns):
    return '<br>'.join([f'{col}: {row[col]}' for col in columns])


# Define the layout of the app
app.layout = html.Div([
    html.H1("Data Visualization Dashboard"),

    html.H2("Upload Files"),
    dcc.Upload(
        id='upload-csv',
        children=html.Div(['Drag and Drop or ', html.A('Select csv File')]),
        style={
            'width': '25%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow only a single file to be uploaded
        multiple=False,
        accept='.csv'
    ),

    # Scatter Plot and Radar Plot
    html.Div([
        html.Div([
            html.H2('Scatter Plot'),
            dcc.Graph(id='scatter-plot'),
            dcc.Dropdown(
                id='dropdown',
                style={'width': '60%'},
                options=[],  # Set initial options to empty
                value=None
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H2('Radar Plot'),
            dcc.Graph(id='radar-plot')
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    # Correlation Plot 1
    html.Div([
        html.H2("Correlation Plot 1"),
        dcc.Dropdown(
            id='xaxis-column-1',
            options=[],  # Set initial options to empty
            value=None,
            style={'width': '35%'},
        ),
        dcc.Dropdown(
            id='yaxis-column-1',
            options=[],  # Set initial options to empty
            value=None,
            style={'width': '35%'},
        ),
        dcc.Graph(id='correlation-plot-1'),
        html.Div([
            html.Label("X-axis range for Correlation Plot 1:"),
            dcc.Input(id='x-min-input-1', type='number', placeholder='Min X'),
            dcc.Input(id='x-max-input-1', type='number', placeholder='Max X'),
            html.Label("Y-axis range for Correlation Plot 1:"),
            dcc.Input(id='y-min-input-1', type='number', placeholder='Min Y'),
            dcc.Input(id='y-max-input-1', type='number', placeholder='Max Y'),
        ]),
    ]),
    # Correlation Plot 2
    html.Div([
        html.H2("Correlation Plot 2"),
        dcc.Dropdown(
            id='xaxis-column-2',
            options=[],  # Set initial options to empty
            value=None,
            style={'width': '35%'},
        ),
        dcc.Dropdown(
            id='yaxis-column-2',
            options=[],  # Set initial options to empty
            value=None,
            style={'width': '35%'},
        ),
        dcc.Graph(id='correlation-plot-2'),
        html.Div([
            html.Label("X-axis range for Correlation Plot 2:"),
            dcc.Input(id='x-min-input-2', type='number', placeholder='Min X'),
            dcc.Input(id='x-max-input-2', type='number', placeholder='Max X'),
            html.Label("Y-axis range for Correlation Plot 2:"),
            dcc.Input(id='y-min-input-2', type='number', placeholder='Min Y'),
            dcc.Input(id='y-max-input-2', type='number', placeholder='Max Y'),
        ]),
    ]),

    # Common Data Points Table
    html.H2("Common Data Points"),
    dash_table.DataTable(id='common-data-table',
    style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }
    ),

    # Download Button
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv"),

    html.Div(id='dataframe-json', style={'display': 'none'}),
    html.Div(id='filtered-data', style={'display': 'none'}),

])


# Callback function to process CSV file upload
@app.callback(
    Output('dataframe-json', 'children'),
    [Input('upload-csv', 'contents')]
)
def handle_csv_upload(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Convert to JSON for intermediate storage
            return df.to_json(date_format='iso', orient='split')

        except Exception as e:
            return html.Div(['There was an error processing the CSV file.'])

@app.callback(
    Output('xaxis-column-1', 'options'),
    [Input('dataframe-json', 'children')]
)
def update_xaxis_column_options(csv_json):
    if csv_json:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        return [{'label': col, 'value': col} for col in df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('yaxis-column-1', 'options'),
    [Input('dataframe-json', 'children')]
)
def update_yaxis_column_options(csv_json):
    if csv_json:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        return [{'label': col, 'value': col} for col in df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('xaxis-column-2', 'options'),
    [Input('dataframe-json', 'children')]
)
def update_xaxis_column_2_options(csv_json):
    if csv_json:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        return [{'label': col, 'value': col} for col in df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('yaxis-column-2', 'options'),
    [Input('dataframe-json', 'children')]
)
def update_yaxis_column_2_options(csv_json):
    if csv_json:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        return [{'label': col, 'value': col} for col in df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available


# Callbacks to update scatter and correlation plots based on dropdown selection


# Update dropdown menu
@app.callback(
    Output('dropdown', 'options'),
    [Input('dataframe-json', 'children')]
)
def update_dropdown_options(csv_json):
    if csv_json is not None:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        return [{'label': col, 'value': col} for col in df.columns if col != 'description']
    else:
        return []  # Return empty or default options if merged_json is None

# Callbacks for updating plots
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('dataframe-json', 'children'),  # Use merged data as input
     Input('dropdown', 'value')]
)
def update_scatter_plot(csv_json, selected_column):
    if csv_json is not None and selected_column is not None:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        fig = go.Figure(data=[
            go.Scatter(
                x=df['description'],
                y=df[selected_column],
                mode='markers',
                marker=dict(color=df[selected_column], colorscale='Viridis'),
                text=df.apply(lambda row: generate_hover_text(row, df.columns), axis=1),
                hoverinfo='text'
            )
        ])
        fig.update_layout(
            title=f"Scatter Plot of {selected_column} vs Description",
            xaxis_title="Description",
            yaxis_title=selected_column
        )
        return fig
    else:
        return go.Figure()

@app.callback(
    Output('radar-plot', 'figure'),
    [Input('dataframe-json', 'children'),
     Input('scatter-plot', 'hoverData')]
)
def update_radar_plot(csv_json, hoverData):
    if csv_json is not None and hoverData is not None:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        if hoverData and 'points' in hoverData and hoverData['points']:
            hover_index = hoverData['points'][0]['pointIndex']
            row = df.iloc[hover_index]
            radar_attributes = [
                'RMSD', 'int_area_to_len_ratio', 'hydrogen_bonds',
                'salt_bridges'
            ]
            radar_data = [row[attr] for attr in radar_attributes if attr in row]
            fig = go.Figure(data=go.Scatterpolar(
                r=radar_data,
                theta=radar_attributes,
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True)
                ),
                showlegend=False
            )
            return fig
    return go.Figure()

def create_correlation_plot(df, x_column, y_column):
    sorted_df = df.sort_values(by=x_column)

    # Check if y_column is numeric and handle NaNs
    if sorted_df[y_column].dtype in ['float64', 'int64']:
        sorted_df = sorted_df.dropna(subset=[y_column])
        color = sorted_df[y_column]
    else:
        color = 'blue'  # Fallback to fixed color if non-numeric

    fig = go.Figure(data=[
        go.Scatter(
            x=sorted_df[x_column],
            y=sorted_df[y_column],
            mode='markers',
            marker=dict(color=color, colorscale='Viridis', showscale=True),
            text=sorted_df.apply(lambda row: generate_hover_text(row, df.columns), axis=1),
            hoverinfo='text'
        )
    ])
    fig.update_layout(
        title=f"Correlation between {x_column} and {y_column}",
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    return fig

def filter_dataframe(df, x_col, y_col, x_min, x_max, y_min, y_max):
    filtered_df = df.copy()
    if x_min is not None:
        filtered_df = filtered_df[filtered_df[x_col] >= x_min]
    if x_max is not None:
        filtered_df = filtered_df[filtered_df[x_col] <= x_max]
    if y_min is not None:
        filtered_df = filtered_df[filtered_df[y_col] >= y_min]
    if y_max is not None:
        filtered_df = filtered_df[filtered_df[y_col] <= y_max]
    return filtered_df

@app.callback(
    Output('correlation-plot-1', 'figure'),
    [Input('dataframe-json', 'children'),
     Input('xaxis-column-1', 'value'),
     Input('yaxis-column-1', 'value'),
     Input('x-min-input-1', 'value'),
     Input('x-max-input-1', 'value'),
     Input('y-min-input-1', 'value'),
     Input('y-max-input-1', 'value')]
)
def update_correlation_plot_1(csv_json, x_col, y_col, x_min, x_max, y_min, y_max):
    if csv_json is not None and x_col is not None and y_col is not None:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        filtered_df = filter_dataframe(df, x_col, y_col, x_min, x_max, y_min, y_max)
        return create_correlation_plot(filtered_df, x_col, y_col)
    else:
        return go.Figure()  # Return an empty figure if any input is None


@app.callback(
    Output('correlation-plot-2', 'figure'),
    [Input('dataframe-json', 'children'),
     Input('xaxis-column-2', 'value'),
     Input('yaxis-column-2', 'value'),
     Input('x-min-input-2', 'value'),
     Input('x-max-input-2', 'value'),
     Input('y-min-input-2', 'value'),
     Input('y-max-input-2', 'value')]
)
def update_correlation_plot_2(csv_json, x_col, y_col, x_min, x_max, y_min, y_max):
    if csv_json is not None and x_col is not None and y_col is not None:
        df = pd.read_json(io.StringIO(csv_json), orient='split')
        filtered_df = filter_dataframe(df, x_col, y_col, x_min, x_max, y_min, y_max)
        return create_correlation_plot(filtered_df, x_col, y_col)
    else:
        return go.Figure()  # Return an empty figure if any input is None


@app.callback(
    [Output('common-data-table', 'data'),
     Output('filtered-data', 'children')],
    [Input('dataframe-json', 'children'),
     Input('correlation-plot-1', 'selectedData'),
     Input('correlation-plot-2', 'selectedData'),
     Input('x-min-input-1', 'value'),
     Input('x-max-input-1', 'value'),
     Input('y-min-input-1', 'value'),
     Input('y-max-input-1', 'value'),
     Input('x-min-input-2', 'value'),
     Input('x-max-input-2', 'value'),
     Input('y-min-input-2', 'value'),
     Input('y-max-input-2', 'value'),
     Input('xaxis-column-1', 'value'),
     Input('yaxis-column-1', 'value'),
     Input('xaxis-column-2', 'value'),
     Input('yaxis-column-2', 'value')]
)
def update_common_data_table(csv_json, selected_correlation_1, selected_correlation_2,
                             x_min_1, x_max_1, y_min_1, y_max_1,
                             x_min_2, x_max_2, y_min_2, y_max_2,
                             x_col_1, y_col_1, x_col_2, y_col_2):
    try:
        if csv_json:
            df = pd.read_json(io.StringIO(csv_json), orient='split')
            # Apply filters based on input box values and dropdown selections
            filtered_df_1 = filter_dataframe(df, x_col_1, y_col_1, x_min_1, x_max_1, y_min_1, y_max_1)
            filtered_df_2 = filter_dataframe(df, x_col_2, y_col_2, x_min_2, x_max_2, y_min_2, y_max_2)

            # Merging with suffixes


            common_data = pd.merge(filtered_df_1, filtered_df_2, on='description', how='inner', suffixes=('', '_drop'))
            common_data = common_data.loc[:, ~common_data.columns.str.contains('_drop')]


            # Check if common_data is valid and not None
            if common_data is not None and not common_data.empty:
                data_for_table = common_data.to_dict('records')
                json_data = common_data.to_json(date_format='iso', orient='split')
                return data_for_table, json_data
            else:
                return [], None  # Return empty list and None for no data
        else:
            return [], None
    except Exception as e:
        # Handle any exceptions
        print(f"Error in update_common_data_table: {e}")
        return [], None  # Return empty list and None in case of an error


# Callback to download CSV
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"),
     Input('common-data-table', 'data')],  # Use filtered data
    prevent_initial_call=True
)
def download_csv(n_clicks, filtered_json):
    if n_clicks is not None and filtered_json is not None:
        filtered_df = pd.read_json(io.StringIO(filtered_json), orient='split')
        return dcc.send_data_frame(filtered_df.to_csv, filename="common_data_points.csv")
    else:
        raise dash.exceptions.PreventUpdate


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
