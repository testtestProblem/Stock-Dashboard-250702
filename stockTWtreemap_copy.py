#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
# 找出所有符合檔名格式的 JSON 檔案
files = glob.glob("twse_data_*.json")

# 如果有符合的檔案
if files:
    # 按照修改時間排序，依照作業系統時間戳記取出最新的
    latest_file = max(files, key=os.path.getmtime)
    
    # 讀取最新檔案
    df = pd.read_json(latest_file)
    
    print(f"✅ 已讀取最新檔案：{latest_file}")
else:
    print("❌ 找不到符合的 twse_data_*.json 檔案")


# In[ ]:





# In[ ]:





# In[2]:


print(df.columns)


# In[3]:


import numpy as np

#name   code   昨日收盤價   開盤價   最低價   最高價   成交量   參考價   ask(highset buy)  bid(lowest sell)
stockData=df[["n","c","y","o","l","h","v","z","a","b"]].copy()
stockData.columns = ["Name", "Code", "PrevClose", "Open", "Low", "High", "Volume", "ReferencePrice", "Ask", "Bid"]
#stockData['bestBuyer'] = stockData["Bid"].apply(lambda x: float(x.strip("_").split("_")[0])if x and x != "-" else None)
stockData['bestBuyer']=stockData["Bid"].apply(
    lambda x: next((float(v) for v in x.strip("_").split("_") if float(v) != 0), None)
    if isinstance(x, str) and x != "-" else None
)
stockData['ReferencePrice']=np.where(
    stockData['ReferencePrice'] == "-",
    stockData['bestBuyer'],
    stockData['ReferencePrice']
    )
# 再將 ReferencePrice 轉成 float（字串變數數值）
stockData["ReferencePrice"] = pd.to_numeric(stockData["ReferencePrice"], errors="coerce")

stockData.head(3)


# In[4]:


stockData['Change']=stockData["ReferencePrice"]-stockData['PrevClose']
stockData['%Change']=round(stockData['Change']/stockData['PrevClose']*100,2)
stockData.head(3)


# #建立分組區間

# In[5]:


import numpy as np

bins = [-float("inf")] + list(np.arange(-9, 10)) + [float("inf")]
labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 9)] + ['≥9%']

# 建立區間欄位
stockData['%Change_Bin'] = pd.cut(stockData['%Change'], bins=bins, labels=labels, include_lowest=True)
stockData['%Change_Bin'] = stockData['%Change_Bin'].astype(str).replace("nan", "NaN")


# In[6]:


bins2 = [-float("inf")] + list(np.arange(-9, 10,2)) + [float("inf")]
labels2 = ['≤-9%'] + [f"{i}%" for i in range(-9, 9,2)] + ['≥9%']

# 建立區間欄位
stockData['%Change_Bin'] = pd.cut(stockData['%Change'], bins=bins, labels=labels, include_lowest=True)
stockData['%Change_Bin'] = stockData['%Change_Bin'].astype(str).replace("nan", "NaN")

print(bins2)
print(labels2)


# In[7]:


print(bins)
print(labels)


# In[8]:


#print(stockData['%Change_Bin2'].unique())


# In[9]:


print(stockData['%Change_Bin'].unique())


# In[ ]:





# #generate color map

# In[10]:


def get_discrete_color_map2(style='taiwan'):
    if style == 'taiwan':
        labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 10)] + ['≥9%'] +['NaN']
        colors = [
            "#003300",  # ≤-9%
            "#004d00", "#006600", "#008000", "#009900", "#00b300",
            "#00cc00", "#00e600", "#1aff1a", "#a3f8b1",  # 綠階層
            "#ffd9d9",                                   # 中性 0%
            "#ffb3b3", "#ff9999", "#ff6666", "#ff4d4d", "#ff3333",
            "#ff1a1a", "#ff0000", "#e60000", "#cc0000",  # 紅階層
            "#990000",   # ≥9%
            "#808080"   # NaN
        ]
        return dict(zip(labels, colors))

    elif style == 'global':
        labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 10)] + ['≥9%']+['NaN']
        colors = [
            "#990000",  # ≤-9%
            "#cc0000", "#e60000", "#ff0000", "#ff1a1a", "#ff3333",
            "#ff4d4d", "#ff6666", "#ff9999", "#ffb3b3",  # 紅階層
            "#c4ffcc",                                   # 中性 0%
            "#80ff80", "#1aff1a", "#00e600", "#00cc00", "#00b300",
            "#009900", "#008000", "#006600", "#004d00",  # 綠階層
            "#003300",   # ≥9%
            "#808080"   # NaN
        ]
        return dict(zip(labels, colors))
    
