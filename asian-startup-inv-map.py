#
# Copyright (C) 2019 by Marek Bialoglowy <marek@bialoglowy.com>
#
# MIT license
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import matplotlib.pyplot as plt
import codecs, json
import networkx as nx
import numpy as np
from networkx.readwrite import json_graph
import io
import pickle
import pprint
import time
import math
from adjustText import adjust_text

from fa2 import ForceAtlas2

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
    layout = graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
        layout = graphviz_layout
    except ImportError:
        print("PyGraphviz and pydot not found;\n"
              "drawing with spring layout;\n"
              "will be slow.")
        layout = nx.spring_layout

def save_positions_to_file(filename, pos):
	with open(filename, 'wb') as f:
		serialized = pickle.dumps(pos, protocol=0)
		f.write(serialized)

def load_positions_from_file(filename):
	with open('force.json.pos', 'rb') as f:
		serialized = f.read()
		pos = pickle.loads(serialized)
		return pos

# DATA

G=nx.MultiGraph()
G.add_node("Go-Jek",type='startup')
G.add_node("Grab",type='startup')
G.add_node("Lazada",type='startup')
G.add_node("Carro",type='startup')
G.add_node("Traveloka",type='startup')
G.add_node("Tiket.com",type='startup')
G.add_node("Bukalapak",type='startup')
G.add_node("PropertyGuru",type='startup')
G.add_node("MoneySmart",type='startup')
G.add_node("99.co",type='startup')
G.add_node("Sea - NYSE:SE",type='startup')
G.add_node("AirTrunk",type='startup')
G.add_node("Trax",type='startup')
G.add_node("KyberNetwork",type='startup')
G.add_node("Bigo",type='startup')
G.add_node("ONE Championship",type='startup')
G.add_node("MyRepublic",type='startup')
G.add_node("Sunseap",type='startup')
G.add_node("Thessa Therapeutics",type='startup')
G.add_node("Carousell",type='startup')
G.add_node("Ninja Van",type='startup')
G.add_node("Zilingo",type='startup')
G.add_node("MC Payment",type='startup')
G.add_node("Republic Protocol",type='startup')
G.add_node("TenX",type='startup')
G.add_node("Tokopedia",type='startup')

investors = ["500 Startups",\
"2W Group",\
"8 Decimal Capital",\
"Abraaj Group",\
"Alexis Berthoud",\
"Alibaba Group",\
"All-Stars Investment",\
"Alpha JWC Ventures",\
"Amadeus Capital Partners",\
"Amino Capital",\
"Andreas Schwartz",\
"Andreas von Arx",\
"Angel Capital Management",\
"Ant Financial",\
"APUS Investments",\
"aucfan Co.,Ltd.",\
"Aura Ventures",\
"B Capital Group",\
"Baillie Gifford and Company",\
"Banpu",\
"Batavia Incubator",\
"Beacon Venture Capital",\
"BEENEXT",\
"Blibli",\
"BlockVC",\
"Booking Holdings",\
"Boyu Capital",\
"Broad Peak Investment",\
"Burda Principal Investments",\
"Capikris Foundation",\
"Central Group of Company",\
"Chain Capital",\
"Charles-Lim Capital Ltd",\
"CLSA Capital Partners",\
"Connor Benoit-Milner",\
"Convergence Ventures",\
"DBS Bank",\
"Dennis Jacobs",\
"Deutsche Bank",\
"Dian Swastatika Sentosa",\
"Didi Chuxing",\
"DPD group",\
"Draper Associates",\
"DST Communications",\
"DST Global",\
"DZW Capital",\
"East Ventures",\
"EDBI",\
"Emtek Group",\
"Enspire Capital",\
"ESW Manage",\
"Expedia",\
"FBG Capital",\
"Fenbushi Capital",\
"Fenox Venture Capital",\
"FF Estate AG",\
"Finn Evdemon Capital Partners",\
"GC Capital",\
"General Atlantic, LLC",\
"GGV Capital",\
"GIC",\
"Global Founders Capital",\
"GMO",\
"Golden Equator Capital",\
"Golden Gate Ventures",\
"Goldman Sachs",\
"Google",\
"GREE Ventures",\
"Greenoaks Capital",\
"Hashed",\
"Heliconia Capital Management",\
"Hera Capital",\
"Hillhouse Capital Group",\
"Honda Motor",\
"Hsbc Holdings Plc",\
"Huobi Capital",\
"HV Holtzbrinck Ventures",\
"Hyperchain Capital",\
"Hyundai Motor Company",\
"ImmobilienScout 24",\
"ING Group",\
"Insignia Ventures Partners",\
"Invesco Ltd.",\
"Investec",\
"IREP",\
"ISOTeam",\
"JD.com",\
"John Rost",\
"Julian Sarokin",\
"K3 Ventures",\
"Kakaku.com",\
"Kamet Capital Partners",\
"Karst Peak Capital",\
"Kohlberg Kravis Roberts (KKR)",\
"Kuo-Yi Lim",\
"Limitless Crypto Investments",\
"Lone Pine Capital, LLC",\
"Makara Capital",\
"Manik Arora",\
"Meituan-Dianping",\
"Microsoft",\
"Mirae Asset-Naver Asia Growth Fund",\
"Mission Holdings",\
"Monk's Hill Ventures",\
"Mustedanagic & Plott Brothers GbR",\
"Natixis",\
"New World Strategic Investment",\
"OLX Group",\
"Openspace Ventures",\
"OPT SEA",\
"Perle Ventures",\
"Ping An Overseas Holdings",\
"Plasma Capital",\
"Polychain",\
"Price (T.Rowe) Associates Inc",\
"PT. Astra International Tbk",\
"Qunar.com",\
"Rakuten Capital",\
"Rocket Internet",\
"Royston Tay",\
"Sequoia Capital India",\
"Sequoia Capital",\
"Singtel Innov8",\
"Skystar Capital",\
"Sofina",\
"Softbank Ventures Asia",\
"SoftBank Vision Fund",\
"SoftBank",\
"SPH Media Fund",\
"Square Peg Capital",\
"Summit Partners",\
"Sunshine Network",\
"Susquehanna International Group (SIG)",\
"Temasek Holdings",\
"Tencent Holdings",\
"TEV | Tengelmann Ventures",\
"Tiger Global Management",\
"Tiger Global Management, LLC",\
"Tigris Capital",\
"Tim Draper",\
"Tokyo Century",\
"Toyota Motor Corporation",\
"TPG",\
"TRIREC",\
"tryb Group",\
"United Overseas Bank",\
"Upstream Ventures",\
"Venturra Capital",\
"Vertex Ventures Southeast Asia & India",\
"Vertex Ventures",\
"Warburg Pincus",\
"Ward Ferry Management (BVI) Ltd",\
"Wavemaker Partners",\
"Xavier Niel",\
"Xueling Li",\
"Yamaha Motor Co.,",\
"YY.com",\
"Chow Tai Fook"]

