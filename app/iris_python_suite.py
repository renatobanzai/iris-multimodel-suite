import irisnative
import json
import networkx as nx
import plotly.graph_objects as go

class irisdomestic():
    def __init__(self, iris_config):
        self.iris_connection = None
        self.get_iris_connection(iris_config)
        self.iris_native = irisnative.createIris(self.iris_connection)
        return

    def isDefined(self, *args):
        self.iris_native.isDefined(*args)

    def kill(self, *args):
        self.iris_native.kill(*args)

    def set(self, value, *args):
        return self.iris_native.set(value, *args)

    def get(self, *args):
        return self.iris_native.get(*args)

    def iterator(self, *args):
        return self.iris_native.iterator(*args)

    def get_iris_connection(self, iris_config):
        #todo: understand the behavior of connection object and implement the correct way
        if not self.iris_connection:
            self.iris_connection = irisnative.createConnection(iris_config["host"],
                                                               iris_config["port"],
                                                               iris_config["namespace"],
                                                               iris_config["username"],
                                                               iris_config["password"])

        return self.iris_connection

    def view_global(self, *global_array, **otherargs):
        newargs = otherargs.copy()
        if not "iris_connection" in otherargs:
            newargs["iris_connection"] = self.iris_connection
        return irisglobal(*global_array, **newargs)

    def view_global_chart(self, *global_array, **otherargs):
        newargs = otherargs.copy()
        if not "iris_connection" in otherargs:
            newargs["iris_connection"] = self.iris_connection
        return irisglobalchart(*global_array, **newargs)

class irisglobal():
    def __init__(self, *global_array, **otherargs):
        if "subscripts_filter" in otherargs:
            self.subscripts_filter = otherargs["subscripts_filter"]
        else:
            self.subscripts_filter = None
        self.global_array = global_array
        self.has_value = False
        self.subscripts = {}
        self.value = None
        self.isDefined = 0
        if "iris_connection" in otherargs:
            self.iris_connection = otherargs["iris_connection"]
            self.iris_native = irisnative.createIris(self.iris_connection)
            self.fill()
        return

    def fill(self):
        self.isDefined = self.iris_native.isDefined(*self.global_array)
        if self.isDefined == 0:
            return

        self.value = self.iris_native.get(*self.global_array)
        if self.value:
            self.has_value = True
        subscripts_iterator = self.iris_native.iterator(*self.global_array)
        if not self.subscripts_filter:
            for subscript_name, subscript_value in subscripts_iterator:
                irisglobal(*(self.global_array+(subscript_name,)),
                           iris_connection=self.iris_connection)
        else:
            for subscript_name in self.subscripts_filter:
                irisglobal(*(self.global_array+(subscript_name,)),
                           iris_connection=self.iris_connection)
        return

    def kill(self):
        self.iris_native.kill(*self.global_array)
        self.has_value = False
        return

    def get(self):
        self.value = self.iris_native.get(*self.global_array)
        return self.value

    def get_json(self):
        self.value = json.loads(self.iris_native.get(*self.global_array))
        return self.value

    def set_json(self, value):
        self.value = value
        return self.iris_native.set(json.dumps(value), *self.global_array)

    def set(self, value):
        self.value = value
        return self.iris_native.set(value, *self.global_array)

class irisglobalchart():
    def __init__(self, *global_array, **otherargs):
        self.id = ".".join(global_array)
        self.obj_nx = otherargs["obj_nx"]
        if "subscripts_filter" in otherargs:
            self.subscripts_filter = otherargs["subscripts_filter"]
        else:
            self.subscripts_filter = None

        if "hover_dict" in otherargs:
            self.hover_dict = otherargs["hover_dict"]
        else:
            self.hover_dict = {}

        if "max_depth" in otherargs:
            self.max_depth = otherargs["max_depth"]
        else:
            self.max_depth = -1

        if "depth" in otherargs:
            self.depth = otherargs["depth"]
        else:
            self.depth = 0

        self.global_array = global_array
        self.has_value = False
        self.subscripts = {}
        self.value = None
        self.isDefined = 0
        self.is_leaf = True
        if "iris_connection" in otherargs:
            self.iris_connection = otherargs["iris_connection"]
            self.iris_native = irisnative.createIris(self.iris_connection)
            self.fill()
        return


    def get_formatted_value(self):
        value = self.iris_native.get(*self.global_array)
        if self.is_leaf:
            color = "#A6CB45"
        else:
            color = "#FEFCD7"
        self.value = {
            "node":",".join(self.global_array),
            "value":value,
            "is_leaf":self.is_leaf,
            "color": color
        }


    def fill(self):
        self.isDefined = self.iris_native.isDefined(*self.global_array)
        if self.isDefined == 0:
            return


        subscripts_iterator = self.iris_native.iterator(*self.global_array)

        if self.max_depth > self.depth:
            if not self.subscripts_filter:
                for subscript_name, subscript_value in subscripts_iterator:
                    self.is_leaf = False
                    new_global_array = self.global_array + (subscript_name,)
                    self.obj_nx.add_edge(self.global_array, new_global_array)
                    irisglobalchart(*new_global_array,
                                    iris_connection=self.iris_connection,
                                    obj_nx=self.obj_nx,
                                    hover_dict=self.hover_dict,
                                    max_depth=self.max_depth,
                                    depth=self.depth+1)
            else:
                for subscript_name in self.subscripts_filter:
                    self.is_leaf = False
                    new_global_array = self.global_array + (subscript_name,)
                    self.obj_nx.add_edge(self.global_array, new_global_array)
                    irisglobalchart(*new_global_array,
                                    iris_connection=self.iris_connection,
                                    obj_nx=self.obj_nx,
                                    hover_dict=self.hover_dict,
                                    max_depth=self.max_depth,
                                    depth=self.depth+1)
        self.get_formatted_value()
        self.hover_dict[self.global_array] = self.value
        if self.value:
            self.has_value = True

        return

    def get_fig(self):
        _nx = self.obj_nx
        pos = nx.spring_layout(_nx)
        edge_x = []
        edge_y = []
        for edge in _nx.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_text = []
        node_hovertext = []
        node_x = []
        node_y = []
        for node in _nx.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node[-1])
            node_hovertext.append(self.hover_dict[node])

        qtt = len(node_text)
        size = 50
        mode = 'markers+text'
        if qtt > 0 and qtt < 40:
            size = 50
            mode = 'markers+text'
        elif qtt > 39 and qtt< 80:
            size = 50
            mode = 'markers+text'
        elif qtt > 79 and qtt < 300:
            size = 10
            mode = 'markers+text'
        elif qtt > 299 and qtt < 400:
            mode = 'markers'
            size = 8
        elif qtt > 399 and qtt < 500:
            mode = 'markers'
            size = 7
        elif qtt > 499:
            size = 5
            mode = 'markers'

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode=mode,
            hoverinfo='text',
            marker=dict(size=size),
            marker_color=node_y,
            text=node_text,
            customdata=node_hovertext,
            hovertext=node_text
        )

        fig = go.FigureWidget(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            clickmode='event+select',
                            showlegend=False,
                            hovermode='closest',
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.update_layout(
            autosize=True,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=4
            ),
            paper_bgcolor="LightSteelBlue",
        )
        return fig