def get_discrete_color_map3(style='taiwan'):
    if style == 'taiwan':
        labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 10, 2)] + ['≥9%'] +['NaN']
        colors = [
            "#003300",                                              # ≤-9%
            "#004d00", "#008000", "#00b300", "#1aff1a",     # 綠階層
            "#e0e0e0",                                             # 中性 0%
            "#ffb3b3", "#ff5555", "#ff0000", "#cc0000",      # 紅階層
            "#990000",                                             # ≥9%
            "#808080"   # NaN
        ]
        return dict(zip(labels, colors))

    elif style == 'global':
        labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 10)] + ['≥9%']+['NaN']
        colors = [
            "#990000",                                             # ≥9%
            "#ffb3b3", "#ff5555", "#ff0000", "#cc0000",      # 紅階層
            "#e0e0e0",                                             # 中性 0%
            "#004d00", "#008000", "#00b300", "#1aff1a",      # 綠階層
            "#003300",                                             # ≤-9%
            "#808080"   # NaN
        ]
        return dict(zip(labels, colors))
    


# In[11]:


def get_color_scale(style='taiwan'):
    """ 
    - 'taiwan'：漲紅跌綠 
    - 'global'：漲綠跌紅 
    "#006400",  # 淺綠
    "#00cc00",   # 深綠
    "#ffffff",  # 中性（0%）
    "#ffcccc",  # 淺紅
    "#ff0000",  # 中紅 
    """
    if style == 'taiwan':
        return ["#006400", "#00cc00", "#ffffff", "#ff9999", "#cc0000"]  # 綠→紅
    elif style == 'global':
        return ["#cc0000", "#ff9999", "#ffffff", "#00cc00", "#006400"]  # 紅→綠 
    else:
        raise ValueError("style must be 'taiwan', 'global'")


# #color legend

# In[12]:


import urllib.parse
from dash import html

def generate_color_legend(style='taiwan'):
    color_map = get_discrete_color_map2(style)
    items = []
    for label, color in color_map.items():
        btn_id=urllib.parse.quote(label)
        # 計算這個 label 在 stockData 中出現幾次
        count = (stockData['%Change_Bin'] == label).sum()

        items.append(html.Div([
            html.Div(style={
                'display': 'inline-block',
                'width': '20px',
                'height': '20px',
                'backgroundColor': color,
                'marginRight': '10px',
                'border': '1px solid #ccc'
            }),
            html.Span(label),
            html.Button("", id={'type': 'legend-button', 'index': label}, n_clicks=0,
                style={
                    'margin': '10px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'cursor': 'pointer',
                    'backgroundColor': color,
                }
            ),
            html.Span(f"({count})", style={'marginLeft': '5px'})  # 顯示數量
        ], style={'marginBottom': '5px'}))

    return html.Div([
        html.H4("📊 顏色對應說明", style={'marginBottom': '10px'}),
        *items
    ], style={'padding': '10px', 'border': '1px solid #ccc', 'width': '200px', 'fontSize': '14px'})


# In[13]:


#filtered_data = stockData[ (stockData['%Change_Bin'] != '-1%')  ]
stockData = stockData[stockData['Volume'] > 0]
#filtered_data = stockData

color_map = get_discrete_color_map2(style='taiwan')
button_ids = [f"btn-{urllib.parse.quote(label)}" for label in color_map.keys() if label != 'NaN']

button_ids


# In[14]:


def fatchLastStockPrice():

    global stockData#, filtered_data
    
    # 找出所有符合檔名格式的 JSON 檔案
    files = glob.glob("twse_data_*.json")

    # 如果有符合的檔案
    if files:
        # 按照修改時間排序，依照作業系統時間戳記取出最新的
        latest_file = max(files, key=os.path.getmtime)
    
        # 讀取最新檔案
        df = pd.read_json(latest_file)
    
        print(f"✅ 已讀取最新檔案：{latest_file}")
    else:
        print("❌ 找不到符合的 twse_data_*.json 檔案")
        return
    
    #name   code   昨日收盤價   開盤價   最低價   最高價   成交量   參考價   ask(highset buy)  bid(lowest sell)
    stockData=df[["n","c","y","o","l","h","v","z","a","b"]].copy()
    stockData.columns = ["Name", "Code", "PrevClose", "Open", "Low", "High", "Volume", "ReferencePrice", "Ask", "Bid"]
    #stockData['bestBuyer'] = stockData["Bid"].apply(lambda x: float(x.strip("_").split("_")[0])if x and x != "-" else None)
    stockData['bestBuyer']=stockData["Bid"].apply(
        lambda x: next((float(v) for v in x.strip("_").split("_") if float(v) != 0), None)
        if isinstance(x, str) and x != "-" else None
    )
    stockData['ReferencePrice']=np.where(
        stockData['ReferencePrice'] == "-",
        stockData['bestBuyer'],
        stockData['ReferencePrice']
        )
    # 再將 ReferencePrice 轉成 float（字串變數數值）
    stockData["ReferencePrice"] = pd.to_numeric(stockData["ReferencePrice"], errors="coerce")

    #Create column Change %Change
    stockData['Change']=stockData["ReferencePrice"]-stockData['PrevClose']
    stockData['%Change']=round(stockData['Change']/stockData['PrevClose']*100,2)

    bins = [-float("inf")] + list(np.arange(-9, 10)) + [float("inf")]
    labels = ['≤-9%'] + [f"{i}%" for i in range(-9, 9)] + ['≥9%']

    # 建立區間欄位
    stockData['%Change_Bin'] = pd.cut(stockData['%Change'], bins=bins, labels=labels, include_lowest=True)
    stockData['%Change_Bin'] = stockData['%Change_Bin'].astype(str).replace("nan", "NaN")
  
    #filtered_data = stockData[ (stockData['%Change_Bin'] != '-1%')  ]
    stockData = stockData[stockData['Volume'] > 0]
    #filtered_data = stockData

    color_map = get_discrete_color_map2(style='taiwan')
    button_ids = [f"btn-{urllib.parse.quote(label)}" for label in color_map.keys() if label != 'NaN']





# In[19]:


import plotly.express as px
import pandas as pd
import webbrowser  
import dash
from dash import State, dcc, html, Input, Output, ALL, MATCH, ctx  # Dash >=2.4 支援 ctx.triggered_id
from datetime import datetime
    
stockData = stockData[stockData['Volume'] > 0]
#stockData = stockData[stockData['Change%'] > 0]
stockTempletList=[]

# 啟動 Dash 應用
app = dash.Dash(__name__)

app.layout = html.Div([
    #html.H2("Treemap 顏色風格選擇"),
    dcc.Dropdown(
        id='style-selector',
        options=[
            {'label': '台式配色（漲紅跌綠）', 'value': 'taiwan'},
            {'label': '國際配色（漲綠跌紅）', 'value': 'global'}
        ],
        value='taiwan'
    ),
    dcc.Graph(
        id='treemap-chart',
        style={'height': '100vh', 'width': '100%'},  # <--- 加這行\n",
        config={
            'displayModeBar': True, 'displaylogo': False,        # 顯示上方工具列
            'modeBarButtonsToAdd': ['fullscreen', 'toImage'],  # 額外加入全螢幕與下載按鈕
            #'toImageButtonOptions': {
            #    'format': 'png',         # 下載格式：'svg', 'png', 'jpeg', 'webp'
            #    'filename': 'treemap',
            #    'height': 1080,
            #    'width': 1920,
            #    'scale': 2               # 圖片解析度倍率
            #}
        }
    ),
    html.Button(
        "🔄 重新整理",
        id="refresh-button", 
        n_clicks=0,
        style={
            'margin': '10px',
            'padding': '10px 20px',
            'fontSize': '16px',
            'cursor': 'pointer'
        }
    ),
    html.Div(id='update-time', 
             style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '16px', 'color': '#888'}),
    html.Div(id='color-legend', children=generate_color_legend()),
    dcc.Store(id='excluded-labels-store', data=[])
], style={'margin': '0', 'height': '100vh'})