G.add_nodes_from(investors, type='investor')

investors = ["Blibli",\
"Capikris Foundation",\
"DST Global",\
"Google",\
"Hera Capital",\
"JD.com",\
"K3 Ventures",\
"Meituan-Dianping",\
"New World Strategic Investment",\
"Openspace Ventures",\
"PT. Astra International Tbk",\
"Rakuten Capital",\
"Sequoia Capital India",\
"Temasek Holdings",\
"Tencent Holdings"]

for i in investors:
	G.add_edge(i,"Go-Jek")

investors = ["All-Stars Investment",\
"Beacon Venture Capital",\
"Booking Holdings",\
"Central Group of Company",\
"Didi Chuxing",\
"GC Capital",\
"GGV Capital",\
"Hillhouse Capital Group",\
"Honda Motor",\
"Hyundai Motor Company",\
"Microsoft",\
"Mirae Asset-Naver Asia Growth Fund",\
"Qunar.com",\
"SoftBank",\
"SoftBank Vision Fund",\
"Tiger Global Management",\
"Tokyo Century",\
"Toyota Motor Corporation",\
"Vertex Ventures",\
"Vertex Ventures Southeast Asia & India",\
"Yamaha Motor Co.,"]

for i in investors:
	G.add_edge(i,"Grab")


investors = ["Convergence Ventures",\
"Golden Gate Ventures",\
"Kakaku.com",\
"OPT SEA",\
"Royston Tay",\
"SPH Media Fund"]

for i in investors:
	G.add_edge(i,"MoneySmart")

investors = ["East Ventures",\
"Expedia",\
"GIC",\
"Global Founders Capital",\
"Hillhouse Capital Group",\
"JD.com",\
"Sequoia Capital"]

for i in investors:
	G.add_edge(i,"Traveloka")

investors = ["Blibli"]

for i in investors:
	G.add_edge(i,"Tiket.com")


investors = ["500 Startups",\
"Ant Financial",\
"Batavia Incubator",\
"Emtek Group",\
"GIC",\
"GREE Ventures",\
"IREP",\
"Mirae Asset-Naver Asia Growth Fund",\
"aucfan Co.,Ltd."]

for i in investors:
	G.add_edge(i,"Bukalapak")

