import base64
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import io
import json
import pandas as pd
import plotly.graph_objs as go
import re


# Modify the 'description' column in the .sc DataFrame
def modify_description(desc):
    desc = desc.replace('design_', '')
    desc = desc.replace('_dldesign_0_cycle1_af2pred', '')
    return re.search(r'\d+', desc).group()

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
        id='upload-sc',
        children=html.Div(['Drag and Drop or ', html.A('Select .sc File')]),
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
        accept='.sc'
    ),
    dcc.Upload(
        id='upload-json',
        children=html.Div(['Drag and Drop or ', html.A('Select .json File')]),
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
        accept='.json'
    ),

    # Scatter Plot and Radar Plot
    html.Div([
        html.Div([
            dcc.Graph(id='scatter-plot'),
            dcc.Dropdown(
                id='dropdown',
                style={'width': '60%'},
                options=[],  # Set initial options to empty
                value=None
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
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

    html.Div(id='intermediate-sc-data', style={'display': 'none'}),
    html.Div(id='intermediate-json-data', style={'display': 'none'}),
    html.Div(id='merged-data', style={'display': 'none'}),
    html.Div(id='filtered-data', style={'display': 'none'}),

])

@app.callback(
    Output('xaxis-column-1', 'options'),
    [Input('merged-data', 'children')]
)
def update_xaxis_column_options(merged_json):
    if merged_json:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        return [{'label': col, 'value': col} for col in merged_df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('yaxis-column-1', 'options'),
    [Input('merged-data', 'children')]
)
def update_yaxis_column_options(merged_json):
    if merged_json:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        return [{'label': col, 'value': col} for col in merged_df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('xaxis-column-2', 'options'),
    [Input('merged-data', 'children')]
)
def update_xaxis_column_2_options(merged_json):
    if merged_json:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        return [{'label': col, 'value': col} for col in merged_df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available

@app.callback(
    Output('yaxis-column-2', 'options'),
    [Input('merged-data', 'children')]
)
def update_yaxis_column_2_options(merged_json):
    if merged_json:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        return [{'label': col, 'value': col} for col in merged_df.columns if col != 'description']
    else:
        return []  # Return empty options if no data is available


# Callback function to process .sc file upload
@app.callback(
    Output('intermediate-sc-data', 'children'),
    [Input('upload-sc', 'contents')]
)
def handle_sc_upload(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\s+')

            # Modify the 'description' column in the .sc DataFrame
            df['description'] = df['description'].apply(modify_description)

            # Convert to JSON for intermediate storage
            return df.to_json(date_format='iso', orient='split')

        except Exception as e:
            return html.Div(['There was an error processing the .sc file.'])

# Callback function to process .json file upload
@app.callback(
    Output('intermediate-json-data', 'children'),
    [Input('upload-json', 'contents')]
)
def handle_json_upload(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        json_data = json.loads(decoded.decode('utf-8'))
        try:
            # Convert to DataFrame and process
            json_df = pd.DataFrame.from_dict(json_data, orient='index')
            json_df.reset_index(inplace=True)
            json_df.rename(columns={'index': 'description'}, inplace=True)

            # Convert 'description' in json_df to string
            json_df['description'] = json_df['description'].astype(str)

            # Convert to JSON for intermediate storage
            return json_df.to_json(date_format='iso', orient='split')

        except Exception as e:
            return html.Div(['There was an error processing the .json file.'])

# Callbacks to update scatter and correlation plots based on dropdown selection

@app.callback(
    Output('merged-data', 'children'),
    [Input('intermediate-sc-data', 'children'),
     Input('intermediate-json-data', 'children')]
)
def merge_data(sc_json, json_json):
    if sc_json is not None and json_json is not None:
        df = pd.read_json(io.StringIO(sc_json), orient='split')
        json_df = pd.read_json(io.StringIO(json_json), orient='split')

        # Merge the DataFrames
        merged_df = pd.merge(df, json_df, on='description', how='inner')

        # Convert all columns to numeric where possible
        for col in merged_df.columns:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

        # Remove unwanted columns
        merged_df.drop(['SCORE:', 'score', 'time', 'PDB_1', 'PDB_2', 'design_name'], axis=1, inplace=True)

        # Convert merged DataFrame to JSON for intermediate storage
        return merged_df.to_json(date_format='iso', orient='split')

# Update dropdown menu
@app.callback(
    Output('dropdown', 'options'),
    [Input('merged-data', 'children')]
)
def update_dropdown_options(merged_json):
    if merged_json is not None:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        return [{'label': col, 'value': col} for col in merged_df.columns if col != 'description']
    else:
        return []  # Return empty or default options if merged_json is None

# Callbacks for updating plots
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('merged-data', 'children'),  # Use merged data as input
     Input('dropdown', 'value')]
)
def update_scatter_plot(merged_json, selected_column):
    if merged_json is not None and selected_column is not None:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        fig = go.Figure(data=[
            go.Scatter(
                x=merged_df['description'],
                y=merged_df[selected_column],
                mode='markers',
                marker=dict(color=merged_df[selected_column], colorscale='Viridis'),
                text=merged_df.apply(lambda row: generate_hover_text(row, merged_df.columns), axis=1),
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
    [Input('merged-data', 'children'),
     Input('scatter-plot', 'hoverData')]
)
def update_radar_plot(merged_json, hoverData):
    if merged_json is not None and hoverData is not None:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        if hoverData and 'points' in hoverData and hoverData['points']:
            hover_index = hoverData['points'][0]['pointIndex']
            row = merged_df.iloc[hover_index]
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
    [Input('merged-data', 'children'),
     Input('xaxis-column-1', 'value'),
     Input('yaxis-column-1', 'value'),
     Input('x-min-input-1', 'value'),
     Input('x-max-input-1', 'value'),
     Input('y-min-input-1', 'value'),
     Input('y-max-input-1', 'value')]
)
def update_correlation_plot_1(merged_json, x_col, y_col, x_min, x_max, y_min, y_max):
    if merged_json is not None and x_col is not None and y_col is not None:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        filtered_df = filter_dataframe(merged_df, x_col, y_col, x_min, x_max, y_min, y_max)
        return create_correlation_plot(filtered_df, x_col, y_col)
    else:
        return go.Figure()  # Return an empty figure if any input is None


@app.callback(
    Output('correlation-plot-2', 'figure'),
    [Input('merged-data', 'children'),
     Input('xaxis-column-2', 'value'),
     Input('yaxis-column-2', 'value'),
     Input('x-min-input-2', 'value'),
     Input('x-max-input-2', 'value'),
     Input('y-min-input-2', 'value'),
     Input('y-max-input-2', 'value')]
)
def update_correlation_plot_2(merged_json, x_col, y_col, x_min, x_max, y_min, y_max):
    if merged_json is not None and x_col is not None and y_col is not None:
        merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
        filtered_df = filter_dataframe(merged_df, x_col, y_col, x_min, x_max, y_min, y_max)
        return create_correlation_plot(filtered_df, x_col, y_col)
    else:
        return go.Figure()  # Return an empty figure if any input is None


@app.callback(
    [Output('common-data-table', 'data'),
     Output('filtered-data', 'children')],
    [Input('merged-data', 'children'),
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
def update_common_data_table(merged_json, selected_correlation_1, selected_correlation_2,
                             x_min_1, x_max_1, y_min_1, y_max_1,
                             x_min_2, x_max_2, y_min_2, y_max_2,
                             x_col_1, y_col_1, x_col_2, y_col_2):
    try:
        if merged_json:
            merged_df = pd.read_json(io.StringIO(merged_json), orient='split')
            # Apply filters based on input box values and dropdown selections
            filtered_df_1 = filter_dataframe(merged_df, x_col_1, y_col_1, x_min_1, x_max_1, y_min_1, y_max_1)
            filtered_df_2 = filter_dataframe(merged_df, x_col_2, y_col_2, x_min_2, x_max_2, y_min_2, y_max_2)

            # Merging with suffixes
            common_data = pd.merge(filtered_df_1, filtered_df_2, on='description', how='inner', suffixes=('_df1', '_df2'))

            # Remove columns that end with '_df2'
            common_data = common_data[[col for col in common_data.columns if not col.endswith('_df2')]]

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
     Input('filtered-data', 'children')],  # Use filtered data
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