@app.callback(
        Output({'type': 'legend-button', 'index': MATCH}, 'style'),
        Input({'type': 'legend-button', 'index': MATCH}, 'n_clicks'),
        State({'type': 'legend-button', 'index': MATCH}, 'style'),
        prevent_initial_call=True
    )
def toggle_button(n, style):
    if style.get('backgroundColor') == 'white':
        return {**style, 'backgroundColor': style.get('_orig', '#ccc')}
    return {**style, '_orig': style.get('backgroundColor'), 'backgroundColor': 'white'}

@app.callback(
    Output('treemap-chart', 'figure'),
    Output('update-time', 'children'),
    #Output('legend-button', 'children'),
    Output('excluded-labels-store', 'data'),
    Input('style-selector', 'value'),
    Input('refresh-button', 'n_clicks'),
    Input({'type': 'legend-button', 'index': ALL}, 'n_clicks'),
    State('excluded-labels-store', 'data'),
)

def update_char(backgroundStyle, n_clicks, legend_clicks, excluded_labels):  
    
    # initialization excluded_labels 為 set
    if excluded_labels is None:
        excluded_labels = set()
        print("test1 set()")
    else:
        excluded_labels = set(excluded_labels)

    triggered_id = ctx.triggered_id

    filtered_data = stockData.copy() 
    if triggered_id == 'refresh-button':
        #filtered_data = stockData.copy()  # 重設為初始資料
        fatchLastStockPrice()
    elif isinstance(triggered_id, dict) and triggered_id['type'] == 'legend-button':
        print(f"Triggered ID: {triggered_id}")
        exclude_label = triggered_id['index']
        print(f"Exclude label: {exclude_label}")

        # toggle 邏輯
        if exclude_label in excluded_labels:
            excluded_labels.remove(exclude_label)
        else:
            excluded_labels.add(exclude_label)

        print(f"Currently excluded labels: {excluded_labels}")
        filtered_data = stockData[~stockData['%Change_Bin'].isin(excluded_labels)]

    
    # Treemap
    fig = px.treemap(
        filtered_data,
        path=['Name'],
        values='Volume',
        color='%Change_Bin',
        color_discrete_map=get_discrete_color_map2(backgroundStyle),
        custom_data=[
            'Open',
            'PrevClose',
            'Volume', 
            'ReferencePrice',
            '%Change',
            'Change',
            'Code'
        ]
    )
    fig.update_layout(
        margin = dict(t=5, l=5, r=5, b=5), 
        paper_bgcolor='white',   # 或 dark 模式時設黑色
        plot_bgcolor='white',
        legend_title_text="%Change 等級",
        legend_traceorder="normal"
    )
    
    fig.update_traces(
        root_color="lightgrey", 
        hovertemplate=           # mouse hover button
            '<b>%{label}</b>(%{customdata[6]})<br>' +
            'Reference Price: %{customdata[3]}<br>'+
            #'Volume: %{customdata[2]}<br>' +
            'Open: %{customdata[0]}<br>' +
            'Previous Colse: %{customdata[1]}<br>' +
            '%Change: %{customdata[4]}%<br>' +
            'Change: %{customdata[5]}',
            texttemplate='%{label}<br>%{customdata[3]}<br>%{customdata[4]}%',
            textposition='middle center'
    )

    
    
    # 取得現在時間
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_text = f"🕒 Data last updated at: {timestamp}"
    
    return fig, update_text,list(excluded_labels)
    #return fig, update_text,generate_color_legend(backgroundStyle),list(excluded_labels)


#@app.callback(
#    Input('refresh-button', 'n_clicks'),
#)
#def reset_char():
#     return 

if __name__ == '__main__':
#    app.run_server(debug=True,port=8051)
    app.run_server(host="0.0.0.0", port=8051, debug=False, use_reloader=False)

# 顯示圖表
# 儲存為 HTML 檔案
#html_file = "treemap.html"
#fig.write_html(html_file)

# 自動在瀏覽器中打開 HTML 檔案
#webbrowser.open(html_file)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