investors = ["Emtek Group",\
"Finn Evdemon Capital Partners",\
"ImmobilienScout 24",\
"Kohlberg Kravis Roberts (KKR)",\
"Square Peg Capital",\
"Tigris Capital",\
"TPG",\
"Upstream Ventures"]

for i in investors:
	G.add_edge(i,"PropertyGuru")

investors = ["Hub Ventures Fund",\
"Pandoros",\
"500 Startups",\
"Monk's Hill Ventures",\
"Right Click Capital",\
"6 degrees Ventures"]

investors = ["500 Startups",\
"Sequoia Capital India",\
"East Ventures",\
"Fenox Venture Capital",\
"Golden Gate Ventures"]

for i in investors:
	G.add_edge(i,"99.co")

investors = ["Tiger Global Management, LLC",\
"Charles-Lim Capital Ltd",\
"Price (T.Rowe) Associates Inc",\
"General Atlantic, LLC",\
"Ward Ferry Management (BVI) Ltd",\
"Invesco Ltd.",\
"Lone Pine Capital, LLC",\
"Baillie Gifford and Company",\
"Hsbc Holdings Plc"]

for i in investors:
	G.add_edge(i,"Sea - NYSE:SE")

investors = ["Goldman Sachs",\
"TPG",\
"Deutsche Bank",\
"Natixis"]

for i in investors:
	G.add_edge(i,"AirTrunk")


investors = ["Boyu Capital",\
"Warburg Pincus",\
"Investec",\
"Broad Peak Investment"]

for i in investors:
	G.add_edge(i,"Trax")


investors = ["YY.com",\
"Xueling Li",\
"Ping An Overseas Holdings"]

for i in investors:
	G.add_edge(i,"Bigo")


investors = ["CLSA Capital Partners",\
"Kamet Capital Partners",\
"Makara Capital",\
"DST Communications",\
"Xavier Niel",\
"Sunshine Network",\
"Dian Swastatika Sentosa"]

for i in investors:
	G.add_edge(i,"MyRepublic")

investors = ["ING Group",\
"Banpu",\
"United Overseas Bank",\
"ISOTeam",\
"APUS Investments",\
"TRIREC",\
"DBS Bank",\
"Enspire Capital",\
"Chow Tai Fook"]

for i in investors:
	G.add_edge(i,"Sunseap")

investors = ["500 Startups",\
"DBS Bank",\
"EDBI",\
"Golden Gate Ventures",\
"K3 Ventures",\
"OLX Group",\
"Rakuten Capital",\
"Sequoia Capital India"]

for i in investors:
	G.add_edge(i,"Carousell")

investors = ["Abraaj Group",\
"B Capital Group",\
"DPD group",\
"Grab",\
"Kuo-Yi Lim",\
"Monk's Hill Ventures"]

for i in investors:
	G.add_edge(i,"Ninja Van")

investors = ["tryb Group",\
"Perle Ventures",\
"2W Group",\
"Aura Ventures",\
"Golden Equator Capital",\
"ESW Manage",\
"DZW Capital"]

for i in investors:
	G.add_edge(i,"MC Payment")

investors = ["Amadeus Capital Partners",\
"Angel Capital Management",\
"BEENEXT",\
"Burda Principal Investments",\
"Draper Associates",\
"EDBI",\
"Manik Arora",\
"Sequoia Capital",\
"Sequoia Capital India",\
"Sofina",\
"Susquehanna International Group (SIG)",\
"Temasek Holdings",\
"Tim Draper",\
"Venturra Capital",\
"Wavemaker Partners"]

for i in investors:
	G.add_edge(i,"Zilingo")

investors = ["Alpha JWC Ventures",\
"B Capital Group",\
"GMO",\
"Golden Gate Ventures",\
"Insignia Ventures Partners",\
"Manik Arora",\
"Singtel Innov8",\
"Skystar Capital",\
"Softbank Ventures Asia",\
"Venturra Capital"]

for i in investors:
	G.add_edge(i,"Carro")

investors = ["Polychain",\
"FBG Capital",\
"Hyperchain Capital",\
"Huobi Capital",\
"Limitless Crypto Investments",\
"BlockVC"]

for i in investors:
	G.add_edge(i,"Republic Protocol")

investors = ["Alexis Berthoud",\
"Andreas von Arx",\
"Chain Capital",\
"Connor Benoit-Milner",\
"Dennis Jacobs",\
"FF Estate AG",\
"Fenbushi Capital",\
"John Rost",\
"Mustedanagic & Plott Brothers GbR"]

for i in investors:
	G.add_edge(i,"TenX", weight=0.5)

investors = ["Alibaba Group",\
"HV Holtzbrinck Ventures",\
"Rocket Internet",\
"Summit Partners",\
"Temasek Holdings",\
"TEV | Tengelmann Ventures"]

for i in investors:
	G.add_edge(i,"Lazada")

investors = ["Sequoia Capital",\
"Greenoaks Capital",\
"Temasek Holdings",\
"Heliconia Capital Management",\
"Sequoia Capital India",\
"Mission Holdings"]

for i in investors:
	G.add_edge(i,"ONE Championship")

investors = ["Temasek Holdings",\
"Heliconia Capital Management",\
"EDBI",\
"Karst Peak Capital"]

for i in investors:
	G.add_edge(i,"Thessa Therapeutics")

investors = ["SoftBank Vision Fund",\
"Alibaba Group",\
"Softbank Ventures Asia",\
"East Ventures",\
"Sequoia Capital India"]

for i in investors:
	G.add_edge(i,"Tokopedia")


investors = ["Andreas Schwartz",\
"Julian Sarokin",\
"Amino Capital",\
"8 Decimal Capital",\
"Chain Capital",\
"Plasma Capital",\
"Hashed"]

for i in investors:
	G.add_edge(i,"KyberNetwork", weight=0.5)


fixed_positions = {\
"Bukalapak":(-6,1),\
"Go-Jek":(-3,-1),\
"Traveloka":(-6,-1),\
"Tiket.com":(-2,-3),\
"Carro":(8,1),\
"Grab":(4,-1),\
"Ninja Van":(6,-3),\
"Trax":(3,4),\
"TenX":(3,-5),\
"KyberNetwork":(6,-5),\
"Republic Protocol":(2,-6),\
"MC Payment":(-2,-5),\
"Lazada":(1,7),\
"Thessa Therapeutics":(0,7),\
"Sunseap":(-1,6),\
"Sea - NYSE:SE":(-5,6),\
"Bigo":(-8,-5),\
"MyRepublic":(-4,-5),\
"PropertyGuru":(-7,4),\
"AirTrunk":(0,5),\
}\

fixed_nodes = fixed_positions.keys()

# extract subgraphs and sort it by sizes

sub_graphs = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)

Glarge = max(nx.connected_component_subgraphs(G), key=len)

for i, sg in enumerate(sub_graphs):
    print("subgraph {} has {} nodes" . format(i, sg.number_of_nodes()))

fig = plt.figure(figsize=(28,16), dpi=150)

# spring_layout returns dict

pos = nx.spring_layout(G, pos=fixed_positions, k=1.35, iterations=65)
pos = nx.fruchterman_reingold_layout(G, pos=pos, k=0.47, iterations=30)
pos = nx.fruchterman_reingold_layout(G, pos=pos, k= 5/math.sqrt(G.order()), iterations=7)

# ===================

str_time = str(time.time())

investor_nodes=[n for n,d in G.nodes(data=True) if d['type']=='investor']
startup_nodes=[n for n,d in G.nodes(data=True) if d['type']=='startup']

nx.draw_networkx_nodes(G, pos, nodelist=investor_nodes, node_color='lime', alpha=0.4)
nx.draw_networkx_nodes(G, pos, nodelist=startup_nodes, node_color='r', node_size=900, alpha=0.7)
nx.draw_networkx_edges(G, pos, style='solid', alpha=0.5)
labels = nx.draw_networkx_labels(G, pos, font_color='black', font_size=7, font_family='sans-serif', label_pos=0.5)

adjust_labels = True

if adjust_labels:
	# Adjust label overlapping
    x_pos = [v[0] for k, v in pos.items()]
    y_pos = [v[1] for k, v in pos.items()]
    
    adjust_text(
                texts=list(labels.values()),
                expand_text=(1.05, 1.05),
                expand_points=(0.11, 0.55),
                force_text=(0.01, 0.15),
                force_points=(0.01, 0.25),
                autoalign='y',
                only_move={'points':'y', 'text':'y'},
                arrowprops=dict(arrowstyle='-',color='red'),
                ha='center',
                x=x_pos,
                y=y_pos)

plt.title("Startup investor map - Singapore/Indonesia\nby Marek Bialoglowy (marek@bialoglowy.com)", fontsize=16)
plt.axis('off')
plt.legend(loc='upper left')

# Saving

plt.savefig("map-" + str_time + '.png', dpi=150, bbox_inches='tight') # save as png
nx.write_gml(G, 'map-' + str_time + '.gml')
d = json_graph.node_link_data(G)  # node-link format to serialize
json.dump(d, open('map-' + str_time + '.dump', 'w'), indent=4)